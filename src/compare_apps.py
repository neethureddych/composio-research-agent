import csv
import re
from pathlib import Path

def normalize(value):
    return re.sub(r"[^a-z0-9]", "", value.lower())

with open("data/apps.csv", encoding="utf-8-sig", newline="") as f:
    target_apps = list(csv.DictReader(f))

with open("data/composio_toolkits.csv", encoding="utf-8-sig", newline="") as f:
    toolkits = list(csv.DictReader(f))

catalogue = {}

for toolkit in toolkits:
    for key in [
        normalize(toolkit["slug"]),
        normalize(toolkit["name"])
    ]:
        catalogue[key] = toolkit

results = []

for app in target_apps:
    name = app["app_name"]
    key = normalize(name)

    match = catalogue.get(key)

    if match:
        status = "Found in Composio catalogue"
        slug = match["slug"]
        auth = match["auth_schemes"]
        toolkit_name = match["name"]
    else:
        status = "Not found by exact name match"
        slug = ""
        auth = ""
        toolkit_name = ""

    results.append({
        "app_name": name,
        "category": app["category"],
        "composio_match": status,
        "toolkit_name": toolkit_name,
        "toolkit_slug": slug,
        "auth_schemes": auth
    })

output = Path("data/app_composio_comparison.csv")

with output.open("w", encoding="utf-8-sig", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=results[0].keys())
    writer.writeheader()
    writer.writerows(results)

matched = sum(
    1 for r in results
    if r["composio_match"] == "Found in Composio catalogue"
)

print("Comparison completed!")
print("Target apps:", len(results))
print("Exact matches:", matched)
print("Not found by exact name:", len(results) - matched)
print("Saved:", output)
