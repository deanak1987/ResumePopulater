import os
from setup_db import db_builder
from db_manager import (
    fetch_data,
    add_education,
    add_coursework,
    add_certification,
    add_publication,
    add_personal_info,
    get_certifications,
    get_education,
    get_publications,
    get_personal_info,
    get_person_info,
    get_education_with_coursework,
    add_employment,
    get_employment,
)
import pytest

db_test_path = r"resume_test.db"


def remove_test_db():
    """Removes the test database file if it exists."""
    if os.path.exists(db_test_path):
        os.remove(db_test_path)


@pytest.fixture(scope="function", autouse=True)
def setup_teardown():
    """Setup and teardown for each test."""
    remove_test_db()
    db_builder(db_test_path)
    yield  # Run the test


def test_add_personal_info():
    add_personal_info(
        db_test_path,
        "John Smith",
        "john.smith@email.com",
        "555-555-5555",
        "linkedin.com/in/john-smith",
        "github.com/john-smith",
        None,
    )
    results = fetch_data(db_test_path, query="SELECT * FROM Personal_Info")
    assert len(results) == 1
    assert results[0][1] == "John Smith"


def test_add_education():
    add_education(
        db_test_path, 1, "Associate's of Art", "College", "Quarter", 2015, 3.75
    )
    results = fetch_data(db_test_path, query="SELECT * FROM Education")
    assert len(results) == 1
    assert results[0][2] == "Associate's of Art"
    assert results[0][3] == "College"
    assert results[0][4] == "Quarter"
    assert results[0][5] == 2015
    assert results[0][6] == 3.75


def test_add_coursework():
    add_coursework(
        db_test_path,
        1,
        "General Chemistry Prep",
        "CHEM 139",
        "Autumn",
        2012,
        3.5,
        5,
        "Chemistry",
    )
    results = fetch_data(db_test_path, query="SELECT * FROM Coursework")
    assert len(results) == 1
    assert results[0][2] == "General Chemistry Prep"
    assert results[0][3] == "CHEM 139"
    assert results[0][4] == "Autumn"
    assert results[0][5] == 2012
    assert results[0][6] == 3.5
    assert results[0][7] == 5
    assert results[0][8] == "Chemistry"


def test_add_publication():
    add_publication(
        db_test_path,
        1,
        "Creating Cool Stuff.",
        "smith, J",
        2024,
        "Cool Stuff",
        "2024(3)",
        "126-221",
    )
    results = fetch_data(db_test_path, query="SELECT * FROM Publications")
    assert len(results) == 1
    assert results[0][2] == "Creating Cool Stuff."
    assert results[0][3] == "smith, J"
    assert results[0][4] == 2024
    assert results[0][5] == "Cool Stuff"
    assert results[0][6] == "2024(3)"
    assert results[0][7] == "126-221"


def test_add_certification():
    add_certification(db_test_path, 1, "Cool Dude", "Studs", 2017, None, "Cool Guys")
    results = fetch_data(db_test_path, query="SELECT * FROM Certifications")
    assert len(results) == 1
    assert results[0][2] == "Cool Dude"
    assert results[0][3] == "Studs"
    assert results[0][4] == "2017"
    assert results[0][5] is None
    assert results[0][6] == "Cool Guys"


def test_add_employment():
    add_employment(
        db_test_path,
        1,
        "Job Inc.",
        "Seattle, WA",
        "Worker",
        "June 2020",
        "Current",
        ["Did work", "Spoke to clients"],
        ["General", "General"],
    )
    # results = fetch_data(db_test_path, query="SELECT E.*, R.description FROM Employment AS E LEFT JOIN Responsibilities AS R ON R.employment_id = E.id")
    results = fetch_data(
        db_test_path,
        query="""
            SELECT 
        E.*, 
        COALESCE(GROUP_CONCAT(R.description, ', '), '') AS responsibilities, 
        COALESCE(GROUP_CONCAT(R.field, ', '), '') AS field 
    FROM Employment AS E 
    LEFT JOIN Responsibilities AS R ON R.employment_id = E.id 
    GROUP BY E.id;""",
    )
    assert len(results) == 1
    assert results[0][2] == "Job Inc."
    assert results[0][3] == "Seattle, WA"
    assert results[0][4] == "Worker"
    assert results[0][5] == "June 2020"
    assert results[0][6] == "Current"
    assert results[0][8] == "Did work, Spoke to clients"
    assert results[0][9] == "General, General"


