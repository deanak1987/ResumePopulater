# from job_posting_scraper import scrape_job
import setup_db
from db_loader import load_info
from db_manager import get_person_info, get_education, get_employment

db_path = r"resume.db"
setup_db.db_builder(db_path)
load_info(db_path)
full_name, email, phone, linkedin, github = get_person_info(db_path, 1)
print(f"{full_name}, {email}, {phone}, {linkedin}, {github}")

eds = get_education(db_path, 1)
for ed in eds:
    print(ed)

emps = get_employment(db_path, 1)
for emp in emps:
    print(emp)


# job_url = "https://www.governmentjobs.com/careers/tacoma/jobs/4779178/customer-service-representative"  # Replace with actual job URL
# job_info = scrape_job(job_url)
#
# for item in job_info:
#     print(f"{item}: {job_info[item]}")
# for table in db_manager.get_schema(db_path):
#     print(table[0])
