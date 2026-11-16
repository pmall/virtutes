# Typing the scans with Kraken — approach under discussion

Virtutes Herbarum. Written 13 November 2026 from a discussion with the project's data lead. **A proposal, not a decision.** Nothing has been installed or tested yet.

## The task

Eight of the selected versions exist only as scans of printed books (1497 to 1916). They must become typed text, with each passage keeping the scan page it comes from (`Version_selection_method.md`, rule 2). This document covers the reading step only; where it fits in the conversion of a version, and the format the text ends in, are in `Conversion_method.md` and `Unified_text_format.md`. The list is in `data/Pilot_selected_versions.csv`, form "Scan, to be typed".

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

## Proposed first book

**Mattioli, Discorsi 1568.** It is hard enough to test the whole method, and it is the edition used by Staub et al. 2016 (`references/`). That study recorded 5,314 uses by hand, so the result can later be judged not only by character errors but by whether the uses extracted from our text match theirs.

## Open points

- **Transcription rules**, to be fixed before any reference page is typed: keep abbreviations, long s and ligatures as printed, or expand and modernise them. Keeping them close to the guidelines the existing models were trained on lets us reuse those models; expansion can be a later, separate step. Listed as undecided in `Project_context.md`.
- **Specialists**: the books span Latin, Middle French, Italian, Old French and English; more than one person may be needed, and their available time is not known.
- **Installation**: Kraken is not installed; it brings PyTorch (several GB). To be asked before installing. Its supported Python versions must be checked against this machine.
- **Hardware**: the laptop (no GPU) can run line finding, reading and small tests; fine-tuning belongs on the RTX 6000 server, to which the assistant has no access yet.

## Not verified

Stated from the assistant's memory, to be checked before use:
- which ready-made Kraken models exist and fit these books (CATMuS Medieval, McCATMuS for the 16th–21st c., community models for early modern French print);
- the current Kraken version;
- how many corrected pages a fine-tune typically needs;
- whether the Hort 1916 PDF already carries a usable text layer.
