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

print("\nCATEGORY-WISE COMPOSIO COVERAGE\n")

for category, values in sorted(stats.items()):
    total = values["total"]
    matched = values["matched"]
    percentage = matched / total * 100
    print(f"{category}: {matched}/{total} ({percentage:.1f}%)")

print("\nOVERALL")
matched = sum(v["matched"] for v in stats.values())
print(f"{matched}/{len(rows)} ({matched / len(rows) * 100:.1f}%) exact-name coverage")
