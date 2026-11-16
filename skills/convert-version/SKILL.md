---
name: convert-version
description: Convert one version of a work (data/<version>/) to the project's unified text format by writing its convert/extract.py and convert/repair.py. Use when asked to convert, reconvert or fix the text of a version.
---

# Task: convert one version to the unified text format

**Goal.** For one version folder `data/<version>/`, write two scripts: `convert/extract.py`, which copies the source into the unified format as it is (`work/raw/`), and `convert/repair.py`, which makes `text/` from it by correcting the source's mistakes. Both outputs are complete, pass the checker and state their limits.

**Read first, in this order:**
1. `docs/Unified_text_format.md` — the target. Every field and rule in it is binding.
2. `docs/Folder_structure.md`, section "One folder per chosen version" — where each file goes.
3. `docs/Conversion_method.md` — why it is done this way, what each of the two scripts may do, and what counts as verified.
4. `data/<version>/metadata/note.txt` — what the source files are and what is not verified about them.
5. `tools/vh_text.py` (top comment) — the checker you must pass.
6. The `convert/` scripts of an already converted version of the same kind, if one exists: reuse their approach.

## Hard constraints

- You write the scripts; the scripts write the text. Never type, paste, correct or complete text of the work yourself, in a script or in the output.
- `extract.py` corrects nothing: if the source is wrong, the raw text is wrong in the same way.
- `repair.py` corrects by rules, each a named function described in its opening comment, each change written to `work/repairs.csv`. A rule may change `ref`, `kind`, `page` and where a passage is cut; never the words. A change to the words is a row of `convert/corrections.csv` that a person asked for.
- **Propose each repair rule to the user before writing it**: the mistake, how many passages, the rule, what it could get wrong.
- `source/` is read-only. Read archives in place (`zipfile`); anything unpacked goes to `work/`.
- Only the packages of `pyproject.toml`; run everything with `uv run`. If the task cannot be done without another package (a reading engine), stop and ask the user.
- Each script takes no arguments, finds its folders from its own path, and gives the same output at every run (no dates, no random order).
- No interpretation: do not identify plants, translate, modernise spelling or tidy punctuation.
- Do not work around the format. If the source has something the format cannot express, stop and propose a change to `docs/Unified_text_format.md` and `tools/vh_text.py`; apply it only after the user agrees, raising the format version, in the same commit.

## Steps

1. **Look at the source before writing anything.**
   - Typed text (XML): list the element names and their counts; find how books, chapters and sections are marked, how pages are marked, where notes and variant readings sit, which elements mark editorial additions, deletions and gaps. Read three stretches in full: the beginning, one plant entry in the middle, the end. Parse large files as a stream (`xml.etree.ElementTree.iterparse`). Check that the file parses with the standard library: named entities such as `&mdash;` need to be declared to the parser.
   - Scan: do not start. Reading scans by machine is not decided (`docs/OCR_Kraken_approach.md`); see `WIP.md` for the state of that question.
2. **Decide the mapping** from the source's structure to `kind`, `ref`, `page`, `marks`, `anchor`. Decide the `ref_scheme` from the citation system scholars use for this work, not from the file's own nesting if they differ. Write these decisions, and the layout of the book, in the comment at the top of `extract.py`; the comment at the top of `repair.py` lists its rules. These two comments are the only description of the version's conversion.
3. **Write `convert/extract.py`.** It writes `work/raw/<lang>.jsonl`, `work/raw/<lang>.info.json` and `work/raw/pages.csv`. Take `sources` and their md5 from the files themselves and compare with `data/Downloads_report.csv`; stop if they differ. Check it: `uv run tools/vh_text.py check <version> --raw`.
4. **List the mistakes of the source** found in the raw text (labels that contradict the printed numbers, numbers typed inside sentences, voices mixed, pages out of order), with counts and examples, and propose a repair rule for each to the user.
5. **Write `convert/repair.py`** with the rules agreed. It reads `work/raw/` and writes the same three files to `text/`, plus `work/repairs.csv`.
6. **Fill `pages.csv` honestly.** If the page images have not been matched to the page numbers, leave `source_file` and `image` empty with `mapping` = `none`. Use `computed` only after verifying the rule on at least five pages spread over each volume, by reading the page number on the image (`tools/page_image.py` writes one page image as a PNG file).
7. **Run the checker**: `uv run tools/vh_text.py check <version>`. Fix the scripts until it prints `OK`.
8. **Verify the content**, and report the figures:
   - nothing lost: the number of characters of running text in the source, in the raw text and in `text/`, per kind, with every difference explained;
   - counts of books, chapters and sections against the figures a scholar would expect, each with its origin;
   - ten passages spread over the work, read with `tools/vh_text.py view`, compared with the source file character by character;
   - if page images can be viewed, three of those passages compared with the image of their page.
9. **Set the info file truthfully.** `status` = `complete` only if the whole version is there. `review` = `none` unless a person compared samples with page images. Everything not verified goes in `notes`, in plain words.
10. **Commit** `convert/` and the updated `WIP.md` together, with a message stating the counts and what was not verified. `work/` and `text/` are not in git.

## Done means

- After deleting `work/` and `text/`, `uv run convert/extract.py` then `uv run convert/repair.py` make them again and the checker prints `OK` for both; a second run gives files with the same checksums.
- The verification figures of step 8 are in the commit message.
- No text of the work was typed by you.

## When unsure

Ask the user, giving the two or three options and the one you recommend. Typical cases: whether a part of the book is `text` or `paratext`; what to do with a passage the source marks as doubtful; a citation system with competing numberings.
