# Resume Populater
This project was designed to practice utilizing SQL in python to build a database comprising all the information necessary to automatically populate a resume that is catered o a particular job posting.

## Database Setup
The Requirements.txt file contains all the necessary dependencies that must be installed

Run the setup.py file to build the SQLite database to house the information.

The db_manager.py file contains all the necessary functions to add and view the different data to the database. 

The test_db_manager.py file runs a test on all the database SQL python functions to ensure that they operate correctly.

### Database Schema
```
sql
CREATE TABLE Personal_Info (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name TEXT,
        email TEXT,
        phone TEXT,
        linkedin TEXT,
        github TEXT,
        portfolio TEXT
    )
CREATE TABLE sqlite_sequence(name,seq)
CREATE TABLE Education (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_id INTEGER,
        degree TEXT,
        institution TEXT,
        term_system TEXT,
        graduation_year INTEGER,
        graduation_gpa FLOAT,
        FOREIGN KEY (person_id) REFERENCES Personal_Info(id) ON DELETE CASCADE
    )
CREATE TABLE Coursework (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        education_id INTEGER,
        course_name TEXT,
        course_id TEXT,
        term TEXT,
        year INTEGER,
        gpa FLOAT,
        course_credits FLOAT,
        field TEXT,
        FOREIGN KEY (education_id) REFERENCES Education(id) ON DELETE CASCADE
    )
CREATE TABLE Employment (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER,
            company TEXT,
            location TEXT,
            job_title TEXT,
            start_date TEXT,
            end_date TEXT,
            field TEXT
    )
CREATE TABLE Responsibilities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            employment_id INTEGER,
            description TEXT,
            field TEXT,
            FOREIGN KEY (employment_id) REFERENCES Employment(id) ON DELETE CASCADE
    )
CREATE TABLE Projects (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_id INTEGER,
        project_name TEXT,
        year INTEGER,
        technologies TEXT,
        project_link TEXT,
        field TEXT,
        type TEXT
    )
CREATE TABLE ProjectDetails (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        project_id INTEGER,
        detail TEXT
    )
CREATE TABLE Skills (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_id INTEGER,
        skill TEXT
    )
CREATE TABLE SkillDetails (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        skill_id INTEGER,
        detail TEXT
    )
CREATE TABLE Certifications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_id INTEGER,
        certification_name TEXT,
        issuing_organization TEXT,
        date_obtained TEXT,
        expiration_date TEXT,
        field TEXT
    )
CREATE TABLE Publications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_id INTEGER,
        title TEXT,
        authors TEXT,
        publication_date INTEGER,
        venue TEXT,
        edition TEXT,
        pages TEXT
    )
CREATE TABLE ProfessionalDevelopment (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_id INTEGER,
        certification_name TEXT,
        issuing_organization TEXT,
        date_completed INTEGER,
        context TEXT,
        field TEXT
    )
CREATE TABLE PDCovered (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            prof_dev_id INTEGER,
            covered TEXT,
            FOREIGN KEY (prof_dev_id) REFERENCES ProfessionalDevelopment(id) ON DELETE CASCADE
    )
CREATE TABLE Custom_Resume_Criteria (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        target_job_title TEXT,
        required_skills TEXT,
        preferred_experience TEXT,
        keywords TEXT
    )
```

## Transcript Parser
The transcript_parser.py file reads in a transcript PDF and loads the educational institution and coursework information into the DB to alleviate having to input the info by hand.
 * Currently only configured to read my UW master of CS transcript
 * Need to add further functionality to read other university transcripts

## Job Posting Scraper
The job_posting_scraper.py file loads a URL for a job posting and scrapes all the pertinent information.
 * Currently only configured and tested for the jobs website Government Jobs
 * Need to add functionality to search other sites

## Resume Populater
The resume_builder.py file takes the information from the database and utilizes a template.docx file to automatically populate a resume.
 * Currently, performs basic population of education and publication sections
 * NTA functionality to populate the other fields
 * NTA functionality to determine the best info based on job posting information
 * WTA AI functionality to automatically populate personal statement utilizing matches between job description and experience data


[![Python application test with Github Actions](https://github.com/deanak1987/ResumePopulator/actions/workflows/makefile.yml/badge.svg)](https://github.com/deanak1987/ResumePopulator/actions/workflows/makefile.yml)
