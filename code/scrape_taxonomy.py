import requests
from pathlib import Path
from code.clients import upsert
from bs4 import BeautifulSoup

DATA_URL = "https://aves.regoch.net/aves.json"
PAGE_URL = "https://aves.regoch.net/index.html"

def run():
    page_response = requests.get(PAGE_URL)
    page_response.raise_for_status()

    soup = BeautifulSoup(page_response.text, "lxml")

    table = soup.find("table", {"id": "speciesTable"})

    if table is None:
        raise Exception(
            "speciesTable not found on Aves Portal page"
        )

    print("Aves Portal page scraped successfully")

    data_response = requests.get(DATA_URL)
    data_response.raise_for_status()

    birds = data_response.json()

    for bird in birds:

        doc = {
            "key": bird.get("key"),
            "species": bird.get("scientificName"),
            "canonical_name": bird.get("canonicalName"),
            "family": bird.get("family"),
            "genus": bird.get("genus"),
            "order": bird.get("order"),
            "rank": bird.get("rank")
        }

        upsert(
            "taxonomy",
            {"key": bird.get("key")},
            doc
        )

    Path("output/scrape.done").touch() #output
    print(
        f"Scraping {len(birds)} taxonomy records."
    )


if __name__ == "__main__":
    run()