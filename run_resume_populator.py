from job_posting_scraper import scrape_job

job_url = "https://www.governmentjobs.com/careers/tacoma/jobs/4779178/customer-service-representative"  # Replace with actual job URL
job_info = scrape_job(job_url)

for item in job_info:
    print(f"{item}: {job_info[item]}")
