# Virtutes Herbarum — project context

Where this file and the data files disagree, the data files are right.

## The project

University research project (UCLy, research unit CONFLUENCE: Sciences et Humanités). Aim: extract from historical texts of all continents and eras every statement "plant X, prepared this way, is good for Y", keep each one tied to the page it comes from, and make plants and virtues comparable across texts, places and centuries. Long-term vision of the project lead: a database explorable by latitude, longitude and year, showing where distant cultures agree or contradict each other about a plant.

Team of four: data, AI and statistics (also partly biology); pharmacology; linguistics and anthropology; history. The project is also meant to show what AI and the university's GPU server bring to research, using small open models run locally rather than large commercial models over thousands of pages.

Pilot: six European works, worked on during 2027. Timeline of the presentation deck: launch October 2026, funding application (ANR) autumn 2027, other traditions from 2028.

Hardware: a laptop with an Intel Core Ultra 5 and no dedicated graphics card, for tests on samples; a server with an Nvidia RTX 6000 (96 GB) for bulk work.

## The catalogue

Five spreadsheets, one per continent, in [`catalogue/`](../catalogue/) (copies; the originals stay in the project's shared folder). Three rows per work: original, English translation, French translation. [`catalogue/catalogue_rows.csv`](../catalogue/catalogue_rows.csv) is the same content as one table.

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

## Three stages, and what AI brings to each

The work is in three stages. The table in [The steps](#the-steps) gives the method and the result of each step inside them.

1. **Finding and obtaining the versions.** For each work, list every known edition and translation, choose the ones to use by the project's criteria, and download them.
2. **From the libraries' files to the texts.** Bring every chosen version to one common text format.
3. **From the texts to plants and virtues.** Find the plant entries, the uses, the plants' identities and the classes of virtues. Not started.

**Stage 1: an AI assistant searches and proposes.** Listing the editions of one work means searching library catalogues, bibliographies and digital libraries across the web, then checking each candidate against the criteria (complete, free of copyright, downloadable, sharp enough). This takes a person countless hours per work; an assistant does it in a fraction of that time. A search of this kind does not give the same result twice, so what makes it verifiable is what it leaves behind: the list of every version found, the rule that decided each choice, and for each downloaded file its exact address and checksum. Methods: [`Edition_mapping_method.md`](Edition_mapping_method.md), [`Version_selection_method.md`](Version_selection_method.md).

**Stage 2: anyone can make the texts again.** For each version, scripts make the text from the exact files a library delivered, so that any researcher who has those files, identified by their checksums, obtains exactly the same text, character for character.

- **An AI assistant writes the scripts.** Each book is laid out its own way and needs scripts fitted to it, which costs a person hours per book and is why projects usually avoid it; an assistant writes them in minutes.
- **Running them needs no AI.** The scripts are ordinary programs: they stop if a source file is not the one recorded, and give the same result at every run, on any computer. The checksums of the results are kept in git, so anyone can verify that they obtained the same text.

How this is done: [`Conversion_method.md`](Conversion_method.md); what must be kept to make the texts again: [`Folder_structure.md`](Folder_structure.md#what-is-in-git-and-what-is-not).

## The pilot

Six works forming one lineage: Theophrastus, Dioscorides, Pliny → *Circa instans* → Mattioli → the "Petit Bauhin". They differ in form (Greek, Latin, Italian, Old and modern French; critical editions and old printings) but belong to a single tradition.

For each work, up to three versions are used: original language, English, French. The pilot has 11 versions giving 12 texts; 5 of the 18 slots are empty. Of the 12 texts, 4 exist as typed texts made by scholarly projects and 8 are scans of printed books to be read by machine. No handwritten manuscript is among them.

## The steps

| Step | Method | Result |
|---|---|---|
| Map every known version of a work | [`Edition_mapping_method.md`](Edition_mapping_method.md) | [`works/Pilot_works_all_versions.csv`](../works/Pilot_works_all_versions.csv) |
| Choose the versions to use | [`Version_selection_method.md`](Version_selection_method.md) | [`works/Pilot_selected_versions.csv`](../works/Pilot_selected_versions.csv) |
| Download them | [`Folder_structure.md`](Folder_structure.md) | One folder per version, with its list of source files (`metadata/sources.csv`) |
| Bring every version to one text format | [`Conversion_method.md`](Conversion_method.md), [`Unified_text_format.md`](Unified_text_format.md); for scans, [`OCR_Kraken_approach.md`](OCR_Kraken_approach.md) | `text/` in each version folder |
| Cut into plant entries, translate, extract the uses, identify the plants, classify the virtues, publish | Not yet defined; positions below, and [`Staub_2015_classification_summary.md`](Staub_2015_classification_summary.md) for the classification | |

## The presentation deck and the reference articles

- Deck: five aims (record, compare, trace transmission, confront with science, explore the untested). Rule: one record per use, proven by a literal quotation. Fields of a record: source; plant as written; use (part, preparation, vehicle, route, dose, indication, precautions); quotation and translation; origin of the knowledge; traceability; a separate science layer (cell, animal, clinical; validated, contradicted, discordant, not studied). Ethics: Nagoya Protocol, CARE principles, copyright. Estimate: 15,000 to 25,000 records for the pilot.
- Staub, Casu, Leonti 2016: 5,314 uses, 536 plant taxa, 924 drugs recorded by hand from Mattioli's 1568 Dioscorides; full data in its supplementary tables. Keeps the text's wording apart from the modern reading. The benchmark for the pilot.
- Staub et al. 2015: how to classify illnesses and remedies depending on the question asked. Summary and what the project takes from it: [`Staub_2015_classification_summary.md`](Staub_2015_classification_summary.md).
- Lardos et al. 2024: a method to judge which modern species a historical plant name means, worked on Dioscorides. An existing study to know and compare with, not a procedure the project follows. Summary and what the project may take from it: [`Lardos_2024_plant_identification_summary.md`](Lardos_2024_plant_identification_summary.md).
- Connelly et al. 2020: a 15th-century English medical text turned into a database, analysed as a network, then tested in the laboratory. (Not in [`references/`](../references/).)

## Positions taken in the preliminary study

Proposals, read only in part by the team; not decisions.

1. Central entity: the **use record**. Plants on three levels (name as written → plant concept → modern species, with a confidence); virtues on two (historical concept → modern category). Interpretation is stored apart from what the text says.
2. Extract from the original language; the translation is a control.
3. A record is rejected if its quotation is not found letter for letter in the text. Extraction is done twice independently; people see only the disagreements.
4. Record who copies whom, so that copies are not counted as independent agreement; weigh agreement by how specific the virtue is.
5. A record has several places and dates (composition, copy, habitat of the plant, cited source); keep them apart.
6. AI is central for reading, structuring, translating and extracting; it assists for plant identity and virtue classification. Expert time, not computer time, is the limit.
7. Small hand-made reference sets for each book, to measure quality.

## Undecided

- The exact fields of a use record. Suggestion: work one plant (wormwood) through all six works by hand first.
- Pivot language for comparison: English, French or both.
- Reference lists for species and for virtues (see the Staub 2015 summary for the virtues).
- What place and date mean on the map.
- How much validation time the specialists have.

## Terms

- **Version**: one edition of a work (a distinct printing) or one manuscript, whatever its languages.
- **Slot**: one of the three places a version can fill for a work: original language, English, French.
- **Typed text**: a text available as characters, as opposed to a **scan**, which is pictures of pages.
- **Use record**: one statement that one plant, used one way, has one effect, with its quotation.
- **Emic / etic**: in the text's own terms / in modern scientific terms.
- **IIIF**: the standard interface libraries use to serve page images; a *manifest* lists the pages of one item.
