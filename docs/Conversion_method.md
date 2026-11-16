# From any source to one text format — method

Virtutes Herbarum. Written 16 November 2026. **A working method proposed by the project's data lead; no version has been converted yet.**

## The goal

Every chosen version ends as text in the unified format (`Unified_text_format.md`), whatever it started as. The selected versions come in three kinds, from the most to the least convenient:

| Kind of source | What has to be done | In the pilot |
|---|---|---|
| **Typed text** made by a scholarly project | Convert its structure; nothing to read | 4 texts: Theophrastus (Greek), Dioscorides (Greek), Pliny (Latin), Pliny (English) |
| **Scan of a printed book** | Read the pages by machine, correct, then structure | 8 books, 1497 to 1916 (list in `OCR_Kraken_approach.md`) |
| **Scan of a manuscript** | Read handwriting by machine, correct, then structure | None in the pilot selection (checked in `data/Pilot_selected_versions.csv`); expected for later works |

When a version has both a typed text and a scan, the typed text is what we work from; the scan is there to look at a page when in doubt (`Version_selection_method.md`, rule 2).

## Why one script per version

Each book is laid out its own way: where the chapter numbers are, how notes are attached, how two languages share a page, how pages are numbered. A general converter would be either wrong for most books or as complicated as all of them together. So each version gets its own short script, `convert/convert.py` in its folder.

Writing such a script by hand takes a person hours per book, which is why projects usually avoid it. An AI assistant writes one in minutes, so the project can afford one per version. The division of work that follows:

- **The assistant writes the script; the script produces the text.** The assistant does not retype or rewrite the text itself. The result is therefore the same at every run, and anyone can read in the script what was done to the source.
- **The shared checker decides whether the output is acceptable** (`tools/vh_text.py check`), the same for all versions.
- **A person checks samples against the page images** and their findings are recorded.

## Steps for one version

1. **Look.** Read `metadata/note.txt`, then the source itself: the structure of the typed text, or a spread of sample pages of the scan (beginning, middle, end, one page of each layout).
2. **Write `convert/NOTES.md`**: how the book is organised, what its citation system is, how pages are marked, which parts are the work, the commentary, the notes; the traps; what is decided and why.
3. **For a scan only: read the pages.** The machine reading goes into `work/`, page by page, with the position of each line. Which reading engine to use is not decided: Kraken, Tesseract and small AI reading models are to be compared on hand-corrected reference pages first (`OCR_Kraken_approach.md`). The reference pages are kept in `convert/reference/`.
4. **Write `convert/convert.py`.** Standard-library Python. It reads `source/` (and `work/`), never writes there, and writes `text/`.
5. **Check.** `python3 tools/vh_text.py check <version folder>` must pass. Then the checks no machine rule covers:
   - counts against known figures (number of books and chapters; for Mattioli 1568, the 831 chapters of Dioscorides counted by Staub et al. 2016);
   - a sample of passages compared by eye with the page image, spread over the whole book, with particular attention to plant names, quantities and parts of plants;
   - for a version with a typed text and a scan: page numbers of the typed text against the scan.
6. **Record the limits** in the `notes` of the info file: what is missing, what was not verified, the measured error rate if any.
7. **Commit** the notes, the script and the text together.

## Order proposed

1. The four typed texts first. They need no reading step, so they test the format and the method at little cost, and they give the project its first complete texts (Theophrastus, Dioscorides and Pliny in the original language).
2. Then the scans, starting as proposed in `OCR_Kraken_approach.md`.

## Open points

- The reading engine for scans, and the transcription rules (both in `OCR_Kraken_approach.md`).
- Who checks the samples for each language, and how much time they have.
- Whether the typed texts, which their projects keep correcting, should be fetched again later; if so the checksum in `data/Downloads_report.csv` tells that a file has changed.
