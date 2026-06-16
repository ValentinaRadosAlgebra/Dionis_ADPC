import os
import requests
from code.clients import find, download_file
from code.kafka_producer import send_observation
from pathlib import Path

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


def run():

    os.makedirs(TEMP_DIR, exist_ok=True)

    files = find("files")

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
                print("No species found in")
                continue

            observation = {
                "file": f["object_name"],
                "species": result.get(
                    "scientificName",
                    result.get("species")
                ),
                "confidence": result.get(
                    "confidence",
                    0
                )
            }

            send_observation(observation)


        except Exception as e:
            print(
                f"Failed processing "
                f"{f['object_name']}: {e}"
            )

        finally:
            if os.path.exists(local_path):
                os.remove(local_path)

    Path("output/classify.done").touch()
    print("classification done")


if __name__ == "__main__":
    run()