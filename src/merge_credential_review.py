import csv

main_path = "output/final_research.csv"
credential_path = "output/credential_access_review.csv"

with open(credential_path, encoding="utf-8-sig", newline="") as f:
    credential_rows = list(csv.DictReader(f))

credential_map = {
    row["app_name"]: row
    for row in credential_rows
    if row["verification_status"] == "Verified against official documentation"
}

with open(main_path, encoding="utf-8-sig", newline="") as f:
    main_rows = list(csv.DictReader(f))
    fields = list(main_rows[0].keys())

updated = 0

for row in main_rows:
    name = row["app_name"]
    if name in credential_map:
        credential = credential_map[name]

        row["credential_access"] = credential["credential_access"]
        row["evidence_checked"] = credential["evidence_url"]
        row["main_blocker"] = credential["notes"]

        if name != "Slack":
            row["verification_status"] = "Credential access verified; other research fields pending"

        updated += 1

with open(main_path, "w", encoding="utf-8-sig", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=fields)
    writer.writeheader()
    writer.writerows(main_rows)

print("Apps merged:", updated)
print("Saved:", main_path)
