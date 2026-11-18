# Reading test — Mattioli, Italian, Discorsi 1568

The test of how well ready-made Kraken models read this scan, on sample pages, done with the skill `test-scan-reading` (method: `docs/OCR_Kraken_approach.md`). Everything below was checked on the files unless marked otherwise.

## The book

One thick folio volume in Italian, *I discorsi di M. Pietro Andrea Matthioli* on the six books of Dioscorides, Venice, Vincenzo Valgrisi, 1568. Scan of the Getty Research Institute copy via Internet Archive: one archive of 1,726 JPEG 2000 images, one page per image, about 1,885–2,375 × 3,000 pixels (`metadata/note.txt`). Image n shows printed page n − 181 on all the pages looked at (image 264 is page 83, image 1570 is page 1389).

Layout: **one column** of 16th-century type (not two columns, as `WIP.md` expected from Du Pinet 1561). Each chapter has a heading line ("Della Lattuca. Cap. CXXV."), then Dioscorides' text in a larger roman, then Mattioli's commentary in a smaller italic, which takes most of the page. Each opens with a drop capital two lines high, followed by spaced small capitals ("L A  L A T T V C A"). Margin notes in small roman on the outer edge ("Lattuca, & ſua eſſam.", "Nomi."), on the right of rectos and the left of versos; line numbers (10, 20 … 60) on the inner edge. Many plant chapters have a large woodcut, often a full page, with a title in spaced capitals above it. Running head "Nel primo lib. di Dioſcoride." with the page number on rectos, "Diſcorſi del Matthioli" on versos; signature and catchword at the foot. Each chapter of the commentary ends with the plant's names in Greek (in Greek type), Latin, Arabic, German, Spanish and French.

What makes it hard: the italic of the commentary is small and set close (many words run together in the readings); long s (ſ) and the italic ſs ligature (ß); the drop capitals; the margin notes close to the text; Greek words; the pages curve towards the binding, so lines bend at the inner edge.

## Sample pages

Pages named by their image in the archive (`img0264` is image 264, `gri_33125014246561_0264.jp2`).

| Page | Printed page | Why |
|---|---|---|
| img0264 | 83 | Book 1, castor oil and almond oil: Dioscorides in roman, commentary in italic, two chapter openings, margin notes on the right; uses (castor oil purges, almond oil for the womb, ears, kidneys, stones) |
| img0730 | 549 | Book 2, lettuce: names of cucumber and melon in six languages with Greek type, a Latin verse quotation, abbreviations; many uses (lettuce juice for sleep, eyes, burns, scorpion stings) |
| img0864 | 683 | Book 3, gentian and birthwort: dense italic commentary with four margin notes, Greek names; uses (gentian against fevers and worms, birthwort for childbirth and poisons) |
| img1535 | 1354 | Book 4, fern and polypody, a verso (margin notes on the left, line numbers on the right): uses with quantities (two obols, six scruples) |
| img1545 | 1364 | Book 4, a page mostly taken by a woodcut (heliotrope), with two lines of Dioscorides and the start of the commentary below it; uses (worms, warts) |
| img1570 | 1389 | Book 5, wines made from quince, pear, wild vine and pomegranate: six short chapter openings, recipes with quantities (twelve pounds in a metreta of must) and uses |

All six carry uses of plants. Images taken from the archive unchanged with `tools/page_image.py`. Image 562 (book 2) was first taken, then dropped once its text was seen to be about insects, not plants; image 730 replaced it. Book 6 (poisons) has no sample page.

Main text, for the scores: chapter headings, Dioscorides' text, Mattioli's commentary, the names, the Latin verse. Not measured, as for the other books: margin notes, line numbers and woodcut titles (third block of the reference), running head with page number, signature and catchword.

## Models tried

The same line finder and ten reading models as for Mathée 1553 and Du Pinet 1561, pinned by DOI and checksum in `convert/ocr_models.csv`; the files were already in `models/` and were checked against the listed size and checksum, nothing was downloaded. CATMuS Gothic Print was left out: the book is in roman and italic type. The two-column line finder was not tried: the pages have one column.

## Scores

`uv run tools/ocr_score.py` against the six reference pages (drafts, see "Reference"), 4,726 main-text words.

