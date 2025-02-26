from job_posting_scraper import scrape_job
import db_manager

db_path = r"resume.db"

# job_url = "https://www.governmentjobs.com/careers/tacoma/jobs/4779178/customer-service-representative"  # Replace with actual job URL
# job_info = scrape_job(job_url)
#
# for item in job_info:
#     print(f"{item}: {job_info[item]}")
for table in db_manager.get_schema(db_path):
    print(table[0])