import sqlite3
from docx import Document


def fetch_resume_data(person_id):
    """Fetches all resume-related data from the database."""
    conn = sqlite3.connect("resume.db")  # Update with your actual DB path
    cursor = conn.cursor()

    # Fetch personal details
    cursor.execute(
        """
    SELECT Personal_Info.full_name, Personal_Info.email, Personal_Info.linkedin 
    FROM Personal_Info WHERE id = ?
    """,
        (person_id,),
    )
    person = cursor.fetchone()
    full_name, email, linkedin = person if person else ("", "", "")

    # Fetch education details
    cursor.execute(
        """
        SELECT Education.degree, Education.institution, Education.graduation_year, Education.gpa
        FROM Education
        WHERE Education.person_id = ?
        ORDER BY Education.graduation_year DESC
    """,
        (person_id,),
    )
    education = cursor.fetchall()

    # Fetch publication details
    cursor.execute(
        """
        SELECT Publications.title, Publications.authors, Publications.publication_date, Publications.venue, Publications.edition, Publications.pages 
        FROM Publications
        WHERE Publications.person_id = ?
        ORDER BY Publications.publication_date DESC
    """,
        (person_id,),
    )
    publications = cursor.fetchall()

    conn.close()
    return {
        "full_name": full_name,
        "email": email,
        "linkedin": linkedin,
        "education": education,
        "publications": publications,
    }


def replace_text_while_keeping_formatting(paragraph, key, value):
    """Replace text in a paragraph while maintaining the original formatting."""
    if key in paragraph.text:
        # Store initial formatting
        runs_with_formats = []
        for run in paragraph.runs:
            runs_with_formats.append(
                {
                    "text": run.text,
                    "bold": run.bold,
                    "italic": run.italic,
                    "underline": run.underline,
                    "font_name": run.font.name,
                    "font_size": run.font.size,
                    "color": run.font.color.rgb if run.font.color else None,
                }
            )

        # Clear the paragraph
        paragraph.clear()

        # Reconstruct the paragraph with the replacement
        for run_format in runs_with_formats:
            original_text = run_format["text"]
            new_text = original_text.replace(key, value)

            if new_text != original_text:  # Text was replaced
                new_run = paragraph.add_run(new_text)
                # Apply stored formatting
                new_run.bold = run_format["bold"]
                new_run.italic = run_format["italic"]
                new_run.underline = run_format["underline"]
                new_run.font.name = run_format["font_name"]
                if run_format["font_size"]:
                    new_run.font.size = run_format["font_size"]
                if run_format["color"]:
                    new_run.font.color.rgb = run_format["color"]
            else:  # Text wasn't replaced, keep original
                new_run = paragraph.add_run(original_text)
                # Apply stored formatting
                new_run.bold = run_format["bold"]
                new_run.italic = run_format["italic"]
                new_run.underline = run_format["underline"]
                new_run.font.name = run_format["font_name"]
                if run_format["font_size"]:
                    new_run.font.size = run_format["font_size"]
                if run_format["color"]:
                    new_run.font.color.rgb = run_format["color"]


def populate_resume(
    person_id, template_path="template.docx", output_file="Resume.docx"
):
    """Loads a Word template and replaces placeholders with actual data."""
    doc = Document(template_path)
    data = fetch_resume_data(person_id)

    print("Before replacement:")
    for i, para in enumerate(doc.paragraphs):
        print(f"Paragraph {i}: '{para.text}'")
        for j, run in enumerate(para.runs):
            print(f"  Run {j}: '{run.text}'")

    # Replace single-value placeholders while maintaining formatting
    for para in doc.paragraphs:
        replace_text_while_keeping_formatting(para, "{full_name}", data["full_name"])
        replace_text_while_keeping_formatting(para, "{email}", data["email"])
        replace_text_while_keeping_formatting(para, "{linkedin}", data["linkedin"])
    print(f"Printed {data['full_name']}, {data['email']}, {data['linkedin']}")

    # Handle multiple education entries
    for para in doc.paragraphs:
        if "{education}" in para.text:
            # Store the original formatting of the paragraph
            original_style = para.style
            original_font = (
                para.runs[0].font if para.runs else None
            )  # Save font details

            para.text = ""  # Clear text while keeping the style

            for degree, institution, graduation_year, gpa in data["education"]:
                run = para.add_run(f"{institution}, \t{graduation_year}\n")
                run.bold = True
                degree_run = para.add_run(f"\t{degree}\t GPA: {gpa}/4.0\n")

                # Preserve original font settings
                if original_font:
                    run.font.name = original_font.name
                    run.font.size = original_font.size
                    degree_run.font.size = original_font.size

            para.style = original_style  # Reapply original style
        if "{publications}" in para.text:
            original_style = para.style
            original_font = (
                para.runs[0].font if para.runs else None
            )  # Save font details
            #
            para.text = ""  # Clear text while keeping the style
            #
            for title, authors, publication_date, venue, edition, pages in data[
                "publications"
            ]:
                # Add publication
                run = para.add_run(
                    f"{authors}. ({publication_date}). {title}\n{venue}, {edition}, {pages}"
                )
                run.font.name = original_style.font.name
                if original_font:
                    run.font.name = original_font.name
                    run.font.size = original_font.size
    doc.save(output_file)
    print(f"Resume saved successfully as {output_file}")


# Example usage
populate_resume(person_id=1)
