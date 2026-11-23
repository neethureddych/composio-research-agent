import csv

path = "output/credential_access_review.csv"

verified = {
    "Slack": (
        "Self-serve app creation; OAuth 2.0 authorization by workspace users; access controlled by requested scopes",
        "https://docs.slack.dev/authentication/; https://docs.slack.dev/authentication/tokens/; https://docs.slack.dev/apis/web-api/",
        "Workspace authorization and requested scopes determine access. Web API uses HTTP RPC-style methods."
    ),
    "Discord": (
        "Self-serve Developer Portal application and bot creation; OAuth 2.0 or bot-token authentication",
        "https://discord.com/developers/docs/topics/oauth2; https://discord.com/developers/docs/quick-start/getting-started; https://discord.com/developers/docs/interactions/slash-commands",
        "Adding an app to a server requires appropriate permissions. Some privileged capabilities have additional requirements."
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
