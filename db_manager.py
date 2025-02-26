import sqlite3


def execute_query(path, query, params=()):
    """Executes a given SQL query with optional parameters."""
    conn = sqlite3.connect(path)
    cursor = conn.cursor()
    cursor.execute(query, params)
    conn.commit()
    conn.close()


def fetch_data(path, query, params=()):
    """Fetches data based on a given SQL query."""
    conn = sqlite3.connect(path)
    cursor = conn.cursor()
    cursor.execute(query, params)
    results = cursor.fetchall()
    conn.close()
    return results


# Example: Adding a new personal info record
def add_personal_info(path, name, email, phone, linkedin, github, portfolio):
    query = """INSERT INTO Personal_Info (full_name, email, phone, linkedin, github, portfolio)
               VALUES (?, ?, ?, ?, ?, ?)"""
    execute_query(path, query, (name, email, phone, linkedin, github, portfolio))
    print("Personal info added successfully!")


# Example: Fetching all personal info
def get_personal_info(path):
    query = "SELECT * FROM Personal_Info"
    results = fetch_data(path, query)
    output = ""
    for row in results:
        output += f"{row}\n"
    return output


def delete_and_reset_ids(path, table, row_id):
    """Deletes a row and resets ID values to maintain sequential order."""
    conn = sqlite3.connect(path)
    cursor = conn.cursor()

    # Delete the specified row
    cursor.execute(f"DELETE FROM {table} WHERE id = ?", (row_id,))

    # Reset ID sequence by recreating the table without the deleted row
    cursor.execute(
        f"DELETE FROM sqlite_sequence WHERE name='{table}'"
    )  # Resets autoincrement counter

    conn.commit()
    conn.close()
    print(f"Row {row_id} deleted and IDs reset in {table}.")


def add_education(
    path,
    person_id,
    degree,
    institution,
    term_system,
    graduation_year,
    graduation_gpa,
):
    """Adds an education record linked to a person."""
    query = """INSERT INTO Education (person_id, degree, institution, term_system, graduation_year, graduation_gpa)
               VALUES (?, ?, ?, ?, ?, ?)"""
    execute_query(
        path,
        query,
        (person_id, degree, institution, term_system, graduation_year, graduation_gpa),
    )
    print(
        f"Education record added for Person ID {person_id} at {institution} from {graduation_year} with gpa of {graduation_gpa}"
    )


def add_coursework(
    path, education_id, course_name, course_id, term, year, gpa, course_credits, field
):
    """Adds a coursework entry linked to an education record."""
    query = "INSERT INTO Coursework (education_id, course_name, course_id, term, year, gpa, course_credits, field) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
    execute_query(
        path,
        query,
        (education_id, course_name, course_id, term, year, gpa, course_credits, field),
    )
    print(
        f"Added course {course_id}: {course_name} for {course_credits} credits and GPA of {gpa} to Education ID {education_id}."
    )


def get_education(path, person_id):
    """Fetches education records for a person."""
    query = """
        SELECT Education.degree, Education.institution, Education.graduation_year, Education.graduation_gpa
        FROM Education
        WHERE Education.person_id = ?
        ORDER BY Education.graduation_year DESC
    """
    results = fetch_data(path, query, (person_id,))

    output = ""
    if results:
        output += f"Education for Person ID {person_id}:\n"
        for row in results:
            degree, institution, grad_year, gpa = row
            output += f"{degree} from {institution} acquired in {grad_year} with a GPA of {gpa}\n"
    else:
        output += f"No education records found for Person ID {person_id}."
    return output


def get_education_with_coursework(path, person_id):
    """Fetches education records along with relevant coursework for a person."""
    query = """
        SELECT Education.degree, Education.institution, Education.graduation_year, Education.graduation_gpa, Coursework.course_name, Coursework.course_id, Coursework.gpa, Coursework.field
        FROM Education
        LEFT JOIN Coursework ON Education.id = Coursework.education_id
        WHERE Education.person_id = ?
        ORDER BY Education.graduation_year DESC
    """
    results = fetch_data(path, query, (person_id,))
    output = ""
    if results:
        output += f"\nEducation and coursework for Person ID {person_id}:\n"
        for row in results:
            degree, institution, grad_year, cum_gpa, course, course_id, gpa, field = row
            output += f"{degree} from {institution} ({grad_year}) Cumulative GPA: {cum_gpa} - Course: {course_id} {course if course else 'No courses listed'}, GPA: {gpa}, Field: {field}\n"
    else:
        output += f"\nNo education records found for Person ID {person_id}."
    return output


def add_publication(
    path, person_id, title, authors, publication_date, venue, edition, pages
):
    """Adds a publication entry to the database."""
    query = """
        INSERT INTO Publications (person_id, title, authors, publication_date, venue, edition, pages)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """
    execute_query(
        path,
        query,
        (person_id, title, authors, publication_date, venue, edition, pages),
    )
    print(
        f"Added publication: '{title}' in {venue} on {publication_date} for person_id: {person_id}"
    )


