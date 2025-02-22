import sqlite3

# Path to the SQLite database
# path = r"C:\Users\deana\OneDrive\Documents\Resume\ResumePopulator\resume.db"


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
        output+= f"{row}\n"
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
    path, education_id, course_name, course_id, term, year, gpa, course_credits
):
    """Adds a coursework entry linked to an education record."""
    query = "INSERT INTO Coursework (education_id, course_name, course_id, term, year, gpa, course_credits) VALUES (?, ?, ?, ?, ?, ?, ?)"
    execute_query(
        path,
        query,
        (education_id, course_name, course_id, term, year, gpa, course_credits),
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
            output += f"{degree} from {institution} aquired in {grad_year} with a GPA of {gpa}\n"
    else:
        output += f"\nNo education records found for Person ID {person_id}."
    return output


def get_education_with_coursework(path, person_id):
    """Fetches education records along with relevant coursework for a person."""
    query = """
        SELECT Education.degree, Education.institution, Education.graduation_year, Education.graduation_gpa, Coursework.course_name, Coursework.course_id, Coursework.gpa
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
            degree, institution, grad_year, cum_gpa, course, course_id, gpa = row
            output += f"{degree} from {institution} ({grad_year}) Cumulative GPA: {cum_gpa} - Course: {course_id} {course if course else 'No courses listed'}, GPA: {gpa} \n"
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
        output += f"Certifications for Person ID {person_id}:"
        for row in results:
            (
                certification_name,
                issuing_organization,
                date_obtained,
                expiration_date,
                field,
            ) = row
        output+=f"\n{certification_name} issued by {issuing_organization} on {date_obtained}, in field of {field}. Expires: {expiration_date}"
            
    else:
        output+= f"\nNo certification records found for Person ID {person_id}."
    return output
