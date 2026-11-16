---
name: select-and-download
description: Choose which versions of a work to use (original, English, French), download them after the user's go-ahead and write their note.txt. Use after a work's edition map exists.
---

# Task: choose the versions of a work, download them, write their note

**Read first:** `docs/Version_selection_method.md` (the rules; apply them in order, do not reinterpret them) and `docs/Folder_structure.md` (folder names, what goes in `source/`, the sections of `note.txt`).

## Steps

1. **Select.** Apply the method to the work's rows of the edition map. Add one row per slot to the selection file, with the same columns as `data/Pilot_selected_versions.csv`: the chosen version or the reason the slot is empty, the deciding rule, why the better-ranked candidates were rejected, with sources.
2. **Present** the result to the user as the table the method prescribes, with the list of files to download, their total size and the expected duration. **Wait for the go-ahead.**
3. **Download** with `tools/download_ia.py` (Internet Archive) or `tools/download_iiif_pages.py` (libraries serving single pages). They write into `source/`, verify checksums and add rows to `data/Downloads_report.csv`. A typed text fetched another way gets its row added the same way, with its md5.
4. **Verify** what the selection relied on, on the files themselves: the edition is the one expected (title page), the copy is complete (page count), the image size is the one recorded.
5. **Write `metadata/note.txt`** with the sections the folder-structure document lists. Every fact carries its source; every open point goes under NOT VERIFIED and nowhere else.
6. **Commit** the selection rows, the report rows, the library records and the note.

## Facts about the libraries

- Internet Archive delivers a whole volume as one archive, with a published md5.
- Wellcome's image server blocks full-size page images after about 60 pages at one page per second: prefer the Internet Archive copy of a Wellcome item when one exists.
- WorldCat, Gallica, HathiTrust and ISTC often refuse automated access. A check that cannot be done is retried another way or reported as open, never assumed.
