import pdfplumber
import re
import json
from typing import List, Dict
from db_manager import add_education, add_coursework


class TranscriptParser:
    """Parses a UW unofficial transcript PDF and extracts structured data."""

    def __init__(self, debug=True):
        self.terms_data = []
        self.education_info = {
            "institution": None,
            "degree": None,
            "graduation_year": None,
            "term_system": "quarter",  # Default for UW
            "graduation_gpa": None,
        }
        self.debug = debug

    def parse_pdf(self, pdf_path: str, output_json: str) -> None:
        """Parses the transcript PDF and outputs structured JSON."""
        try:
            with pdfplumber.open(pdf_path) as pdf:
                full_text, first_page_text = "", ""

                if pdf.pages:
                    first_page_text = self._extract_columns(pdf.pages[0])
                    full_text = "\n".join(
                        self._extract_columns(page) for page in pdf.pages
                    )

                self._extract_education_info(first_page_text, full_text)
                self._process_transcript(full_text)
                self._save_json(output_json)

        except Exception as e:
            print(f"❌ Error processing PDF: {str(e)}")

    def _extract_columns(self, page) -> str:
        """Extracts text from a two-column layout by splitting the page."""
        width = page.width / 2
        left_text = (
            page.within_bbox((0, 0, width, page.height)).extract_text(
                x_tolerance=3, y_tolerance=3
            )
            or ""
        )
        right_text = (
            page.within_bbox((width, 0, page.width, page.height)).extract_text(
                x_tolerance=3, y_tolerance=3
            )
            or ""
        )
        return (left_text + "\n" + right_text).strip()

    def _extract_education_info(self, first_page_text: str, full_text: str) -> None:
        """Extracts institution, degree, and graduation year from the transcript."""
        if self.debug:
            print("\n📘 Extracting education information...")

        # Remove unnecessary newlines
        first_page_text = first_page_text.replace("\n", " ").strip()
        full_text = full_text.replace("\n", " ").strip()

        # Remove known transcript metadata lines
        transcript_metadata_patterns = [
            r"\bUnofficial Academic Transcript\b.*",  # Remove anything after "Unofficial Academic Transcript"
            r"\bStudent ID:\s*\d+\b",  # Remove "Student ID: XXXXXXXX"
            r"\bCampus Location:.*",  # Remove "Campus Location"
            r"\bDegrees Earned:.*",  # Remove "Degrees Earned"
        ]
        for pattern in transcript_metadata_patterns:
            first_page_text = re.sub(
                pattern, "", first_page_text, flags=re.IGNORECASE
            ).strip()

        # Extract institution name
        institution_match = re.search(
            r"(UNIVERSITY OF [A-Z][A-Z\s]+)", first_page_text, re.IGNORECASE
        )
        if institution_match:
            self.education_info["institution"] = (
                institution_match.group(1).title().strip()
            )

        # Extract degree and graduation year from "DEGREES EARNED" section
        degrees_section_match = re.search(
            r"UNIVERSITY OF WASHINGTON DEGREES EARNED:(.*?)\(\d{2}/\d{2}/\d{2}\)",
            full_text,
            re.IGNORECASE,
        )
        if degrees_section_match:
            degrees_section = degrees_section_match.group(1).strip()

            # Extract degree name, ensuring we stop before any term (Winter, Spring, etc.)
            degree_match = re.search(
                r"((?:BACHELOR|MASTER|DOCTOR) OF [A-Z][A-Z\s]+?)(?:\s+(?:AUTUMN|WINTER|SPRING|SUMMER))?\s*\d{4}",
                degrees_section,
                re.IGNORECASE,
            )
            if degree_match:
                self.education_info["degree"] = degree_match.group(1).title().strip()

            # Extract graduation year
            year_match = re.search(
                r"\b(?:AUTUMN|WINTER|SPRING|SUMMER)?\s*(\d{4})",
                degrees_section,
                re.IGNORECASE,
            )
            if year_match:
                self.education_info["graduation_year"] = int(year_match.group(1))

        # Determine term system
        if "QUARTER" in full_text or "QTR" in full_text:
            self.education_info["term_system"] = "quarter"
        elif "SEMESTER" in full_text or "SEM" in full_text:
            self.education_info["term_system"] = "semester"

        if self.debug:
            print("✅ Education info extracted:", self.education_info)

    def _process_transcript(self, text: str) -> None:
        """Processes extracted transcript text into structured data."""
        if self.debug:
            print("\nProcessing transcript text...")

        lines = text.split("\n")
        current_term = None
        current_section = []
        final_cumulative_gpa = None  # Store final cumulative GPA

        for line in lines:
            line = re.sub(r"\s+", " ", line).strip()  # Clean up spaces

            # Match term headers (e.g., "AUTUMN 2019")
            term_match = re.match(
                r"((?:AUTUMN|WINTER|SPRING|SUMMER)\s+\d{4})", line, re.IGNORECASE
            )
            if term_match:
                if current_term and current_section:
                    self._process_term_section(current_term, current_section)

                current_term = term_match.group(1).upper()
                current_section = [line]
                if self.debug:
                    print(f"\nFound term: {current_term}")
            elif current_term:
                current_section.append(line)

            # Extract final cumulative GPA (always take the last occurrence)
            cum_match = re.search(r"CUM\s+GPA:\s*(\d+\.\d+)", line)
            if cum_match:
                final_cumulative_gpa = float(
                    cum_match.group(1)
                )  # Keep updating until last occurrence

        if current_term and current_section:
            self._process_term_section(current_term, current_section)

        # Store the final cumulative GPA
        if final_cumulative_gpa:
            self.education_info["gpa"] = final_cumulative_gpa

    def _process_term_section(self, term: str, lines: List[str]) -> None:
        """Extracts course and GPA data from a term section."""
        courses, qtr_attempted, qtr_earned, qtr_gpa = [], 0.0, 0.0, 0.0
        cum_attempted, cum_earned, cum_gpa = 0.0, 0.0, 0.0

        for line in lines:
            if "CAMPUS" in line.upper():
                continue

            course_match = re.match(
                r"([A-Z]+\s*\d{3})\s+([^0-9]+?)\s+(\d+\.?\d*)\s+([0-4]\.\d+|CR|NC|S|NS|W|I|HW)",
                line,
                re.IGNORECASE,
            )
            if course_match:
                courses.append(
                    {
                        "course_id": course_match.group(1),
                        "course_name": course_match.group(2).strip(),
                        "course_credits": float(course_match.group(3)),
                        "grade": (
                            course_match.group(4)
                            if course_match.group(4).isalpha()
                            else float(course_match.group(4))
                        ),
                    }
                )
                continue

            qtr_match = re.search(
                r"QTR ATTEMPTED:\s*(\d+\.?\d*)\s+EARNED:\s*(\d+\.?\d*)\s+GPA:\s*(\d+\.?\d*)",
                line,
            )
            if qtr_match:
                qtr_attempted, qtr_earned, qtr_gpa = map(float, qtr_match.groups())
                continue

            cum_match = re.search(
                r"CUM ATTEMPTED:\s*(\d+\.?\d*).*CUM GPA:\s*(\d+\.?\d*)", line
            )
            if cum_match:
                cum_attempted, cum_gpa = float(cum_match.group(1)), float(
                    cum_match.group(2)
                )
                cum_earned = qtr_earned  # Assume cumulative earned updates per term
                continue

        self.terms_data.append(
            {
                "term": term,
                "courses": courses,
                "qtr_attempted": qtr_attempted,
                "qtr_earned": qtr_earned,
                "qtr_gpa": qtr_gpa,
                "cum_attempted": cum_attempted,
                "cum_earned": cum_earned,
                "cum_gpa": cum_gpa,
            }
        )

    def _save_json(self, output_file: str) -> None:
        """Saves extracted transcript data as a JSON file."""
        try:
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(
                    {"education": self.education_info, "terms": self.terms_data},
                    f,
                    indent=4,
                )
            print(f"✅ Transcript saved to {output_file}")
        except Exception as e:
            print(f"❌ Error saving JSON: {str(e)}")

    def load_to_db(self, person_id: int, education_id: int) -> None:
        """Loads extracted data into the database."""
        if self.education_info["institution"]:
            add_education(person_id, **self.education_info)

        for term in self.terms_data:
            for course in term["courses"]:
                add_coursework(
                    education_id=education_id,
                    course_name=course["course_name"],
                    course_id=course["course_id"],
                    term=term["term"].split()[0],
                    year=int(term["term"].split()[1]),
                    gpa=course["grade"],
                    course_credits=course["credits"],
                )


def main():
    db_path = r"C:\Users\deana\OneDrive\Documents\Resume\ResumePopulator\resume.db"
    parser = TranscriptParser(debug=True)
    parser.parse_pdf("UWUnofficialTranscript FINAL.pdf", "transcript_parsed.json")
    parser.load_to_db(DB_PATH=db_path, person_id=1, education_id=1)


if __name__ == "__main__":
    main()
