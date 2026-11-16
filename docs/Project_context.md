# Virtutes Herbarum — project context

Background for everything else in this folder. Rewritten 16 November 2026 from the handoff note of 10 November and the work done since. Where this file and the data files disagree, the data files are right (`data/Pilot_works_all_versions.csv`, `data/Pilot_selected_versions.csv`).

Trust labels used below: **[files]** checked in the files of this folder; **[memory]** stated from an AI model's general knowledge, never checked.

## The project

University research project (UCLy, research unit CONFLUENCE: Sciences et Humanités). Aim: extract from historical texts of all continents and eras every statement "plant X, prepared this way, is good for Y", keep each one tied to the page it comes from, and make plants and virtues comparable across texts, places and centuries. Long-term vision of the project lead: a database explorable by latitude, longitude and year, showing where distant cultures agree or contradict each other about a plant.

Team of four: data, AI and statistics (also partly biology); pharmacology; linguistics and anthropology; history. The project is also meant to show what AI and the university's GPU server bring to research, using small open models run locally rather than large commercial models over thousands of pages.

Pilot: six European works, worked on during 2027. Timeline of the presentation deck: launch October 2026, funding application (ANR) autumn 2027, other traditions from 2028.

Hardware: a laptop with an Intel Core Ultra 5 and no dedicated graphics card, for tests on samples; a server with an Nvidia RTX 6000 (96 GB) for bulk work, not yet used.

## The catalogue [files]

Five spreadsheets, one per continent, in `catalogue/` (copies; the originals stay in the project's shared folder). Three rows per work: original, English translation, French translation. `catalogue/catalogue_rows.csv` is the same content as one table.

| Continent | Works | With at least one open link |
|---|---|---|
| Europe | 81 | 64 |
| Asia | 71 | 35 |
| Americas | 44 | 24 |
| Africa | 20 | 16 |
| Oceania | 11 | 7 |
| **Total** | **227** | **146** |

- Scope: texts organised plant by plant that give virtues, up to 1900. Most entries are printed books, not handwritten manuscripts.
- 240 rows carry a link. The catalogue's own notes say every link remains to be verified; this has not been done.
- Ibn al-Baytar appears in three of the files.

## The pilot

Six works forming one lineage: Theophrastus, Dioscorides, Pliny → *Circa instans* → Mattioli → the "Petit Bauhin". They differ in form (Greek, Latin, Italian, Old and modern French; critical editions and old printings) but belong to a single tradition.

| Step | State on 16 November 2026 | Where |
|---|---|---|
| Map every known version of each work | Done: 529 versions | `Edition_mapping_method.md`, `data/Pilot_works_all_versions.csv` |
| Choose up to three versions per work (original, English, French) | Done: 11 versions giving 12 texts; 5 of the 18 slots left empty, with the reason | `Version_selection_method.md`, `data/Pilot_selected_versions.csv` |
| Download the chosen versions | Done and checked: 9.4 GB | `Folder_structure.md`, `data/Downloads_report.csv` |
| Bring every version to one text format | Format and method defined; nothing converted yet | `Unified_text_format.md`, `Conversion_method.md` |
| Read the scans by machine | Approach under discussion; nothing installed or tested | `OCR_Kraken_approach.md` |

Of the 12 texts, 4 exist as typed texts made by scholarly projects and 8 are scans of printed books to be read. No handwritten manuscript is among the chosen versions.

## The presentation deck and the reference articles

- Deck: five aims (record, compare, trace transmission, confront with science, explore the untested). Rule: one record per use, proven by a literal quotation. Fields of a record: source; plant as written; use (part, preparation, vehicle, route, dose, indication, precautions); quotation and translation; origin of the knowledge; traceability; a separate science layer (cell, animal, clinical; validated, contradicted, discordant, not studied). Ethics: Nagoya Protocol, CARE principles, copyright. Estimate: 15,000 to 25,000 records for the pilot.
- Staub, Casu, Leonti 2016: 5,314 uses, 536 plant taxa, 924 drugs recorded by hand from Mattioli's 1568 Dioscorides; full data in its supplementary tables. Keeps the text's wording apart from the modern reading. The benchmark for the pilot.
- Staub et al. 2015: how to classify illnesses and remedies depending on the question asked. Summary and what the project takes from it: `Staub_2015_classification_summary.md`.
- Connelly et al. 2020: a 15th-century English medical text turned into a database, analysed as a network, then tested in the laboratory. (Not in `references/`.)

## Positions taken in the preliminary study

Proposals, read only in part by the team; not decisions.

1. Central entity: the **use record**. Plants on three levels (name as written → plant concept → modern species, with a confidence); virtues on two (historical concept → modern category). Interpretation is stored apart from what the text says.
2. Steps: acquire → bring to one text format → cut into plant entries → translate → extract uses → identify plants → classify virtues → publish.
3. Source files are kept untouched.
4. Extract from the original language; the translation is a control.
5. A record is rejected if its quotation is not found letter for letter in the text. Extraction is done twice independently; people see only the disagreements.
6. Record who copies whom, so that copies are not counted as independent agreement; weigh agreement by how specific the virtue is.
7. A record has several places and dates (composition, copy, habitat of the plant, cited source); keep them apart.
8. AI is central for reading, structuring, translating and extracting; it assists for plant identity and virtue classification. Expert time, not computer time, is the limit.
9. Small hand-made reference sets for each book, to measure quality.

Candidate models **[memory, mid-2026; to be looked up again and measured before any choice]**: page layout — DocLayout-YOLO, YALTAi, Kraken; reading print — olmOCR, PaddleOCR-VL, dots.ocr, LightOnOCR, DeepSeek-OCR, MinerU, Chandra; reading handwriting — Kraken/eScriptorium with CATMuS Medieval, TrOCR; language models — Qwen, Mistral, Gemma, Llama; text similarity — BGE-M3, multilingual-E5, PhilBERTa; plant name references — World Flora Online, POWO, GBIF, Global Names.

## Undecided

- The exact fields of a use record. Suggestion: work one plant (wormwood) through all six works by hand first.
- Transcription rules for the scans.
- Pivot language for comparison: English, French or both.
- Reference lists for species and for virtues (see the Staub 2015 summary for the virtues).
- What place and date mean on the map.
- How much validation time the specialists have.

## Practical facts learnt so far

- Wellcome's image server blocked full-size page images after 64 pages at one page per second (12 November 2026). Internet Archive delivers whole volumes as one archive without such a limit.
- WorldCat, Gallica, HathiTrust and ISTC often refuse automated access (details in `Edition_mapping_method.md`).
- On the laptop: Python 3 (standard library only), poppler tools (`pdftotext`, `pdftoppm`, `pdfimages`), curl, git. Not installed: Kraken, Tesseract, PyTorch, pandas, openpyxl, ImageMagick.

## Terms

- **Version**: one edition of a work (a distinct printing) or one manuscript, whatever its languages.
- **Slot**: one of the three places a version can fill for a work: original language, English, French.
- **Typed text**: a text available as characters, as opposed to a **scan**, which is pictures of pages.
- **Use record**: one statement that one plant, used one way, has one effect, with its quotation.
- **Emic / etic**: in the text's own terms / in modern scientific terms.
- **IIIF**: the standard interface libraries use to serve page images; a *manifest* lists the pages of one item.
