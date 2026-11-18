# Folder structure

## The workspace

One self-contained folder for all works, pilot and later. It is a git repository. Every path in the documents, notes and tools is relative to it, so it can be moved or cloned anywhere.

```
<workspace>/
    README.md                        what this is, and the index of the documents
    docs/                            the project explained: methods, structure, text format
    AGENTS.md, skills/               how AI assistants must work here: the rules, and one skill per task
    .claude/skills/                  links to skills/, so that Claude finds the skills
    WIP.md                           what remains to do, in order
    tools/                           scripts shared by all works
    pyproject.toml, uv.lock          the Python version and packages the scripts need, exact versions
    catalogue/                       the 5 catalogue spreadsheets (copies) + catalogue_rows.csv
    references/                      articles the project relies on (README.md lists them)
    works/
        Pilot_works_all_versions.csv     the edition map: every known version of the pilot works
        Pilot_selected_versions.csv      the selection: one row per work and slot
        <version folder>/                one folder per chosen version
```

## One folder per chosen version

Name: `<work number>_<Work>_<slot>_<editor or place>_<year>`

- slot is `original`, `english` or `french`; a book filling two slots joins them: `original-english`.
- Examples: [`2_Dioscorides_original_Wellmann_1906-1914`](../works/2_Dioscorides_original_Wellmann_1906-1914/), [`1_Theophrastus_original-english_Hort_1916`](../works/1_Theophrastus_original-english_Hort_1916/).

Each version folder is a small workshop of its own, with the same five parts:

```
<version folder>/
    metadata/
        note.txt          plain-language note: what the files are, why this version, what is not verified
        sources.csv       the source files the version works from: name, size, checksum, address
    source/               what the libraries delivered, untouched
        <typed text>.xml              a typed text made by a scholarly project, when one exists
        <identifier>_jp2.zip          a scan, one archive per volume, as the library provides it
        <identifier>.pdf              a scan that only exists as a PDF
        <identifier>_jpg.zip          when the library serves single pages: all page images of one
                                      volume, packed by us without recompression
        <identifier>_manifest.json    with it: the library's own page list, unchanged
        <identifier>_pages.csv        with it: one row per page image, with its checksum
        <identifier>_metadata.json    the library's own record of each scanned item, unchanged
    convert/              this version's own scripts and notes; <lang> is the language of a text,
                          and a version with two languages has the three scripts once for each
        extract_<lang>.py   makes work/raw/ from source/: the text as the source has it,
                            mistakes included; its opening comment describes the book's layout
        repair_<lang>.py    makes text/ from work/raw/: corrects the mistakes by rules written
                            in it; its opening comment lists the rules
        images_<lang>.py    links each page of the text to its image in the scans; optional,
                            the text is complete without it
        results.md5         the checksum of every file the scripts produce: the reference the
                            results are compared with (Conversion_method.md)
        corrections.csv     corrections found by people, applied by repair_<lang>.py
        reference/          hand-corrected pages used to train and to measure the reading of a scan
                            (OCR_Kraken_approach.md, "Reference pages")
        ocr_models.csv      the reading models tried or used for a scan, each pinned by its
                            checksum and the DOI of its exact version (OCR_Kraken_approach.md)
    work/                 intermediate files, made again by the scripts
        raw/              the raw text, in the unified text format
        <lang>.repairs.csv  every change repair_<lang>.py made: passage, rule, before, after
        ...               unpacked page images, raw machine reading, trials
                          (work/raw/ and text/ hold nothing but what the scripts wrote there)
    text/                 the result: the repaired text, in the unified text format
                          (Unified_text_format.md), and the optional link from pages to images
```

`convert/`, `work/` and `text/` are created when the conversion of the version starts.

Rules:

