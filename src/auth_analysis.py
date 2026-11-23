import csv
from collections import Counter

with open("data/composio_toolkits.csv", encoding="utf-8-sig") as f:
    toolkits = list(csv.DictReader(f))

auth_counts = Counter()

for toolkit in toolkits:
    schemes = toolkit["auth_schemes"].strip()

    if schemes:
        for scheme in schemes.split(";"):
            auth_counts[scheme.strip()] += 1
    else:
        auth_counts["Not specified"] += 1

print("\nAUTHENTICATION METHOD DISTRIBUTION\n")

for scheme, count in auth_counts.most_common():
    print(f"{scheme}: {count}")

print("\nTotal toolkit records:", len(toolkits))