def test_get_personal_info():
    add_personal_info(
        db_test_path,
        "John Smith",
        "john.smith@email.com",
        "555-555-5555",
        "linkedin.com/in/john-smith",
        "github.com/john-smith",
        None,
    )
    assert (
        get_personal_info(db_test_path)
        == "(1, 'John Smith', 'john.smith@email.com', '555-555-5555', 'linkedin.com/in/john-smith', 'github.com/john-smith', None)\n"
    )

def test_get_person_info():
    add_personal_info(
        db_test_path,
        "John Smith",
        "john.smith@email.com",
        "555-555-5555",
        "linkedin.com/in/john-smith",
        "github.com/john-smith",
        None,
    )
    assert (
        get_person_info(db_test_path, 1)
        == ('John Smith', 'john.smith@email.com', '555-555-5555', 'linkedin.com/in/john-smith', 'github.com/john-smith')
    )


def test_get_certifications():
    add_certification(db_test_path, 1, "Cool Dude", "Studs", 2017, None, "Cool Guys")
    assert (
        get_certifications(db_test_path, 1)
        == "Certifications for Person ID 1:\nCool Dude issued by Studs on 2017, in field of Cool Guys. Expires: None"
    )


def test_get_education():
    assert (
        get_education(db_test_path, 1) == "No education records found for Person ID 1."
    )
    add_education(
        db_test_path, 1, "Associate's of Art", "College", "Quarter", 2015, 3.75
    )
    assert (
        get_education(db_test_path, 1)
        == "Education for Person ID 1:\nAssociate's of Art from College acquired in 2015 with a GPA of 3.75\n"
    )


def test_get_publications():
    add_publication(
        db_test_path,
        1,
        "Creating Cool Stuff.",
        "smith, J",
        2024,
        "Cool Stuff",
        "2024(3)",
        "126-221",
    )
    assert (
        get_publications(db_test_path, 1)
        == "Publications for Person ID 1:\nsmith, J. (2024). Creating Cool Stuff.\nCool Stuff,2024(3), 126-221\n"
    )


def test_get_education_with_coursework():
    add_education(
        db_test_path, 1, "Associate's of Art", "College", "Quarter", 2015, 3.75
    )
    add_coursework(
        db_test_path,
        1,
        "General Chemistry Prep",
        "CHEM 139",
        "Autumn",
        2012,
        3.5,
        5,
        "Chemistry",
    )
    assert (
        get_education_with_coursework(db_test_path, 1)
        == "\nEducation and coursework for Person ID 1:\nAssociate's of Art from College (2015) Cumulative GPA: 3.75 - Course: CHEM 139 General Chemistry Prep, GPA: 3.5, Field: Chemistry\n"
    )


def test_get_employment():
    assert (
        get_employment(db_test_path, 1)
        == "Employment history for Person ID 1:\nNo work history."
    )
    add_employment(
        db_test_path,
        1,
        "Job Inc.",
        "Seattle, WA",
        "Worker",
        "June 2020",
        "Current",
        ["Did work", "Spoke to clients"],
        ["General", "General"],
    )
    assert (
        get_employment(db_test_path, 1)
        == "Employment history for Person ID 1:\nWorked for Job Inc. as Worker at Seattle, WA from June 2020 - Current with the following responsibilities:\n\t• Did work\n\t• Spoke to clients"
    )
