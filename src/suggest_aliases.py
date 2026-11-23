import csv
import re
from difflib import get_close_matches

def normalize(value):
    return re.sub(r"[^a-z0-9]", "", value.lower())

with open("data/app_composio_comparison.csv", encoding="utf-8-sig") as f:
    unmatched = [
        row for row in csv.DictReader(f)
        if row["composio_match"] == "Not found by exact name match"
    ]

with open("data/composio_toolkits.csv", encoding="utf-8-sig") as f:
    toolkits = list(csv.DictReader(f))

names = {
    normalize(t["name"]): t for t in toolkits
}

print("\nPOSSIBLE TOOLKIT NAME MATCHES\n")

for app in unmatched:
    app_name = app["app_name"]
    key = normalize(app_name)

    matches = get_close_matches(key, names.keys(), n=3, cutoff=0.45)

    print(f"\n{app_name}:")
    if matches:
        for match in matches:
            toolkit = names[match]
            print(f"  - {toolkit['name']} ({toolkit['slug']})")
    else:
        print("  - No close name match found")
