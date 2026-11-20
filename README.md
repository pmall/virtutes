# Virtutes Herbarum

Research project of UCLy (research unit CONFLUENCE: Sciences et Humanités). From historical herbals, extract every statement "plant X, prepared this way, is good for Y", tied to its page and comparable across texts, places and centuries. The pilot covers six European works, from Theophrastus to a 17th-century French herbal.

This repository holds the methods, the tables of versions, the tools and the scripts that bring each work to one common text format. It does not hold the scans and typed texts the libraries delivered, nor the texts made from them: the first are listed, with exact address and checksum, in the `metadata/sources.csv` of each version; the second are made again by the scripts ([`docs/Folder_structure.md`](docs/Folder_structure.md#what-is-in-git-and-what-is-not)).

## Setting up

Python and the packages the scripts need are managed with [uv](https://docs.astral.sh/uv/), the only program to install by hand. [`pyproject.toml`](pyproject.toml) names the Python version and the packages; [`uv.lock`](uv.lock) records the exact version and checksum of each. From the repository folder:

```bash
uv sync
```

This fetches the right Python if the computer does not have it and installs the packages in `.venv/`, inside the folder. Every script is then run with `uv run`, for example `uv run tools/vh_check.py`, which compares everything the scripts have produced so far with the recorded results.

## The documents

| To learn about | Read |
|---|---|
| The project, its steps, its vocabulary | [`docs/Project_context.md`](docs/Project_context.md) |
| How all versions of a work are found | [`docs/Edition_mapping_method.md`](docs/Edition_mapping_method.md) |
| How the versions to use are chosen | [`docs/Version_selection_method.md`](docs/Version_selection_method.md) |
| How the folders are organised, what is in git | [`docs/Folder_structure.md`](docs/Folder_structure.md) |
| The single text format all works are brought to | [`docs/Unified_text_format.md`](docs/Unified_text_format.md) |
| How a version is brought to it | [`docs/Conversion_method.md`](docs/Conversion_method.md) |
| Reading the scans by machine (proposal) | [`docs/OCR_Kraken_approach.md`](docs/OCR_Kraken_approach.md) |
| Retraining the model that marks the blocks of a page (on trial) | [`docs/Layout_fine_tuning.md`](docs/Layout_fine_tuning.md) |
| Classifying illnesses and remedies (Staub et al. 2015) | [`docs/Staub_2015_classification_summary.md`](docs/Staub_2015_classification_summary.md) |
| Identifying the plants of historical texts (Lardos et al. 2024) | [`docs/Lardos_2024_plant_identification_summary.md`](docs/Lardos_2024_plant_identification_summary.md) |
| The articles relied on | [`references/README.md`](references/README.md) |

Each chosen version has its own folder under [`works/`](works/), with a plain-language `metadata/note.txt`.

## Three kinds of files, each with one job

- **Documentation** (`README.md`, [`docs/`](docs/), the `note.txt` files): what the project is and how it is defined. No dates, no progress.
- **Instructions** ([`AGENTS.md`](AGENTS.md), [`skills/`](skills/)): how AI assistants must work here.
- **Work in progress** ([`WIP.md`](WIP.md)): what remains to do, in order.

History is in git. Each script is described in its own opening comment.
