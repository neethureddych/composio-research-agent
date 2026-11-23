import csv
import time
import requests
from bs4 import BeautifulSoup
from pathlib import Path

INPUT_FILE = Path("data/apps.csv")
OUTPUT_FILE = Path("output/research_results.csv")

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; AppResearchStudent/1.0)"
}

def research_app(app):
    url = app["docs_url"]
    result = {
        "app_name": app["app_name"],
        "category": app["category"],
        "website": app["website"],
        "docs_url": url,
        "page_title": "",
        "description": "",
        "status_code": "",
        "research_status": "Not checked",
        "evidence_url": url
    }

    try:
        response = requests.get(
            url,
            headers=HEADERS,
            timeout=15
        )
        result["status_code"] = response.status_code

        soup = BeautifulSoup(response.text, "html.parser")

        if soup.title:
            result["page_title"] = soup.title.get_text(" ", strip=True)

        description = soup.find(
            "meta",
            attrs={"name": "description"}
        )

        if description:
            result["description"] = description.get("content", "").strip()

        if response.status_code == 200:
            result["research_status"] = "Page fetched - manual verification required"
        else:
            result["research_status"] = "HTTP response - manual review required"

    except requests.RequestException as error:
        result["research_status"] = f"Fetch failed: {type(error).__name__}"

    return result


def main():
    with INPUT_FILE.open("r", encoding="utf-8-sig", newline="") as file:
        apps = list(csv.DictReader(file))

    results = []

    print(f"Starting research for {len(apps)} apps...\n")

    for number, app in enumerate(apps, start=1):
        print(f"[{number}/{len(apps)}] Researching {app['app_name']}")

        result = research_app(app)
        results.append(result)

        time.sleep(0.5)

    OUTPUT_FILE.parent.mkdir(exist_ok=True)

    with OUTPUT_FILE.open("w", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)

    successful = sum(
        1 for item in results
        if item["research_status"].startswith("Page fetched")
    )

    print("\nResearch completed!")
    print(f"Total apps: {len(results)}")
    print(f"Pages fetched successfully: {successful}")
    print(f"Needs review: {len(results) - successful}")
    print(f"Results saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
