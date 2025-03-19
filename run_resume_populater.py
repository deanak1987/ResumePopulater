import setup_db
import os
from db_manager import (
    get_person_info,
    get_education,
    get_employment,
    get_professional_development,
    get_skills,
    get_projects,
)

try:
    if os.path.exists("db_loader1.py"):
        from db_loader import load_info

        db_path = "resume.db"
        setup_db.db_builder(db_path)
        load_info(db_path)
    else:
        raise ImportError  # Force fallback if db_loader isn't available
except ImportError:
    from db_loader_generic import load_generic

    db_path = "resume_generic.db"
    setup_db.db_builder(db_path)
    load_generic(db_path)


full_name, email, linkedin, github = get_person_info(db_path, 1)
print(f"\n{full_name}, {email}, {linkedin}, {github}\n")

print("Education")
eds = get_education(db_path, 1)
for ed in eds:
    print(ed)

print("\nEmployment")
emps = get_employment(db_path, 1)
for emp in emps:
    print(emp)

print("\nProfessional Development")
pds = get_professional_development(db_path, 1)
for pd in pds:
    print(pd)

print("\nSkills")
sk = get_skills(db_path, 1)
for s in sk:
    print(s)

print("\nProjects")
pjs = get_projects(db_path, 1)  # , fields=["Data Science", "Data Analysis"])
for pj in pjs:
    print(pj)
# job_url = "https://www.governmentjobs.com/careers/tacoma/jobs/4779178/customer-service-representative"  # Replace with actual job URL
# job_info = scrape_job(job_url)
#
# for item in job_info:
#     print(f"{item}: {job_info[item]}")
# for table in db_manager.get_schema(db_path):
#     print(table[0])
