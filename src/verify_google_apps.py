import csv

path = "output/credential_access_review.csv"

verified = {
    "Google Meet": (
        "Self-serve Google Cloud project and OAuth consent setup",
        "https://developers.google.com/workspace/meet/api/guides/authenticate-authorize",
        "Users authorize requested OAuth scopes. Sensitive or restricted scopes can require additional verification."
    ),
    "Gmail": (
        "Self-serve Google Cloud project and OAuth setup",
        "https://developers.google.com/workspace/gmail/api/auth/scopes",
        "Sensitive and restricted Gmail scopes can require Google verification and additional security assessment."
    )
}

with open(path, encoding="utf-8-sig", newline="") as f:
    rows = list(csv.DictReader(f))
    fields = list(rows[0].keys())

updated = 0

for row in rows:
    if row["app_name"] in verified:
        access, url, notes = verified[row["app_name"]]
        row["credential_access"] = access
        row["evidence_url"] = url
        row["notes"] = notes
        row["verification_status"] = "Verified against official documentation"
        updated += 1

with open(path, "w", encoding="utf-8-sig", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=fields)
    writer.writeheader()
    writer.writerows(rows)

print("Verified records updated:", updated)
print("Saved:", path)
