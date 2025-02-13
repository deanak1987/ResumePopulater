import pdfplumber
import re
import json
from typing import List, Dict
from  db_manager import add_education, add_coursework

class UWTranscriptParser:
    def __init__(self, debug=True):
        self.terms_data = []
        self.debug = debug

    def parse_pdf(self, pdf_path: str, output_json: str) -> None:
        """Parse the entire transcript PDF and output structured JSON."""
        try:
            with pdfplumber.open(pdf_path) as pdf:
                full_text = ""
                for page in pdf.pages:
                    # Extract text from two-column layout
                    text = self._extract_columns(page)
                    if text:
                        full_text += text + "\n"

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
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(self.terms_data, f, indent=4)
            print(f"✅ Transcript successfully saved to {output_file}")
        except Exception as e:
            print(f"Error saving JSON: {str(e)}")

    def load_to_db(data: Dict, person_id: int, school_id: int):
        if "education" in data and data["education"]:
            edu = data["education"]
            add_education(person_id, edu["degree"], edu["school"], edu["term_system"], edu["year"])

        for course in data["courses"]:
            add_coursework(school_id, course["course"], course["course_id"], course["term"], course["year"],
                           course["grade"], course["credits"])

def main():
    parser = UWTranscriptParser(debug=True)
    parser.parse_pdf("UWUnofficialTranscript FINAL.pdf", "transcript_parsed.json")


if __name__ == "__main__":
    main()
