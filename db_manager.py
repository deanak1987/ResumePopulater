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


def fetch_one_data(path, query, params=()):
    """Fetches data based on a given SQL query."""
    conn = sqlite3.connect(path)
    cursor = conn.cursor()
    cursor.execute(query, params)
    results = cursor.fetchone()
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


def get_person_info(path, person_id):
    query = """
    SELECT full_name, email, linkedin, github 
    FROM Personal_Info WHERE id = ?
    """
    result = fetch_one_data(path, query, (person_id,))
    return result


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


# def get_education(path, person_id):
#     """Fetches education records for a person."""
#     query = """
#         SELECT Education.degree, Education.institution, Education.graduation_year, Education.graduation_gpa
#         FROM Education
#         WHERE Education.person_id = ?
#         ORDER BY Education.graduation_year DESC
#     """
#     results = fetch_data(path, query, (person_id,))
#
#     output = ""
#     if results:
#         output += f"Education for Person ID {person_id}:\n"
#         for row in results:
#             degree, institution, grad_year, gpa = row
#             output += f"{degree} from {institution} acquired in {grad_year} with a GPA of {gpa}\n"
#     else:
#         output += f"No education records found for Person ID {person_id}."
#     return output


def get_education(path, person_id):
    """Fetches education records for a person."""
    query = """
        SELECT Education.degree, Education.institution, Education.graduation_year, Education.graduation_gpa
        FROM Education
        WHERE Education.person_id = ?
        ORDER BY Education.graduation_year DESC
    """
    return fetch_data(path, query, (person_id,))


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
    return fetch_data(path, query, (person_id,))


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
    return fetch_data(path, query, (person_id,))


def add_employment(
    path,
    person_id,
    company,
    location,
    job_title,
    start_date,
    end_date,
    field,
    responsibilities,
    fields,
):
    """Adds an employment entry and associated responsibilities."""
    conn = sqlite3.connect(path)
    cursor = conn.cursor()

    try:
        # Insert job details
        cursor.execute(
            """
            INSERT INTO Employment (person_id, company, location, job_title, start_date, end_date, field)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (person_id, company, location, job_title, start_date, end_date, field),
        )

        employment_id = cursor.lastrowid  # Get the last inserted job ID

        # Insert responsibilities only if lists are not empty
        if responsibilities and fields:
            data = [
                (employment_id, desc, field)
                for desc, field in zip(responsibilities, fields)
            ]
            cursor.executemany(
                "INSERT INTO Responsibilities (employment_id, description, field) VALUES (?, ?, ?)",
                data,
            )

        conn.commit()
        print(
            f"✅ Added job at {company} ({job_title}) with {len(responsibilities)} responsibilities."
        )

    except sqlite3.Error as e:
        conn.rollback()  # Undo changes if there's an error
        print(f"❌ Database error: {e}")

    finally:
        conn.close()  # Ensure the connection is closed


def get_employment(path, person_id, filters=None):
    """Fetches employment history along with filtered responsibilities."""
    if filters is None:
        filters = {}
    fields = filters["filters"] if "field" in filters else None
    exclude_fields = filters["exclude_fields"] if "exclude_fields" in filters else None
    resp_fields = filters["resp_fields"] if "resp_fields" in filters else None
    # Base query
    query = """
        SELECT 
            E.company, E.location, E.job_title, E.start_date, E.end_date, E.field, 
            COALESCE(GROUP_CONCAT(R.description, ';'), '') AS responsibilities
        FROM Employment AS E 
        LEFT JOIN Responsibilities AS R ON R.employment_id = E.id
        WHERE E.person_id = ?
    """

    params = [person_id]

    # # Filter employment fields
    # if fields:
    #     placeholders = ",".join("?" * len(fields))
    #     query += f" AND E.field IN ({placeholders})"
    #     params.extend(fields)

    # if exclude_fields:
    #     placeholders = ",".join("?" * len(exclude_fields))
    #     query += f" AND E.field NOT IN ({placeholders})"
    #     params.extend(exclude_fields)
    #
    # # Filter responsibilities field
    # if resp_fields:
    #     placeholders = ",".join("?" * len(resp_fields))
    #     query += f" AND R.field IN ({placeholders})"
    #     params.extend(resp_fields)

    # Grouping & Ordering
    query += """
        GROUP BY E.id, E.company, E.location, E.job_title, E.start_date, E.end_date, E.field
        ORDER BY 
            SUBSTR(E.end_date, -4) || 
            CASE 
                WHEN SUBSTR(E.end_date, 1, 3) = 'Jan' THEN '-01'
                WHEN SUBSTR(E.end_date, 1, 3) = 'Feb' THEN '-02'
                WHEN SUBSTR(E.end_date, 1, 3) = 'Mar' THEN '-03'
                WHEN SUBSTR(E.end_date, 1, 3) = 'Apr' THEN '-04'
                WHEN SUBSTR(E.end_date, 1, 3) = 'May' THEN '-05'
                WHEN SUBSTR(E.end_date, 1, 3) = 'Jun' THEN '-06'
                WHEN SUBSTR(E.end_date, 1, 3) = 'Jul' THEN '-07'
                WHEN SUBSTR(E.end_date, 1, 3) = 'Aug' THEN '-08'
                WHEN SUBSTR(E.end_date, 1, 3) = 'Sep' THEN '-09'
                WHEN SUBSTR(E.end_date, 1, 3) = 'Oct' THEN '-10'
                WHEN SUBSTR(E.end_date, 1, 3) = 'Nov' THEN '-11'
                WHEN SUBSTR(E.end_date, 1, 3) = 'Dec' THEN '-12'
            END DESC;
    """

    try:
        with sqlite3.connect(path) as conn:
            cursor = conn.cursor()

            # # Debugging output
            # print("Executing SQL query:\n", query)
            # print("With parameters:", params)

            cursor.execute(query, params)
            return cursor.fetchall()

    except sqlite3.Error as e:
        print(f"❌ Database error: {e}")
        return []

def add_professional_development(
    path,
    person_id,
    certification_name,
    issuing_organization,
    date_completed,
    context,
    field,
    covered,
):
    """Adds a professional development entry to the database."""
    try:
        with sqlite3.connect(path) as conn:
            cursor = conn.cursor()

            # Insert professional development entry
            cursor.execute(
                """
                INSERT INTO ProfessionalDevelopment (person_id, certification_name, issuing_organization, date_completed, context, field)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    person_id,
                    certification_name,
                    issuing_organization,
                    date_completed,
                    context,
                    field,
                ),
            )
            prof_dev_id = cursor.lastrowid  # Get the last inserted ID

            # Insert covered topics only if 'covered' is a non-empty list
            if covered and isinstance(covered, list):
                data = [(prof_dev_id, item) for item in covered]
                cursor.executemany(
                    "INSERT INTO PDCovered (prof_dev_id, covered) VALUES (?, ?)", data
                )

            conn.commit()
            print(
                f"✅ Added certification: {context} '{certification_name}' from {issuing_organization} "
                f"completed in {date_completed} for person_id: {person_id}, field: {field}"
            )

    except sqlite3.Error as e:
        print(f"❌ Database error: {e}")


