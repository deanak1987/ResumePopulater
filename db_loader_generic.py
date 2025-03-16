from setup_db import db_builder
from db_manager import (
    add_education,
    add_coursework,
    add_certification,
    add_publication,
    add_personal_info,
    add_employment,
    add_professional_development,
    add_skills,
    get_certifications,
    get_education,
    get_publications,
    get_personal_info,
    get_education_with_coursework,
    get_skills,
)
import os


def load_generic(db_path):
    # db_path = r"/\resume_gen.db"
    if os.path.exists(db_path):
        os.remove(db_path)
    db_builder(db_path)
    add_personal_info(
        db_path,
        "John Smith",
        "john.smith@email.com",
        "555-555-5555",
        "linkedin.com/in/john-smith",
        "github.com/john-smith",
        None,
    )

    get_personal_info(db_path)

    add_education(db_path, 1, "Associate's of Art", "College", "Quarter", 2015, 3.75)

    # OC Courses
    add_coursework(
        db_path,
        1,
        "General Chemistry Prep",
        "CHEM 139",
        "Autumn",
        2012,
        3.5,
        5,
        "Chemistry",
    )
    add_coursework(
        db_path, 1, "Precalculus I: Algebra", "MATH 141", "Autumn", 2012, 3.1, 5, "Math"
    )
    add_coursework(
        db_path, 1, "Spanish I ", "SPAN 121", "Autumn", 2012, 4, 5, "Language"
    )
    add_coursework(
        db_path,
        1,
        "General Chemistry I",
        "CHEM 141",
        "Winter",
        2013,
        3.8,
        5,
        "Chemistry",
    )

    add_publication(
        db_path,
        1,
        "Creating Cool Stuff.",
        "smith, J",
        2024,
        "Cool Stuff",
        "2024(3)",
        "126–221",
    )

    add_employment(
        db_path,
        1,
        "Company Inc.",
        "Seattle",
        "Worker",
        "Jan. 2010",
        "Current",
        "General",
        [
            "Worked hard",
            "Helped customers",
        ],
        [
            "General",
            "Customer Service",
        ],
    )

    add_professional_development(
        db_path,
        1,
        "Working",
        "Company Inc.",
        "Jan. 2010",
        "Certified",
        "General",
        ["Working Hard"],
    )

    add_skills(db_path, 1, "Working", ["Working hard", "Don't stop"])

    add_certification(db_path, 1, "Cool Dude", "Studs", 2017, None, "Cool Guys")
    # Fetch education with coursework for Person ID = 1
    get_education(db_path, 1)
    get_education_with_coursework(db_path, 1)
    get_publications(db_path, 1)
    get_certifications(db_path, 1)
    get_skills(db_path, 1)
