import csv

path = "output/credential_access_review.csv"

verified = {
    "Zendesk": (
        "Self-serve OAuth client configuration by a Zendesk administrator",
        "https://developer.zendesk.com/documentation/authentication/api-tokens-to-oauth/; https://developer.zendesk.com/documentation/authentication/using-oauth-to-authenticate-zendesk-api-requests-in-a-web-app/",
        "Creating an OAuth client requires Zendesk admin access. Supports authorization-code and client-credentials flows."
    ),
    "Twilio": (
        "Self-serve API key creation through Twilio Console",
        "https://www.twilio.com/docs/iam/api-keys/keys-in-console; https://www.twilio.com/docs/iam/api-keys",
        "Main, Standard and Restricted API keys offer different access levels. Keys can be managed through the Console."
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
