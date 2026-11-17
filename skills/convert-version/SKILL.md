---
name: convert-version
description: Convert one version of a work (data/<version>/) to the project's unified text format by writing its convert/extract.py, convert/repair.py and convert/images.py. Use when asked to convert, reconvert or fix the text of a version.
---

# Task: convert one version to the unified text format

**Goal.** For one version folder `data/<version>/`, write three scripts: `convert/extract.py`, which copies the source into the unified format as it is (`work/raw/`); `convert/repair.py`, which makes `text/` from it by correcting the source's mistakes; and, when the version has a scan, `convert/images.py`, which links each page to its image. The raw text and the final text are complete, pass the checker and state their limits.

**Read first, in this order:**
1. `docs/Unified_text_format.md` — the target. Every field and rule in it is binding.
2. `docs/Folder_structure.md`, section "One folder per chosen version" — where each file goes.
3. `docs/Conversion_method.md` — why it is done this way, what each of the three scripts may do and which source files it may open, and what counts as verified.
4. `data/<version>/metadata/note.txt` — what the source files are and what is not verified about them.
5. `tools/vh_check.py`, `tools/vh_record.py` and `tools/vh_text.py` (top comments) — the check you must pass and how results are recorded.
6. The `convert/` scripts of an already converted version of the same kind, if one exists: reuse their approach.

## Hard constraints

- You write the scripts; the scripts write the text. Never type, paste, correct or complete text of the work yourself, in a script or in the output.
- `extract.py` corrects nothing: if the source is wrong, the raw text is wrong in the same way.
- `repair.py` corrects by rules, each a named function described in its opening comment, each change written to `work/repairs.csv`. A rule may change `ref`, `kind`, `page` and where a passage is cut; never the words. A change to the words is a row of `convert/corrections.csv` that a person asked for.
- **Propose each repair rule to the user before writing it**: the mistake, how many passages, the rule, what it could get wrong.
- `source/` is read-only. Read archives in place (`zipfile`); anything unpacked goes to `work/`.
- Each script lists, in a constant `SOURCES` near its top, the files of `source/` it reads, and gets them through `require()` of `tools/vh_sources.py` before doing anything else. No other code opens or checksums a source file. For a typed text, `extract.py` names the typed file only and `repair.py` names nothing: the text must build with the scans absent. Only `images.py` names the scans.
- A script writes only its own files: it never deletes or changes what another script made, and never writes `convert/results.md5`.
- No options: a script of `convert/` takes no argument, and a shared tool takes the version folder and nothing else. Do not add flags.
- Only the packages of `pyproject.toml`; run everything with `uv run`. If the task cannot be done without another package (a reading engine), stop and ask the user.
- Each script takes no arguments, finds its folders from its own path, and gives the same output at every run (no dates, no random order).
- No interpretation: do not identify plants, translate, modernise spelling or tidy punctuation.
- Do not work around the format. If the source has something the format cannot express, stop and propose a change to `docs/Unified_text_format.md` and `tools/vh_text.py`; apply it only after the user agrees, raising the format version, in the same commit.

## Steps

1. **Look at the source before writing anything.**
   - Typed text (XML): list the element names and their counts; find how books, chapters and sections are marked, how pages are marked, where notes and variant readings sit, which elements mark editorial additions, deletions and gaps. Read three stretches in full: the beginning, one plant entry in the middle, the end. Parse large files as a stream (`xml.etree.ElementTree.iterparse`). Check that the file parses with the standard library: named entities such as `&mdash;` need to be declared to the parser.
   - Scan: do not start. Reading scans by machine is not decided (`docs/OCR_Kraken_approach.md`); see `WIP.md` for the state of that question.
2. **Decide the mapping** from the source's structure to `kind`, `ref`, `page`, `marks`, `anchor`. Decide the `ref_scheme` from the citation system scholars use for this work, not from the file's own nesting if they differ. Write these decisions, and the layout of the book, in the comment at the top of `extract.py`; the comment at the top of `repair.py` lists its rules. These two comments are the only description of the version's conversion.
3. **Write `convert/extract.py`.** It writes `work/raw/<lang>.jsonl`, `work/raw/<lang>.info.json` and `work/raw/pages.csv`. The `sources` of the info file are what `require()` returned. Check it: `uv run tools/vh_check.py <version>`.
4. **List the mistakes of the source** found in the raw text (labels that contradict the printed numbers, numbers typed inside sentences, voices mixed, pages out of order), with counts and examples, and propose a repair rule for each to the user.
5. **Write `convert/repair.py`** with the rules agreed. It reads `work/raw/` only and writes the same three files to `text/`, plus `work/repairs.csv`. If a rule was decided by looking at a page image, say in its description what was seen; the script itself does not open the scan.
6. **Write `convert/images.py`** if the version has a scan. It reads `text/pages.csv` and the scans and writes `text/page_images.csv`; its opening comment gives the rule and the pages it was checked on. A page that could not be matched gets no row. Use `computed` only after verifying the rule on at least five pages spread over each volume, by reading the page number on the image (`tools/page_image.py` writes one page image as a PNG file).
7. **Run the check**: `uv run tools/vh_check.py <version>`. Fix the scripts until every script is `OK` and the last line is `OK`.
8. **Verify the content**, and report the figures:
   - nothing lost: the number of characters of running text in the source, in the raw text and in `text/`, per kind, with every difference explained;
   - counts of books, chapters and sections against the figures a scholar would expect, each with its origin;
   - ten passages spread over the work, read with `uv run tools/vh_view.py <file> <ref>`, compared with the source file character by character.
   For a typed text, do not compare its words with the page images: open an image only to settle a doubt about a label or a page number (`docs/Conversion_method.md`).
9. **Set the info file truthfully.** `status` = `complete` only if the whole version is there. `review` = `none` unless a person compared samples of a machine-read text with page images. Everything not verified goes in `notes`, in plain words; that the words of a typed text were not read against the scan is not a limit to list.
10. **Record the results**: `uv run tools/vh_record.py <version>`. It deletes the results, runs the scripts in order and writes `convert/results.md5`. Do this again after any later change to a script; if the checksums change, say in the commit message which and why.
11. **Commit** `convert/` (scripts and `results.md5`) and the updated `WIP.md` together, with a message stating the counts and what was not verified. `work/` and `text/` are not in git.

## Done means

- After deleting `work/` and `text/`, `uv run convert/extract.py` then `uv run convert/repair.py` make them again and `uv run tools/vh_check.py <version>` prints `OK` against the committed `convert/results.md5`.
- For a typed text, this holds with the scans moved out of `source/`. `uv run convert/images.py` then adds `text/page_images.csv` without changing any other file, and stops with the standard message when a scan is absent.
- `git status` shows no change to `convert/results.md5` after a last `uv run tools/vh_record.py <version>`.
- The verification figures of step 8 are in the commit message.
- No text of the work was typed by you.

## When unsure

Ask the user, giving the two or three options and the one you recommend. Typical cases: whether a part of the book is `text` or `paratext`; what to do with a passage the source marks as doubtful; a citation system with competing numberings.
