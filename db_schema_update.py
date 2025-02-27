from db_manager import get_schema
import re

db_path = r"resume.db"
schema_text = "### Database Schema\n```\nsql\n"

schema_text += "\n".join(table[0] for table in get_schema(db_path) if table[0])
schema_text += "\n```\n"

with open("README.md", "r", encoding="utf-8") as f:
    readme_content = f.read()

new_readme = re.sub(
    r"### Database Schema\n```\nsql\n.*?\n```\n",
    schema_text,
    readme_content,
    flags=re.DOTALL,
)
# readme_content.split("### Database Schema")[0] + schema_text)

with open("README.md", "w", encoding="utf-8") as f:
    readme_content = f.write(new_readme)

print("README.md file updated with latest database schema.")
