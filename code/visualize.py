import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
from code.clients import find
from pathlib import Path


def run():
    output_dir = Path("output/plots")
    output_dir.mkdir(parents=True, exist_ok=True)

    data = list(find("clean_observations"))

    counts = {}

    for d in data:
        species = d.get("species_normalized") or d.get("species")

        if not species:
            continue

        species = str(species).strip()

        if not species or species.lower() in ["none", "null"]:
            continue

        counts[species] = counts.get(species, 0) + 1

    if not counts:
        print("No valid species data")

        plt.figure()
        plt.text(0.5, 0.5, "No data", ha="center", va="center")
        plt.axis("off")

        out_file = output_dir / "birds.png"
        plt.savefig(out_file, dpi=150, bbox_inches="tight")
        plt.close()
        return

    labels = list(counts.keys())
    values = list(counts.values())

    plt.figure()
    plt.bar(labels, values)

    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()

    out_file = output_dir / "birds.png"
    plt.savefig(out_file, dpi=150, bbox_inches="tight")
    plt.close()

    print("visualisation done", out_file)


if __name__ == "__main__":
    run()