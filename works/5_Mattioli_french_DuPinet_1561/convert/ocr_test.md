# Reading test — Mattioli, French, Du Pinet 1561

The test of how well ready-made Kraken models read this scan, on sample pages, done with the skill `test-scan-reading` (method: `docs/OCR_Kraken_approach.md`). Everything below was checked on the files unless marked otherwise.

## The book

One folio volume in French, *Les commentaires de M. Pierre André Matthioli* on Dioscorides, translated by Antoine Du Pinet, Lyon, 1561. Scan via Internet Archive: one archive of 662 JPEG 2000 images at 600 dpi, about 5,400–5,750 × 8,000–8,200 pixels (`metadata/note.txt`). Image n shows printed page n − 77 on the pages looked at (image 90 is page 13).

Layout: two columns of 16th-century roman type on a large page, set very close. Each chapter opens with the plant's names in italic in several languages ("Caſsia. François, Cannelle: Arabes, Selicha…"), then "CHAP. XII.", then Dioscorides' text in a larger roman, then Mattioli's commentary in a smaller roman, which takes most of the page. Line numbers (10, 20 … 60) are printed in the gutter between the columns. Margin notes in small italic, on the outer edge (references such as "Galen. lib. 7. ſimpl. medic.", or a topic: "Mandegloires fabuleuſes."). Woodcuts of the plants, with italic captions, often with the text running in a narrow column beside them. Running head "DIOSCOR. LIVRE III." on rectos and "MATTHIOL. SVR" on versos, page number, signature and catchword at the foot.

What makes it hard: the two columns are close, and the gutter numbers bridge them; long s (ſ); letters with a stroke for a missing m or n (cõbien, plãte, rẽdent) and q̃ for "que"; words set very close together; italic in the headings and notes; page images six times larger in pixels than those of Mathée 1553, so each step is slow on the laptop.

## Sample pages

Pages named by their image in the archive (`img0090` is image 90, `FOL_S82_1INV121RES_0090.jp2`).

| Page | Printed page | Why |
|---|---|---|
| img0090 | 13 | Book 1, cassia and cinnamon: Dioscorides' text on both columns, two chapter headings, margin notes; uses (eye medicines, against viper bites, to tighten the womb) |
| img0175 | 98 | Book 1, myrtle, a verso (margin notes on the left): narrow column beside a woodcut, two woodcuts with captions, a long list of uses (leaves, juice, wine of the berries) |
| img0340 | 263 | Book 3, cumin, ammi and coriander: two woodcuts with the narrow column beside them, three chapter openings, uses (coriander with honey, raisins, ceruse) |
| img0430 | 353 | Book 4, mandrake: Dioscorides' text on the left (juice, wine, quantities: two oboles, three cyathes), Mattioli's commentary on the right |
| img0580 | 503 | Book 6, poisons: henbane and mandrake, remedies with many plant names (rue, wormwood, laurel, coriander, pennyroyal) |

All five carry uses of plants. Images taken from the archive unchanged with `tools/page_image.py`.

Main text, for the scores: the chapter headings with the names, "CHAP." lines, Dioscorides' text and Mattioli's commentary. Not measured, as for Mathée 1553: margin notes, woodcut captions and gutter line numbers (third block of the reference), running head, page number, signature and catchword.

## Models tried

The three models of every reading in this report: layout model, none; line finder, Kraken's general one, unless said otherwise; reading model, the one named in each row.

The same line finder and ten reading models as for Mathée 1553, pinned by DOI and checksum in `convert/ocr_models.csv`; the files were already in `models/` and were checked against the listed size and checksum without being fetched again. CATMuS Gothic Print was left out: the book is in roman and italic type.

