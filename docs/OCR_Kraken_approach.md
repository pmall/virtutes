# Typing the scans with Kraken — approach under discussion

**A proposal, not a decision.**

## The task

Eight of the selected versions exist only as scans of printed books (1497 to 1916). They must become typed text, with each passage keeping the scan page it comes from ([`Version_selection_method.md`](Version_selection_method.md#the-rules), rule 2). This document covers the reading step only; where it fits in the conversion of a version, and the format the text ends in, are in [`Conversion_method.md`](Conversion_method.md) and [`Unified_text_format.md`](Unified_text_format.md). The list is in [`works/Pilot_selected_versions.csv`](../works/Pilot_selected_versions.csv), form "Scan, to be typed".

Kraken is open-source software that reads page images. It does not read by itself: it runs models, each doing one thing, and puts their results together into a text. Each model can be adapted ("fine-tuned") to a kind of book from a small number of corrected pages.

## The three models of a reading

| Model | What it finds on the page | What happens without it |
|---|---|---|
| **Layout model** | The blocks, each with a name: column of text, heading, margin note, running title, page number, picture | The order of the lines is guessed from the lines alone: on some pages in two columns the columns are mixed. Nothing tells main text from margin notes or running titles |
| **Line finder** | Each line of print | Nothing can be read: the reading model reads one line at a time |
| **Reading model** | The letters of one line | No text |

The layout model and the line finder both look at the page image and do not depend on each other. The lines are then put in order with the help of the blocks, and each line is read. The text is the lines as read, in that order. A wrong text can so come from four places: a block missed or misnamed, a line badly cut, lines in the wrong order, letters misread.

A score of a reading means nothing without its three models. Kraken's usual command uses two, the line finder and a reading model; the layout model is a recent addition, kept in a separate package, and how Kraken is meant to use it together with the line finder is not yet established ([`Layout_fine_tuning.md`](Layout_fine_tuning.md#not-established)).

## What "good enough" means

The aim is not an exact copy of the page. The text is read so that use records can be taken from it ([`Project_context.md`](Project_context.md)): which plant, which part, prepared how, good for what, in what quantity. A reading is good enough when the records taken from it are the same as those that would be taken from an exact copy. Those records come from the words of the main text, so what counts is:

- **the main-text words**, as the extraction will see them: case, punctuation, note numbers, spacing and the shape of quotes and dashes do not change a record;
- **which words are wrong**: a wrong plant name, part, preparation, effect or quantity can change a record; a wrong "the" cannot;
- **no main-text line lost or out of order**: a lost line is a lost record.

Running heads, page numbers and the notes are not measured: the notes of these editions are mostly variant readings and references. If an edition's notes carry uses, its notes become main text for this purpose.

Proposed threshold, to be confirmed: fewer than 1 main-text word in 100 wrong, none of them a word that carries a record, and no main-text line lost.

## The method, per book

1. **Sample pages.** About 5 pages spread over the book, with pages that carry uses among them.
2. **Read them** with the ready-made models (one line finder, several reading models: [below](#the-models-and-how-they-are-pinned)). As written, this step uses no layout model; adding one is on trial ([`Layout_fine_tuning.md`](Layout_fine_tuning.md)).
3. **Reference of the main text.** The assistant transcribes the sample pages from the images, then looks again, on a zoomed image, at every line where one of the best models reads something else, and settles it. Care goes into the main text; the rest of the page only needs to be close enough to align the readings ([below](#reference-pages-provisional-rules)).
4. **Measure** with [`tools/ocr_score.py`](../tools/ocr_score.py): main-text words wrong, and the list of those words.
5. **Report.** Steps 1 to 4 are the test of a book; its evidence is written in the version's `convert/ocr_test.md`, all reports in the same form (skill `test-scan-reading`).
6. **Decide, for all books together.** Once every scanned book is tested, the reports are reviewed together, by the user with a larger AI model, before any book is read in full: which model for each book, whether it is good enough, which books need another model or fine-tuning (on the GPU server, measured again on the same sample pages, which are never used for training). The review rests on the reports; a person reads the lists of wrong words and the points the assistant could not settle, not every line.
7. **Read the whole book**, then look for what the sample may have missed: lines read as empty or very short, pages with far fewer lines than their neighbours, lines with many words found in no other page of the book.

## Who does what

- **Kraken reads the books.**
- **The AI assistant (Claude)** runs the method: reading, the reference of the main text, measuring, the report, and later reading the whole book.
- **A person** decides whether a reading is good enough, from the reports, with a larger AI model to review them. Specialists are needed where the assistant's reading of the page is unsure: Greek, old abbreviations, old spellings.

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

**Likely harder than the reading itself:** the blocks and the reading order on pages with two columns, margin notes, running heads, notes and woodcuts: the work of the layout model.

## Order of the books

The books are tested from the easiest to the hardest, so that the method settles on the easy ones: Hort 1916 (English pages), Dorveaux 1913, Poinsinet 1771–1782, Petit Bauhin 1671, Mathée 1553, Du Pinet 1561, Mattioli 1568, Venice 1497. Mattioli 1568 is the edition used by Staub et al. 2016 ([`references/`](../references/)), who recorded 5,314 uses by hand: once its text is read, the uses extracted from it can be compared with theirs, a test of the whole chain.

## The models, and how they are pinned

The ready-made Kraken models are kept on Zenodo, a public research archive; `kraken list` lists them. Most are 1 to 25 MB; a fine-tuned model has the size of the model it starts from. Each version of a model has its own DOI, which never points to a later version, and each file has a checksum. The models a version tries or uses are listed in its `convert/ocr_models.csv`: role (finding lines, or reading), name, file, size, checksum, and the DOI of the exact version. The line-finding model that comes with Kraken is not used: it is not the same file as any version on Zenodo, so it cannot be pinned.

## Measuring a reading

[`tools/ocr_score.py`](../tools/ocr_score.py) compares a reading with the reference pages. Its main measure is the share of main-text words wrong, with the list of those words; it also gives the character error rate of the whole page, comparable with what other projects publish. Its opening comment says exactly what is counted.

## Reference pages (provisional rules)

Until the transcription rules are decided. For all books: four blocks separated by one empty line, running head, main text, notes, page number; one printed line per line of text, top to bottom; no space before `;` and `:` (the printer's thin space is dropped); a note number is written as a plain number, separated by spaces; small capitals as lower case; italics not marked; quotes and dashes as printed (‘ ’ –); a word cut at the end of a line keeps its hyphen; Greek with its accents as printed. For books printed before 1800, what is printed is transcribed: long s as ſ, abbreviations with their signs (not expanded), u/v and i/j as printed; the scores set aside long s, ligatures, u/v and i/j, which do not change a word for the extraction ([`tools/ocr_score.py`](../tools/ocr_score.py)), and the report counts the abbreviated words of the main text, whose expansion is decided later. A reference page is `convert/reference/<page>.draft.txt` until a person has accepted it (step 4 of the method), then `<page>.txt`.

## Open points

- **Abbreviations of the older books**: the references keep them as printed ([above](#reference-pages-provisional-rules)); whether the text used for extraction expands them is decided from the counts in the reports. The test is the extraction: an abbreviated or misread plant name (a long s read as f turns "sage" into "fage") is a plant the extraction will not recognise.
- **Specialists**: the books span Latin, Middle French, Italian, Old French and English; more than one person may be needed, and their available time is not known.
- **Hardware**: the laptop (no GPU) can run line finding, reading and small tests; fine-tuning belongs on the RTX 6000 server, which needs PyTorch with GPU support instead of the version without it named in [`pyproject.toml`](../pyproject.toml).

## Installation

Kraken is one of the project's packages ([`pyproject.toml`](../pyproject.toml)); `uv sync` installs it. It comes with a model that finds the lines on a page. The models that read the text are downloaded separately, one per need.

## Not verified

Stated from the assistant's memory, to be checked before use:
- which ready-made models fit the books printed before 1900. Candidates in the list, besides those tried on Hort: CATMuS Gothic Print, Latin Incunabula and Early Prints, Gallicorpora+ (reading); Kraken segmentation model for two-column prints (finding lines);
- how many corrected pages a fine-tune typically needs;
- the alternatives to compare Kraken with. Candidates named so far: for reading print, Tesseract, olmOCR, PaddleOCR-VL, dots.ocr, LightOnOCR, DeepSeek-OCR, MinerU, Chandra; for page layout, DocLayout-YOLO, YALTAi; for handwriting, TrOCR.