def get_publications(path, person_id):
    """Fetches publication records for a person."""
    query = """
        SELECT Publications.title, Publications.authors, Publications.publication_date, Publications.venue, Publications.edition, Publications.pages 
        FROM Publications
        WHERE Publications.person_id = ?
        ORDER BY Publications.publication_date DESC
    """
    results = fetch_data(path, query, (person_id,))
    output = ""
    if results:
        output += f"Publications for Person ID {person_id}:\n"
        for row in results:
            title, authors, publication_date, venue, edition, pages = row
            output += f"{authors}. ({publication_date}). {title}\n{venue},{edition}, {pages}\n"
    else:
        output += f"\nNo publication records found for Person ID {person_id}."
    return output


def add_certification(
    path,
    person_id,
    certification_name,
    issuing_organization,
    date_obtained,
    expiration_date,
    field,
):
    """Adds a publication entry to the database."""
    query = """
        INSERT INTO Certifications (person_id, certification_name, issuing_organization, date_obtained, expiration_date, field)
        VALUES (?, ?, ?, ?, ?, ?)
    """
    execute_query(
        path,
        query,
        (
            person_id,
            certification_name,
            issuing_organization,
            date_obtained,
            expiration_date,
            field,
        ),
    )
    print(
        f"Added certification: '{certification_name}' from {issuing_organization} issued on {date_obtained} for person_id: {person_id}, field: {field}"
    )


def get_certifications(path, person_id):
    """Fetches certification records for a person."""
    query = """
        SELECT Certifications.certification_name, Certifications.issuing_organization, Certifications.date_obtained, Certifications.expiration_date, Certifications.field 
        FROM Certifications
        WHERE Certifications.person_id = ?
        ORDER BY Certifications.date_obtained DESC
    """
    results = fetch_data(path, query, (person_id,))
    output = ""
    if results:
        output += f"Certifications for Person ID {person_id}:\n"
        for row in results:
            (
                certification_name,
                issuing_organization,
                date_obtained,
                expiration_date,
                field,
            ) = row
            output += f"{certification_name} issued by {issuing_organization} on {date_obtained}, in field of {field}. Expires: {expiration_date}\n"

    else:
        output += f"No certification records found for Person ID {person_id}."
    return output.strip()


def add_employment(
        path,
        person_id,
        company,
        location,
        job_title,
        start_date,
        end_date,
        responsibilities,
        fields
    ):
    """Adds an employment entry and associated responsibilities."""
    conn = sqlite3.connect(path)
    cursor = conn.cursor()

    # Insert job details
    cursor.execute(
        """
        INSERT INTO Employment (person_id, company, location, job_title, start_date, end_date)
        VALUES (?, ?, ?, ?, ?, ?)
    """,
        (person_id, company, location, job_title, start_date, end_date),
    )

    employment_id = cursor.lastrowid  # Get the last inserted job ID

    # Insert responsibilities
    data = [(employment_id, desc, field) for desc, field in zip(responsibilities, fields)]
    cursor.executemany(
        "INSERT INTO Responsibilities (employment_id, description, field) VALUES (?, ?, ?)",
        data,
    )

    conn.commit()
    conn.close()
    print(
        f"Added job at {company} ({job_title}) with {len(responsibilities)} responsibilities."
    )


def get_employment(path, person_id):
    """Fetches employment history along with responsibilities."""
    query = """
        SELECT e.id, e.company, e.location, e.job_title, e.start_date, e.end_date
        FROM Employment e
        WHERE e.person_id = ?
        ORDER BY e.start_date DESC
    """

    results = fetch_data(path, query, (person_id,))
    output = f"Employment history for Person ID {person_id}:\n"
    if results:
        for job in results:
            job_id, company, location, job_title, start_date, end_date = job

            # Fetch responsibilities correctly using job_id
            responsibilities_query = (
                "SELECT description, field FROM Responsibilities WHERE employment_id = ?"
            )
            responsibilities_results = fetch_data(
                path, responsibilities_query, (job_id,)
            )

            output += f"Worked for {company} as {job_title} at {location} from {start_date} - {end_date} with the following responsibilities:\n"
            output += "".join(
                f"\t• {resp[0]}\n" for resp in responsibilities_results
            )  # Unpack tuple correctly
            output += "\n"  # Extra line break between jobs

    else:
        output += "No work history."

    return output.strip()

def get_employment_resume(path, person_id):
    """Fetches employment history along with responsibilities."""
    query = """
        SELECT e.id, e.company, e.location, e.job_title, e.start_date, e.end_date
        FROM Employment e
        WHERE e.person_id = ?
        ORDER BY e.start_date DESC
    """

    results = fetch_data(path, query, (person_id,))
    output = ""
    if results:
        for job in results:
            job_id, company, location, job_title, start_date, end_date = job

            # Fetch responsibilities correctly using job_id
            responsibilities_query = (
                "SELECT description FROM Responsibilities WHERE employment_id = ?"
            )
            responsibilities_results = fetch_data(
                path, responsibilities_query, (job_id,)
            )

            output += f"{company}\n\t{job_title}, {location}\t{start_date} - {end_date}\n"
            output += "".join(
                f"\t• {resp[0]}\n" for resp in responsibilities_results
            )  # Unpack tuple correctly
            output += "\n"  # Extra line break between jobs
    else:
        output += "No work history."
    return output.strip()

def get_schema(path):
    """ Fetches SQL DB schema"""
    query = """
    SELECT sql FROM sqlite_master WHERE type='table'
    """
    results = fetch_data(path, query=query)
    return results

