import sqlite3


def db_builder(db_path):
    print(f"Building database in {db_path}")
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
        graduation_gpa FLOAT,
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
        course_credits FLOAT,
        field TEXT,
        FOREIGN KEY (education_id) REFERENCES Education(id) ON DELETE CASCADE
    );
    
    CREATE TABLE IF NOT EXISTS Employment (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER,
            company TEXT,
            location TEXT,
            job_title TEXT,
            start_date TEXT,
            end_date TEXT,
            field TEXT
    );

    CREATE TABLE IF NOT EXISTS Responsibilities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            employment_id INTEGER,
            description TEXT,
            field TEXT,
            FOREIGN KEY (employment_id) REFERENCES Employment(id) ON DELETE CASCADE
    );
    
    CREATE TABLE IF NOT EXISTS Projects (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        project_name TEXT,
        technologies TEXT,
        description TEXT,
        project_link TEXT,
        field, TEXT
    );
    
    CREATE TABLE IF NOT EXISTS Skills (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_id INTEGER,
        skill TEXT
    );
    
    CREATE TABLE IF NOT EXISTS SkillDetails (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        skill_id INTEGER,
        detail TEXT
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
    
    CREATE TABLE IF NOT EXISTS ProfessionalDevelopment (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_id INTEGER,
        certification_name TEXT,
        issuing_organization TEXT,
        date_completed INTEGER,
        context TEXT,
        field TEXT
    );
    
    CREATE TABLE IF NOT EXISTS PDCovered (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            prof_dev_id INTEGER,
            covered TEXT,
            FOREIGN KEY (prof_dev_id) REFERENCES ProfessionalDevelopment(id) ON DELETE CASCADE
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
