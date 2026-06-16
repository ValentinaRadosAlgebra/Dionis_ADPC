import os
import pandas as pd

from code.clients import find

OUTPUT_DIR = "output"


def run():

    os.makedirs(
        OUTPUT_DIR,
        exist_ok=True
    )

    data = find("clean_observations")

    if not data:
        return

    df = pd.DataFrame(data)

    if "_id" in df.columns:
        df = df.drop(columns=["_id"])

    report_path = (
        f"{OUTPUT_DIR}/report.csv"
    )

    df.to_csv(
        report_path,
        index=False
    )


if __name__ == "__main__":
    run()