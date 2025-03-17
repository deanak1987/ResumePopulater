import pdfplumber
import json
import openai
from dotenv import load_dotenv
import os
from db_manager import add_education, add_coursework, get_education

load_dotenv()

# OpenAI API key (replace with your actual key)
API_KEY = os.getenv("OPENAI_API_KEY")

def extract_text_from_pdf(pdf_path):
    """Extracts text from a given PDF file."""
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text.strip()

def process_transcript_with_gpt(transcript_text):
    """Uses OpenAI GPT to extract degree and course information from the transcript text."""
    client = openai.OpenAI(api_key=API_KEY)

    prompt = f"""
    Here is a student's transcript:

    \"\"\"  
    {transcript_text}  
    \"\"\"  

    Extract the following details in **valid JSON format**:

    - Institution Name
    - Term System (Semester, Quarter)
    - Degrees Earned (Degree Name, Graduation Year, GPA)
    - Courses Taken (Course Name, Course ID, Term, Year, GPA, Credits, Field)
    
    for degree info, ensure that abbreviations are not used. So in instances of BS, for example, use Bachelor of Science
    for the course field, enter a field for which the course falls under, for example: mechanical engineering, civil engineering, computer science, data science, math, physics, etc...

    Return as JSON with the structure:
    {{
        "institution": "...",
        "term_system": "...",
        "degrees": [
            {{
                "degree": "...",
                "graduation_year": ...,
                "graduation_gpa": ...
            }}
        ],
        "courses": [
            {{
                "course_name": "...",
                "course_id": "...",
                "term": "...",
                "year": ...,
                "gpa": ...,
                "course_credits": ...,
                "field": ...
            }}
        ]
    }}
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )

        response_text = response.choices[0].message.content

        # Convert response to JSON
        transcript_data = json.loads(response_text.strip("```json").strip("```").strip())
        return transcript_data

    except Exception as e:
        print("Error processing transcript:", e)
        return None

# def save_json(data, output_path):
#     """Saves extracted data to a JSON file."""
#     with open(output_path, "w", encoding="utf-8") as f:
#         json.dump(data, f, indent=4)
#     print(f"Transcript data saved to {output_path}")

def save_transcript_to_db(db_path_fn, person_id, transcript_data):
    """Saves extracted transcript data into the database."""
    if not transcript_data:
        print("No data to save.")
        return

    institution = transcript_data["institution"]
    term_system = transcript_data["term_system"]

    for degree in transcript_data["degrees"]:
        education_id = add_education(db_path_fn, person_id, degree["degree"], institution, term_system, degree["graduation_year"], degree["graduation_gpa"])

        for course in transcript_data["courses"]:
            # field = degree["degree"]  # Assuming field relates to the degree
            add_coursework(db_path_fn, education_id, course["course_name"], course["course_id"], course["term"], course["year"], course["gpa"], course["course_credits"], course["field"])

def main():
    pdf_paths = ["OlympicCollegeTranscripts12-2-2020.pdf", "Final Graduation WSU Transcript.pdf", "UWUnofficialTranscript FINAL.pdf"]
    output_json = "transcript_data.json"

    for pdf_path in pdf_paths:
        print("Extracting text from PDF...")
        transcript_text = extract_text_from_pdf(pdf_path)

        print("Processing transcript with GPT...")
        transcript_data = process_transcript_with_gpt(transcript_text)

        db_path_file_name = "resume_generic.db"
        if transcript_data:
            # print(transcript_data)
            print("Saving transcript data to database...")
            save_transcript_to_db(db_path_file_name, 1, transcript_data)
        # get_education_with_coursework(db_path, 1)
        # save_json(transcript_data, output_json)

if __name__ == "__main__":
    main()
    db_path = "resume_generic.db"
    # print(get_education_with_coursework(db_path, 1))
    edus = get_education(db_path, 1)
    for ed in edus:
        print(ed)