import os
import pandas as pd

from code.clients import find

OUTPUT_DIR = "output"


def run():

    os.makedirs(
        OUTPUT_DIR,
        exist_ok=True
    )

    data = find(
        "clean_observations"
    )

    if not data:
        print("No data")
        return

    df = pd.DataFrame(data)

    if "_id" in df.columns:
        df = df.drop(
            columns=["_id"]
        )

    species_col = (
        "species_normalized"
        if "species_normalized" in df.columns
        else "species"
    )

    report = (
        df.groupby(species_col)
        .agg(
            sightings=(
                species_col,
                "count"
            ),
            avg_confidence=(
                "confidence",
                "mean"
            )
        )
        .reset_index()
    )

    report.columns = [
        "species_name",
        "classified_sightings",
        "avg_confidence"
    ]

    report = report.sort_values(
        by="classified_sightings",
        ascending=False
    )

    report.to_csv(
        f"{OUTPUT_DIR}/report.csv",
        index=False
    )

    print(
        f"Report generated ({len(report)} species)"
    )


if __name__ == "__main__":
    run()