---
name: test-scan-reading
description: Test how well ready-made Kraken models read one scanned version (works/<version>/) on a few sample pages, and write its report convert/ocr_test.md, so that the reading can be judged good enough or not before the whole book is read. Use when asked to test, try or evaluate the reading (OCR) of a scan.
---

# Task: test the reading of one scanned version

**Goal.** For one version that exists only as a scan, find out on about 5 sample pages whether a ready-made model reads it well enough to take use records from it, and write the evidence in `works/<version>/convert/ocr_test.md`. The decision (which model, good enough or not, fine-tune or not) is not taken here: it is taken later, from the reports of all the books together. Do not read the whole book in this task.

**Read first, in this order:**
1. `docs/OCR_Kraken_approach.md` — what "good enough" means, the method, the reference-page rules, how models are pinned. Binding.
2. `works/<version>/metadata/note.txt` — what the scan files are.
3. `works/1_Theophrastus_original-english_Hort_1916/convert/ocr_test.md` — the first report, the model for yours; and that version's `convert/ocr_models.csv` and `convert/reference/`.
4. The opening comments of `tools/ocr_models.py`, `tools/ocr_trial.py`, `tools/ocr_score.py`, `tools/ocr_disagree.py`.

## Hard constraints

- **Never download without the user's go-ahead** (models included): list each model, its size, the total. A go-ahead recorded in `WIP.md` for named models counts.
- `source/` is read-only; page images are written to `work/ocr_trial/pages/`.
- The reference is what the page shows, read on the image. Never copy a model's reading into a reference without looking at the line on the image.
- Say, for every point, whether it is checked or assumed. The recommendation in the report is a proposal.

## Steps

1. **Choose about 5 sample pages**, spread over the book (or over each volume), at least two of them with uses of plants; no title pages, indexes or plates. Say in the report why each page was taken. For a layout the book changes (two columns, two languages, a commentary in another type), take a page of each kind.
2. **Make the page images**, losslessly, in `work/ocr_trial/pages/<page>.png`, `<page>` naming the image in the scan (`img0134` for image 134 of an archive, `pdf0056` for page 56 of a PDF):
   - archive of JPEG 2000 or JPEG images: `uv run tools/page_image.py <version> <archive> <image number>`, then move the PNG from `work/pages/` and rename it;
   - PDF: `pdfimages -png -f <n> -l <n> <pdf> <prefix>` keeps the embedded image as it is; take the full-page image.
   Look at one page: type, columns, notes, margins, woodcuts, languages.
3. **Choose the candidate models** and write `convert/ocr_models.csv` (columns: role, name, file, bytes, md5, address). Exactly one of role `segmentation`; for two-column pages, compare the general line finder with the two-column one on one page and keep the better. Take the reading models of Hort's list plus those made for this kind of print (`uv run kraken list`, and the Zenodo record of each for its file, size and checksum: `https://zenodo.org/api/records/<record>`). The address is the DOI of the exact version: `https://doi.org/10.5281/zenodo.<record>`.
4. **Fetch and read**: `uv run tools/ocr_models.py <version>`, then `uv run tools/ocr_trial.py <version>` (minutes; run it in the background).
5. **Write the reference of each sample page**, `convert/reference/<page>.draft.txt`, by reading the image (cut it in halves or smaller to read the small print). Four blocks separated by one empty line: running head, main text, notes, page number (an empty block if there is none). Follow the reference-page rules of `docs/OCR_Kraken_approach.md`; for a book printed before 1800, transcribe what is printed: long s as ſ, abbreviations with their signs, u/v and i/j as printed. Care goes into the main text.
6. **Look again at every disputed line**: `uv run tools/ocr_disagree.py <version> <best model> <second> <third>` (take the three best of a first `tools/ocr_score.py` run). Open each image it saves, settle who is right, correct the reference where it was wrong. Keep the list of lines you could not settle, with why.
7. **Score**: `uv run tools/ocr_score.py --show works/<version>/convert/reference works/<version>/work/ocr_trial/ocr/*`. Read the list of wrong main-text words of the best models: mark each one that carries a record (plant, part, preparation, effect, quantity).
8. **Check the lines** on each sample page: main-text lines lost (read as empty), cut in two, or out of reading order (compare `seg/<page>.xml` and the readings with the image). For two columns, check that the left column is read before the right one.
9. **Count the abbreviations** of the main text (words written with an abbreviation sign) and give a few examples: whether to expand them is decided later.
10. **Write `convert/ocr_test.md`**, with these sections, in plain language:
    - *The book*: type, layout, languages, what makes it hard.
    - *Sample pages*: each page, its image in the scan, why it was taken.
    - *Models tried*: the list (with `convert/ocr_models.csv` for the pins), beginning with the three models of the readings: layout model, line finder, reading models (`docs/OCR_Kraken_approach.md`, "The three models of a reading"); "none" for a step not used.
    - *Scores*: the output of `tools/ocr_score.py`, as a table, one row per model.
    - *Wrong main-text words* of the two best models, each marked "carries a record" or not.
    - *Lines*: lost, cut, out of order.
    - *Reference*: how sure it is; the points not settled.
    - *Abbreviations*: count and examples.
    - *Speed*: seconds per page for finding lines and for the best model, and the machine.
    - *Proposal*: which model; good enough by the threshold of `docs/OCR_Kraken_approach.md` or not; if not, what to try next (another model, fine-tuning, another line finder).
11. **Leave things true**: update `WIP.md`; commit (`ocr_models.csv`, `reference/`, `ocr_test.md`, and any tool change).