def get_professional_development(path, person_id):
    """Fetches professional development records for a person."""
    query = """
        SELECT PD.certification_name, PD.issuing_organization, PD.date_completed, PD.context, PD.field, 
               GROUP_CONCAT(C.covered, ';') AS covered 
        FROM ProfessionalDevelopment AS PD
        LEFT JOIN PDCovered AS C ON C.prof_dev_id = PD.id
        WHERE PD.person_id = ?
        GROUP BY PD.id
        ORDER BY 
        SUBSTR(PD.date_completed, -4) || 
        CASE 
            WHEN SUBSTR(PD.date_completed, 1, 3) = 'Jan' THEN '-01'
            WHEN SUBSTR(PD.date_completed, 1, 3) = 'Feb' THEN '-02'
            WHEN SUBSTR(PD.date_completed, 1, 3) = 'Mar' THEN '-03'
            WHEN SUBSTR(PD.date_completed, 1, 3) = 'Apr' THEN '-04'
            WHEN SUBSTR(PD.date_completed, 1, 3) = 'May' THEN '-05'
            WHEN SUBSTR(PD.date_completed, 1, 3) = 'Jun' THEN '-06'
            WHEN SUBSTR(PD.date_completed, 1, 3) = 'Jul' THEN '-07'
            WHEN SUBSTR(PD.date_completed, 1, 3) = 'Aug' THEN '-08'
            WHEN SUBSTR(PD.date_completed, 1, 3) = 'Sep' THEN '-09'
            WHEN SUBSTR(PD.date_completed, 1, 3) = 'Oct' THEN '-10'
            WHEN SUBSTR(PD.date_completed, 1, 3) = 'Nov' THEN '-11'
            WHEN SUBSTR(PD.date_completed, 1, 3) = 'Dec' THEN '-12'
        END DESC;
    """
    try:
        with sqlite3.connect(path) as conn:
            cursor = conn.cursor()
            cursor.execute(query, (person_id,))
            return cursor.fetchall()

    except sqlite3.Error as e:
        print(f"❌ Database error: {e}")
        return []

def add_skills(
    path,
    person_id,
    skill,
    details
):
    """Adds a professional development entry to the database."""
    try:
        with sqlite3.connect(path) as conn:
            cursor = conn.cursor()

            # Insert professional development entry
            cursor.execute(
                """
                INSERT INTO Skills (person_id, skill)
                VALUES (?, ?)
                """,
                (
                    person_id,
                    skill,
                ),
            )
            skill_id = cursor.lastrowid  # Get the last inserted ID

            # Insert covered topics only if 'covered' is a non-empty list
            if details and isinstance(details, list):
                data = [(skill_id, item) for item in details]
                cursor.executemany(
                    "INSERT INTO SkillDetails (skill_id, detail) VALUES (?, ?)", data
                )

            conn.commit()
            print(
                f"✅ Added skill: {skill} for person_id: {person_id}"
            )

    except sqlite3.Error as e:
        print(f"❌ Database error: {e}")


