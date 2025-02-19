# Resume Populator
This project was designed to practice utilizing SQL in python to build a database comprising all the information necessary to automatically populate a resume that is catered o a particular job posting.

## Database Setup
The Requirements.txt file contains all the necessary dependencies that must be installed

Run the setup.py file to build the SQLite database that will house the information.

The db_manager.py file contains all the necessary functions to add and view the different data to the database. 

The transcript_parser.py file (currently only configured to read my UW master of CS transcript) reads in a transcript PDF and loads the educational institution and coursework information into the DB to alleviate having to input the info by hand.

The job_posting_scraper.py file (currently only configured and tested for the jobs website Government Jobs) loads an url for a job posting and scrapes all the pertinent information.

The resume_builder.py file takes the information from the database and utilizes a template.docx file to automatically populate a resume.