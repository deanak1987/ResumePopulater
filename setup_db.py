import sqlite3

# Define the path where the database will be stored (modify as needed)
db_path = r"import sqlite3"

# Define the path where the database will be stored (modify as needed)
db_path = r"C:\Users\deana\OneDrive\Documents\Resume\ResumePopulator\resume.db"

# Connect to the SQLite database (creates file if it doesn't exist)
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Create tables
cursor.executescript(
    """
CREATE TABLE IF NOT EXISTS Personal_Info (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT,
    email TEXT,
    phone TEXT,
    linkedin TEXT,
    github TEXT,
    portfolio TEXT
);

CREATE TABLE IF NOT EXISTS Education (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    person_id INTEGER,
    degree TEXT,
    institution TEXT,
    term_system TEXT,
    graduation_year INTEGER,
    gpa FLOAT,
    FOREIGN KEY (person_id) REFERENCES Personal_Info(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Coursework (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    education_id INTEGER,
    course_name TEXT,
    course_id TEXT,
    term TEXT,
    year INTEGER,
    gpa FLOAT,
    credits FLOAT,
    FOREIGN KEY (education_id) REFERENCES Education(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Work_Experience (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    job_title TEXT,
    company TEXT,
    start_date TEXT,
    end_date TEXT,
    responsibilities TEXT,
    key_achievements TEXT
);

CREATE TABLE IF NOT EXISTS Projects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_name TEXT,
    technologies TEXT,
    description TEXT,
    project_link TEXT
);

CREATE TABLE IF NOT EXISTS Skills (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    skill_name TEXT,
    proficiency_level TEXT
);

CREATE TABLE IF NOT EXISTS Certifications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    person_id INTEGER,
    certification_name TEXT,
    issuing_organization TEXT,
    date_obtained TEXT,
    expiration_date TEXT,
    field TEXT
);

CREATE TABLE IF NOT EXISTS Publications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    person_id INTEGER,
    title TEXT,
    authors TEXT,
    publication_date INTEGER,
    venue TEXT,
    edition TEXT,
    pages TEXT
);

CREATE TABLE IF NOT EXISTS Custom_Resume_Criteria (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    target_job_title TEXT,
    required_skills TEXT,
    preferred_experience TEXT,
    keywords TEXT
);
"""
)

# Commit and close
conn.commit()
conn.close()

print("Database setup complete! 🎉")


# Connect to the SQLite database (creates file if it doesn't exist)
conn = sqlite3.connect(db_path)
cursor = conn.cursor()
#
# # Create tables
# cursor.executescript("""
# CREATE TABLE IF NOT EXISTS Personal_Info (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     full_name TEXT,
#     email TEXT,
#     phone TEXT,
#     linkedin TEXT,
#     github TEXT,
#     portfolio TEXT
# );
#
# CREATE TABLE IF NOT EXISTS Education (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     person_id INTEGER,
#     degree TEXT,
#     institution TEXT,
#     graduation_year INTEGER,
#     FOREIGN KEY (person_id) REFERENCES Personal_Info(id) ON DELETE CASCADE
# );
#
# CREATE TABLE IF NOT EXISTS Coursework (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     education_id INTEGER,
#     course_name TEXT,
#     FOREIGN KEY (education_id) REFERENCES Education(id) ON DELETE CASCADE
# );
#
# CREATE TABLE IF NOT EXISTS Work_Experience (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     job_title TEXT,
#     company TEXT,
#     start_date TEXT,
#     end_date TEXT,
#     responsibilities TEXT,
#     key_achievements TEXT
# );
#
# CREATE TABLE IF NOT EXISTS Projects (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     project_name TEXT,
#     technologies TEXT,
#     description TEXT,
#     project_link TEXT
# );
#
# CREATE TABLE IF NOT EXISTS Skills (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     skill_name TEXT,
#     proficiency_level TEXT
# );
#
# CREATE TABLE IF NOT EXISTS Certifications (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     certification_name TEXT,
#     issuing_organization TEXT,
#     date_obtained TEXT,
#     expiration_date TEXT
# );
#
# CREATE TABLE IF NOT EXISTS Publications (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     title TEXT,
#     venue TEXT,
#     publication_date TEXT
# );
#
# CREATE TABLE IF NOT EXISTS Custom_Resume_Criteria (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     target_job_title TEXT,
#     required_skills TEXT,
#     preferred_experience TEXT,
#     keywords TEXT
# );
# """)
#
# # Commit and close
# conn.commit()
# conn.close()
#
# print("Database setup complete! 🎉")
