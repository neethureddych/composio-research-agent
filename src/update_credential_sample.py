import csv

updates = {
    "Slack": [
        "Self-serve app creation and OAuth",
        "https://docs.slack.dev/authentication/; https://docs.slack.dev/authentication/tokens/; https://docs.slack.dev/apis/web-api/",
        "Workspace approval, OAuth scopes and permissions."
    ],
    "Discord": [
        "Self-serve Developer Portal application and bot creation",
        "https://discord.com/developers/docs/topics/oauth2; https://discord.com/developers/docs/quick-start/getting-started; https://discord.com/developers/docs/reference",
        "Server installation requires authorization from a member with appropriate permissions. Some OAuth scopes require Discord approval."
    ],
    "Microsoft Teams": [
        "Self-serve app registration",
        "https://learn.microsoft.com/microsoftteams/app-permissions",
        "Admin consent may be required for application permissions."
    ],
    "Zoom": [
        "Self-serve developer app creation",
        "https://developers.zoom.us/docs/integrations/create/",
        "Account and developer permissions; admin approval may apply."
    ],
    "Google Meet": [
        "Self-serve Google Cloud project and OAuth setup",
        "https://developers.google.com/workspace/meet/api/guides/authenticate-authorize",
        "User consent and possible OAuth verification or security assessment."
    ],
    "Gmail": [
        "Self-serve Google Cloud project and OAuth setup",
        "https://developers.google.com/workspace/gmail/api/auth/scopes",
        "Sensitive and restricted scopes require additional verification."
    ],
    "Outlook": [
        "Self-serve Microsoft Entra app registration",
        "https://learn.microsoft.com/en-us/graph/auth-v2-service",
        "Administrator consent may be required for application permissions."
    ],
    "Intercom": [
        "Self-serve app creation and OAuth setup",
        "https://developers.intercom.com/docs/build-an-integration/learn-more/authentication",
        "Public integrations require customer authorization; private apps use workspace access tokens."
    ],
    "Zendesk": [
        "Self-serve OAuth configuration for account admins",
        "https://developer.zendesk.com/documentation/authentication/api-tokens-to-oauth/",
        "Creating an OAuth client requires Zendesk admin access."
    ],
    "Twilio": [
        "Self-serve API key creation through Console",
        "https://www.twilio.com/docs/iam/api-keys/keys-in-console",
        "Appropriate account permissions are needed to create and manage API keys."
    ]
}

path = "output/credential_access_review.csv"

with open(path, encoding="utf-8-sig", newline="") as f:
    rows = list(csv.DictReader(f))
    fields = list(rows[0].keys())

updated = 0

for row in rows:
    if row["app_name"] in updates:
        access, url, notes = updates[row["app_name"]]
        row["credential_access"] = access
        row["evidence_url"] = url
        row["verification_status"] = "Manually reviewed against official documentation"
        row["notes"] = notes
        updated += 1

with open(path, "w", encoding="utf-8-sig", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=fields)
    writer.writeheader()
    writer.writerows(rows)

print("Updated records:", updated)
print("Remaining unreviewed:", len(rows) - updated)
print("Saved:", path)
