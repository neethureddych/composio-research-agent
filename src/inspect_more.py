import csv

wanted = {
    "zoho", "monday", "whatsapp", "devin_mcp",
    "highlevel_agency", "highlevel_location",
    "highlevel_mcp", "mermaid_chart_mcp",
    "monday_mcp", "mongodb", "mongodb_mcp",
    "netlify_mcp", "otter_ai_mcp", "pylon_mcp",
    "threads"
}

with open("data/composio_toolkits.csv", encoding="utf-8-sig") as f:
    rows = csv.DictReader(f)
    matches = [
        row for row in rows
        if row["slug"].lower() in wanted
    ]

with open("output/candidate_details.csv", "w", encoding="utf-8-sig", newline="") as f:
    fields = [
        "name", "slug", "description", "tools_count",
        "triggers_count", "auth_schemes", "app_url"
    ]
    writer = csv.DictWriter(f, fieldnames=fields)
    writer.writeheader()

    for row in matches:
        writer.writerow({field: row.get(field, "") for field in fields})

print("Candidate records saved:", len(matches))
print("File: output/candidate_details.csv")