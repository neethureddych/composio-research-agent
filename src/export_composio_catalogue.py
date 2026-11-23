
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
        meta = getattr(toolkit, "meta", None)

        categories = getattr(meta, "categories", []) or []

        all_toolkits.append({
            "slug": getattr(toolkit, "slug", ""),
            "name": getattr(toolkit, "name", ""),
            "app_url": getattr(meta, "app_url", "") if meta else "",
            "description": getattr(meta, "description", "") if meta else "",
            "auth_schemes": "; ".join(
                getattr(toolkit, "auth_schemes", []) or []
            ),
            "composio_managed_auth_schemes": "; ".join(
                getattr(toolkit, "composio_managed_auth_schemes", []) or []
            ),
            "category": "; ".join(
                getattr(category, "name", "") for category in categories
            ),
            "tools_count": getattr(meta, "tools_count", 0) if meta else 0,
            "triggers_count": getattr(meta, "triggers_count", 0) if meta else 0,
            "version": getattr(meta, "version", "") if meta else "",
            "updated_at": getattr(meta, "updated_at", "") if meta else "",
            "toolkit_type": getattr(toolkit, "toolkit_type", "")
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
        fieldnames=list(all_toolkits[0].keys())
    )
    writer.writeheader()
    writer.writerows(all_toolkits)

print("\nCollection completed!")
print("Total toolkits:", len(all_toolkits))
print("Pages collected:", page)
print("Saved to:", output_file)
