# Reading test — Pliny, French with the Latin, Poinsinet 1771–1782

The test of how well ready-made Kraken models read this scan, on sample pages, done with the skill `test-scan-reading` (method: `docs/OCR_Kraken_approach.md`). Everything below was checked on the files unless marked otherwise.

## The book

Poinsinet de Sivry's *Histoire naturelle de Pline*, Paris, 1771–1782, 12 tomes: the Latin text and a French translation facing it, with the translator's notes. Biblioteca Nazionale di Napoli copy scanned by Google: one archive of JPEG 2000 images per tome, about 1,740 × 2,500 pixels, 8,449 images in all (`metadata/note.txt`). The plant books of Pliny (XII to XXVII) are in tomes 4 to 9 (checked: tome 5 holds book XV, tome 7 book XX, tome 8 book XXIV, tome 9 book XXVII; assumed for tome 4 and the limits of each tome).

Layout of a text opening: the Latin on the left-hand page, the French on the right-hand page, each in one column of 18th-century roman type, with a running head ("NATURALIS HISTORIÆ LIB. XX." with the page number; "HISTOIRE NATURELLE, LIV. XX." with the page number). Below the text, the notes, in two columns and smaller type, in French with Latin and some Greek quotations in italic. The French text calls its notes by numbers in parentheses, (40). Some pages carry only two or three lines of text above long notes (the translator's observations, which run over several pages). At the foot, the catchword (the first word of the next page) and, on some pages, the printer's signature ("Tome VII. Bb").

What makes it hard: long s (ſ), æ and œ, the ct and ſt ligatures, show-through and ink spots on some pages, and the two columns of notes under a one-column text. The type itself is clear.

## Sample pages

Pages named by tome and image number in that tome's archive (`t07_img0200` is image 200 of tome 7).

| Page | Archive | Printed page | Language | Why |
|---|---|---|---|---|
| t05_img0300 | bub_gb_TZhhOdJ7iucC | 291, book XV | French | Tome 5; making olive oil (decanting, pressing, the first oil); show-through and faint print |
| t07_img0200 | bub_gb_P9MWMRado88C | 192, book XX | Latin | Uses of radish and hibiscus (juice in the ears, leaves in water against the belly, root against scrofula); an ink blot on one word |
| t07_img0201 | bub_gb_P9MWMRado88C | 193, book XX | French | The French facing t07_img0200: the same uses, to compare the two languages |
| t08_img0302 | bub_gb_A3GmeoIGTQwC | 295, book XXIV | French | Two lines of text above two long blocks of notes in two columns: are the text lines kept apart from the notes? |
| t09_img0100 | bub_gb_6LPXIUPt5VsC | 92, book XXVII | Latin | Short chapters of plants with uses (onosma, onopordon, osyris, oxys, polyanthemum) |
| t09_img0101 | bub_gb_6LPXIUPt5VsC | 93, book XXVII | French | The French facing t09_img0100; plant names in italic |

Four pages carry uses of plants (t07 and t09); t05 carries a preparation (olive oil). Images taken from the archives unchanged with `tools/page_image.py`.

Main text, for the scores: the text of both languages, Latin and French; the catchwords and signatures are put with the page number, the notes are not measured.

## Models tried

The three models of every reading in this report: layout model, none; line finder, Kraken's general one, unless said otherwise; reading model, the one named in each row.

The same line finder and nine reading models as for Dorveaux 1913, pinned by DOI and checksum in `convert/ocr_models.csv`. No other model in `kraken list` was found made for 18th-century French or Latin print (checked on the list; two candidates there turned out to be for Ottoman and Persian).

Line finders compared on t07_img0200 and t08_img0302, both read with PP-OCRv6 (small): the general one (in `ocr_models.csv`) and the Kraken segmentation model for two-column prints (`seg_news_1.0.mlmodel`, 5,250,514 bytes, md5 6f7e68e826a44e810320c389a263bf0d, https://doi.org/10.5281/zenodo.10783346). The two-column one cut the lines into fragments ("HISTOI", "touchement fa") and gave 42 main-text words wrong out of 123, against 1 with the general one. The general one is kept.

## Scores

`uv run tools/ocr_score.py` against the six reference pages (drafts, see "Reference"), 948 main-text words; then the Latin pages (233 words) and the French pages (715 words) apart.

| Reading | Main-text words wrong (all) | Latin | French | CER (whole page) |
|---|---|---|---|---|
| PP-OCRv6 (medium) | 2 (0.21%) | 1 | 1 | 3.55% |
| CATMuS-Print [Large] | 2 (0.21%) | 1 | 1 | 6.39% |
| CATMuS-Print [Small] | 5 (0.53%) | 2 | 3 | 6.78% |
| PP-OCRv6 (small) | 6 (0.63%) | 1 | 5 | 3.61% |
| CATMuS-Print [Tiny] | 12 (1.27%) | 2 | 10 | 6.69% |
| PP-OCRv6 (tiny) | 13 (1.37%) | 5 | 8 | 4.04% |
| Gallicorpora+ | 28 (2.95%) | 2 | 26 | 4.36% |
| McCATMuS | 74 (7.81%) | 26 | 48 | 9.17% |
| A generalized model for English printed text | 1,780 (187.76%) | 479 | 1,301 | 77.51% |

The CATMuS models write long s as s; the scores of words set that aside, the CER does not, which is why their CER is higher with as few wrong words.

## Wrong main-text words of the two best models

| Model | Page | Reference | Reading | Carries a record |
|---|---|---|---|---|
| PP-OCRv6 (medium) | t05_img0300 | les | lès (a speck above the e read as an accent) | No |
| PP-OCRv6 (medium) | t07_img0200 | ſimile (Pastinacæ simile hibiscum, "hibiscum, like the parsnip") | imile (the s is under an ink blot) | No: a description; the two plant names around it are read right |
| CATMuS-Print [Large] | t07_img0200 | ſimile | lmile | No (as above) |
| CATMuS-Print [Large] | t09_img0101 | uniforme ("rend ſa couleur uniforme", of the skin) | uniforie (a damaged m) | No: describes the effect, which "efface les taches de la peau" already gives |

No wrong word carries a record. Every plant name of the sample pages (raifort, hyſſope, ibiſque, panais, onoſma, onopordon, oſyris, oxys, polyanthêmon, batrakhion and the Latin ones) is read right by both models.

## Lines

Checked for PP-OCRv6 (medium) and CATMuS-Print [Large] on all six pages: each main-text line of the reference matched with the reading.
- Lost: none in the main text.
- Cut in two: none in the main text.
- Out of order: none; on each page the main-text lines come in order, before the notes. On t08_img0302 the two text lines stay apart from the notes below.
- In the notes (not measured): the left column is read before the right one, but on t08_img0302 the line finder joins the last line of the left column to the last line of the right ("inhérente, crocis."). If the notes were ever used, that would need its own treatment.
- One empty line in the reading of PP-OCRv6 (medium) on t05_img0300 and t07_img0200, outside the main text (a speck or the rule).

## Reference

Drafted by the assistant from the images, then every line where one of the three best models (PP-OCRv6 medium, CATMuS-Print Large and Small) read other words was looked at again on the line image (61 lines, 5 of them main text): no error found in the drafts. Points not settled, or settled by choice:
- t07_img0200, "ſimile": the first letter is under an ink blot on this copy; the reference keeps the word the sense requires.
- t09_img0101, "forme" (end of "uni-forme"): the m is damaged and looks like "rn" or "in"; the reference keeps "forme".
- t05_img0300, "les": a mark above the e taken for a speck, not an accent.
- Notes: Greek words (t07_img0201, t09_img0100, t09_img0101) are transcribed with modern letters where the print uses old ligatures (ου); spacing in the notes is close, not exact. Notes are not measured.
No person has checked the references yet.

## Abbreviations

No abbreviation signs in the main text, apart from the ampersand (&) for "et", 34 times on the sample pages, in both languages. The scorer leaves & out, as punctuation; both best models read every & as &. Ligatures (ct, ſt, ſſ, æ, œ) are read as their letters.

## Speed

On the laptop (Intel Core Ultra 5 235U, no GPU), 8 threads, one page (t07_img0201), times including starting Kraken and loading the model: finding the lines 20 s; reading with CATMuS-Print [Large] 14 s, PP-OCRv6 (small) 20 s, (medium) 47 s. The whole set (8,449 images, front matter and indexes included) would take about 80 hours with CATMuS-Print [Large] and about 160 hours with PP-OCRv6 (medium); the plant books alone (tomes 4 to 9, 4,006 images), about 38 and 75 hours (assumed from these times; reading many pages in one run should be faster).

## Proposal

**Good enough by the threshold** with either PP-OCRv6 (medium) or CATMuS-Print [Large]: 2 main-text words wrong in 948 (0.21%), none carrying a record, no main-text line lost or out of order, in both the Latin and the French.

Proposed: **CATMuS-Print [Large]**, as good on the words and about three times faster. Its one cost is that it writes long s as s, so the text it gives is not a transcription of the print in that point; for the extraction this changes nothing (long s and s are the same letter). If the text should keep ſ, PP-OCRv6 (medium) instead.

To decide (step 6 of the method):
- Whether the Latin is read too, or only the French (the Latin original is already taken from Mayhoff, `works/Pilot_selected_versions.csv`); reading only the French halves the time.
- The ink spots: a spot over a letter can hide it (ſimile) or look like an accent (lès). The checks of step 7 (words found nowhere else in the book) would catch most of them.
- No fine-tuning proposed for this book.