| Reading | Main-text words wrong | CER (whole page) |
|---|---|---|
| PP-OCRv6 (medium) | 353 (7.47%) | 6.48% |
| PP-OCRv6 (small) | 417 (8.82%) | 6.80% |
| CATMuS-Print [Large] | 473 (10.01%) | 10.38% |
| CATMuS-Print [Small] | 603 (12.76%) | 10.75% |
| Gallicorpora+ | 651 (13.77%) | 7.61% |
| CATMuS-Print [Tiny] | 667 (14.11%) | 11.19% |
| PP-OCRv6 (tiny) | 698 (14.77%) | 7.37% |
| Latin Incunabula and Early Prints | 1,124 (23.78%) | 9.44% |
| McCATMuS | 1,141 (24.14%) | 12.20% |
| A generalized model for English printed text | 4,845 (102.52%) | 95.59% |

Where the wrong words of PP-OCRv6 (medium) come from: the scorer lists 131 differences (a difference can count several words). Sorted by cause by the assistant, from that list:
- About 36 from margin notes read into the text lines (see "Lines"): the note's words are added in the middle of a sentence, often cutting a word in two ("mon gentiana etagne" for montagne, "pettim essam brosa" for Pettimbroſa).
- About 33 from words run together, nearly all in the small italic: an article or preposition joined to the next word ("iuermini" for i uermini, "iserpenti", "idolori", "conminore", "difuore", "mondificale").
- 8 lines read in part or not at all (see "Lines"), about 110 words.
- About 15 from the drop capitals: the first letter is lost or misread ("O olio" for LO olio, "l ssendo" for Eſſendo, "a latτ uca" for la lattuca) and the heading line above is sometimes misread ("Demolio" for Dell'olio, "ena Lattuca" for Della Lattuca).
- 6 from the Greek words (all wrong: "zíxns i μεροs" for Σίκυς ἥμερος).
- 1 from the italic ß ("notißsima"), which the scorer does not set aside as ſs (the same point as for Mathée 1553).
- About 30 other misreadings of one or two letters ("ſeeche" for ſecche, "diſecehi" for diſecchi, "fiemma" for flemma, "d'intrigidire" for d'infrigidire, "uano" for unto, "uaſsi" for Faſsi).

## Wrong main-text words of the two best models

PP-OCRv6 (medium), the differences that carry a record (plant, part, preparation, effect, quantity); the others do not (articles, accents, heading words, the names in other languages, the description of a plant's form):

| Page | Reference | Reading | Cause |
|---|---|---|---|
| img0264 | Meſſo ne gli impiaſtri, gli fa piu efficaci: & beuuto purga l'acqua (castor oil in plasters, drunk purges) | "Meno ne gu pg p puga raequa" | line read in part |
| img0264 | unto (anointed: how it is applied) | uano | misreading |
| img0264 | i dolori (pains) | idolori | words run together |
| img0730 | la lattuca (plant name, commentary opening) | a latτ uca | drop capital |
| img0730 | i fiori (flowers, a part) | ifiori | words run together |
| img0730 | i uenerei (calori) (venereal heat, an effect) | iuenerei | words run together |
| img0730 | medeſimo gioua parimente à gl'ardori (lettuce seed with poppy milk helps burning urine) | "memoim urbri" | line read in part |
| img0864 | d'aſſottigliare (to thin, an effect of gentian) | d'aſſottiglia gentiana re | margin note in the word |
| img0864 | i uermini (worms) | iuermini | words run together |
| img0864 | Pettimbroſa (plant name) | pettim eſſam broſa | margin note in the word |
| img0864 | Dell'Ariſtolochia (plant name, heading) | nomi ennariſtolochia | margin note and heading |
| img0864 | dactiliſite (a name of the long birthwort) | dactilite | misreading |
| img0864 | à i ſerpenti (against snakes) | iſerpenti | words run together |
| img0864 | mondifica le (gengiue) (cleans the gums) | mondificale | words run together |
| img1535 | ſecche (dried roots) | ſeeche | misreading |
| img1535 | diſecchi (dries ulcers) | diſecehi | misreading |
| img1535 | femina (the female fern, a kind) | feminomi na | margin note in the word |
| img1535 | La fillicola (plant name, commentary opening) | polipodio t afillicola | margin note and drop capital |
| img1535 | flemma (phlegm, what polypody purges) | fiemma | misreading |
| img1545 | i uermini (worms) | iuermini | words run together |
| img1545 | con ſale quelle uerruche (with salt, warts) | ee aele | line read in part |
| img1570 | ma-cera: chiarificaſi poſcia (macerate, then clear: preparation) | ma cera chiarificaſipoſcia | words run together |
| img1570 | Dell'Omphacomele (a preparation, heading) | mphacomele | misreading |
| img1570 | con tre (parti) (a quantity) | contre | words run together |
| img1570 | d'infrigidire (to cool, an effect) | d'intrigidire | misreading |
| img1570 | dell'interiora (fluxes of the bowels) | delpinteriora | misreading |
| img1570 | Gioua à gli ſtomachi debili, alla nauſea del cibo, à i fluſsi ſtomachali, & diſenterici (wild-vine wine) | "deſme anamamrea derelſo …" | line read in part |
| img1570 | uino (wine) | ui no | one word read as two |
| img1570 | me-lagrani, bol-lendo (pomegranates, boiling) | me uino di pomi lagrani, bol granati lendo | margin note in the word |
| img1570 | ſime, & maligne, & ſpegne la ſete; Beuuto con acqua di Piantagine, ò di portulaca, ò di roſe riſtagna gli ſputi del ſan-(gue) | lost | line lost |

30 differences carry a record. Words run together are the commonest kind: they would likely be split by a rule that knows the articles (i, à, la, di) and the plant words, but that is a proposal, not tested. The plant names read right by PP-OCRv6 (medium), counted in the reference and in the reading: lattuca and lattuga (11 and 11), mele cotogne (8 and 8), mandorle (13 and 13), ricino (10; 11 with a margin note), melagrani (6 and 6), felce (6 and 6), polipodio (13; 16 with the margin notes), gentiana (10; 12), ariſtolochia (3 and 3), clematite, papauero, Acetoſa, Indiuia, Bugloſſa; Piantagine and portulaca are lost with their line.

PP-OCRv6 (small) makes most of the same errors, plus more long s read as f ("diſtefi", "fu" for ſu, "Mefue"), more words run together ("mahapiu", "lunghezzadi", "laradice") and more letters misread ("bannto" for hauuto, "cost" for coſi); it reads the same eight lines in part or not at all.

## Lines

Checked on all six pages for PP-OCRv6 (medium): the seg files compared with the readings and with the reference.
- **Lost or read in part: 8 main-text lines** (img0264 1, img0730 1, img0864 2, img1545 2, img1570 2). The three best models garble the same lines in the same way, so the cause is the line finder, not the reading; the lines are cleanly printed on the image. Four are the last line of the page (img0730, img0864, img1545, img1570); on img1570 the line finder drew one line over two printed lines and the lower one ("ſime, & maligne … Piantagine … portulaca") is lost whole. Why the others are garbled was not settled: assumed to be the line's outline drawn by the line finder, where the page curves.
- **Margin notes read into text lines: 25 lines** (img0264 4, img0730 3, img0864 10, img1535 4, img1570 4): the line finder draws the text line on into the note beside it, so the note's words come at the end (rectos) or the start (versos) of the line, or in the middle of a word cut at the line's end. Counted from the line positions in the seg files.
- **Out of order**: the main-text lines are in order on every page. Margin notes not joined to a line are put among the text lines near them (img1535: five note lines in the middle of the commentary). The heading line of a chapter is read as two lines (title, then "Cap."), in order. "cioè", printed at the end of a verse line (img0730), is read at the end of the page.
- Cut in two: none, beside the headings.
- Drop capitals: on most of the 19 chapter openings of the sample, the first letter is lost or read as a separate mark.

## Reference

Drafted by the assistant from the page images, each page cut in seven or eight strips to read the small italic. Then the lines where the three best models (PP-OCRv6 medium and small, CATMuS-Print Large) read other words were listed (`tools/ocr_disagree.py`, 187 lines); the 92 lines where at least two of them agreed against the reference were looked at, and the 13 of these with a single disputed word were looked at again on the line image (`work/ocr_trial/check/`). Three corrections of the draft: "ſuffoli" (img0264, printed ff), "Beffaigi" and "Baumffarr" (img1535). The other lines, where the three models disagree among themselves, were not all opened. Points settled by choice, or not settled:
- Misprints written as printed: "can mele" (img1535, for con), "dactiliſite" (img0864), "Plypode" (img1535).
- Damaged or turned type written as the sense requires: "chiamano" (img1535, printed "chivmano"), "caccia" (img1545, the second c broken), "non" (img0864, last line).
- "Beffaigi", "Baumffarr" (img1535): ff or ſſ is hard to tell apart in this italic; written ff, not settled.
- The Greek words (περὶ σικύων, Σίκυς ἥμερος, Πέπων, Γεντιανή, Πτέρις, πτέριον, πολυπόδιον) are written with the accents the assistant read on small type; a reader of Greek should check them. They are names, not uses.
- The italic ſs ligature (ß) is written ſs, as for Du Pinet 1561 ("notiſsima", "roſsigno").
- The drop capital and the small capitals after it are written as one word in lower case ("LO olio", "Chiamasi", "La lattvca"); "E'" for the E with an accent mark after it.
- The heading and its "Cap." number are one line in the reference.
- Margin notes, line numbers and woodcut titles are in the third block, not measured; their transcription is close but not checked line by line.
No person has checked the references yet.

## Abbreviations

Checked on the six reference pages, main text (5,068 words counted by the assistant's own pattern; the scorer counts 4,726):
- 5 words with a stroke over a vowel for a missing m or n, all on img0730: Mãgiata, frequentemẽte, minutamẽte, tãto, cõ. PP-OCRv6 (medium) keeps the stroke in all five.
- About 14 words shortened with a full stop, all in references to books and chapters: Cap. and cap. (11), Plin., lib.
- No q̃ or other sign for "que".
- The ampersand (&) for "et", 246 times; the scorer leaves it out, as punctuation.
Far fewer than in Du Pinet 1561 (75 in five pages). Whether to expand them is decided later.

## Speed

On the laptop (Intel Core Ultra 5 235U, no GPU), 8 threads, from the times of the files written by `tools/ocr_trial.py`: finding the lines about 15 s per page; reading with PP-OCRv6 (small) about 20 s per page, PP-OCRv6 (medium) about 1 minute per page. The whole book (1,726 images, of which an unknown share are full-page woodcuts) would take about 17 hours with PP-OCRv6 (small) and about 36 hours with PP-OCRv6 (medium) (assumed from these times).

## Proposal

**Not good enough by the threshold** with any ready-made model. The best, PP-OCRv6 (medium), has 353 main-text words wrong in 4,726 (7.47%), 30 of its differences carry a record, and 8 main-text lines are lost or read in part.

Proposed, for the review of all reports (step 6 of the method):
- **Line finding first**, as for Du Pinet 1561 but for other reasons: here the reading order is right, but the line finder runs text lines into the margin notes (25 lines in six pages) and loses or garbles lines, the last line of the page most often (8 lines). To compare: fine-tune the line finder on a few pages of this book, or find the text block and the margin as separate regions with a layout model (YALTAi, DocLayout-YOLO, named in `docs/OCR_Kraken_approach.md`). Cutting each line at the edge of the text block would remove most of the margin-note words; that is not tested.
- **Model: PP-OCRv6 (medium)**, the fewest wrong words, ahead of the small model mostly on long s and words run together.
- **Fine-tune it** on corrected pages of this book (on the GPU server, not on the sample pages): most of its errors are words of the small italic run together, and the drop capitals, of the kinds a fine-tune learns. Whether one fine-tune can serve this book with Mathée 1553 and Du Pinet 1561 (roman and italic of the same years, but French and Italian) is a question for the review.
- **Greek names**: no model reads them; they are names, not uses, so they could be left as they are or marked for a specialist.
- Whether the woodcut titles and the margin notes stay out of the main text, as counted here, is to be confirmed. The margin notes name what each paragraph is about ("Virtù della Cruciata", "Nomi.") and could help to find the uses; they carry no use themselves on the sample pages.
