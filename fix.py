import json
import os

# Path to your KJV JSON file inside bible_data folder
json_path = os.path.join("bible_data", "kjv.json")

# Load the original JSON (strip BOM if present)
with open(json_path, "r", encoding="utf-8-sig") as f:
    data = json.load(f)

# Make sure it's a list
if isinstance(data, list):
    fixed = {}
    for book_obj in data:
        name = book_obj["name"]
        abbrev = book_obj["abbrev"]
        chapters = book_obj["chapters"]

        fixed[name] = {
            "abbrev": abbrev,
            "chapters": chapters
        }

    # Save fixed version
    with open("bible_fixed.json", "w", encoding="utf-8") as f:
        json.dump(fixed, f, ensure_ascii=False, indent=2)

    print("✅ Fixed JSON saved as bible_fixed.json")
else:
    print("❌ Error: Input JSON is not a list. Nothing fixed.")
