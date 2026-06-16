from rapidfuzz import process
from code.clients import find, insert
from pathlib import Path


def run():
    taxonomy = find("taxonomy")
    observations = find("observations")

    species_list = [t["species"] for t in taxonomy if "species" in t]

    for obs in observations:
        result = process.extractOne(obs.get("species", ""), species_list)

        if result is None:
            obs["species_normalized"] = obs.get("species")
        else:
            match, score, _ = result
            obs["species_normalized"] = match if score > 70 else obs.get("species")

        obs.pop("_id", None)

        if not obs.get("species"):
            continue

        insert("clean_observations", obs)

    Path("output/fuzzy.done").touch()
    print("fuzzy done")


if __name__ == "__main__":
    run()