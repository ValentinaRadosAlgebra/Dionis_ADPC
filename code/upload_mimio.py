import os
from code.clients import init_bucket, upload_file, upsert
from pathlib import Path

AUDIO_DIR = "data/audio"
LATITUDE = 45.8150
LONGITUDE = 15.9819

def run():
    init_bucket()

    for file in os.listdir(AUDIO_DIR):

        path = os.path.join(AUDIO_DIR, file)

        if not os.path.isfile(path):
            continue

        result = upload_file(path, file)

        metadata = {
            "name": file,
            "object_name": file,
            "size": os.path.getsize(path),
            "etag": getattr(result, "etag", None),
            "latitude": LATITUDE,
            "longitude": LONGITUDE
        }

        upsert(
            "files",
            {"object_name": file},
            metadata
        )

    Path("output/upload.done").touch()
    #print("Inserted:", file)


if __name__ == "__main__":
    run()