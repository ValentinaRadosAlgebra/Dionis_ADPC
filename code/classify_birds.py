import json
import os
from pathlib import Path

import requests

from code.clients import (
    find,
    download_file,
    insert,
    upload_json
)

from code.kafka_producer import send_observation

API_URL = "https://aves.regoch.net/api/classify"
TEMP_DIR = "temp"

def classify_audio(audio_file):
    with open(audio_file, "rb") as f:

        response = requests.post(
            API_URL,
            files={"file": f}
        )

    response.raise_for_status()

    data = response.json()

    if not data.get("results"):
        return None

    return data["results"][0]


def extract_species(result):

    if not result:
        return None

    return (
        result.get("scientificName")
        or result.get("species")
        or result.get("canonicalName")
        or result.get("label")
    )

def run():

    os.makedirs(TEMP_DIR, exist_ok=True)

    files = find("files")

    if not files:
        print("No files found")
        return

    for f in files:

        local_path = os.path.join(
            TEMP_DIR,
            f["object_name"]
        )

        try:

            download_file(
                f["object_name"],
                local_path
            )

            result = classify_audio(local_path)

            if result is None:
                continue

            species = extract_species(result)

            taxonomy = find(
                "taxonomy",
                {"species": species}
            )

            species_key = None

            if taxonomy:
                species_key = taxonomy[0]["key"]

            classification_doc = {
                "file": f["object_name"],
                "species": species,
                "species_key": species_key,
                "confidence": result.get(
                    "confidence",
                    0
                ),
                "latitude": f.get(
                    "latitude"
                ),
                "longitude": f.get(
                    "longitude"
                )
            }

            insert(
                "classifications",
                classification_doc
            )

            log = {
                "file": f["object_name"],
                "request": API_URL,
                "response": result
            }

            upload_json(
                json.dumps(log, indent=2),
                f"logs/{f['object_name']}.json"
            )

            try:
                send_observation(classification_doc)
            except Exception as e:
                print("Kafka failed, fallback to DB:", e)
                insert("observations", classification_doc)

        except Exception as e:

            print(
                f"Failed processing {f['object_name']}: {e}"
            )

        finally:

            if os.path.exists(local_path):
                os.remove(local_path)

    Path(
        "output/classify.done"
    ).touch()

    print("classification done")


if __name__ == "__main__":
    run()
