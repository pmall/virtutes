# From any source to one text format

Every chosen version ends as text in the unified format ([`Unified_text_format.md`](Unified_text_format.md)), whatever it started as. How an assistant carries out a conversion: [`skills/convert-version/SKILL.md`](../skills/convert-version/SKILL.md).

## Three kinds of source

| Kind of source | What has to be done | In the pilot |
|---|---|---|
| **Typed text** made by a scholarly project | Convert its structure; nothing to read | 4 texts: Theophrastus (Greek), Dioscorides (Greek), Pliny (Latin), Pliny (English) |
| **Scan of a printed book** | Read the pages by machine, correct, then structure | 8 books, 1497 to 1916 (list in [`OCR_Kraken_approach.md`](OCR_Kraken_approach.md)) |
| **Scan of a manuscript** | Read handwriting by machine, correct, then structure | None in the pilot selection; expected for later works |

When a version has both a typed text and a scan, the typed text is what we work from; the scan is there to look at a page when in doubt ([`Version_selection_method.md`](Version_selection_method.md#the-rules), rule 2).

## Two scripts per version

Each book is laid out its own way: where the chapter numbers are, how notes are attached, how two languages share a page, how pages are numbered. A general converter would be either wrong for most books or as complicated as all of them together. So each version gets its own short scripts, in the folder `convert/` of the version.

A source also has mistakes of its own: a typed text with a chapter under the wrong number, a page number typed twice. Copying and correcting are kept apart, in two scripts run one after the other:

1. **`extract.py` copies.** It brings the source to the unified format without correcting anything: what is wrong in the source is wrong in the same way in its output, the raw text (`work/raw/`).
2. **`repair.py` corrects.** It makes the final text (`text/`) from the raw text, by rules written in the script, and lists every change it makes (`work/repairs.csv`). A rule may change the labels around the words (place in the work, kind of passage, page) and where a passage is cut. The words themselves change only through a correction a person asked for (`convert/corrections.csv`).

So a doubt about the final text can always be settled: the raw text shows what the source had, the list shows what was changed and by which rule.

Writing such scripts by hand takes a person hours per book, which is why projects usually avoid it. An AI assistant writes them in minutes, so the project can afford them for each version. The division of work:

- **The assistant writes the scripts; the scripts produce the text.** The assistant never retypes or rewrites the text itself. The result is therefore the same at every run, and anyone can read in the scripts what was done to the source. This is why the texts are not kept in git: the scripts and the exact sources are enough to make them again ([`Folder_structure.md`](Folder_structure.md#what-is-in-git-and-what-is-not)).
- **The shared checker verifies the shape of the result**, the same for all versions.
- **People verify the words of machine-read texts**, on samples compared with the page images. The words of a typed text are taken as the scholarly project typed them and are not read again against the scans: avoiding that reading is why a typed text is preferred. The scan of a typed text is opened only to settle a doubt (a label, a page number). Corrections a person asks for are stored beside the script and applied at each run.

## What counts as verified

A text is `complete` when the whole version is there and passes the checker. Its `review` level says how far the words were verified:

- **Counts** agree with known figures: number of books and chapters; for Mattioli 1568, the 831 chapters of Dioscorides counted by Staub et al. 2016.
- For a machine-read text: **samples** spread over the whole book were compared by eye with the page image, with particular attention to plant names, quantities and parts of plants. A typed text has no such review; its `review` stays `none` and this is not listed as a limit.
- For a version with a typed text and a scan: the page numbers of the typed text were matched to the scan.

Whatever was not verified is written in the `notes` of the text's info file.

## Open points

- The reading engine for scans and the transcription rules ([`OCR_Kraken_approach.md`](OCR_Kraken_approach.md)).
- Who checks the samples for each language, and how much time they have.
- Whether to move later to a newer state of the typed texts, which their projects keep correcting. Each is recorded at one exact commit in [`data/Downloads_report.csv`](../data/Downloads_report.csv); moving to a newer one is a decision, followed by a new conversion.
