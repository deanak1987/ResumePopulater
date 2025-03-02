import sqlite3
from docx import Document

# from db_manager import get_employment_resume




def fetch_resume_data(db_path, person_id):
    """Fetches all resume-related data from the database."""
    conn = sqlite3.connect(db_path)  # Update with your actual DB path
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
        SELECT Education.degree, Education.institution, Education.graduation_year, Education.graduation_gpa
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

    # Fetch employment details
    cursor.execute(
        """
        SELECT E.company, E.location, E.job_title, E.start_date, E.end_date, GROUP_CONCAT(R.description, ';') AS responsibilities 
        FROM Employment AS E 
        LEFT JOIN Responsibilities AS R ON R.employment_id = E.id
        WHERE E.person_id = ?
        GROUP BY E.company, E.location, E.job_title, E.start_date, E.end_date
        ORDER BY E.start_date DESC
        """,
        (person_id,),
    )
    employment = cursor.fetchall()

    conn.close()
    return {
        "full_name": full_name,
        "email": email,
        "linkedin": linkedin,
        "education": education,
        "employment": employment,
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
    person_id, db_path, template_path="template.docx", output_file="Resume.docx"
):
    """Loads a Word template and replaces placeholders with actual data."""
    # from docx.shared import Pt, Inches
    # from docx.enum.text import WD_PARAGRAPH_ALIGNMENT

    doc = Document(template_path)
    data = fetch_resume_data(db_path, person_id)

    # Replace single-value placeholders while maintaining formatting
    for para in doc.paragraphs:
        replace_text_while_keeping_formatting(para, "{full_name}", data["full_name"])
        replace_text_while_keeping_formatting(para, "{email}", data["email"])
        replace_text_while_keeping_formatting(para, "{linkedin}", data["linkedin"])

    # Handle education, publications and employment sections
    for para in doc.paragraphs:
        if not para.runs:
            continue

        # original_style = para.style
        original_font = para.runs[0].font if para.runs else None

        if "{education}" in para.text:
            # Clear the paragraph while keeping its style
            para.clear()

            for degree, institution, graduation_year, gpa in data["education"]:
                run = para.add_run(f"{institution}, \t{graduation_year}\n")
                run.bold = True
                degree_run = para.add_run(f"\t{degree}\t GPA: {gpa}/4.0\n")

                # Preserve original font settings
                if original_font:
                    run.font.name = original_font.name
                    run.font.size = original_font.size
                    degree_run.font.name = original_font.name
                    degree_run.font.size = original_font.size

        elif "{publications}" in para.text:
            # Clear the paragraph while keeping its style
            para.clear()

            for title, authors, publication_date, venue, edition, pages in data[
                "publications"
            ]:
                run = para.add_run(
                    f"{authors}. ({publication_date}). {title}\n{venue}, {edition}, {pages}\n\n"
                )
                if original_font:
                    run.font.name = original_font.name
                    run.font.size = original_font.size

        elif "{employment}" in para.text:
            # Clear the paragraph
            current_para = para
            current_para.clear()
            prev_company = ""

            # Store the original paragraph format for resetting
            original_indent = para.paragraph_format.left_indent

            for (
                company,
                location,
                title,
                start_date,
                end_date,
                responsibilities,
            ) in data["employment"]:
                # Reset paragraph indentation for each new company
                if prev_company != company:
                    # Reset to original indent (usually 0 for left margin)
                    current_para.paragraph_format.left_indent = original_indent

                    # Add company with bold formatting
                    company_run = current_para.add_run(f"{company}")
                    company_run.bold = True

                    # Add location if available
                    if location:
                        current_para.add_run(f", {location}")

                    current_para.add_run("\n")

                    # Apply font formatting to company name
                    if original_font:
                        company_run.font.name = original_font.name
                        company_run.font.size = original_font.size

                # Add job title and dates with tab spacing
                date_range = (
                    f"\t{start_date} - {end_date}"
                    if end_date
                    else f"{start_date} - Present"
                )
                title_run = current_para.add_run(f"\t{title}  {date_range}\n")

                if original_font:
                    title_run.font.name = original_font.name
                    title_run.font.size = original_font.size

                # Process responsibilities as bullet points
                if responsibilities:
                    for responsibility in responsibilities.split(";"):
                        if responsibility.strip():
                            # Create a properly formatted bullet point with the dash and spaces
                            bullet_run = current_para.add_run("•\t")

                            resp_run = current_para.add_run(
                                f"{responsibility.strip()}\n"
                            )

                            # Preserve font formatting
                            if original_font:
                                bullet_run.font.name = original_font.name
                                bullet_run.font.size = original_font.size
                                resp_run.font.name = original_font.name
                                resp_run.font.size = original_font.size

                # Add space between job entries
                current_para.add_run("\n")

                # Update previous company
                prev_company = company

    doc.save(output_file)
    print(f"Resume saved successfully as {output_file}")


populate_resume(1, db_path = "resume.db")
