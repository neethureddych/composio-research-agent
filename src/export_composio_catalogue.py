import csv
from pathlib import Path
from dotenv import load_dotenv
from composio import Composio

load_dotenv()

client = Composio()
all_toolkits = []
cursor = None
page = 1

print("Starting Composio toolkit collection...")

while True:
    response = client.toolkits.list(
        limit=1000,
        cursor=cursor
    )

    items = response.items

    for toolkit in items:
        all_toolkits.append({
            "slug": getattr(toolkit, "slug", ""),
            "name": getattr(toolkit, "name", ""),
            "auth_schemes": "; ".join(
                getattr(toolkit, "auth_schemes", []) or []
            ),
            "description": getattr(toolkit, "description", ""),
            "category": getattr(toolkit, "category", "")
        })

    print(f"Page {page}: collected {len(items)} toolkits")
    cursor = response.next_cursor

    if not cursor:
        break

    page += 1

output_file = Path("data/composio_toolkits.csv")
output_file.parent.mkdir(exist_ok=True)

with output_file.open("w", encoding="utf-8-sig", newline="") as file:
    writer = csv.DictWriter(
        file,
        fieldnames=[
            "slug", "name", "auth_schemes",
            "description", "category"
        ]
    )
    writer.writeheader()
    writer.writerows(all_toolkits)

print("\nCollection completed!")
print("Total toolkits:", len(all_toolkits))
print("Pages collected:", page)
print("Saved to:", output_file)
