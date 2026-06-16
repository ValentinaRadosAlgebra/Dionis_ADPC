import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
from code.clients import find
from pathlib import Path
import os

# def run():
#     base_dir = Path(os.getcwd())
#     output_dir = base_dir / "output" / "plots"
#     output_dir.mkdir(parents=True, exist_ok=True)

#     data = find("clean_observations")

#     counts = {}

#     for d in data:
#         species = d.get("species_normalized") or d.get("species")

#         if not species:
#             continue

#         species = str(species).strip().lower()

#         if species in ["none", "null", ""]:
#             continue

#         counts[species] = counts.get(species, 0) + 1

#     if not counts:
#         print("No valid species data → creating empty plot")

#         out_file = output_dir / "birds.png"

#         plt.figure()
#         plt.text(0.5, 0.5, "No valid data", ha='center')
#         plt.axis("off")

#         plt.savefig(out_file, dpi=150, bbox_inches="tight")
#         plt.close()

#         return

#     labels = list(counts.keys())
#     values = list(counts.values())

#     out_file = output_dir / "birds.png"

#     plt.figure()
#     plt.bar(labels, values)
#     plt.xticks(rotation=45)
#     plt.tight_layout()

#     plt.savefig(out_file, dpi=150, bbox_inches="tight")
#     plt.close()

#     print("visualisation done →", out_file)

# if __name__ == "__main__":
#     run()


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

        if species:
            counts[species] += 1 if species in counts else 1

    # 🔥 FIX: ensure deterministic ordering + valid types
    if not counts:
        print("No valid species data → creating empty plot safely")

        plt.figure()
        plt.text(0.5, 0.5, "No data", ha="center", va="center")
        plt.axis("off")

        out_file = output_dir / "birds.png"
        plt.savefig(out_file, dpi=150, bbox_inches="tight")
        plt.close()
        return

    labels = list(map(str, counts.keys()))
    values = list(map(int, counts.values()))

    plt.figure()

    # 🔥 FIX: force categorical-safe plotting
    plt.bar(labels, values)

    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()

    out_file = output_dir / "birds.png"

    # 🔥 IMPORTANT: save FIRST, close AFTER
    plt.savefig(out_file, dpi=150, bbox_inches="tight")
    plt.close()

    # 🔥 ensure file is flushed to disk (Windows fix for Snakemake)
    with open(out_file, "rb") as f:
        f.read()

    print("visualisation done")


if __name__ == "__main__":
    run()