- **`source/` is never modified.** A file delivered by a library is kept exactly as delivered: never converted, resized, renamed, unpacked in place or repacked, so its published checksum still applies. Files keep the library's own identifiers as names. Only when a library serves single page images do we pack them ourselves, unchanged, with a checksum for each page.
- **`text/` is never edited by hand.** It is always the output of `repair_<lang>.py`, plus `<lang>.page_images.csv` from `images_<lang>.py`. A correction goes into the script or into `corrections.csv`, so that running the script again keeps it.
- **`work/` and `text/` can be deleted at any time** without losing anything: the scripts make them again, the same at every run. [`tools/vh_check.py`](../tools/vh_check.py) tells whether what is there is what the scripts must give ([`Conversion_method.md`](Conversion_method.md#the-recorded-results-and-one-check)).
- Code needed by several versions moves to [`tools/`](../tools/); a version's scripts keep only what is specific to that book.

## What is in git and what is not

| In git | Not in git |
|---|---|
| Documents, skills, tools, catalogue, the two CSV files of [`works/`](../works/) | The scans (`*.zip`, `*.pdf`): 9.4 GB for the pilot |
| `metadata/` of every version (`note.txt`, `sources.csv`) | The typed texts as delivered (`*.xml`, 1 to 13 MB each) |
| The libraries' small records in `source/` (`*.json`, `*_pages.csv`) | `work/` and `text/` of every version |
| `convert/` of every version | The article PDFs in [`references/`](../references/) (publishers' copyright) |
| `pyproject.toml`, `uv.lock` | The Python environment (`.venv/`) |

The rule behind the table: git holds what we write, and nothing that can be made or fetched again. It does not hold what a library delivered, nor what a script produces from it. The list is enforced by [`.gitignore`](../.gitignore).

The repository must be enough to make everything again, on any computer:

- **The sources.** `metadata/sources.csv` of each version gives, for each file, its exact address, its size and its checksum ([below](#the-list-of-source-files)). A typed text kept in a git repository is recorded at the address of one exact commit, never of a branch, so the same file is delivered whatever its project changes later. A library that serves scans has no such addresses: there the checksum tells whether the file fetched again is the same.
- **The texts.** In each version folder, `convert/extract_<lang>.py` then `convert/repair_<lang>.py` make `text/` from the source files the text is made from, and `convert/results.md5` says what they must give; `convert/images_<lang>.py` then adds the link from pages to images, if the scans are there ([`Conversion_method.md`](Conversion_method.md#three-scripts-per-text)).
- **What the scripts need.** [`pyproject.toml`](../pyproject.toml) names the Python version and every package used beyond what comes with Python; [`uv.lock`](../uv.lock) records the exact version and checksum of each. One command installs them ([`README.md`](../README.md#setting-up)).

## The list of source files

`metadata/sources.csv` of a version lists the files of `source/` the version works from, one row each: `file`, `bytes`, `md5`, `address`. It is the reference for what the source files must be: the scripts refuse a file that is not in it or has another checksum, and [`tools/vh_check.py`](../tools/vh_check.py) verifies the files present against it. The libraries' own small records (`*.json`, `*_pages.csv`), which are in git themselves, are not listed.

- **Who writes a row.** The download tools, once the file is verified against what its library publishes. A file obtained another way gets its row by hand after the same verification, and the note says how it was verified.
- **The address** is where that exact file can be fetched: for Internet Archive, the file itself; for a typed text kept in a git repository, one exact commit.
- **A scan packed by us** (`*_jpg.zip`, from a library that serves single pages) has the address of the library's page list. Its checksum is that of our archive, which [`tools/download_iiif_pages.py`](../tools/download_iiif_pages.py) packs in a fixed way: the same pages always give the same archive. What the library delivered is verified page by page in `<identifier>_pages.csv`.

## The note.txt

Written for a researcher who opens the folder without any other context. Same sections in every note:

1. **Heading**: work, version (editor or translator, place, year, volumes), slot(s) filled.
2. **FILES**: each file of `source/` named, with *What* it is and *Why here*.
3. **WHY THIS VERSION**: the facts that decided it, each with its source, and the rule number applied.
4. **NOT VERIFIED**: every open point, stated as open, with what would change if it turned out otherwise. Nothing unverified appears anywhere else in the note.
5. **RIGHTS**: rights of the text, of the typed text and of the scan, as stated by their sources.
6. **FILE TYPES** and pointers to the method files and to the CSV files.
