# The unified text format

Version 0.3. Any change to the format raises this number.

## Purpose

Every version of every work ends as text in **one and the same format**, whether it started as a typed text from a scholarly project, a scan of a printed book or a scan of a manuscript. All later steps (cutting into plant entries, translating, extracting uses, comparing) read this format and nothing else. They never need to know where a text came from.

What the format must guarantee:

1. **Nothing is guessed.** The words are those of the typed source, or those the reading engine read, errors included. No person and no AI completes, corrects or modernises them. A correction is a recorded change that a person asked for. A use will be accepted only if its quotation is found letter for letter in the text.
2. **Every passage is tied to its page.** A separate, optional file ties each page to its image in the scan.
3. **The voices are kept apart**: the work itself, a commentator, the modern editor's notes, the list of variant readings.
4. **No interpretation.** No plant identification, no modern disease name, no translation. Those are separate layers built on top (see [`Staub_2015_classification_summary.md`](Staub_2015_classification_summary.md)).
5. **Plain files** that a short script can read, that git can compare line by line, and that a person can open.

## The files

In each version folder ([`Folder_structure.md`](Folder_structure.md)), the folder `text/` holds the files below. The raw text in `work/raw/` ([`Conversion_method.md`](Conversion_method.md#three-scripts-per-text)) has the same files in the same format, `<lang>.page_images.csv` aside; the difference is that its labels still carry the mistakes of the source.

| File | Content |
|---|---|
| `<lang>.jsonl` | The text in one language, one passage per line |
| `<lang>.info.json` | What this text is, where it comes from, how far it has been checked |
| `<lang>.pages.csv` | The pages this text is on |
| `<lang>.page_images.csv` | Optional: the scan image of each page |

`<lang>` is the three-letter ISO 639-3 code of the language: `grc` ancient Greek, `lat` Latin, `eng` English, `fra` French, `ita` Italian, `frm` Middle French (about 1400–1600), `fro` Old French. A bilingual book gives two texts in the same folder, each with its own four files: neither needs the other to be made or read. They are lined up through `ref` and through the page identifiers.

Files are UTF-8 without byte-order mark, lines end with a line feed.

## A passage

One line of `<lang>.jsonl` is one passage: a paragraph of the work, a heading, a note. Each line is a JSON object.

```
{"id":"004217","kind":"text","ref":"3.48.1","page":"v2p228","text":"λίθους θρύπτει καὶ ἐξουρεῖν ποιεῖ καὶ σπλῆνα ἐσκιρρωμένον τήκει …","breaks":[[412,"v2p229"]]}
```

| Field | Required | Content |
|---|---|---|
| `id` | yes | Identifier of the passage, unique in the file. By convention a six-digit number in reading order |
| `kind` | yes | Which voice or part of the book (list below) |
| `page` | yes | The page on which the passage begins: a value of the column `page` of `<lang>.pages.csv` |
| `text` | yes | The words, as one continuous string (rules below) |
| `ref` | when the work has one | The place in the work in its usual citation system, with dots: `3.48.1` = book 3, chapter 48, section 1. What each number means is stated in the info file. A translation carries the same `ref` as its original, which is how the two are lined up |
| `breaks` | no | Page changes inside the passage: a list of `[position, page]`. The text from that position on is on that page |
| `marks` | no | Stretches of the text with a special status: a list of `[start, end, type]` (list below) |
| `anchor` | no | For a note, a variant or a marginal note: `[id, position]`, the point of the main text it is attached to |
| `lang` | no | Language of this passage when it differs from the language of the file |
| `conf` | no | For machine-read text: the reading engine's own confidence, from 0 to 1 |
| `checked` | no | `true` when a person has compared this passage with the page image |

Positions count characters (Unicode code points) from 0. `start` is included, `end` excluded.

A converter may add fields of its own for one version; their names begin with `x_`. Later steps ignore them.

### Kinds

| `kind` | What |
|---|---|
| `text` | The work itself |
| `head` | A heading: book, chapter, name of the plant at the head of its entry |
| `commentary` | A commentator's text printed with the work as part of the same book (Mattioli's *discorsi* after each chapter of Dioscorides) |
| `note` | A note of the editor or translator (footnote, endnote) |
| `apparatus` | The list of variant readings in a critical edition |
| `margin` | A printed marginal note or summary |
| `caption` | The caption of an illustration |
| `paratext` | Everything around the work: title page, dedication, preface, index, table of contents |

Running heads, page numbers, catchwords and signatures are not text: they are dropped (the page number goes into `<lang>.pages.csv`).

### Rules for `text`

- The characters of the typed source, or those the reading engine read: no modernised spelling, no correction, no completion, no expansion of abbreviations beyond what the transcription rules allow. **The transcription rules for scans (long s, ligatures, abbreviations, u/v, i/j) are not yet decided**; they will be added here before the first scan is typed.
- Unicode form NFC. Words separated by one plain space; no space at either end; no line breaks, tabs or other control characters.
- The line breaks of the printed page are not kept. A word cut by a hyphen at the end of a line is joined again.
- No markup inside the text. Anything that needs marking goes into `marks`.

### Marks

| Type | Meaning |
|---|---|
| `add` | Words supplied by the editor, absent from the manuscripts (angle brackets in a critical edition) |
| `del` | Words the editor judges not to belong to the work (square brackets in a critical edition). They stay in `text`, marked |
| `gap` | Something lost or unreadable. The text holds the single character `…` at that place |
| `unclear` | A doubtful reading |
| `hi` | Typographic emphasis in the source: italics, small capitals, spaced letters |
| `foreign` | Words in another language than the passage |

## The pages file

`<lang>.pages.csv`, one row per page the text is on, in reading order, with this header:

```
page,volume,printed
```

| Column | Content |
|---|---|
| `page` | Identifier of the page, unique in the file. Convention: `v<volume>p<printed number>` when the source is a typed text that gives printed page numbers (`v2p228`); `v<volume>i<position of the image>` when the text was read from the scan (`v1i0134`) |
| `volume` | Volume number (1 for a single volume) |
| `printed` | The page or folio number as printed or written; empty if none |

## The page images file

`<lang>.page_images.csv` says where the image of each page is in the scans. It is **optional**: the text is complete without it, and the other files are the same whether it is there or not. It exists so that a page can be shown beside its text; it is the only file of `text/` that cannot be made without the scans when the text comes from a typed file ([`Conversion_method.md`](Conversion_method.md#three-scripts-per-text)). It is never in `work/raw/`.

One row per page that has an image, with this header:

```
page,source_file,image,mapping
```

| Column | Content |
|---|---|
| `page` | A value of the column `page` of `<lang>.pages.csv`, at most once |
| `source_file` | The scan this page is in: name of the file in `source/` |
| `image` | The image inside that file: its name in the archive, or the page number for a PDF |
| `mapping` | How the page was matched to its image: `checked` (compared by eye) or `computed` (by rule, e.g. a constant shift, verified on a few pages) |

A page not yet matched has no row.

## The info file

`<lang>.info.json`, one JSON object:

| Key | Content |
|---|---|
| `format` | `vh-text/0.3` |
| `version` | Name of the version folder |
| `work_no`, `work` | As in the selection file |
| `lang` | Same as the file name |
| `origin` | `typed` (converted from a typed text), `ocr` (read by machine from a printed scan), `htr` (read by machine from handwriting) |
| `sources` | The files of `source/` the text was made from, each `{"file": …, "md5": …}` |
| `converter` | Path of the script that produced the text |
| `ref_scheme` | Meaning of the parts of `ref`, e.g. `["book","chapter","section"]`; empty list if the work has no citation system |
| `rights` | Rights of this text, as stated by its source |
| `status` | `draft` or `complete` (the whole version is there) |
| `review` | How much a person has checked: `none`, `sampled` (with the result in `notes`), `full` |
| `notes` | Known limits, in plain words: what is missing, what was not verified, measured error rate |

## The checker

Each version is converted by its own script, so nothing guarantees by itself that two scripts produce files of the same shape. [`tools/vh_text.py`](../tools/vh_text.py) is the common gate: it reads a `text/` or `work/raw/` folder and verifies its **shape** (every field present and well formed, every page known, every position inside its text, no stray spaces or markup; and `<lang>.page_images.csv` when it is there). It does not look at the source and does not judge whether the words are right; for a machine-read text that is done by comparing samples with the page images, while a typed text is taken as its project typed it ([`Conversion_method.md`](Conversion_method.md#what-counts-as-verified)). A text that fails the check is not accepted. It is run as part of the check of a version, [`tools/vh_check.py`](../tools/vh_check.py) ([`Conversion_method.md`](Conversion_method.md#the-recorded-results-and-one-check)).

## Choices made, and why

- **One line per passage (JSON Lines) rather than TEI XML or plain text.** TEI can express all of this, but every project uses it differently (the four typed texts we hold use three different layouts), so each later step would again need per-source code. Plain text cannot carry pages and voices without inventing a markup. JSON Lines is read by a few lines of code in any language and compares cleanly in git.
- **Marks beside the text, not in it**, so that a quotation can be searched letter for letter.
- **The paragraph as unit**, with page changes recorded inside it, rather than cutting at each page: a sentence that runs over two pages stays whole.
- **Editorial notes and variants are kept**, as their own kinds, because they are the cheapest to keep now and impossible to recover later; a step that does not need them filters on `kind`.

## Open points

- Transcription rules for scans (above).
- How to mark the language of Old and Middle French texts consistently (`fro`, `frm`), to be confirmed with the linguist.
- A regularised spelling for searching (long s → s, u/v) would be a second, derived text, not a change to this one. Not defined yet.
- Tables and recipes laid out in columns: no special treatment yet.
- Identifiers are stable for a given state of a text. If a converter is improved and passages are cut differently, the numbers change; a record that quotes the text should therefore keep `ref`, the quotation and the git revision, not the `id` alone.
