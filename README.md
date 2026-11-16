# Virtutes Herbarum

Research project of UCLy (research unit CONFLUENCE: Sciences et Humanités). From historical herbals, extract every statement "plant X, prepared this way, is good for Y", tied to its page and comparable across texts, places and centuries. The pilot covers six European works, from Theophrastus to a 17th-century French herbal.

This repository holds the methods, the tools, the tables of versions and, as they are produced, the texts of the works in one common format. It does not hold the scans (9.4 GB for the pilot): they are listed, with source and checksum, in `data/Downloads_report.csv`.

## Where to start

| To learn about | Read |
|---|---|
| The project, its state, its vocabulary | `docs/Project_context.md` |
| How all versions of a work were found | `docs/Edition_mapping_method.md` → `data/Pilot_works_all_versions.csv` |
| How the versions to use were chosen | `docs/Version_selection_method.md` → `data/Pilot_selected_versions.csv` |
| How the folders are organised, what is in git | `docs/Folder_structure.md` |
| The single text format all works are brought to | `docs/Unified_text_format.md` |
| How each version is converted to it | `docs/Conversion_method.md` |
| Reading the scans by machine (under discussion) | `docs/OCR_Kraken_approach.md` |
| Classifying illnesses and remedies (Staub et al. 2015) | `docs/Staub_2015_classification_summary.md` |

Each chosen version has its own folder under `data/`, with a plain-language `metadata/note.txt`.

## State (16 November 2026)

Versions mapped, chosen and downloaded for the six pilot works. Text format and conversion method defined. Next: convert the four versions that exist as typed texts, then read the eight that exist only as scans.

## Tools

Python 3, standard library only. Run from this folder; each script explains itself when run without arguments.

| Script | What it does |
|---|---|
| `tools/vh_text.py` | Checks a text in the unified format, or prints it for reading |
| `tools/catalogue_export.py` | Flattens the catalogue spreadsheets into one table |
| `tools/merge_edition_maps.py` | Checks and merges the per-work lists of versions |
| `tools/download_ia.py`, `tools/download_iiif_pages.py` | Download a scan from a library, with checksums (never without prior agreement on size and duration) |
