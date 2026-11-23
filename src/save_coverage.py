import csv
from collections import defaultdict

with open("data/app_composio_comparison.csv", encoding="utf-8-sig") as f:
    rows = list(csv.DictReader(f))

stats = defaultdict(lambda: {"total": 0, "matched": 0})

for row in rows:
    category = row["category"]
    stats[category]["total"] += 1
    if row["composio_match"] == "Found in Composio catalogue":
        stats[category]["matched"] += 1

with open("output/category_coverage.csv", "w", encoding="utf-8-sig", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["category", "total_apps", "exact_matches", "coverage_percent"])

    for category, values in sorted(stats.items()):
        percentage = round(values["matched"] / values["total"] * 100, 1)
        writer.writerow([category, values["total"], values["matched"], percentage])

print("Saved output/category_coverage.csv")
