# From any source to one text format

Every chosen version ends as text in the unified format ([`Unified_text_format.md`](Unified_text_format.md)), whatever it started as. How an assistant carries out a conversion: [`skills/convert-version/SKILL.md`](../skills/convert-version/SKILL.md).

The goal this serves, texts that anyone can make again from the exact sources: [`Project_context.md`](Project_context.md#three-stages-and-what-ai-brings-to-each).

## Three kinds of source

| Kind of source | What has to be done | In the pilot |
|---|---|---|
| **Typed text** made by a scholarly project | Convert its structure; nothing to read | 4 texts: Theophrastus (Greek), Dioscorides (Greek), Pliny (Latin), Pliny (English) |
| **Scan of a printed book** | Read the pages by machine, correct, then structure | 8 books, 1497 to 1916 (list in [`OCR_Kraken_approach.md`](OCR_Kraken_approach.md)) |
| **Scan of a manuscript** | Read handwriting by machine, correct, then structure | None in the pilot selection; expected for later works |

When a version has both a typed text and a scan, the typed text is what we work from; what the scan is for: [`Version_selection_method.md`](Version_selection_method.md#the-rules), rule 2.

## Three scripts per version

Each book is laid out its own way: where the chapter numbers are, how notes are attached, how two languages share a page, how pages are numbered. A general converter would be either wrong for most books or as complicated as all of them together. So each version gets its own short scripts, in the folder `convert/` of the version. Every version has the same scripts, with the same names, however little one of them has to do for a given book.

A source also has mistakes of its own: a typed text with a chapter under the wrong number, a page number typed twice. Copying and correcting are kept apart. Linking the pages to their scan images is kept apart too, because it is not needed to make the text:

| Script | What it does | Source files it needs |
|---|---|---|
| 1. `extract.py` | **Copies.** Brings the source to the unified format without correcting anything: what is wrong in the source is wrong in the same way in its output, the raw text (`work/raw/`) | The files the text is made from: the typed file, or the scan when the text is read from it |
| 2. `repair.py` | **Corrects.** Makes the final text (`text/`) from the raw text, by rules written in the script, and lists every change it makes (`work/repairs.csv`) | None: it reads the raw text only |
| 3. `images.py` | **Links pages to images.** Writes the optional `text/page_images.csv` ([`Unified_text_format.md`](Unified_text_format.md#the-page-images-file)) from the pages of the final text | The scans |

- **A script opens only the source files its result is made from.** The text of a version that has a typed file is made by `extract.py` and `repair.py` from that file alone: a researcher who does not have the scans, often hundreds of times larger, obtains exactly the same text. Only `images.py` needs them, and nothing else depends on its result.
- **A scan may decide a rule without being needed to run it.** When a look at a page image settles how a label or a page number must be repaired, the rule and what was seen are written in `repair.py`; running the rule does not open the scan.
- **What a repair rule may change**: the labels around the words (place in the work, kind of passage, page) and where a passage is cut. The words themselves change only through a correction a person asked for (`convert/corrections.csv`).
- **One check of the source files, the same everywhere.** Each script names the source files it needs and gets them through [`tools/vh_sources.py`](../tools/vh_sources.py) before doing anything else. A file that is missing, or whose checksum is not the one recorded in [`data/Downloads_report.csv`](../data/Downloads_report.csv), stops the script with a message that says which file and where to fetch it.

So a doubt about the final text can always be settled: the raw text shows what the source had, the list shows what was changed and by which rule.

The division of work:

- **The assistant writes the scripts; the scripts produce the text.** The assistant never retypes or rewrites the text itself, so anyone can read in the scripts what was done to the source. This is why the texts are not kept in git: the scripts and the exact sources are enough to make them again.
- **The shared check verifies what was produced**, the same for all versions (below).
- **People verify the words of machine-read texts**, on samples compared with the page images. The words of a typed text are taken as the scholarly project typed them and are not read again against the scans: avoiding that reading is why a typed text is preferred. The scan of a typed text is opened only to settle a doubt (a label, a page number). Corrections a person asks for are stored beside the script and applied at each run.

## One check for everything produced

[`tools/vh_check.py`](../tools/vh_check.py) checks any version, whatever its source. It knows the process, not the book.

Each script, when it finishes, writes a small record beside its result (`made_by_extract.json`, `made_by_repair.json`, `made_by_images.json`): the checksum of the script itself, of every file it read and of every file it wrote. From these records the check tells, for each script:

- whether a file it wrote has been changed or deleted since;
- whether its result is out of date, because a file it read has changed (an earlier script was run again and this one was not) or because the script itself has changed;
- whether the source files it read are the recorded ones;
- whether a file lies beside the results that no script made.

It then verifies the shape of the raw text and of the final text ([`Unified_text_format.md`](Unified_text_format.md#the-checker)).

No script touches the result of another. If `repair.py` is run again and the pages change, `page_images.csv` is left as it is and the check says it is out of date; if the pages did not change, it is still good. A script that has not been run is not a fault, and a source file that is absent is not one either: its recorded checksum is enough to compare.

## What counts as verified

A text is `complete` when the whole version is there and passes the check. Its `review` level says how far the words were verified:

- **Counts** agree with known figures: number of books and chapters; for Mattioli 1568, the 831 chapters of Dioscorides counted by Staub et al. 2016.
- For a machine-read text: **samples** spread over the whole book were compared by eye with the page image, with particular attention to plant names, quantities and parts of plants. A typed text has no such review; its `review` stays `none` and this is not listed as a limit.
- For a version with a typed text and a scan, when `images.py` has been written: its rule for matching pages to images was verified by reading the page number on images spread over each volume. This says nothing about the words.

Whatever was not verified is written in the `notes` of the text's info file.

## Open points

- The reading engine for scans and the transcription rules ([`OCR_Kraken_approach.md`](OCR_Kraken_approach.md)).
- Who checks the samples for each language, and how much time they have.
- Whether to move later to a newer state of the typed texts, which their projects keep correcting. Each is recorded at one exact commit in [`data/Downloads_report.csv`](../data/Downloads_report.csv); moving to a newer one is a decision, followed by a new conversion.
