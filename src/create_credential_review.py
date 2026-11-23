import csv

with open("data/apps.csv", encoding="utf-8-sig") as f:
    apps = list(csv.DictReader(f))

with open("output/credential_access_review.csv", "w", encoding="utf-8-sig", newline="") as f:
    writer = csv.DictWriter(
        f,
        fieldnames=[
            "app_name",
            "category",
            "credential_access",
            "evidence_url",
            "verification_status",
            "notes"
        ]
    )
    writer.writeheader()

    for app in apps:
        writer.writerow({
            "app_name": app["app_name"],
            "category": app["category"],
            "credential_access": "Unreviewed",
            "evidence_url": "",
            "verification_status": "Pending official documentation review",
            "notes": ""
        })

print("Credential review file created!")
print("Apps ready for review:", len(apps))
print("Saved: output/credential_access_review.csv")
