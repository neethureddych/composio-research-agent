import csv
from collections import Counter

with open("data/composio_toolkits.csv", encoding="utf-8-sig") as f:
    toolkits = list(csv.DictReader(f))

counts = Counter()

for toolkit in toolkits:
    schemes = toolkit["auth_schemes"].strip()
    if schemes:
        for scheme in schemes.split(";"):
            counts[scheme.strip()] += 1
    else:
        counts["Not specified"] += 1

with open("output/auth_distribution.csv", "w", encoding="utf-8-sig", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["authentication_method", "toolkit_count"])

    for scheme, count in counts.most_common():
        writer.writerow([scheme, count])

print("Saved output/auth_distribution.csv")
print("Authentication methods:", len(counts))
