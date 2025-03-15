from openai import OpenAI, OpenAIError
import requests
import json
import os
from dotenv import load_dotenv
from db_manager import add_job_posting, get_job_postings
load_dotenv()
def scrape_job_data(posting_url):
    try:
        api_response = requests.post(
            "https://api.zyte.com/v1/extract",
            auth=(os.getenv("ZYTE_API_KEY"), ""),
            json={
                "url": posting_url,
                "httpResponseBody": True,
                "jobPosting": True,
                "jobPostingOptions": {"extractFrom": "httpResponseBody", "ai": True},
            },
            timeout=10  # Added timeout (10 seconds)
        )

        # Check for HTTP errors
        api_response.raise_for_status()

        job = api_response.json().get("jobPosting", {})
        if not job:
            print("Warning: No job posting data extracted.")
            return None

        for item, value in job.items():
            print(f"{item}: {value}")

        return job

    except requests.exceptions.Timeout:
        print("Error: Request timed out.")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None


def process_job_text(job_text):
    client = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY")
    )
    prompt = f"""
    Here is a job posting:

    \"\"\"  
    {job_text}  
    \"\"\"  

    Extract the following job details from the text above:

    - Job Title  
    - Company Name  
    - Location  
    - Job Type (Full-time, Part-time, Contract, etc.)  
    - Job Description  
    - Responsibilities  
    - Requirements (Must-have qualifications)  
    - Preferred Qualifications (Nice-to-have skills)  
    - Technologies required  
    - Soft Skills needed  
    - Salary Range (if available)  
    - Application Deadline  
    - Application URL  
    - Posting Date  
    - Job ID  
    - Hiring Manager (if available)  
    - Hiring Address (if available)  

    Return the response as a **valid JSON** object with these exact keys:
    {{
        "job_title": "...",
        "company_name": "...",
        "location": "...",
        "job_type": "...",
        "job_description": "...",
        "responsibilities": "...",
        "requirements": "...",
        "preferred_qualifications": "...",
        "technologies": "...",
        "soft_skills": "...",
        "salary_range": "...",
        "application_deadline": "...",
        "application_url": "...",
        "posting_date": "...",
        "job_id": "...",
        "hiring_manager": "...",
        "hiring_address": "..."
    }}
    """

    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )

        # Ensure response contains the expected content
        if not completion.choices or not completion.choices[0].message:
            print("Error: API returned an unexpected response structure.")
            return None

        response_text = completion.choices[0].message.content.strip()
        print("\nRaw API Response:", response_text)

        # Ensure JSON is properly extracted
        json_start = response_text.find("{")
        json_end = response_text.rfind("}") + 1
        if json_start == -1 or json_end == 0:
            print("Error: Failed to locate JSON in response.")
            return None

        json_data = response_text[json_start:json_end]

        # Parse the JSON response safely
        job_data = json.loads(json_data)
        return job_data

    except json.JSONDecodeError as e:
        print("Error decoding JSON:", e)
        return None
    except OpenAIError as e:
        print("OpenAI API Error:", e)
        return None


# job_url = "https://www.governmentjobs.com/careers/tacoma/jobs/4779178/customer-service-representative"
# db_path="resume.db"
def get_scraped_job_data(db_path, job_url):
    if not get_job_postings(db_path=db_path, job_url=job_url):
        print("Job posting not yet in the database")
        job_text = scrape_job_data(job_url)
        job_json = process_job_text(job_text)
        print(f"\nJOB INFO\n{job_json}")
        add_job_posting(db_path=db_path, job_data=job_json)
        job_data = get_job_postings(db_path=db_path, job_url=job_url)[0]
    else:
        print("Job posting already in the database")
        job_data = get_job_postings(db_path=db_path, job_url=job_url)[0]
    return job_data

