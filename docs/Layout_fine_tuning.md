# Retraining the layout model — approach on trial

**A proposal, not a decision.** Retrained layout models exist; that they give a better text is not yet established ([below](#not-established)).

## Why

A reading of a scan uses three models ([`OCR_Kraken_approach.md`](OCR_Kraken_approach.md#the-three-models-of-a-reading)). The layout model is the one that marks the blocks of a page and names them: main text, heading, margin note, running title, page number, picture. The blocks are what tells in which order the lines are read (one column, then the other) and which lines are main text. Without a layout model the order of the lines on a page in two columns is guessed, and the guess fails on some books.

The ready-made layout model (D-FINE trained on LADaS, "Large") misses many blocks on the 16th-century herbals. Retraining it on a few corrected pages ("fine-tuning") changes this, and can be done on a laptop without a graphics card.

A layout model learns to imitate the corrected pages it is given: it cannot be better than they are. The work is therefore in the corrected pages, and above all in having a page of every page design of a book: a design absent from them (commentary in italic after the chapter text, quoted verse, a table) is a design the model has not learned.

## What is fixed and what is open

Fixed:

- The corrected pages and the scripts are not tied to one version: they are in [`finetuning/layout/`](../finetuning/layout/) and [`tools/`](../tools/), outside `works/`. A retraining can take its pages from several versions.
- A retrained model is never changed once a version uses it. A new retraining gets a new name (`<name>_v1`, `<name>_v2`).
- A retrained model is not published and cannot be fetched again: it is kept in `models/` and backed up with the scans.

Open:

- **One model per book, or one for several books that look alike.** Both were tried on three books ([figures](#figures-so-far)); the figures do not settle it.
- How a version records the layout model it uses (proposal: by name and checksum in its `convert/ocr_models.csv`, role `layout`).

## The folder of a retraining

```
finetuning/layout/<name>/
    pages.csv                     the pages: version, archive in source/, image number, set
    pages/<version>/img<n>.xml    the corrected layout of one page (PAGE XML); in git
    pages/<version>/img<n>.jpg    the page image, 2000 px high; not in git, made again from source/
    work/                         lists for the trainer, the model's own layout, pictures, the trained model; not in git
```

`set` is `train` or `held_out`. Held-out pages are never trained on: they tell whether the model has learned or only memorised. Every version has held-out pages. The sample pages of a version's reading test ([`OCR_Kraken_approach.md`](OCR_Kraken_approach.md), step 1) are in neither set.

The scripts are shared, in [`tools/`](../tools/): `layout_pages.py` (images and lists), `layout_cli.py` (the model: marking pages, retraining), `layout_view.py` (a page with its blocks drawn), `layout_fix.py` (the corrected layout from the model's layout and a list of fixes), `layout_cover.py` (a rough indicator, [below](#how-a-layout-model-is-judged)).

## How a page is corrected

The ready-made model marks the page; its blocks are drawn on the page; each block is kept, relabelled, dropped or redrawn. The labels are the SegmOnto names the model was trained with. The rules, applied the same way on every page:

| Block | Label | Rule |
|---|---|---|
| Running text of a column | `MainZone-P` | One block from one heading to the next; paragraphs are not separated. Commentary in italic is main text too. Text running beside a picture is its own block, the full-width lines above and below are others. |
| Chapter heading | `MainZone-Head` | The name lines and the "Chap." line together are one block. Also the word "ANNOTATIONS". |
| Picture | `GraphicZone` | The woodcut without its caption. |
| Caption or title of a picture | `GraphicZone-Head` | |
| Note in the margin | `MarginTextZone-Notes` | One block per note, the one-word notes ("Nomi.") included. |
| Running title | `RunningTitleZone` | |
| Page number, line counter in the margin | `NumberingZone` | A line counter cut by the binding or the edge of the image is not marked. |
| Signature and catchword at the foot | `QuireMarksZone` | Never inside the text block above. |

Drop capitals are left inside their text block. Blocks are rectangles.

## How a layout model is judged

Two measures count; neither has been taken yet.

1. **Words wrong in the text.** The sample pages are read with the three models named, and the main-text words wrong are counted against the reference pages ([`tools/ocr_score.py`](../tools/ocr_score.py)), once per layout model compared. This is the measure of the project.
2. **Blocks right, place and name.** The model's blocks are compared with the corrected blocks of pages it was not trained on, by the scoring of the layout tool itself, with one figure per kind of block. It needs corrected pages kept for testing only: the held-out pages are too few for this (two per book).

One rough indicator was used so far: for each sample page, how many of the lines found by the line finder lie inside a block of the layout model ([`tools/layout_cover.py`](../tools/layout_cover.py)). It tells whether text is left outside every block. It says nothing of the name of a block, of its limits (one block over two columns counts as well as two), or of the text read. It is not a measure of quality and no model is chosen from it.

## The retrainings

| Name | Versions its pages come from | Pages (train + held out) | Model |
|---|---|---|---|
| `herbal_16c`: printed herbals of the 16th century, one or two columns, woodcuts in the text, margin notes | Mathée 1553, Du Pinet 1561, Mattioli 1568 | 31 + 6 | `models/herbal_16c_v1/herbal_16c_v1.safetensors`, 125878904 bytes, md5 `aeabd4ff30d23a278583f0af85d1c74b` (30 passes, 1 h 50 on a laptop) |

The same pages were also used one book at a time (10 or 11 pages, same settings, about 40 minutes each): three models, in `finetuning/layout/herbal_16c/work/single/<book>/` (not in git).

## Figures so far

All figures here are the rough indicator: lines of the sample pages lying inside a block. Layout model: as named in the column; line finder: Kraken's general one; reading model: none (nothing is read). 44 sample pages, five or six per book; each retraining was run once.

| Sample pages of | Ready-made | Mathée only | Du Pinet only | Mattioli 1568 only | The three together (`herbal_16c_v1`) |
|---|---|---|---|---|---|
| Hort 1916 | 98% | 93% | 75% | 89% | 95% |
| Mathée 1553 | 75% | 96% | 92% | 73% | 99% |
| Poinsinet 1771-1782 | 95% | 100% | 90% | 88% | 92% |
| Dorveaux 1913 | 98% | 88% | 89% | 99% | 74% |
| Venice 1497 | 90% | 76% | 86% | 80% | 82% |
| Du Pinet 1561 | 59% | 68% | 98% | 99% | 97% |
| Mattioli 1568 | 90% | 85% | 97% | 98% | 91% |
| Petit Bauhin 1671 | 92% | 84% | 88% | 92% | 78% |

What can be said:

- On Mathée 1553 and Du Pinet 1561 the ready-made model leaves a large part of the text outside every block, and every model retrained on the book does not.
- Between the retrained models, the gaps on the three books come from one block on one page each: on Mattioli 1568 a page with commentary in italic and a quoted poem (39 lines of 69 with `herbal_16c_v1`, 66 with the Mattioli-only model); on Mathée a chapter end at the top of a column (24 lines missed by the Mathée-only model). They do not rank the models.

The trainer's own score on the six held-out pages, place and name of each block counted: 0.82 out of 1 for `herbal_16c_v1`.

## Not established

- **That a retrained layout model gives a better text.** No reading has yet been made with a layout model whose blocks were used for the order of the lines.
- **How Kraken uses a layout model and a line finder together.** The instructions of the layout package tell how to train it and how to get blocks from it, not how to get a text. Given both models in one file, Kraken put 145 of the 148 lines of a Du Pinet page in a page-wide block that the line finder makes itself, and ordered them as before; the way meant by Kraken's authors has to be read in its documentation first.
- **Which retrained model is better**, and so whether to retrain per book or for several books.
- **The names of the blocks** given by the models, beyond the few pages looked at on pictures.
