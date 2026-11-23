import csv
from pathlib import Path

input_file = Path("output/research_results.csv")
output_file = Path("output/final_research.csv")

with input_file.open("r", encoding="utf-8-sig", newline="") as file:
    rows = list(csv.DictReader(file))

new_fields = [
    "auth_methods",
    "credential_access",
    "api_type",
    "api_coverage",
    "existing_mcp",
    "buildability",
    "main_blocker",
    "evidence_checked",
    "verification_status"
]

for row in rows:
    for field in new_fields:
        row[field] = "Not verified"

    if row["research_status"].startswith("Fetch failed") or row["status_code"] != "200":
        row["verification_status"] = "Manual review required"
        row["main_blocker"] = "Documentation access issue; investigate manually"
    else:
        row["verification_status"] = "Needs official documentation review"

fields = list(rows[0].keys())

with output_file.open("w", encoding="utf-8-sig", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=fields)
    writer.writeheader()
    writer.writerows(rows)

print("Research template created successfully!")
print("Total apps:", len(rows))
print("Output:", output_file)
print("New research fields:", len(new_fields))
