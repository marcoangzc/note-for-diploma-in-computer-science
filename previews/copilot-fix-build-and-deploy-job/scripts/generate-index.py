from pathlib import Path
from html import escape

notes_dir = Path("notes")
output = Path("index.html")

notes = sorted(
    notes_dir.rglob("*.html"),
    key=lambda path: path.name.lower()
) if notes_dir.exists() else []

links = []

for note in notes:
    relative_path = note.as_posix()
    title = note.stem.replace("-", " ").replace("_", " ")
    links.append(
        f'      <li><a href="{escape(relative_path)}">{escape(title)}</a></li>'
    )

if not links:
    links.append("      <li>No notes available yet.</li>")

html = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Notes</title>
  <style>
    body {{
      max-width: 900px;
      margin: 40px auto;
      padding: 0 20px;
      font-family: Arial, sans-serif;
      line-height: 1.6;
    }}

    a {{
      color: #0969da;
      text-decoration: none;
    }}

    a:hover {{
      text-decoration: underline;
    }}
  </style>
</head>
<body>
  <h1>Computer Science Notes</h1>
  <ul>
{chr(10).join(links)}
  </ul>
</body>
</html>
"""

output.write_text(html, encoding="utf-8")
print(f"Generated {output} with {len(notes)} note(s).")
