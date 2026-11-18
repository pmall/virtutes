# Typing the scans with Kraken — approach under discussion

**A proposal, not a decision.**

## The task

Eight of the selected versions exist only as scans of printed books (1497 to 1916). They must become typed text, with each passage keeping the scan page it comes from ([`Version_selection_method.md`](Version_selection_method.md#the-rules), rule 2). This document covers the reading step only; where it fits in the conversion of a version, and the format the text ends in, are in [`Conversion_method.md`](Conversion_method.md) and [`Unified_text_format.md`](Unified_text_format.md). The list is in [`works/Pilot_selected_versions.csv`](../works/Pilot_selected_versions.csv), form "Scan, to be typed".

Kraken is open-source software that finds the lines on a page image and reads them. A Kraken reading model can be adapted ("fine-tuned") to a particular typeface or hand from a small number of corrected pages.

## What "good enough" means

The aim is not an exact copy of the page. The text is read so that use records can be taken from it ([`Project_context.md`](Project_context.md)): which plant, which part, prepared how, good for what, in what quantity. A reading is good enough when the records taken from it are the same as those that would be taken from an exact copy. Those records come from the words of the main text, so what counts is:

- **the main-text words**, as the extraction will see them: case, punctuation, note numbers, spacing and the shape of quotes and dashes do not change a record;
- **which words are wrong**: a wrong plant name, part, preparation, effect or quantity can change a record; a wrong "the" cannot;
- **no main-text line lost or out of order**: a lost line is a lost record.

Running heads, page numbers and the notes are not measured: the notes of these editions are mostly variant readings and references. If an edition's notes carry uses, its notes become main text for this purpose.

Proposed threshold, to be confirmed: fewer than 1 main-text word in 100 wrong, none of them a word that carries a record, and no main-text line lost.

## The method, per book

1. **Sample pages.** About 5 pages spread over the book, with pages that carry uses among them.
2. **Read them** with the ready-made models (one line finder, several reading models: [below](#the-models-and-how-they-are-pinned)).
3. **Reference of the main text.** The assistant transcribes the sample pages from the images, then looks again, on a zoomed image, at every line where one of the best models reads something else, and settles it. Care goes into the main text; the rest of the page only needs to be close enough to align the readings ([below](#reference-pages-of-modern-print-provisional-rules)).
4. **Measure** with [`tools/ocr_score.py`](../tools/ocr_score.py): main-text words wrong, and the list of those words. A person reads the list and the points the assistant could not settle, not every line.
5. **Decide.** If the best model is good enough, it reads the whole book. If not, try the next models; then fine-tune the best one on corrected pages (on the GPU server) and measure again on the same sample pages, which are never used for training.
6. **Read the whole book**, then look for what the sample may have missed: lines read as empty or very short, pages with far fewer lines than their neighbours, lines with many words found in no other page of the book.

## Who does what

- **Kraken reads the books.**
- **The AI assistant (Claude)** runs the method: reading, the reference of the main text, measuring, choosing, reading the whole book.
- **A person** decides whether a reading is good enough, from the list of wrong words and the open points. Specialists are needed where the assistant's reading of the page is unsure: Greek, old abbreviations, old spellings.

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

[`tools/ocr_score.py`](../tools/ocr_score.py) compares a reading with the reference pages. Its main measure is the share of main-text words wrong, with the list of those words; it also gives the character error rate of the whole page, comparable with what other projects publish. Its opening comment says exactly what is counted.

## Reference pages of modern print (provisional rules)

Used for the reference pages of Hort 1916, until the transcription rules are decided: four blocks separated by one empty line, running head, main text, notes, page number; one printed line per line of text, top to bottom; no space before `;` and `:` (the printer's thin space is dropped); a note number is written as a plain number, separated by spaces; small capitals as lower case; italics not marked; quotes and dashes as printed (‘ ’ –); a word cut at the end of a line keeps its hyphen; Greek with its accents as printed. A reference page is `convert/reference/<page>.draft.txt` until a person has accepted it (step 4 of the method), then `<page>.txt`.

## Open points

- **Transcription rules for the older books**: keep abbreviations, long s and ligatures as printed, or expand and modernise them. The test is the extraction: a long s read as f turns "sage" into "fage", a plant name the extraction will not recognise. Keeping close to the guidelines the existing models were trained on lets us reuse those models; expansion can be a later, separate step.
- **Specialists**: the books span Latin, Middle French, Italian, Old French and English; more than one person may be needed, and their available time is not known.
- **Hardware**: the laptop (no GPU) can run line finding, reading and small tests; fine-tuning belongs on the RTX 6000 server, which needs PyTorch with GPU support instead of the version without it named in [`pyproject.toml`](../pyproject.toml).

## Installation

Kraken is one of the project's packages ([`pyproject.toml`](../pyproject.toml)); `uv sync` installs it. It comes with a model that finds the lines on a page. The models that read the text are downloaded separately, one per need.

## Not verified

Stated from the assistant's memory, to be checked before use:
- which ready-made models fit the books printed before 1900 (candidates in the list: CATMuS-Print, CATMuS Gothic Print, Latin Incunabula and Early Prints, Gallicorpora+, McCATMuS, PP-OCRv6);
- how many corrected pages a fine-tune typically needs;
- the alternatives to compare Kraken with. Candidates named so far: for reading print, Tesseract, olmOCR, PaddleOCR-VL, dots.ocr, LightOnOCR, DeepSeek-OCR, MinerU, Chandra; for page layout, DocLayout-YOLO, YALTAi; for handwriting, TrOCR.
