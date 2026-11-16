# From any source to one text format

Every chosen version ends as text in the unified format ([`Unified_text_format.md`](Unified_text_format.md)), whatever it started as. How an assistant carries out a conversion: [`skills/convert-version/SKILL.md`](../skills/convert-version/SKILL.md).

## Three kinds of source

| Kind of source | What has to be done | In the pilot |
|---|---|---|
| **Typed text** made by a scholarly project | Convert its structure; nothing to read | 4 texts: Theophrastus (Greek), Dioscorides (Greek), Pliny (Latin), Pliny (English) |
| **Scan of a printed book** | Read the pages by machine, correct, then structure | 8 books, 1497 to 1916 (list in [`OCR_Kraken_approach.md`](OCR_Kraken_approach.md)) |
| **Scan of a manuscript** | Read handwriting by machine, correct, then structure | None in the pilot selection; expected for later works |

When a version has both a typed text and a scan, the typed text is what we work from; the scan is there to look at a page when in doubt ([`Version_selection_method.md`](Version_selection_method.md#the-rules), rule 2).

## One script per version

Each book is laid out its own way: where the chapter numbers are, how notes are attached, how two languages share a page, how pages are numbered. A general converter would be either wrong for most books or as complicated as all of them together. So each version gets its own short script, `convert/convert.py` in its folder.

Writing such a script by hand takes a person hours per book, which is why projects usually avoid it. An AI assistant writes one in minutes, so the project can afford one per version. The division of work:

- **The assistant writes the script; the script produces the text.** The assistant never retypes or rewrites the text itself. The result is therefore the same at every run, and anyone can read in the script what was done to the source.
- **The shared checker verifies the shape of the result**, the same for all versions.
- **People verify the words**, on samples compared with the page images. Their corrections are stored beside the script and applied at each run.

## What counts as verified

A text is `complete` when the whole version is there and passes the checker. Its `review` level says how far the words were verified:

- **Counts** agree with known figures: number of books and chapters; for Mattioli 1568, the 831 chapters of Dioscorides counted by Staub et al. 2016.
- **Samples** spread over the whole book were compared by eye with the page image, with particular attention to plant names, quantities and parts of plants.
- For a version with a typed text and a scan: the page numbers of the typed text were matched to the scan.

Whatever was not verified is written in the `notes` of the text's info file.

## Open points

- The reading engine for scans and the transcription rules ([`OCR_Kraken_approach.md`](OCR_Kraken_approach.md)).
- Who checks the samples for each language, and how much time they have.
- Whether the typed texts, which their projects keep correcting, should be fetched again later; the checksum in [`data/Downloads_report.csv`](../data/Downloads_report.csv) tells whether a file has changed.
