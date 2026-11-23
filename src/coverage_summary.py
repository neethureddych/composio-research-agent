import csv
from collections import defaultdict

stats = defaultdict(lambda: {"total": 0, "matched": 0})

with open("data/app_composio_comparison.csv", encoding="utf-8-sig") as f:
    for row in csv.DictReader(f):
        category = row["category"]
        stats[category]["total"] += 1

        if row["composio_match"].strip() == "Found in Composio catalogue":
            stats[category]["matched"] += 1

print("\nCATEGORY-WISE EXACT MATCH COVERAGE")
print("-" * 65)

total_apps = 0
total_matches = 0

for category, values in sorted(stats.items()):
    total = values["total"]
    matched = values["matched"]
    percentage = matched / total * 100

    total_apps += total
    total_matches += matched

    print(f"{category:40} {matched:2}/{total:2} ({percentage:.1f}%)")

print("-" * 65)
print("Total categories:", len(stats))
print("Total apps:", total_apps)
print("Exact matches:", total_matches)
print("Exact match coverage:", f"{total_matches / total_apps * 100:.1f}%")