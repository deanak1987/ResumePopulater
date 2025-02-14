import pdfplumber
import re
import json
from typing import List, Dict
from db_manager import add_education, add_coursework


class UWTranscriptParser:
    def __init__(self, debug=True):
        self.terms_data = []
        self.education_info = {
            "institution": None,
            "degree": None,
            "graduation_year": None,
            "term_system": "quarter"  # Default for UW
        }
        self.debug = debug

    def parse_pdf(self, pdf_path: str, output_json: str) -> None:
        """Parse the entire transcript PDF and output structured JSON."""
        try:
            with pdfplumber.open(pdf_path) as pdf:
                full_text = ""
                first_page_text = ""

                # Get first page separately for education info
                if len(pdf.pages) > 0:
                    first_page_text = self._extract_columns(pdf.pages[0])

                # Get full text for course info
                for page in pdf.pages:
                    text = self._extract_columns(page)
                    if text:
                        full_text += text + "\n"

                # Extract education info first (primarily from first page)
                self._extract_education_info(first_page_text, full_text)
                # Then process transcript data
                self._process_transcript(full_text)

            # Save as JSON
            self._save_json(output_json)

        except Exception as e:
            print(f"Error processing PDF: {str(e)}")

    def _extract_columns(self, page) -> str:
        """Extracts text from two-column layout by splitting the page in half."""
        width = page.width
        half_width = width / 2

        left_crop = page.within_bbox((0, 0, half_width, page.height))
        right_crop = page.within_bbox((half_width, 0, width, page.height))

        left_text = left_crop.extract_text(x_tolerance=3, y_tolerance=3) if left_crop else ""
        right_text = right_crop.extract_text(x_tolerance=3, y_tolerance=3) if right_crop else ""

        return (left_text + "\n" + right_text).strip()

    def _extract_education_info(self, first_page_text: str, full_text: str) -> None:
        """Extracts university and degree information from the transcript."""
        if self.debug:
            print("\nExtracting education information...")

        # Look for institution name (typically at the top of transcript)
        institution_patterns = [
            r'(UNIVERSITY OF [A-Z]+(?:\s+[A-Z]+)*)',
            r'([A-Z]+\s+(?:UNIVERSITY|COLLEGE)(?:\s+[A-Z]+)*)',
            r'([A-Z]+\s+(?:STATE)\s+(?:UNIVERSITY|COLLEGE)(?:\s+[A-Z]+)*)',
            r'((?:THE\s+)?[A-Z]+\s+INSTITUTE\s+OF\s+[A-Z]+(?:\s+[A-Z]+)*)',
            r'([A-Z]+\s+SCHOOL\s+OF\s+[A-Z]+(?:\s+[A-Z]+)*)'
        ]

        # Try first page first, then full text
        for text in [first_page_text, full_text]:
            for pattern in institution_patterns:
                match = re.search(pattern, text)
                if match:
                    self.education_info["institution"] = match.group(1).title()
                    break
            if self.education_info["institution"]:
                break

        # Look for degree information
        degree_patterns = [
            r'(?:DEGREE|PROGRAM):\s*((?:Bachelor|Master|Doctor) of [A-Za-z]+(?:\s+[A-Za-z]+)*)',
            r'(Bachelor of [A-Za-z]+(?:\s+[A-Za-z]+)*)',
            r'(Master of [A-Za-z]+(?:\s+[A-Za-z]+)*)',
            r'(Doctor of [A-Za-z]+(?:\s+[A-Za-z]+)*)',
            r'(B\.?[A-Z].?\s*(?:in\s+[A-Za-z]+(?:\s+[A-Za-z]+)*)?)',
            r'(M\.?[A-Z].?\s*(?:in\s+[A-Za-z]+(?:\s+[A-Za-z]+)*)?)',
            r'(Ph\.?D\.?\s*(?:in\s+[A-Za-z]+(?:\s+[A-Za-z]+)*)?)',
            r'MAJOR:\s*([A-Za-z]+(?:\s+[A-Za-z]+)*)'  # Fallback to major if degree not found
        ]

        for pattern in degree_patterns:
            match = re.search(pattern, full_text, re.IGNORECASE)
            if match:
                degree = match.group(1).strip()
                # If we only found a major, prefix it with "Bachelor of" as default
                if pattern.startswith('MAJOR'):
                    degree = f"Bachelor of Science in {degree}"
                self.education_info["degree"] = degree
                break

        # Look for graduation year
        grad_patterns = [
            r'GRADUATED?\s+(?:IN\s+)?(\d{4})',
            r'DEGREE\s+AWARDED:?\s+(?:[A-Z]+\s+)?(\d{4})',
            r'CLASS\s+OF\s+(\d{4})',
            r'EXPECTED\s+GRADUATION:?\s*(\d{4})',
            r'ANTICIPATED\s+COMPLETION:?\s*(\d{4})'
        ]

        for pattern in grad_patterns:
            match = re.search(pattern, full_text, re.IGNORECASE)
            if match:
                self.education_info["graduation_year"] = int(match.group(1))
                break

        # Determine term system based on terms found
        if any(term in full_text for term in ['QUARTER', 'QTR']):
            self.education_info["term_system"] = "quarter"
        elif any(term in full_text for term in ['SEMESTER', 'SEM']):
            self.education_info["term_system"] = "semester"

        if self.debug:
            print("Education info found:", self.education_info)

    def _process_transcript(self, text: str) -> None:
        """Processes extracted transcript text into structured data."""
        if self.debug:
            print("\nProcessing transcript text...")

        lines = text.split('\n')
        current_term = None
        current_section = []

        for line in lines:
            line = re.sub(r'\s+', ' ', line).strip()  # Clean up spaces

            # Match term headers (e.g., "AUTUMN 2019")
            term_match = re.match(r'((?:AUTUMN|WINTER|SPRING|SUMMER)\s+\d{4})', line, re.IGNORECASE)
            if term_match:
                if current_term and current_section:
                    self._process_term_section(current_term, current_section)

                current_term = term_match.group(1).upper()
                current_section = [line]
                if self.debug:
                    print(f"\nFound term: {current_term}")
            elif current_term:
                current_section.append(line)

        if current_term and current_section:
            self._process_term_section(current_term, current_section)

    def _process_term_section(self, term: str, lines: List[str]) -> None:
        """Extracts structured course and GPA data from a term section."""
        courses = []
        qtr_attempted = qtr_earned = qtr_gpa = 0.0
        cum_attempted = cum_earned = cum_gpa = 0.0

        for line in lines:
            if "CAMPUS" in line.upper():
                continue

            # Match courses (course ID, name, credits, grade)
            course_match = re.match(
                r'([A-Z]+\s*\d{3})\s+([^0-9]+?)\s+(\d+\.?\d*)\s+([0-4]\.\d+|CR|NC|S|NS|W|I|HW)',
                line,
                re.IGNORECASE
            )
            if course_match:
                courses.append({
                    "course_id": course_match.group(1),
                    "course_name": course_match.group(2).strip(),
                    "credits": float(course_match.group(3)),
                    "grade": course_match.group(4) if course_match.group(4).isalpha() else float(course_match.group(4))
                })
                continue

            # Match quarter stats
            qtr_match = re.search(r'QTR\s+ATTEMPTED:\s*(\d+\.?\d*)\s+EARNED:\s*(\d+\.?\d*)\s+GPA:\s*(\d+\.?\d*)', line)
            if qtr_match:
                qtr_attempted, qtr_earned, qtr_gpa = map(float, qtr_match.groups())
                continue

            # Match cumulative stats
            cum_match = re.search(r'CUM\s+ATTEMPTED:\s*(\d+\.?\d*).*CUM\s+GPA:\s*(\d+\.?\d*)', line)
            if cum_match:
                cum_attempted, cum_gpa = float(cum_match.group(1)), float(cum_match.group(2))
                cum_earned = qtr_earned  # Assume cumulative earned updates per term
                continue

        self.terms_data.append({
            "term": term,
            "courses": courses,
            "qtr_attempted": qtr_attempted,
            "qtr_earned": qtr_earned,
            "qtr_gpa": qtr_gpa,
            "cum_attempted": cum_attempted,
            "cum_earned": cum_earned,
            "cum_gpa": cum_gpa
        })

    def _save_json(self, output_file: str) -> None:
        """Save parsed transcript data as a JSON file."""
        try:
            output_data = {
                "education": self.education_info,
                "terms": self.terms_data
            }

            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(output_data, f, indent=4)
            print(f"✅ Transcript successfully saved to {output_file}")
        except Exception as e:
            print(f"Error saving JSON: {str(e)}")

    def load_to_db(self, person_id: int, education_id: int) -> None:
        """Load the parsed transcript data into the database."""
        # Add education information
        if self.education_info["institution"]:
            add_education(
                person_id=person_id,
                degree=self.education_info["degree"],
                institution=self.education_info["institution"],
                term_system=self.education_info["term_system"],
                graduation_year=self.education_info["graduation_year"]
            )

        # Add coursework
        for term in self.terms_data:
            for course in term["courses"]:
                add_coursework(
                    education_id=education_id,
                    course_name=course["course_name"],
                    course_id=course["course_id"],
                    term=term["term"].split()[0],  # Extract term name (AUTUMN, WINTER, etc.)
                    year=int(term["term"].split()[1]),  # Extract year
                    gpa=course["grade"],
                    credits=course["credits"]
                )


def main():
    parser = UWTranscriptParser(debug=True)
    parser.parse_pdf("UWUnofficialTranscript FINAL.pdf", "transcript_parsed.json")
    # Example of loading to database
    parser.load_to_db(person_id=1, education_id=1)


if __name__ == "__main__":
    main()