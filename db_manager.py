import sqlite3

# Path to the SQLite database
DB_PATH = r"C:\Users\deana\OneDrive\Documents\Resume\ResumePopulator\resume.db"

def execute_query(query, params=()):
    """Executes a given SQL query with optional parameters."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(query, params)
    conn.commit()
    conn.close()

def fetch_data(query, params=()):
    """Fetches data based on a given SQL query."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(query, params)
    results = cursor.fetchall()
    conn.close()
    return results

# Example: Adding a new personal info record
def add_personal_info(name, email, phone, linkedin, github, portfolio):
    query = """INSERT INTO Personal_Info (full_name, email, phone, linkedin, github, portfolio)
               VALUES (?, ?, ?, ?, ?, ?)"""
    execute_query(query, (name, email, phone, linkedin, github, portfolio))
    print("Personal info added successfully!")

# Example: Fetching all personal info
def get_personal_info():
    query = "SELECT * FROM Personal_Info"
    results = fetch_data(query)
    for row in results:
        print(row)


def delete_and_reset_ids(table, row_id):
    """Deletes a row and resets ID values to maintain sequential order."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Delete the specified row
    cursor.execute(f"DELETE FROM {table} WHERE id = ?", (row_id,))

    # Reset ID sequence by recreating the table without the deleted row
    cursor.execute(f"DELETE FROM sqlite_sequence WHERE name='{table}'")  # Resets autoincrement counter

    conn.commit()
    conn.close()
    print(f"Row {row_id} deleted and IDs reset in {table}.")

def add_education(person_id, degree, institution, term_system, graduation_year):
    """Adds an education record linked to a person."""
    query = """INSERT INTO Education (person_id, degree, institution, term_system, graduation_year)
               VALUES (?, ?, ?, ?, ?)"""
    execute_query(query, (person_id, degree, institution, term_system, graduation_year))
    print(f"Education record added for Person ID {person_id} at {institution}")

def add_coursework(education_id, course_name, course_id, term, year, gpa, credits):
    """Adds a coursework entry linked to an education record."""
    query = "INSERT INTO Coursework (education_id, course_name, course_id, term, year, gpa, credits) VALUES (?, ?, ?, ?, ?, ?, ?)"
    execute_query(query, (education_id, course_name, course_id, term, year, gpa, credits))
    print(f"Added course '{course_id}: {course_name}' to Education ID {education_id} with GPA {gpa}")

def get_education(person_id):
    """Fetches education records for a person."""
    query = """
        SELECT Education.degree, Education.institution, Education.graduation_year
        FROM Education
        WHERE Education.person_id = ?
        ORDER BY Education.graduation_year DESC
    """
    results = fetch_data(query, (person_id,))

    if results:
        print(f"Education and coursework for Person ID {person_id}:")
        for row in results:
            degree, institution, grad_year = row
            print(f"{degree} from {institution} ({grad_year})")
    else:
        print(f"No education records found for Person ID {person_id}.")


def get_education_with_coursework(person_id):
    """Fetches education records along with relevant coursework for a person."""
    query = """
        SELECT Education.degree, Education.institution, Education.graduation_year, Coursework.course_name, Coursework.course_id
        FROM Education
        LEFT JOIN Coursework ON Education.id = Coursework.education_id
        WHERE Education.person_id = ?
        ORDER BY Education.graduation_year DESC
    """
    results = fetch_data(query, (person_id,))

    if results:
        print(f"Education and coursework for Person ID {person_id}:")
        for row in results:
            degree, institution, grad_year, course, id= row
            print(f"{degree} from {institution} ({grad_year}) - Course: {id} {course if course else 'No courses listed'}")
    else:
        print(f"No education records found for Person ID {person_id}.")

def add_publication(person_id, title, authors, publication_date, venue, edition, pages):
    """Adds a publication entry to the database."""
    query = """
        INSERT INTO Publications (person_id, title, authors, publication_date, venue, edition, pages)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """
    execute_query(query, (person_id, title, authors, publication_date, venue, edition, pages))
    print(f"Added publication: '{title}' in {venue} on {publication_date} for person_id: {person_id}")

def get_publications(person_id):
    """Fetches publication records for a person."""
    query = """
        SELECT Publications.title, Publications.authors, Publications.publication_date, Publications.venue, Publications.edition, Publications.pages 
        FROM Publications
        WHERE Publications.person_id = ?
        ORDER BY Publications.publication_date DESC
    """
    results = fetch_data(query, (person_id,))

    if results:
        print(f"Publications for Person ID {person_id}:")
        for row in results:
            title, authors, publication_date, venue, edition, pages= row
            print(f"{authors}. ({publication_date}). {title}\n{venue},{edition}, {pages}")
    else:
        print(f"No publication records found for Person ID {person_id}.")

def add_certification(person_id, certification_name, issuing_organization, date_obtained, expiration_date, field):
    """Adds a publication entry to the database."""
    query = """
        INSERT INTO Certifications (person_id, certification_name, issuing_organization, date_obtained, expiration_date, field)
        VALUES (?, ?, ?, ?, ?, ?)
    """
    execute_query(query, (person_id, certification_name, issuing_organization, date_obtained, expiration_date, field))
    print(f"Added certification: '{certification_name}' from {issuing_organization} issued on {date_obtained} for person_id: {person_id}")

def get_certifications(person_id):
    """Fetches certification records for a person."""
    query = """
        SELECT Certifications.certification_name, Certifications.issuing_organization, Certifications.date_obtained, Certifications.expiration_date, Certifications.field 
        FROM Certifications
        WHERE Certifications.person_id = ?
        ORDER BY Certifications.date_obtained DESC
    """
    results = fetch_data(query, (person_id,))

    if results:
        print(f"Certifications for Person ID {person_id}:")
        for row in results:
            certification_name, issuing_organization, date_obtained, expiration_date, field = row
            print(f"{certification_name} issued by {issuing_organization} on {date_obtained}. Expires: {expiration_date}")
    else:
        print(f"No certification records found for Person ID {person_id}.")


# Example Usage
if __name__ == "__main__":
    # add_personal_info("Dean Kelley", "dean.a.kelley@gmail.com", "425-614-6257",
    #                   "linkedin.com/in/dean-kelley-0a7616103", "github.com/deanak1987", None)


    get_personal_info()

    # add_education(1, "Associate's of Art", "Olympic College", "Quarter", 2015)
    # add_education(1, "Bachelor's of Science in Mechanical Engineering", "Washington State University", "Semester", 2017)
    # add_education(1, "Master's of Science in Computer Science", "University of Washington", "Quarter", 2024)
    #
    # # OC Courses
    # add_coursework(1, "General Chemistry Prep", "CHEM 139", "Autumn", 2012,3.5, 5)
    # add_coursework(1, "Precalculus I: Algebra", "MATH 141", "Autumn", 2012,3.1, 5)
    # add_coursework(1, "Spanish I ", "SPAN 121", "Autumn", 2012,4, 5)
    # add_coursework(1, "General Chemistry I", "CHEM 141", "Winter", 2013,3.8, 5)
    # add_coursework(1, "General Chem Lab I", "CHEM 151", "Winter", 2013,3.7, 1.5)
    # add_coursework(1, "Spanish II ", "SPAN 122", "Winter", 2013,4, 5)
    # add_coursework(1, "General Chemistry II", "CHEM 142", "Spring", 2013,3.6, 5)
    # add_coursework(1, "General Chem Lab II", "CHEM 152", "Spring", 2013,4, 1.5)
    # add_coursework(1, "Intro to Engineering", "ENGR 100", "Spring", 2013,4, 1)
    # add_coursework(1, "Precalculus II: Trig", "MATH 142", "Spring", 2013,3.0, 5)
    # add_coursework(1, "Technical Writing", "ENGL 235", "Autumn", 2013,4.0, 5)
    # add_coursework(1, "Engineering Graphics", "ENGR 114", "Autumn", 2013,4.0, 5)
    # add_coursework(1, "Calculus I", "MATH 151", "Autumn", 2013,4.0, 5)
    # add_coursework(1, "Engineering Problems", "ENGR 111", "Winter", 2014,3.6, 5)
    # add_coursework(1, "Intro to Design", "ENGR 104", "Winter", 2014,4.0, 5)
    # add_coursework(1, "Calculus II", "MATH 152", "Winter", 2014,4.0, 5)
    # add_coursework(1, "Macro Economics", "ECON 202", "Spring", 2014,4.0, 5)
    # add_coursework(1, "Statics", "ENGR 214", "Spring", 2014,4.0, 5)
    # add_coursework(1, "Calculus 3", "MATH 163", "Spring", 2014,3.7, 5)
    # add_coursework(1, "Mechanics of Materials", "ENGR 225", "Autumn", 2014,3.9, 5)
    # add_coursework(1, "Calculus 4", "MATH 264", "Autumn", 2014,3.6, 5)
    # add_coursework(1, "Engineering Physics I", "PHYS 254", "Autumn", 2014,3.4, 5)
    # add_coursework(1, "Applied Num Methods", "ENGR 240", "Winter", 2015,3.9, 5)
    # add_coursework(1, "Linear Algebra", "MATH 250", "Winter", 2015,3.6, 5)
    # add_coursework(1, "Engineering Physics II", "PHYS 255", "Winter", 2015,2.9, 5)
    # add_coursework(1, "Dynamics", "ENGR 215", "Spring", 2015,3.9, 5)
    # add_coursework(1, "Differential Equations I", "MATH 221", "Spring", 2015,3.3, 5)
    # add_coursework(1, "Engineering Physics III", "PHYS 256", "Spring", 2015,3.5, 5)
    # add_coursework(1, "Public Speaking", "CMST 220", "Summer", 2015,4, 5)
    # add_coursework(1, "Electrical Circuits", "ENGR 204", "Summer", 2015,4, 5)
    # add_coursework(1, "Thermodynamics", "ENGR 224", "Fall", 2015,3.9, 5)
    # add_coursework(1, "CAD Apps for Engr Design", "ENGR 216", "Winter", 2016,4, 3)
    # add_coursework(1, "Funds/Materials Science", "ENGR 270", "Winter", 2016,3.6, 4)
    # add_coursework(1, "Materials Sciences La", "ENGR 271", "Winter", 2016,3.9, 2)
    # add_coursework(1, "Intro to Mass Media", "CMST 102", "Spring", 2016,4, 5)
    # add_coursework(1, "Adv/Intro Manu Processes", "MANU 210", "Spring", 2016,4, 5)
    # add_coursework(1, "Adv/CNC Manu Process Lab", "MANU 211", "Spring", 2016,4, 5)
    # add_coursework(1, "Computer Science I Java", "CS 141", "Winter", 2019,4, 5)
    #
    # # WSU COURSES
    # add_coursework(2, "Fluid Mechanics", "ME 303", "Autumn", 2015,3.7, 3)
    # add_coursework(2, "Engineering Analysis", "ME 313", "Autumn", 2015,3.3, 3)
    # add_coursework(2, "Intro to Nuclear Engineering", "ME 461", "Autumn", 2015,4, 3)
    # add_coursework(2, "Intro Statistics for Engineers", "STAT 370", "Autumn", 2015,3.3, 3)
    # add_coursework(2, "Heat Transfer", "ME 304", "Spring", 2016,4, 3)
    # add_coursework(2, "Thermal and Fluids Laboratory", "ME 306", "Spring", 2016,3.3, 2)
    # add_coursework(2, "Mech Component Analysis Design", "ME 316", "Autumn", 2016,4, 3)
    # add_coursework(2, "Dynamics Systems", "ME 348", "Autumn", 2016,4, 3)
    # add_coursework(2, "Engineering Design", "ME 414", "Autumn", 2016,3.3, 3)
    # add_coursework(2, "Combustion Engines", "ME 436", "Autumn", 2016,4, 3)
    # add_coursework(2, "Mechatronics", "ME 401", "Spring", 2017,4, 3)
    # add_coursework(2, "Thermal Systems Design", "ME 405", "Spring", 2017,4, 3)
    # add_coursework(2, "Experimental Design", "ME 406", "Spring", 2017,4, 3)
    # add_coursework(2, "Mechanical Systems Design", "ME 416", "Spring", 2017,4, 3)
    #
    #
    # # UW COURSES
    # add_coursework(3, "PROGRAMMING PRACT", "TCSS 305", "Autumn", 2019,4, 5)
    # add_coursework(3, "DISCRETE STRUCT I", "TCSS 321", "Autumn", 2019,3.6, 5)
    # add_coursework(3, "DIGITAL SIG PROC", "TEE 453", "Autumn", 2019,3.5, 5)
    # add_coursework(3, "DATA STRUCTURES", "TCSS 342", "Winter", 2020, 3.8, 5)
    # add_coursework(3, "MACHINE ORGANIZATION", "TCSS 371", "Winter", 2020,4, 5)
    # add_coursework(3, "DES & ANALYS OF ALG", "TCSS 343", "Spring", 2020,4, 5)
    # add_coursework(3, "SOFTWARE DEV & QA", "TCSS 360", "Spring", 2024,4, 5)
    # add_coursework(3, "COMP ARCH", "TCSS 372", "Spring", 2020,4, 5)
    # add_coursework(3, "BIG DATA ANALYTICS", "TCSS 551", "Autumn", 2022,4, 5)
    # add_coursework(3, "MACHINE LEARNING", "TCSS 555", "Autumn", 2022,3.8, 5)
    # add_coursework(3, "APP DIST COMP", "TCSS 558", "Winter", 2023,4, 5)
    # add_coursework(3, "INDEPNDNT STDY/RSCH", "TCSS 600", "Winter", 2023,4, 5)
    # add_coursework(3, "CRYPTOLOGY", "TCSS 581", "Spring", 2023,4, 5)
    # add_coursework(3, "DESIGN PROJECT CSS", "TCSS 700", "Autumn", 2023,4, 5)
    # add_coursework(3, "MASTERS SEMINAR", "TCSS 598", "Autumn", 2023,4, 3)
    # add_coursework(3, "DESIGN PROJECT CSS", "TCSS 700", "Winter", 2024,4, 5)
    # add_coursework(3, "MASTERS SEMINAR", "TCSS 598", "Winter", 2023,4, 2)

    # add_publication(1, "Privacy-Preserving Membership Queries for Federated Anomaly Detection.", "Kelley, D., Vos, J., Pentyala, S., Golob, S., Maia, R., Erkin, Z., De Cock, M., & Nascimento, A", 2024, "Proceedings on Privacy Enhancing Technologies", "2024(3)", "186–201")

    # add_certification(1, "Engineer-in-training", "BRPLES", 2017, None, "Mechanical Engineering")
    # Fetch education with coursework for Person ID = 1
    get_education_with_coursework(1)
    get_publications(1)
    get_certifications(1)

