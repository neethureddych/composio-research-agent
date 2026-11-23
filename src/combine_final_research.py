import csv
from pathlib import Path

def load_csv(path):
    with open(path, encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))

apps = load_csv("data/apps.csv")
docs = {r["app_name"]: r for r in load_csv("output/research_results.csv")}
composio = {r["app_name"]: r for r in load_csv("data/app_composio_comparison.csv")}
credentials = {r["app_name"]: r for r in load_csv("output/credential_access_review.csv")}

fields = [
    "app_name",
    "category",
    "website",
    "docs_url",
    "page_title",
    "description",
    "status_code",
    "research_status",
    "evidence_url",
    "composio_match",
    "toolkit_name",
    "toolkit_slug",
    "auth_schemes",
    "credential_access",
    "credential_verification_status",
    "credential_evidence_url",
    "credential_notes",
]

output = Path("output/final_research.csv")

with output.open("w", encoding="utf-8-sig", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=fields)
    writer.writeheader()

    for app in apps:
        name = app["app_name"]
        doc = docs.get(name, {})
        comp = composio.get(name, {})
        cred = credentials.get(name, {})

        writer.writerow({
            "app_name": name,
            "category": app["category"],
            "website": app.get("website", ""),
            "docs_url": app.get("docs_url", ""),
            "page_title": doc.get("page_title", ""),
            "description": doc.get("description", ""),
            "status_code": doc.get("status_code", ""),
            "research_status": doc.get("research_status", "Missing research record"),
            "evidence_url": doc.get("evidence_url", ""),
            "composio_match": comp.get("composio_match", "Not checked"),
            "toolkit_name": comp.get("toolkit_name", ""),
            "toolkit_slug": comp.get("toolkit_slug", ""),
            "auth_schemes": comp.get("auth_schemes", ""),
            "credential_access": cred.get("credential_access", ""),
            "credential_verification_status": cred.get("verification_status", "Pending verification"),
            "credential_evidence_url": cred.get("evidence_url", ""),
            "credential_notes": cred.get("notes", ""),
        })

print("Final research file created.")
print("Assignment apps:", len(apps))
print("Documentation records:", len(docs))
print("Composio comparison records:", len(composio))
print("Credential records:", len(credentials))
print("Saved to:", output)