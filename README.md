# Virtutes Herbarum

Research project of UCLy (research unit CONFLUENCE: Sciences et Humanités). From historical herbals, extract every statement "plant X, prepared this way, is good for Y", tied to its page and comparable across texts, places and centuries. The pilot covers six European works, from Theophrastus to a 17th-century French herbal.

This repository holds the methods, the tables of versions, the tools and the texts of the works in one common format. It does not hold the scans: they are listed, with source and checksum, in `data/Downloads_report.csv`.

## The documents

| To learn about | Read |
|---|---|
| The project, its steps, its vocabulary | `docs/Project_context.md` |
| How all versions of a work are found | `docs/Edition_mapping_method.md` |
| How the versions to use are chosen | `docs/Version_selection_method.md` |
| How the folders are organised, what is in git | `docs/Folder_structure.md` |
| The single text format all works are brought to | `docs/Unified_text_format.md` |
| How a version is brought to it | `docs/Conversion_method.md` |
| Reading the scans by machine (proposal) | `docs/OCR_Kraken_approach.md` |
| Classifying illnesses and remedies (Staub et al. 2015) | `docs/Staub_2015_classification_summary.md` |
| The articles relied on | `references/README.md` |

Each chosen version has its own folder under `data/`, with a plain-language `metadata/note.txt`.

## Three kinds of files, each with one job

- **Documentation** (`README.md`, `docs/`, the `note.txt` files): what the project is and how it is defined. No dates, no progress.
- **Instructions** (`AGENTS.md`, `skills/`): how AI assistants must work here.
- **Work in progress** (`WIP.md`): what remains to do, in order.

History is in git. Each script is described in its own opening comment.
