from db_manager import (
    add_education,
    add_coursework,
    add_certification,
    add_publication,
    add_personal_info,
    get_certifications,
    get_education,
    get_publications,
    get_personal_info,
    get_education_with_coursework,
)

if __name__ == "__main__":
    add_personal_info(
        "John Smith",
        "john.smith@email.com",
        "555-555-5555",
        "linkedin.com/in/john-smith",
        "github.com/john-smith",
        None,
    )

    get_personal_info()

    add_education(1, "Associate's of Art", "College", "Quarter", 2015, 3.75)

    # OC Courses
    add_coursework(1, "General Chemistry Prep", "CHEM 139", "Autumn", 2012, 3.5, 5)
    add_coursework(1, "Precalculus I: Algebra", "MATH 141", "Autumn", 2012, 3.1, 5)
    add_coursework(1, "Spanish I ", "SPAN 121", "Autumn", 2012, 4, 5)
    add_coursework(1, "General Chemistry I", "CHEM 141", "Winter", 2013, 3.8, 5)

    add_publication(
        1, "Creating Cool Stuff.", "smith, J", 2024, "Cool Stuff", "2024(3)", "126–221"
    )

    add_certification(1, "Cool Dude", "Studs", 2017, None, "Cool Guys")
    # Fetch education with coursework for Person ID = 1
    get_education(1)
    get_education_with_coursework(1)
    get_publications(1)
    get_certifications(1)
