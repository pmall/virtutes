# Retraining the layout model — approach on trial

**A proposal, not a decision.** It becomes part of the method of [`OCR_Kraken_approach.md`](OCR_Kraken_approach.md) once a retrained model has been measured and accepted.

## Why

Before the lines of a page are found and read, a layout model marks its blocks: main text, heading, margin note, running title, page number, picture. The blocks tell which lines are main text and in which order the columns are read. The ready-made model (D-FINE trained on LADaS, "Large") misses blocks on the 15th and 16th-century books. Retraining it on a few corrected pages ("fine-tuning") repairs this, and can be done on a laptop without a graphics card.

## One retraining per type of book, not per book

A model retrained on pages of one book also reads better the books that look like it, and worse the books that do not. So:

- A retraining belongs to a **type** of book, never to one version. Its pages come from several versions of that type.
- **A type is defined by measurement, not by date or look.** A book belongs to the type whose model finds the most of its sample-page lines. The ready-made model is one of the choices: a book it already reads well keeps it.
- A retrained model is never changed once a version uses it. A new retraining gets a new name (`<type>_v1`, `<type>_v2`), and each version records the model it used, by name and checksum, in its `convert/ocr_models.csv` under the role `layout`.
- A retrained model is not published and cannot be fetched again: it is kept in `models/` and backed up with the scans.

## The folder of a retraining

```
finetuning/layout/<type>/
    pages.csv                     the pages: version, archive in source/, image number, set
    pages/<version>/img<n>.xml    the corrected layout of one page (PAGE XML); in git
    pages/<version>/img<n>.jpg    the page image, 2000 px high; not in git, made again from source/
    work/                         lists for the trainer, the model's own layout, pictures, the trained model; not in git
```

`set` is `train` or `held_out`. Held-out pages are never trained on: they tell whether the model has learned or only memorised. Every version of the type has held-out pages. The sample pages of a version's reading test ([`OCR_Kraken_approach.md`](OCR_Kraken_approach.md), step 1) are in neither set, so the measure below stays honest.

The scripts are shared, in [`tools/`](../tools/): `layout_pages.py` (images and lists), `layout_cli.py` (the model: marking pages, retraining), `layout_view.py` (a page with its blocks drawn), `layout_fix.py` (the corrected layout from the model's layout and a list of fixes), `layout_cover.py` (the measure).

## How a page is corrected

The ready-made model marks the page; its blocks are drawn on the page; each block is kept, relabelled, dropped or redrawn. The labels are the SegmOnto names the model was trained with. Rules followed so far (the assistant's choices, not yet checked by a person):

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

## The measure

For each sample page of each scanned version: how many of the lines found by the line finder lie inside a block of the model ([`tools/layout_cover.py`](../tools/layout_cover.py)). The base of comparison is the ready-made model. The figure tells how much of the page the blocks hold; whether each block has the right label and the right limits is looked at on the pictures.

## The types

| Type | Versions its pages come from | Pages (train + held out) | Model |
|---|---|---|---|
| `herbal_16c`: printed herbals of the 16th century, one or two columns, woodcuts in the text, margin notes | Mathée 1553, Du Pinet 1561, Mattioli 1568 | 31 + 6 | `models/herbal_16c_v1/herbal_16c_v1.safetensors`, 125878904 bytes, md5 `aeabd4ff30d23a278583f0af85d1c74b` (30 passes, 1 h 50 on a laptop) |

## What was measured

Lines of the sample pages lying inside a block, ready-made model against `herbal_16c_v1` (checked, 44 sample pages):

| Version | Ready-made | `herbal_16c_v1` | Model to use (proposal) |
|---|---|---|---|
| Hort 1916 | 98% | 95% | ready-made |
| Mathée 1553 | 75% | 99% | `herbal_16c_v1` |
| Poinsinet 1771-1782 | 95% | 92% | ready-made |
| Dorveaux 1913 | 98% | 74% | ready-made |
| Venice 1497 | 90% | 82% | ready-made for now; its own type if 90% is not enough |
| Du Pinet 1561 | 59% | 97% | `herbal_16c_v1` |
| Mattioli 1568 | 90% | 91% | `herbal_16c_v1`, to be improved |
| Petit Bauhin 1671 | 92% | 78% | ready-made |

Looked at on pictures (two pages only): on Du Pinet the blocks and their labels are right, columns, pictures, line counters and catchword included; two of four margin notes are missed. On Mattioli 1568 one page loses a whole block of commentary in italic and a quoted poem (39 lines of 69 found, 65 with the ready-made model), while another gains 23 lines: the 13 pages of this book do not yet cover its page designs.

## Not verified

- No person has looked at the corrected pages.
- Whether one model for all books would do as well as one per type has not been tried.
- The labels and limits of the blocks were looked at on two sample pages only.
