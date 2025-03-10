# from base64 import b64decode
from openai import OpenAI
import requests
import json

import keys
from db_manager import add_job_posting, get_job_postings

def scrape_job_data(posting_url):
    api_response = requests.post(
        "https://api.zyte.com/v1/extract",
        auth=(keys.get_zyte_key(), ""),
        json={
            "url": posting_url,
            "httpResponseBody": True,
            "jobPosting": True,
            "jobPostingOptions": {"extractFrom":"httpResponseBody","ai":True},
        },
    )
    # http_response_body: bytes = b64decode(
    #     api_response.json()["httpResponseBody"])
    # # with open("http_response_body.html", "wb") as fp:
    # #      fp.write(http_response_body)
    job = api_response.json()["jobPosting"]
    for item in job:
        print(f"{item}: {job[item]}")
    return job

def process_job_text(job_text):
    client = OpenAI(
        api_key=keys.get_gpt_key()
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

        # Print raw response for debugging
        response_text = completion.choices[0].message.content
        print("\nRaw API Response:", response_text)

        # Attempt to parse the JSON response
        job_data = json.loads(response_text.strip("```json").strip("```").strip())  # Convert string to dictionary
        return job_data

    except Exception as e:
        print("Error processing job text:", e)
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

