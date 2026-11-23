import csv
from pathlib import Path

matches = [
    ["Zoho CRM", "Zoho", "zoho", "OAUTH2", "Partial - CRM actions need verification"],
    ["Monday.com", "Monday; Monday MCP", "monday; monday_mcp", "OAUTH2; DCR_OAUTH", "Strong candidate - action verification pending"],
    ["WhatsApp Business", "WhatsApp", "whatsapp", "OAUTH2; API_KEY", "Strong candidate - Business API described"],
    ["GoHighLevel", "HighLevel Agency; HighLevel Location; HighLevel MCP", "highlevel_agency; highlevel_location; highlevel_mcp", "OAUTH2; BEARER_TOKEN; API_KEY", "Strong candidate - action verification pending"],
    ["Devin", "Devin MCP", "devin_mcp", "API_KEY", "Partial - repository analysis scope"],
    ["Mermaid CLI", "Mermaid Chart MCP", "mermaid_chart_mcp", "NO_AUTH", "Related product - CLI not confirmed"],
    ["MongoDB Atlas", "MongoDB; MongoDB MCP", "mongodb; mongodb_mcp", "S2S_OAUTH2", "Strong candidate - Atlas explicitly described"],
    ["Netlify", "Netlify MCP", "netlify_mcp", "DCR_OAUTH", "Strong candidate - Netlify explicitly described"],
    ["Otter AI", "Otter.ai MCP", "otter_ai_mcp", "DCR_OAUTH", "Strong candidate - Otter explicitly described"],
    ["Pylon", "Pylon MCP", "pylon_mcp", "DCR_OAUTH", "Strong candidate - Pylon explicitly described"],
    ["Threads (Meta)", "Threads", "threads", "OAUTH2", "Strong candidate - Meta Threads explicitly described"],
]

output = Path("data/alias_review.csv")
output.parent.mkdir(exist_ok=True)

with output.open("w", encoding="utf-8-sig", newline="") as f:
    writer = csv.writer(f)
    writer.writerow([
        "target_app",
        "composio_toolkit",
        "toolkit_slug",
        "auth_schemes",
        "review_status"
    ])
    writer.writerows(matches)

print("Alias review saved to:", output)
print("Candidate records:", len(matches))