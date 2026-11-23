import csv

path = "output/credential_access_review.csv"

verified = {
    "Microsoft Teams": (
        "Self-serve app registration; Microsoft Graph delegated and application permissions",
        "https://learn.microsoft.com/microsoftteams/app-permissions",
        "Admin consent is required for application permissions. Delegated permissions may depend on organization consent settings."
    ),
    "Zoom": (
        "Self-serve OAuth app creation through Zoom App Marketplace, subject to developer permissions",
        "https://developers.zoom.us/docs/integrations/create/; https://developers.zoom.us/docs/api/authentication/; https://developers.zoom.us/docs/internal-apps/s2s-oauth/",
        "Supports user-based OAuth 2.0 and Server-to-Server OAuth. Developer permissions and scope approval may be required."
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
