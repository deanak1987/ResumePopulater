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
    get_education_with_coursework,
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
    add_education(db_test_path, 1, "Associate's of Art", "College", "Quarter", 2015, 3.75)
    results = fetch_data(db_test_path, query="SELECT * FROM Education")
    assert len(results) == 1
    assert results[0][2] == "Associate's of Art"
    assert results[0][3] == "College"
    assert results[0][4] == "Quarter"
    assert results[0][5] == 2015
    assert results[0][6] == 3.75
