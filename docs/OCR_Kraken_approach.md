# Typing the scans with Kraken — approach under discussion

**A proposal, not a decision.**

## The task

Eight of the selected versions exist only as scans of printed books (1497 to 1916). They must become typed text, with each passage keeping the scan page it comes from ([`Version_selection_method.md`](Version_selection_method.md#the-rules), rule 2). This document covers the reading step only; where it fits in the conversion of a version, and the format the text ends in, are in [`Conversion_method.md`](Conversion_method.md) and [`Unified_text_format.md`](Unified_text_format.md). The list is in [`works/Pilot_selected_versions.csv`](../works/Pilot_selected_versions.csv), form "Scan, to be typed".

Kraken is open-source software that finds the lines on a page image and reads them. A Kraken reading model can be adapted ("fine-tuned") to a particular typeface or hand from a small number of corrected pages.

## Who does what

- **Kraken reads the books.** The aim is a model that reads one whole book (or a family of similar books) correctly.
- **The AI assistant (Claude)** drafts the transcription of a few pages per book and runs the rest of the loop: finding lines, testing existing models, fine-tuning, measuring errors, comparing models, then reading the whole book with the chosen model.
- **A human specialist** confirms every line of the drafted pages. Their corrected version is the reference. Nothing the assistant reads counts as a reference until a specialist has confirmed it.

## The loop, per book

1. **Reference pages.** A few pages: Kraken finds the lines, the assistant drafts the text, the specialist corrects both the lines and the text. The pages are split into training pages and test pages; test pages are never used for training.
2. **Existing models first.** Run the ready-made Kraken models on the test pages and measure the character error rate.
3. **Fine-tune if needed**, starting from the best existing model, and measure again on the same test pages. Training on 2, 5 and 10 pages gives a curve showing how many corrected pages a book needs, which tells us what each later work of the catalogue will cost.
4. **Read the whole book** with the chosen model; spot-check pages that were not used for training.

Besides the overall error rate, check separately the words the project depends on: plant names, quantities, parts of the plant, preparations. A low overall rate is not enough if the errors fall on these.

**Checking the drafts.** A specialist correcting a draft tends to accept its mistakes. To measure this once, the specialist types one or two pages from scratch, without seeing the draft, and the two versions are compared.

## The eight books

| Book | Type | Expected difficulty (not yet tested) |
|---|---|---|
| Theophrastus, Hort 1916 (English pages) | Modern type | Low; existing models are probably enough |
| *Circa instans*, Dorveaux 1913 | Modern type, Old French text | Low for the type; the Old French spelling is the trap |
| Pliny, Poinsinet 1771–1782 | 18th-c. roman type, Latin + French | Medium; mainly layout (two languages and notes on one page) |
| Dioscorides, Mathée 1553 | 16th-c. type | Medium to high: long s, ligatures, abbreviations |
| Mattioli, Du Pinet 1561 | 16th-c. type, two dense columns | Medium to high |
| Mattioli, Discorsi 1568 | 16th-c. roman and italic, woodcuts | Medium to high |
| Petit Bauhin 1671 | 17th-c. type, small format | Medium |
| *Circa instans*, Venice 1497 | Gothic type, heavy abbreviation | High; closest to a manuscript |

Probably one fine-tuned model per book, or per family of similar typefaces.

**Likely harder than the reading itself:** finding the lines and the reading order on pages with two columns, margin notes, running heads, notes and woodcuts. Kraken's line finder can also be fine-tuned; reading order may need its own treatment.

## Order of the books

**First, the English pages of Hort 1916**, the easiest book, to set up and test the loop. **Then Mattioli, Discorsi 1568**: hard enough to test the whole method, and the edition used by Staub et al. 2016 ([`references/`](../references/)). That study recorded 5,314 uses by hand, so the result can later be judged not only by character errors but by whether the uses extracted from our text match theirs.

## The models, and how they are pinned

The ready-made Kraken models are kept on Zenodo, a public research archive; `kraken list` lists them. Most are 1 to 25 MB; a fine-tuned model has the size of the model it starts from. Each version of a model has its own DOI, which never points to a later version, and each file has a checksum. The models a version tries or uses are listed in its `convert/ocr_models.csv`: role (finding lines, or reading), name, file, size, checksum, and the DOI of the exact version. The line-finding model that comes with Kraken is not used: it is not the same file as any version on Zenodo, so it cannot be pinned.

## Measuring a reading

[`tools/ocr_score.py`](../tools/ocr_score.py) compares a reading with the reference pages and gives the character and word error rates; its opening comment says exactly what is counted. Besides the plain character error rate it gives one with spacing and the shape of quotes and dashes set aside, which separates misreadings from differences of transcription rules.

## Reference pages of modern print (provisional rules)

Used for the drafts of Hort 1916, until the transcription rules are decided: one printed line per line of text, top to bottom, running head and page number included; a note number is written as a plain number, separated by spaces; small capitals as lower case; italics not marked; quotes and dashes as printed (‘ ’ –); a word cut at the end of a line keeps its hyphen; Greek with its accents as printed. A reference page is `convert/reference/<page>.draft.txt` while it is a draft and becomes `<page>.txt` once a person has confirmed every line against the image.

## Open points

- **Transcription rules**, to be fixed before any reference page is typed: keep abbreviations, long s and ligatures as printed, or expand and modernise them. Keeping them close to the guidelines the existing models were trained on lets us reuse those models; expansion can be a later, separate step.
- **Specialists**: the books span Latin, Middle French, Italian, Old French and English; more than one person may be needed, and their available time is not known.
- **Hardware**: the laptop (no GPU) can run line finding, reading and small tests; fine-tuning belongs on the RTX 6000 server, which needs PyTorch with GPU support instead of the version without it named in [`pyproject.toml`](../pyproject.toml).

## Installation

Kraken is one of the project's packages ([`pyproject.toml`](../pyproject.toml)); `uv sync` installs it. It comes with a model that finds the lines on a page. The models that read the text are downloaded separately, one per need.

## Not verified

Stated from the assistant's memory, to be checked before use:
- which ready-made models fit the books printed before 1900 (candidates in the list: CATMuS-Print, CATMuS Gothic Print, Latin Incunabula and Early Prints, Gallicorpora+, McCATMuS, PP-OCRv6);
- how many corrected pages a fine-tune typically needs;
- the alternatives to compare Kraken with. Candidates named so far: for reading print, Tesseract, olmOCR, PaddleOCR-VL, dots.ocr, LightOnOCR, DeepSeek-OCR, MinerU, Chandra; for page layout, DocLayout-YOLO, YALTAi; for handwriting, TrOCR.
