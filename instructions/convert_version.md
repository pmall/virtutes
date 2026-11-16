# Task: convert one version to the unified text format

**Goal.** For one version folder `data/<version>/`, write `convert/convert.py` so that running it produces `text/` in the unified format, complete, passing the checker, with its limits stated.

**Read first, in this order:**
1. `docs/Unified_text_format.md` — the target. Every field and rule in it is binding.
2. `docs/Folder_structure.md`, section "One folder per chosen version" — where each file goes.
3. `docs/Conversion_method.md` — why it is done this way, and what counts as verified.
4. `data/<version>/metadata/note.txt` — what the source files are and what is not verified about them.
5. `tools/vh_text.py` (top comment) — the checker you must pass.
6. A `convert/convert.py` of an already converted version of the same kind, if one exists: reuse its approach.

## Hard constraints

- You write the script; the script writes the text. Never type, paste, correct or complete text of the work yourself, in the script or in the output. If the source is wrong, the output is wrong in the same way, or the fix is a row of `convert/corrections.csv` that a person asked for.
- `source/` is read-only. Read archives in place (`zipfile`); anything unpacked goes to `work/`.
- Python standard library only. If the task cannot be done without another package (decoding JPEG 2000 images, a reading engine), stop and ask the user.
- The script takes no arguments, finds its folders from its own path, and gives the same output at every run (no dates, no random order).
- No interpretation: do not identify plants, translate, modernise spelling or tidy punctuation.
- Do not work around the format. If the source has something the format cannot express, stop and propose a change to `docs/Unified_text_format.md` and `tools/vh_text.py`; apply it only after the user agrees, raising the format version, in the same commit.

## Steps

1. **Look at the source before writing anything.**
   - Typed text (XML): list the element names and their counts; find how books, chapters and sections are marked, how pages are marked, where notes and variant readings sit, which elements mark editorial additions, deletions and gaps. Read three stretches in full: the beginning, one plant entry in the middle, the end. Parse large files as a stream (`xml.etree.ElementTree.iterparse`). Check that the file parses with the standard library: named entities such as `&mdash;` need to be declared to the parser.
   - Scan: do not start. Reading scans by machine is not decided (`docs/OCR_Kraken_approach.md`); see `WIP.md` for the state of that question.
2. **Decide the mapping** from the source's structure to `kind`, `ref`, `page`, `marks`, `anchor`. Decide the `ref_scheme` from the citation system scholars use for this work, not from the file's own nesting if they differ. Write these decisions, and the layout of the book, in the comment at the top of `convert.py`: this comment is the only description of the version's conversion.
3. **Write `convert/convert.py`.** It writes `text/<lang>.jsonl`, `text/<lang>.info.json` and `text/pages.csv`. Take `sources` and their md5 from the files themselves and compare with `data/Downloads_report.csv`; stop if they differ.
4. **Fill `pages.csv` honestly.** If the page images have not been matched to the page numbers, leave `source_file` and `image` empty with `mapping` = `none`. Use `computed` only after verifying the rule on at least five pages spread over each volume, by reading the page number on the image.
5. **Run the checker**: `python3 tools/vh_text.py check <version>`. Fix the script until it prints `OK`.
6. **Verify the content**, and report the figures:
   - nothing lost: the number of characters of running text in the source and in the output, per kind, with every difference explained;
   - counts of books, chapters and sections against the figures a scholar would expect, each with its origin;
   - ten passages spread over the work, read with `tools/vh_text.py view`, compared with the source file character by character;
   - if page images can be viewed, three of those passages compared with the image of their page.
7. **Set the info file truthfully.** `status` = `complete` only if the whole version is there. `review` = `none` unless a person compared samples with page images. Everything not verified goes in `notes`, in plain words.
8. **Commit** `convert/` and `text/` together, with a message stating the counts and what was not verified.
9. **Update `WIP.md`** (see `AGENTS.md`).

## Done means

- `python3 convert/convert.py` followed by the checker prints `OK`, twice in a row with identical output (`git status` clean after the second run).
- The verification figures of step 6 are in the commit message.
- No text of the work was typed by you.

## When unsure

Ask the user, giving the two or three options and the one you recommend. Typical cases: whether a part of the book is `text` or `paratext`; what to do with a passage the source marks as doubtful; a citation system with competing numberings.
