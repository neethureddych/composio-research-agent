import csv
from pathlib import Path

apps_file = Path("data/apps.csv")
backup_file = Path("output/credential_access_review_backup.csv")
output_file = Path("output/credential_access_review.csv")

# Load the corrected 100-app assignment list
with apps_file.open(encoding="utf-8-sig", newline="") as f:
    apps = list(csv.DictReader(f))

# Load previous credential research
with backup_file.open(encoding="utf-8-sig", newline="") as f:
    old_records = {
        row["app_name"].strip(): row
        for row in csv.DictReader(f)
    }

fields = [
    "app_name",
    "category",
    "credential_access",
    "evidence_url",
    "verification_status",
    "notes",
]

verified_count = 0

with output_file.open("w", encoding="utf-8-sig", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=fields)
    writer.writeheader()

    for app in apps:
        name = app["app_name"].strip()
        old = old_records.get(name, {})

        # Reuse only records verified against official documentation
        if old.get("verification_status", "").strip() == "Verified against official documentation":
            credential_access = old.get("credential_access", "")
            evidence_url = old.get("evidence_url", "")
            status = "Verified against official documentation"
            notes = old.get("notes", "")
            verified_count += 1
        else:
            credential_access = "Not yet verified"
            evidence_url = ""
            status = "Pending verification"
            notes = "Requires review of official authentication and API documentation."

        writer.writerow({
            "app_name": name,
            "category": app["category"],
            "credential_access": credential_access,
            "evidence_url": evidence_url,
            "verification_status": status,
            "notes": notes,
        })

print("Corrected credential review created.")
print("Total assignment apps:", len(apps))
print("Verified records carried over:", verified_count)
print("Pending records:", len(apps) - verified_count)
print("Saved to:", output_file)