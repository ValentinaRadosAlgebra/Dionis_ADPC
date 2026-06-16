import requests
from pathlib import Path
from code.clients import upsert

URL = "https://aves.regoch.net/aves.json"


def run():

    response = requests.get(URL)

    response.raise_for_status()

    birds = response.json()

    for bird in birds:

        doc = {
            "key": bird.get("key"),
            "species": bird.get("scientificName"),
            "canonical_name": bird.get(
                "canonicalName"
            ),
            "family": bird.get("family"),
            "genus": bird.get("genus"),
            "order": bird.get("order")
        }

        upsert(
            "taxonomy",
            {"key": bird.get("key")},
            doc
        )

    Path("output/scrape.done").touch()
    print("srape done")


if __name__ == "__main__":
    run()