def get_skills(path, person_id):
    """Fetches professional development records for a person."""
    query = """
        SELECT S.skill, GROUP_CONCAT(D.detail, ';') AS details 
        FROM Skills AS S
        LEFT JOIN SkillDetails AS D ON D.skill_id = S.id
        WHERE S.person_id = ?
        GROUP BY S.id
    """
    try:
        with sqlite3.connect(path) as conn:
            cursor = conn.cursor()
            cursor.execute(query, (person_id,))
            return cursor.fetchall()

    except sqlite3.Error as e:
        print(f"❌ Database error: {e}")
        return []

def add_project(
    path,
    person_id,
    project_name, year, technologies, project_link, field, project_type,
    details
):
    """Adds a professional development entry to the database."""
    try:
        with sqlite3.connect(path) as conn:
            cursor = conn.cursor()

            # Insert professional development entry
            cursor.execute(
                """
                INSERT INTO Projects (person_id, project_name, year, technologies, project_link, field, project_type)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    person_id,
                    project_name, year, technologies, project_link, field, project_type,
                ),
            )
            project_id = cursor.lastrowid  # Get the last inserted ID

            # Insert covered topics only if 'covered' is a non-empty list
            if details and isinstance(details, list):
                data = [(project_id, item) for item in details]
                cursor.executemany(
                    "INSERT INTO ProjectDetails (project_id, detail) VALUES (?, ?)", data
                )

            conn.commit()
            print(
                f"✅ Added project: {project_name} for person_id: {person_id}"
            )

    except sqlite3.Error as e:
        print(f"❌ Database error: {e}")


def get_projects(path, person_id, fields=None, types=None, exclude_fields=None, exclude_types=None):
    """Fetches professional development records for a person, filtered by field and type."""
    query = """
        SELECT P.project_name, P.year, P.technologies, P.project_link, P.field, P.project_type, 
               GROUP_CONCAT(D.detail, ';') AS details 
        FROM Projects AS P
        LEFT JOIN ProjectDetails AS D ON D.project_id = P.id
        WHERE P.person_id = ?
    """

    params = [person_id]

    if fields:
        query += f" AND P.field IN ({','.join('?' * len(fields))})"
        params.extend(fields)

    if types:
        query += f" AND P.project_type IN ({','.join('?' * len(types))})"
        params.extend(types)

    if exclude_fields:
        query += f" AND P.field NOT IN ({','.join('?' * len(exclude_fields))})"
        params.extend(exclude_fields)

    if exclude_types:
        query += f" AND P.project_type NOT IN ({','.join('?' * len(exclude_types))})"
        params.extend(exclude_types)

    query += " GROUP BY P.id"

    try:
        with sqlite3.connect(path) as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            return cursor.fetchall()

    except sqlite3.Error as e:
        print(f"❌ Database error: {e}")
        return []


def add_job_posting(db_path, job_data):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO Job_Postings (
            job_title, company_name, location, job_type, job_description,
            responsibilities, requirements, preferred_qualifications, technologies,
            soft_skills, salary_range, application_deadline, application_url,
            posting_date, job_id, hiring_manager, hiring_address
        ) VALUES (
            ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
        )
    """, (
        job_data["job_title"], job_data["company_name"], job_data["location"],
        job_data["job_type"], job_data["job_description"], job_data["responsibilities"],
        job_data["requirements"], job_data["preferred_qualifications"], job_data["technologies"],
        job_data["soft_skills"], job_data["salary_range"], job_data["application_deadline"],
        job_data["application_url"], job_data["posting_date"], job_data["job_id"],
        job_data["hiring_manager"], job_data["hiring_address"]
    ))

    conn.commit()
    conn.close()


def get_job_postings(db_path, job_url=None, job_title=None): #-> List:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # SQL query to fetch job posting(s)
    query = """
        SELECT 
            job_title, company_name, location, job_type, 
            job_description, responsibilities, requirements, 
            preferred_qualifications, technologies, soft_skills, 
            salary_range, application_deadline, application_url, 
            posting_date, job_id, hiring_manager, hiring_address 
        FROM Job_Postings
    """

    conditions = []
    params = []

    if job_url:
        conditions.append("application_url = ?")
        params.append(job_url)

    if job_title:
        conditions.append("job_title = ?")
        params.append(job_title)

    # Append conditions if any, otherwise fetch all
    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    cursor.execute(query, params)
    rows = cursor.fetchall()

    conn.close()
    return rows

def get_schema(path):
    """Fetches SQL DB schema"""
    query = """
    SELECT sql FROM sqlite_master WHERE type='table'
    """
    results = fetch_data(path, query=query)
    return results
