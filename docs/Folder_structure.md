# Folder structure

## The workspace

One self-contained folder for all works, pilot and later. It is a git repository. Every path in the documents, notes and tools is relative to it, so it can be moved or cloned anywhere.

```
<workspace>/
    README.md                        what this is, and the index of the documents
    docs/                            the project explained: methods, structure, text format
    AGENTS.md, instructions/         how AI assistants must work here
    WIP.md                           where the work stands; rewritten at each session
    tools/                           scripts shared by all works
    catalogue/                       the 5 catalogue spreadsheets (copies) + catalogue_rows.csv
    references/                      articles the project relies on (README.md lists them)
    data/
        Pilot_works_all_versions.csv     the edition map: every known version of the pilot works
        Pilot_selected_versions.csv      the selection: one row per work and slot
        Downloads_report.csv             one row per downloaded file: source, size, checksum, result
        <version folder>/                one folder per chosen version
```

## One folder per chosen version

Name: `<work number>_<Work>_<slot>_<editor or place>_<year>`

- slot is `original`, `english` or `french`; a book filling two slots joins them: `original-english`.
- Examples: `2_Dioscorides_original_Wellmann_1906-1914`, `1_Theophrastus_original-english_Hort_1916`.

Each version folder is a small workshop of its own, with the same five parts:

```
<version folder>/
    metadata/
        note.txt          plain-language note: what the files are, why this version, what is not verified
    source/               what the libraries delivered, untouched
        <typed text>.xml              a typed text made by a scholarly project, when one exists
        <identifier>_jp2.zip          a scan, one archive per volume, as the library provides it
        <identifier>.pdf              a scan that only exists as a PDF
        <identifier>_jpg.zip          when the library serves single pages: all page images of one
                                      volume, packed by us without recompression
        <identifier>_manifest.json    with it: the library's own page list, unchanged
        <identifier>_pages.csv        with it: one row per page image, with its checksum
        <identifier>_metadata.json    the library's own record of each scanned item, unchanged
    convert/              this version's own scripts and notes
        convert.py        makes text/ from source/ (and from work/ when the text is read from a scan);
                          its opening comment describes how the book is laid out and the choices made
        corrections.csv   corrections found by people, applied by convert.py at each run
        reference/        hand-corrected pages used to train and to measure the reading of a scan
    work/                 intermediate files that can be made again: unpacked page images,
                          raw machine reading, trials
    text/                 the result, in the unified text format (Unified_text_format.md)
```

`convert/`, `work/` and `text/` are created when the conversion of the version starts.

Rules:

- **`source/` is never modified.** A file delivered by a library is kept exactly as delivered: never converted, resized, renamed, unpacked in place or repacked, so its published checksum still applies. Files keep the library's own identifiers as names. Only when a library serves single page images do we pack them ourselves, unchanged, with a checksum for each page.
- **`text/` is never edited by hand.** It is always the output of `convert.py`. A correction goes into the script or into `corrections.csv`, so that running the script again keeps it.
- **`work/` can be deleted at any time** without losing anything.
- Code needed by several versions moves to `tools/`; a version's `convert.py` keeps only what is specific to that book.

## What is in git and what is not

| In git | Not in git |
|---|---|
| Documents, instructions, tools, catalogue, the three CSV files of `data/` | The scans (`*.zip`, `*.pdf`): 9.4 GB for the pilot |
| `metadata/note.txt` of every version | The typed texts as delivered (`*.xml`, 1 to 13 MB each) |
| The libraries' small records in `source/` (`*.json`, `*_pages.csv`) | `work/` |
| `convert/` and `text/` of every version | The article PDFs in `references/` (publishers' copyright) |

The rule behind the table: git holds everything we write and everything needed to understand it; it does not hold what a library delivered in bulk and can deliver again. `data/Downloads_report.csv` gives, for each such file, where it came from, its size and its checksum, so a missing file can be fetched again and verified. The list is enforced by `.gitignore`.

A copy of the repository alone is therefore enough to read and analyse the texts; the bulky sources are needed only to rebuild a text or to look at a page.

## The note.txt

Written for a researcher who opens the folder without any other context. Same sections in every note:

1. **Heading**: work, version (editor or translator, place, year, volumes), slot(s) filled.
2. **FILES**: each file of `source/` named, with *What* it is and *Why here*.
3. **WHY THIS VERSION**: the facts that decided it, each with its source, and the rule number applied.
4. **NOT VERIFIED**: every open point, stated as open, with what would change if it turned out otherwise. Nothing unverified appears anywhere else in the note.
5. **RIGHTS**: rights of the text, of the typed text and of the scan, as stated by their sources.
6. **FILE TYPES** and pointers to the method files and to the CSV files.
