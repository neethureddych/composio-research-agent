import csv

candidates = [
    "monday", "zoho", "intercom", "plausible_analytics",
    "netlify_mcp", "sentry", "sentry_mcp",
    "discordbot", "discord", "whatsapp"
]

with open("data/composio_toolkits.csv", encoding="utf-8-sig") as f:
    toolkits = list(csv.DictReader(f))

for slug in candidates:
    for t in toolkits:
        if t["slug"].lower() == slug:
            print("\nName:", t["name"])
            print("Slug:", t["slug"])
            print("Authentication:", t["auth_schemes"])
            print("Description:", t["description"][:350])
            print("-" * 60)