Line finders compared on img0090, both read with PP-OCRv6 (small): the general one (in `ocr_models.csv`) and the Kraken segmentation model for two-column prints (`seg_news_1.0.mlmodel`, 5,250,514 bytes, md5 6f7e68e826a44e810320c389a263bf0d, https://doi.org/10.5281/zenodo.10783346). With the two-column one, 919 main-text words wrong out of 1,055 (87.1%), against 407 (38.6%) with the general one; it found 115 lines against 156 and took 204 s against 32 s to find them. The general one is kept. Neither keeps the reading order of this page (see "Lines").

## Scores

`uv run tools/ocr_score.py` against the five reference pages (drafts, see "Reference"), 5,965 main-text words. Two columns:
- **Kraken's order**: the readings as `tools/ocr_trial.py` writes them, the measure of the method.
- **Column order**: the same readings with their lines put back in column order from their positions on the page (`uv run tools/ocr_reorder.py <version> <model> <folder>`), to measure the reading apart from the order. A test of a possible fix, not part of the method.

| Reading | Words wrong, Kraken's order | Words wrong, column order | CER, column order |
|---|---|---|---|
| PP-OCRv6 (medium) | 3,348 (56.13%) | 389 (6.52%) | 7.15% |
| PP-OCRv6 (small) | 3,174 (53.21%) | 436 (7.31%) | 7.33% |
| CATMuS-Print [Large] | 3,252 (54.52%) | 552 (9.25%) | 11.30% |
| CATMuS-Print [Small] | 3,633 (60.91%) | 561 (9.40%) | 11.21% |
| CATMuS-Print [Tiny] | 3,300 (55.32%) | 590 (9.89%) | 11.30% |
| Gallicorpora+ | 3,631 (60.87%) | 603 (10.11%) | 8.01% |
| PP-OCRv6 (tiny) | 3,581 (60.03%) | 778 (13.04%) | 7.91% |
| McCATMuS | 4,098 (68.70%) | 1,037 (17.38%) | 12.13% |
| Latin Incunabula and Early Prints | 4,183 (70.13%) | 1,598 (26.79%) | 10.23% |
| A generalized model for English printed text | 6,053 (101.48%) | 6,053 (101.48%) | 96.49% |

In Kraken's order every model is above 53%: the reading order, not the reading, is what fails first on this book.

Where the wrong words of PP-OCRv6 (medium), column order, come from: the scorer lists 159 differences (a difference can count several words). Sorted by cause by a short script and by the assistant, from that list:
- 21 from the 13 lines drawn across the gutter (see "Lines"): each such line is a left-column line and a right-column line read as one, so its words turn up in the wrong place and count twice.
- 31 from running heads, margin notes and woodcut captions read among the lines of text or into them ("deco galen in ſuc ction", "Septẽ iudai lbr trion").
- 36 from a sign over a letter: the stroke for a missing m or n read as an accent or dropped (rẽdent → rédent, plãte → plate, Mãdra → madra, ſeruẽt → ſeruêt), and accents or diaereses dropped (cauſées → cauſees, queuë → queue, Ciguë → Cigue).
- About 19 from close-set words read as one (auec vin → auecuin, les racines → lesracines, vingt cinq → vingtcinq) or one word read as two (ce luy, cel le, dor mir, entais lent).
- About 8 from long s read as f (Fuchfius, pluſtoft, monftré, auffi, diffimuler).
- 5 from the italic chapter headings and the "CHAP." lines (Caßia for Caſsia, "iemy opignolz" for "Amey: Eſpaignolz", Cyrillic letters in "CHAP", XII for XIII).
- 1 word lost ("ſoy", damaged type).
- About 38 other misreadings of one or two letters (truict for fruict, uicil for vieil, zeſcorce for l'eſcorce, numeur for humeur, ſonnes for bonnes, geoitoires for genitoires).

## Wrong main-text words of the two best models

PP-OCRv6 (medium), column order, the differences that carry a record (plant, part, preparation, effect, quantity); the others do not (accents on common words, close-set "ce luy", author names, heading names in other languages):

| Page | Reference | Reading | Cause |
|---|---|---|---|
| img0090 | Caſsia (plant name, heading) | caßia | italic ſs read as ß |
| img0090 | (es emplaſtres remol)litifz (softening plasters) | litif | letter lost |
| img0175 | auec vin (pur) (with wine) | auecuin | close-set words |
| img0175 | (de) vin vieil (old wine) | uicil | misreading |
| img0175 | Meurtes (myrtles, plant name) | meur ces | misreading |
| img0175 | fruict (fruit, a part) | truict | misreading |
| img0175 | Tarẽte (myrtle of Tarentum, a kind of plant) | tarete | stroke lost |
| img0340 | fleur (flower, a part) | feur | misreading |
| img0340 | efface (meurtriſſures) (removes bruises) | efſace | misreading |
| img0340 | genitoires (the genitals, where it acts) | geoitoires | misreading |
| img0430 | l'eſcorce (the bark, a part) | zeſcorce | misreading |
| img0430 | les racines (the roots, a part) | lesracines | close-set words |
| img0430 | appaiſer (les douleurs) (to soothe pain) | a ppaiſer | one word read as two |
| img0430 | humeur (the juice taken from the root) | numeur | misreading |
| img0430 | Coleuurée (bryony, plant name) | coleuo urée | one word read as two |
| img0430 | plãte (plant) | plate | stroke lost |
| img0430 | Mãdra(gore) (mandrake, plant name) | madra | stroke lost |
| img0580 | aſſoupiſſement … Letargie (effect of mandrake) | moved into another line | line across the gutter |
| img0580 | aſſoupit les gens … (effect of mandrake) | moved into another line | line across the gutter |

19 differences carry a record. The plant names read right by PP-OCRv6 (medium) include Cannelle, Cinnamome, Malabathrum, Spica Nardi, Cardamomum, Meurte (36 times in the reading, 35 in the reference, the extra one from a caption), Grenadier, Oliues, Cumin, Ammi, Origan, Perſil, Coriandre, Feues, Ceruſe, Mandragore (15 times in both, singular and plural), Iuſquiame, Aluyne, Ruë, Laurier, Pouliot, Serpolet, Sarriette, Ellebore, Ranunculus, Piſtaches. The lines drawn across the gutter (13 in five pages) carry records too: their words are not lost but are set in the wrong place, next to the wrong plant.

PP-OCRv6 (small) makes most of the same errors, plus more long s read as f ("fimples", "fauoir", "fauuage", "plufieurs"), "pronoque" for prouoque, "cencantmoins" for ceneantmoins and more misread letters; among those that carry a record: fleur read "feur" twice, "ſauuage" read "fauuage", "efhace" for efface.

## Lines

Checked on all five pages for PP-OCRv6 (medium): the seg files compared with the readings and with the reference (`tools/ocr_disagree.py`, which matches lines whatever their order).
- **Out of order, Kraken's order: on every page.** The general line finder cuts each column into blocks and gives the blocks in an order that mixes the two columns: on img0090 the reading gives the top of the left column, then a block of the right column, then the rest of the left column, then the rest of the right. Margin notes are set among the lines of the nearest block. This is what puts every model above 53% wrong words.
- **Drawn across the gutter: 13 lines** (img0090 3, img0175 4, img0340 2, img0430 2, img0580 2): a left-column line and the right-column line level with it are read as one line, often where a gutter line number (10, 20 …) bridges the two columns. Counted from the line positions in the seg files.
- Lost: none, except one word: "ſoy" (img0175), whose type is damaged on the page.
- Cut in two: none seen outside the 13 lines across the gutter.
- The narrow column beside a woodcut is read in its place in column order, except on img0175, where two of its lines are joined across the gutter to lines of the right column.
- With the lines put back in column order (`tools/ocr_reorder.py`), the left column is read before the right one on every page, and the margin notes come last.

## Reference

Drafted by the assistant from the page images, each column cut in seven pieces to read the small type. Then the lines where the three best models (PP-OCRv6 medium and small, CATMuS-Print Large) read other words were listed (292 lines); the 126 where at least two of them agreed against the reference were looked at, and about 25 of these again on the line image (`work/ocr_trial/check/`). Six corrections of the draft: "où" (img0175, printed with an accent), "ſouueraines" and "Meurtés" (img0175, as printed), "chande" (img0340, a misprint for chaude, written as printed), "euacuë" (img0430, printed with a diaeresis), "nomme" (img0430, printed without accent). Points settled by choice, or not settled:
- Misprints written as printed: "aromarique" (img0090, for aromatique), "tapport" (img0090, for rapport), "Alexandxie", "le Aray Ammi", "l'Amers", "plns", "eu Egypte", "Apcthicaires", "chande" (img0340), "ſuruient" (img0340, perhaps for ſubuient).
- Damaged type written as the sense requires: "ſi deſſeche" (img0090, stain over ſi), "trop" (img0175), "ſoy" (img0175), "occaſion" (img0430, printed "occaiion").
- Signs that look like an accent over a vowel where the sense needs a missing n, written as the stroke: "odorãs" (img0090), "appellẽt", "rendẽt", "viẽ-nent" (img0175), "rẽdent" (img0430).
- "q̃" is written for the q with a sign of img0175 and img0430; whether the sign is ꝗ or q̃ was not settled on this type.
- Close-set words written as two, as the sense requires ("mais que", "groſſe eſcorce", "ce qu'on"), as for Mathée 1553.
- "remol / litifz" (img0090): printed without a hyphen at the end of the line, written as printed.
- "Caſsia": the italic ſs ligature, written ſs.
- Margin notes, captions and gutter numbers are in the third block, not measured; their transcription is close but not checked line by line.
No person has checked the references yet.

## Abbreviations

Checked on the five reference pages, main text (6,455 words counted by the assistant's own pattern, punctuation included; the scorer counts 5,965):
- 75 words with an abbreviation sign: 63 with a stroke over a vowel for a missing m or n (cõbien, cõme, plãte, Mãdragore, conuiẽt, ordõnez, quãtité), 12 with q̃ for "que". They are not spread evenly: 48 on img0430, 20 on img0175, 2 or 3 on the other pages: the compositor used them to fit Mattioli's longer commentary lines.
- The ampersand (&) for "et", 296 times; the scorer leaves it out, as punctuation.
PP-OCRv6 (medium) keeps the stroke in most of them, but loses it or reads it as an accent in about 19 (plãte → plate, Mãdra → madra, iurãt → iurat, ſeruẽt → ſeruêt, rẽdent → rédent). Whether to expand them is decided later.

## Speed

On the laptop (Intel Core Ultra 5 235U, no GPU), 8 threads, from the times of the files written by `tools/ocr_trial.py` (the CPU was partly shared with another Kraken run during finding the lines and the small model): finding the lines about 35 s per page; reading with PP-OCRv6 (small) about 70 s per page, PP-OCRv6 (medium) about 2 minutes per page. The 600 dpi images are about six times the pixels of those of Mathée 1553. The whole book (662 images) would take about 19 hours with PP-OCRv6 (small) and about 28 hours with PP-OCRv6 (medium) (assumed from these times).

## Proposal

**Not good enough by the threshold** with any ready-made model and line finder. In Kraken's order, more than half of the main-text words are wrong for every model, because the general line finder mixes the blocks of the two columns. Put back in column order, the best, PP-OCRv6 (medium), still has 389 main-text words wrong in 5,965 (6.52%), 19 of its differences carry a record, and 13 lines are drawn across the gutter.

Proposed, for the review of all reports (step 6 of the method):
- **Line finding first.** Reading order must be fixed before any reading model is judged on this book. Two ways, to compare: put the lines back in column order after the line finder, as `tools/ocr_reorder.py` does (it leaves the 13 lines across the gutter, and needs the margin notes recognised as such); or fine-tune the line finder, or use a layout model (YALTAi, DocLayout-YOLO, named in `docs/OCR_Kraken_approach.md`), on a few pages of this book, to find the two columns and the margin as separate regions. The lines across the gutter can only be cured by the line finder.
- **Model: PP-OCRv6 (medium)**, the fewest wrong words in column order, ahead of the small model mostly on long s.
- **Fine-tune it** on corrected pages of this book (on the GPU server, not on the sample pages): its errors are of the kinds a fine-tune learns (the stroke over vowels, close-set words, long s, the italic headings). As proposed for Mathée 1553, the same fine-tune may serve both books; Mathée's errors are mostly of the same kinds.
- **Image size**: reading the book on the laptop would take about a day; the GPU server is the place for it.
- Whether the gutter numbers, margin notes and captions stay out of the main text, as counted here, is to be confirmed.
