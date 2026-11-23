import csv

path = "output/credential_access_review.csv"

verified = {
    "Outlook": (
        "Self-serve Microsoft Entra app registration; OAuth 2.0 authorization",
        "https://learn.microsoft.com/en-us/graph/auth-v2-service",
        "Delegated permissions can involve user consent. Application permissions generally require administrator consent."
    ),
    "Intercom": (
        "Self-serve app creation and OAuth setup; private apps can use access tokens",
        "https://developers.intercom.com/docs/build-an-integration/learn-more/authentication",
        "Public integrations require customer authorization. Private integrations use workspace access tokens."
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
