import csv

matches = [
    ["Monday.com", "Monday", "monday", "OAUTH2", "Possible match - verify product coverage"],
    ["Zoho CRM", "Zoho", "zoho", "OAUTH2", "Possible match - verify CRM coverage"],
    ["Intercom CRM", "Intercom", "intercom", "OAUTH2", "Possible match - verify CRM coverage"],
    ["Plausible", "Plausible Analytics", "plausible_analytics", "API_KEY", "Likely match - verify official integration"],
    ["Netlify", "Netlify MCP", "netlify_mcp", "DCR_OAUTH", "Possible match - verify supported tools"],
    ["Sentry Dev", "Sentry", "sentry", "OAUTH2", "Likely match - verify supported tools"],
    ["Sentry Dev", "Sentry MCP", "sentry_mcp", "DCR_OAUTH", "Possible match - verify supported tools"],
    ["Discord Bots", "Discord Bot", "discordbot", "OAUTH2", "Possible match - verify bot functionality"],
    ["Discord Bots", "Discord", "discord", "OAUTH2", "Possible match - verify bot functionality"],
    ["WhatsApp Business", "WhatsApp", "whatsapp", "OAUTH2; API_KEY", "Possible match - verify Business API support"]
]

with open("data/alias_review.csv", "w", encoding="utf-8-sig", newline="") as f:
    writer = csv.writer(f)
    writer.writerow([
        "target_app", "composio_toolkit", "toolkit_slug",
        "auth_schemes", "review_status"
    ])
    writer.writerows(matches)

print("Alias review saved to data/alias_review.csv")
print("Candidate records:", len(matches))
