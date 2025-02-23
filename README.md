# Resume Populator
This project was designed to practice utilizing SQL in python to build a database comprising all the information necessary to automatically populate a resume that is catered o a particular job posting.

## Database Setup
The Requirements.txt file contains all the necessary dependencies that must be installed

Run the setup.py file to build the SQLite database to house the information.

The db_manager.py file contains all the necessary functions to add and view the different data to the database. 

The test_db_manager.py file runs a test on all of the database SQL python functions to ensure that they operate correctly.

## Transcript Parser
The transcript_parser.py file reads in a transcript PDF and loads the educational institution and coursework information into the DB to alleviate having to input the info by hand.
 * Currently only configured to read my UW master of CS transcript
 * Need to add further functionality to read other university transcripts

## Job Posting Scraper
The job_posting_scraper.py file loads a URL for a job posting and scrapes all the pertinent information.
 * Currently only configured and tested for the jobs website Government Jobs
 * Need to add functionality to search other sites

## Resume Populator
The resume_builder.py file takes the information from the database and utilizes a template.docx file to automatically populate a resume.
 * Currently performs basic population of education and publication sections
 * NTA functionality to populate the other fields
 * NTA functionality to determine best info based on job posting information
 * WTA AI functionality to automatically populate personal statement utilizing matches between job description and experience data


[![Python application test with Github Actions](https://github.com/deanak1987/ResumePopulator/actions/workflows/makefile.yml/badge.svg)](https://github.com/deanak1987/ResumePopulator/actions/workflows/makefile.yml)
