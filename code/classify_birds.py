import os
import requests
from pathlib import Path

from code.clients import find, download_file, insert
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


def extract_species(result: dict):
    """
    Robust species extraction from API response.
    Different APIs return different keys.
    """
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
        print("No files found in MongoDB 'files' collection")
        return

    for f in files:
        local_path = os.path.join(TEMP_DIR, f["object_name"])

        try:
            download_file(f["object_name"], local_path)

            result = classify_audio(local_path)

            if result is None:
                print(f"No classification result for {f['object_name']}")
                continue

            species = extract_species(result)

            observation = {
                "file": f["object_name"],
                "species": species,
                "confidence": result.get("confidence", 0)
            }

            # print("OBS:", observation)

            send_observation(observation)

            # insert("observations", observation)

        except Exception as e:
            print(f"Failed processing {f['object_name']}: {e}")

        finally:
            if os.path.exists(local_path):
                os.remove(local_path)

    Path("output/classify.done").touch()
    print("classification done")


if __name__ == "__main__":
    run()