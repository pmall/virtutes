# Virtutes Herbarum — entry point for AI agents

Research project (UCLy, CONFLUENCE): extract from historical herbals every statement "plant X, prepared this way, is good for Y", tied to its page, comparable across texts, places and centuries. Pilot: six European works. Full context: `docs/Project_context.md`.

This folder is a self-contained git repository: every path below is relative to it. Keep this file short: pointers and rules only; put detail in the linked files.

## Where things are

| Path | What |
|---|---|
| `docs/Project_context.md` | Project, aims, team, hardware, state, study positions, terms |
| `docs/Edition_mapping_method.md` | How to map every version of a work |
| `docs/Version_selection_method.md` | How to choose the versions to use (original, English, French) |
| `docs/Folder_structure.md` | Workspace and version folders; what is in git; the note.txt |
| `docs/Unified_text_format.md` | The single text format every version ends in; all later analysis reads it |
| `docs/Conversion_method.md` | How a version is converted: one script per version, steps, checks |
| `docs/OCR_Kraken_approach.md` | Proposal under discussion: reading the scans with Kraken |
| `docs/Staub_2015_classification_summary.md` | Classifying illnesses and remedies; ideas taken for the project |
| `tools/` | Shared scripts: format check (`vh_text.py`), catalogue export, edition-map merge, downloads |
| `catalogue/` | Copies of the 5 catalogue spreadsheets (227 works) and `catalogue_rows.csv`; the originals in the project folder remain the source of truth |
| `references/` | Articles the project relies on (PDFs not in git; list in `references/README.md`) |
| `data/Pilot_works_all_versions.csv` | Every known edition and translation of the 6 pilot works (do not modify) |
| `data/Pilot_selected_versions.csv` | The versions chosen, the deciding rule, why the others lost |
| `data/Downloads_report.csv` | Every downloaded file, its source and checksum |
| `data/<n>_<Work>_<slot>_<Version>_<year>/` | One folder per chosen version: `metadata/note.txt`, `source/` (as delivered), `convert/` (its own scripts and notes), `work/` (intermediate), `text/` (result) |

## Status

- 2026-11-12: edition map done; selection done; all selected versions downloaded and checked.
- 2026-11-16: folder made a git repository; unified text format (v0.1) and conversion method defined. No version converted yet.
- Next step: convert the 4 typed texts (Theophrastus grc, Dioscorides grc, Pliny lat, Pliny eng), adjusting the format if needed. Then the 8 scans: compare Kraken, Tesseract and small AI reading models on hand-corrected reference pages first. Hardware: laptop Intel Core Ultra 5 (tests); GPU server RTX 6000 96 GB (bulk).

## Rules

- **Never download without the user's explicit go-ahead.** Give size and duration first, then wait.
- **`source/` files are never touched**: kept exactly as the library delivered them. Scripts read them, never write there.
- **`text/` is never edited by hand**: it is the output of the version's `convert/convert.py` and must pass `python3 tools/vh_text.py check <version folder>` before it is committed.
- The text layer holds no interpretation (no plant identification, no modern disease name).
- Bulky files stay out of git (`.gitignore`); never force-add scans, typed-text sources or article PDFs.
- Present works as **one table, one row per version, the works as entry points**. One version = one edition or one manuscript, whatever its languages. Count the same way every time.
- Say whether a fact was checked or assumed; never state an unverified fact as verified. Study proposals are not decisions.
- Documents are for researchers from other fields: plain language, not addressed to the user.
- Deliverables are local files in this folder; nothing online unless asked.
- Be polite to libraries: low request rate, generic client name, no personal or project details.
- Paths may contain spaces and accents: quote them. Python: standard library only; ask before installing anything.
