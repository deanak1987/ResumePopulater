import pdfplumber
import re
import json
import sqlite3
from typing import List, Dict
from db_manager import add_education, add_coursework


def parse_transcript(pdf_path: str) -> Dict:
    data = {"courses": [], "education": {}}

    with pdfplumber.open(pdf_path) as pdf:
        full_text = "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])

    term_pattern = re.compile(r'((?:AUTUMN|WINTER|SPRING|SUMMER) \d{4})')
    course_pattern = re.compile(r'([A-Z]+\s*\d{3})\s+([^\d]+?)\s+(\d+\.\d+)\s+([0-4]\.\d*|CR|NC|S|NS|W|I|HW)')
    degree_pattern = re.compile(r'DEGREE EARNED (\d{2}/\d{2}/\d{2}).*?\n([A-Z ]+)', re.MULTILINE)

    lines = full_text.split("\n")
    current_term = None

    for line in lines:
        line = line.strip()

        term_match = term_pattern.match(line)
        if term_match:
            current_term = term_match.group(1)
            continue

        course_match = course_pattern.match(line)
        if course_match and current_term:
            course_id, course_name, credits, grade = course_match.groups()
            year = int(current_term.split()[-1])
            data["courses"].append({
                "term": current_term,
                "year": year,
                "course_id": course_id,
                "course": course_name.strip(),
                "credits": float(credits),
                "grade": grade
            })

    degree_match = degree_pattern.search(full_text)
    if degree_match:
        grad_date, degree_name = degree_match.groups()
        year = int(grad_date.split("/")[-1]) + 2000
        data["education"] = {
            "degree": degree_name.strip(),
            "school": "University of Washington Tacoma",
            "term_system": "QUARTER",
            "year": year
        }

    return data


def save_to_json(data: Dict, filename: str) -> None:
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)


def load_to_db(data: Dict, person_id: int, school_id: int):
    if "education" in data and data["education"]:
        edu = data["education"]
        add_education(person_id, edu["degree"], edu["school"], edu["term_system"], edu["year"])

    for course in data["courses"]:
        add_coursework(school_id, course["course"], course["course_id"], course["term"], course["year"],
                       course["grade"], course["credits"])


def main():
    pdf_path = "UWUnofficialTranscript FINAL.pdf"
    json_path = "transcript_data.json"
    db_path = "resume.db"
    person_id = 1
    school_id = 1

    data = parse_transcript(pdf_path)
    save_to_json(data, json_path)
    load_to_db(data, person_id, school_id)


if __name__ == "__main__":
    main()
