# Reading test — *Circa instans*, Latin, Venice 1497

The test of how well ready-made Kraken models read this scan, on sample pages, done with the skill `test-scan-reading` (method: `docs/OCR_Kraken_approach.md`). Everything below was checked on the files unless marked otherwise.

## The book

The *Circa instans* (*Liber de simplici medicina* "secundum Platearium") in a folio volume of medical works printed at Venice by Bonetus Locatellus for Octavianus Scotus, 16 December 1497. Scan of the Bayerische Staatsbibliothek copy: one archive of 52 JPEG images, leaves 186r to 211v only, one page per image, about 3,410–3,560 × 5,080 pixels (`metadata/note.txt`). Image n shows leaf 186 + (n − 375) / 2 rounded down, a recto for odd n and a verso for even n, on all the pages looked at (image 378 is leaf 187v, image 425 is leaf 211r).

Layout: **two columns** of gothic type (rotunda), 66 lines each. Each chapter opens with a heading line ("¶ De apio.") with its number in roman figures at the right of the column ("VIII."); then the name of the simple in large gothic type, as high as two lines, with the text running on beside it ("Apium omne.ca.eſt in p̄ncipio.3.gra.…"). A paragraph sign (¶) opens each use. At the start of each letter of the alphabet, a numbered table of that letter's chapters, and the first chapter opens with a woodcut initial. Running head "Platearius" on versos, "De ſimplici medicina" with the leaf number on rectos; signature at the foot of some rectos. No printed margin notes; this copy has a few handwritten ones in red (leaf 207r).

What makes it hard: the **abbreviations**, far more than in any other book of the project: about one main-text word in four carries an abbreviation sign, and "et" is the tironian sign ⁊ throughout (see "Abbreviations"); gothic letter forms that look alike (b and h, G and H, q with a stroke and g, c and t, the ij ligature and y); the two columns set close, with headings, roman numbers and the large chapter names at their edges.

## Sample pages

Pages named by their image in the archive (`img0378` is image 378, `0378.jpg`).

| Page | Leaf | Why |
|---|---|---|
| img0378 | 187v | A: alum, celery (*apium*), starch (*amidum*), antimony, acacia; many recipes with quantities (syrup of celery juice with ℥ and ʒ), uses against dropsy, jaundice, epilepsy, haemorrhoids |
| img0392 | 194v | C: saffron, hemlock, cyperus, sweet flag, coral; hemlock ointment for the spleen, cyperus against strangury, coral against nosebleed |
| img0404 | 200v | L: laudanum, liquorice, lapis lazuli, lily, *licium*, mercury, *lingua avis*; the line finder keeps the columns apart on this page |
| img0417 | 207r | P and R: raisins, pistachios, lead, *polium*, pitch, then rose (water, honey, sugar, syrup, oil of roses): a recto with leaf number, the table of the letter R, a woodcut initial, four handwritten notes in red in the margin |
| img0425 | 211r | T to Z: cobweb, mullein, tartar, turpentine, *tetrahit*, violet, glass, shepherd's purse, ginger, sugar: two tables and two woodcut initials |

All five carry uses of plants. Images taken from the archive unchanged with `tools/page_image.py`. Images 416 (206v) and 424 (210v) were first taken, then replaced by 417 and 425 so that two of the five are rectos (running head and leaf number differ); their readings were set aside and are not scored.

Main text, for the scores: everything in the two columns, chapter headings with their roman numbers, the large chapter names, and the tables of chapters. Not measured, as for the other books: running head with leaf number, signature, the handwritten notes (third block of the reference).

## Models tried

The three models of every reading in this report: layout model, none; line finder, Kraken's general one, unless said otherwise; reading model, the one named in each row.

Twelve reading models, pinned by DOI and checksum in `convert/ocr_models.csv`: the ten tried on Mattioli 1568, plus CATMuS Gothic Print, made for gothic print; the Latin Incunabula and Early Prints model was already among the ten. All files were already in `models/`; their sizes and checksums were checked against the list, nothing was downloaded.

Line finding: the general model of Mattioli 1568. The two-column line finder (`seg_news_1.0.mlmodel`, downloaded for this test, `WIP.md`) was compared with it on img0378: it found 84 lines instead of 143, most of them drawn across both columns, and took 3 minutes 15 seconds instead of 31 seconds. The general model was kept; the two-column one is not in `ocr_models.csv`.

## Scores

`uv run tools/ocr_score.py` against the five reference pages (drafts, see "Reference"), 5,071 main-text words. Two columns, as for Du Pinet 1561:
- **Kraken's order**: the readings as `tools/ocr_trial.py` writes them, the measure of the method.
- **Column order**: the same readings with their lines put back in column order (`uv run tools/ocr_reorder.py <version> <model> <folder>`), to measure the reading apart from the order. A test of a possible fix, not part of the method.

| Reading | Words wrong, Kraken's order | Words wrong, column order | CER, column order |
|---|---|---|---|
| Latin Incunabula and Early Prints | 1,622 (31.99%) | 733 (14.45%) | 9.34% |
| PP-OCRv6 (small) | 1,927 (38.00%) | 894 (17.63%) | 9.33% |
| PP-OCRv6 (medium) | 1,978 (39.01%) | 925 (18.24%) | 10.31% |
| PP-OCRv6 (tiny) | 2,116 (41.73%) | 1,086 (21.42%) | 9.88% |
| CATMuS Gothic Print | 3,220 (63.50%) | 2,495 (49.20%) | 18.90% |
| Gallicorpora+ | 3,659 (72.16%) | 2,952 (58.21%) | 16.83% |
| CATMuS-Print [Large] | 3,700 (72.96%) | 2,979 (58.75%) | 20.26% |
| CATMuS-Print [Tiny] | 4,125 (81.34%) | 3,223 (63.56%) | 22.38% |
| CATMuS-Print [Small] | 3,985 (78.58%) | 3,349 (66.04%) | 21.96% |
| McCATMuS | 4,348 (85.74%) | 3,699 (72.94%) | 24.49% |
| A generalized model for English printed text | 5,129 (101.14%) | 5,116 (100.89%) | 94.40% |

The models that read best are those trained on early print with MUFI abbreviation signs (Latin Incunabula, the PP-OCRv6 family); CATMuS Gothic Print, made for this type, is far behind (49% in column order): it writes the abbreviation stroke as a tilde and reads u and v as y in many words ("yel", "yalet" for vel, valet).

Where the 733 wrong words of Latin Incunabula and Early Prints come from, in column order: the scorer lists 345 differences (a difference can count several words). Sorted with a script that compares each pair with the abbreviation signs and the spaces taken out (the script is not kept):
- 97 differences (194 words): **a word cut at the end of a line not joined again**, because the model misses the small slanted hyphen of this type about half the time (31 of 66 on img0378: "ſu det", "fricen tur", "her ba").
- 81 differences (112 words): **an abbreviation sign written otherwise** than in the reference, sometimes with a split as well: the bar of ħ, đ and ƀ dropped ("qd" for qđ, "h" for ħ), a stroke over i where the reference has none ("īunge", "Deīde", see "Reference"), ꝑ for p.
- 82 differences (177 words): other differences in one or a few words. About 30 of them (counted by the assistant from the list) are **words of a chapter opening inserted in a line**: the large chapter name and the short line beside it are read as separate lines and put back in the wrong place ("conſtrin tela aranea gendi", "ultrama piſtacee ca ſunt rinis"). The rest are letters misread ("alumidis" for aluminis, "cumore" for tumore, "ficca" for ſicca, "capacium" for Lapacium).
- 62 differences (92 words): a word missing or added, mostly the roman chapter numbers and the chapter names moved.
- 23 differences (158 words): main-text lines lost, garbled or out of place (see "Lines").

## Wrong main-text words of the two best models

Latin Incunabula and Early Prints, column order: the differences that carry a record (plant, part, preparation, effect, quantity). The others do not (abbreviation signs written otherwise, words cut at the line end, roman chapter numbers, words of description).

| Page | Reference | Reading | Cause |
|---|---|---|---|
| img0378 | alumi-nis (alum, in a mouth wash) | alumidis | misreading |
| img0378 | latur.virtutē habꝫ diureticam.¶ Succus apij in quo d̄- (celery is diuretic; celery juice…) | out of place | line finder |
| img0378 | ueris reubarbari.℥.ſ.⁊ mane cum cal̓a exhibeatur (half an ounce of rhubarb, given with warm water) | garbled | line finder |
| img0378 | ctum emplaſtrū dolorē iteſtinorum mitigat (the plaster soothes pains of the bowels) | garbled | line finder |
| img0378 | fluētem (blood flowing from the mouth: what alum stops) | fiuētem | misreading |
| img0378 | ſplenis (spleen) | ſple uis | misreading |
| img0378 | tumore (tumour of haemorrhoids) | cumore | misreading |
| img0378 | Amidum, Antimonium, Acacia (chapter names) | out of place | chapter opening |
| img0378 | prunellorū īmaturorum (acacia is the juice of unripe sloes) | out of place | line finder |
| img0392 | Cicuta, Ciperus, Calamus, Corallus (chapter names) | out of place or lost | chapter opening |
| img0392 | tellis ouoruꝫ.⁊ bombix itinctus oculis ſupponat̄ (saffron with egg yolk, on cotton, laid on the eyes) | garbled | line finder |
| img0392 | valet predictū cataplaſma … cōtra ſtranguriā (the plaster helps strangury) | garbled | line finder |
| img0392 | diſſuriam (dysuria) | diſtiriam | misreading |
| img0392 | vrinam (urine) | vrioam | misreading |
| img0392 | bñ triti (well ground: preparation) | ti | misreading |
| img0392 | limfetur (wine mixed with the decoction) | limrētur | misreading |
| img0392 | coralli (coral) | coral ui | misreading |
| img0404 | Liquiricia, Lingua auis, Lapacium, Linochites (chapter names) | ciquiricia, gracingua, capacium, cinochites | chapter opening |
| img0404 | tota interius crocea eſt … non pul- (how to choose liquorice) | lost | line finder |
| img0404 | in primo gradu; in tertio gradu (degree of the quality) | out of place, garbled | chapter opening |
| img0404 | ſarcocolla (a simple) | ſarcocoila | misreading |
| img0417 | Piſtacee, Plumbum, Polium, Pix (chapter names) | out of place or lost | chapter opening |
| img0417 | hūectādi (moistening, a virtue) | hūecādi | misreading |
| img0417 | ſplenis ⁊ rñū (spleen and kidneys) | ſpleuis ī nū | misreading |
| img0417 | picis naualis:dū coꝗtur naualis pix liꝗda remanet (how liquid pitch is made) | garbled | line finder |
| img0417 | Roſa fri.eſt ī prio ḡdu (rose, cold in the first degree) | out of place | chapter opening |
| img0417 | cuꝫ exp̄mūt ⁊ ide faciūt ſirupū (rose syrup from pressed juice) | garbled | line finder |
| img0425 | Tela aranea, Tapſus barbaſſus, Tartarum, Terebentina, Viola, Virga paſtoris, Zinziber, Zuccara (chapter names) | out of place | chapter opening |
| img0425 | ſicca (dry: the dry plant is worth little) | ficca | misreading |
| img0425 | electuario (an electuary) | eletmuario | misreading |
| img0425 | Zuccarum viol̓.ſic fit vt roſatum (sugar of violets) | zucconm viotitſitutroſatum | line garbled |

About 30 differences carry a record, without counting the chapter names one by one; the most serious are the chapter names, since the name of the simple at the head of the chapter is what every record of the chapter is about. Read in their own line, apart from the order, most chapter names are right ("Tela aranea", "Tapſus barbaſſus", "Zinziber"); four are misread at their first letter, the large initial (L read as c in Liquiricia, Lapacium, Linochites).

PP-OCRv6 (small) makes nearly the same errors on the chapter openings and the lost lines (the same line finder), more errors with words cut at the line end (129 differences against 97) and with abbreviation signs (142 against 81: it mixes tilde and macron, "cõmunis", "decoctiõis"), and about as many misread letters (90 other differences against 82).

## Lines

Checked on all five pages, with a script that looks for each reference line in each reading (a line counted lost when less than half of it is found in any line of the reading) and from the positions in the seg files.
- **Lost or garbled: 16 main-text lines** for Latin Incunabula (img0378 2, img0392 4, img0404 3, img0417 5, img0425 2), and the same lines for PP-OCRv6 small and medium (19 and 16); the lines are cleanly printed, so the cause is the line finder. Most are lines beside a large chapter name or a woodcut initial.
- **Lines drawn across both columns: 5** (img0378 4, img0392 1): the line finder joins a line of the left column to the line beside it in the right one ("… ⁊ multum valet. ¶ Apiū riſus in vino …").
- **Out of order**: in Kraken's order, the lines of the two columns are mixed on two pages of five: img0378 (13 runs of lines alternating between the columns) and img0392 (6 runs), as on Du Pinet 1561; on the other three the left column comes before the right one, but for a few lines of the chapter openings and the running head. This takes the best model from 14% to 32% of words wrong. The chapter openings stay out of order even in column order (see "Scores").
- Cut in two: the chapter openings (large name, then the short line beside it, read as separate lines).

## Reference

Drafted by the assistant from the page images, each column cut in six or seven strips. Then the lines where the three best models (Latin Incunabula, PP-OCRv6 small and medium) read other words were listed (`tools/ocr_disagree.py`, 373 lines); the 147 where at least two of them agreed on another word were listed by a script, and a dozen of these, chosen as examples of each kind, were looked at again on the line image (`work/ocr_trial/check/`). Corrections of the draft, settled on the image and by the sense:
- Letters taken for others in this type: "Gumi" (gum, img0425, twice), first written "Humi"; "liꝗda", "coꝗtur" (liquida, coquitur, img0417), first written "ligda", "cogtur"; "vn̄.G." (Galen, img0378), first written "H."
- Strokes over i missed in the draft, where the sense needs them: "medicīs", "medicīe" (medicinis, medicine), "frīduꝫ", "frīditate" (frigid-); "ꝗa" and "ẜm" (quia, secundum), first written with other signs.
- The ij ligature, which looks like y, first written y and then ij ("apij", "lilij", "licij", "Alij", "iij"); the true y of Greek words is kept ("ydropicis", "emorroydas").
- The general abbreviation stroke is written as a macron (ā ē ī ō ū q̄ t̄), as the models trained on early print write it and as it looks in this type (a straight bar); the stroke through the top of l (cal̓a, viol̓, dol̓) as a combining comma above the l, as these models write it.

Points settled by choice, or not settled:
- About 130 of the 147 lines were not opened: most of them differ by an abbreviation sign or a stroke over i ("Deīde", "īunge", "īterius", "coīs", "frīda"); the reference keeps what the assistant read on the strips. A person should settle whether these strokes are printed.
- ħ, đ and ƀ (hoc, quod, -b-) are written with their bar, as printed; the models write h, d, b.
- b or h: "ĩnbibet" (img0378, the models read "inhibet", which the sense prefers), "Tetrabit" (img0425, the models read "Tetrahit", which the assistant believes is the usual form of this name: not checked); written as the assistant read them, not settled.
- Misprints written as printed: "candem" read as "eandem" (img0404, not settled), "Cōntra", "manerici", "radieē", "ſophicant", "medicis" (medicinis, with its stroke).
- The large chapter name is written at the start of the first line of the chapter, in reading order; a woodcut initial is written as the first letter of the word ("Roſa", "Viola", "Zinziber").
- The roman chapter numbers and the tables of chapters are main text (the extraction will have to skip them; they carry no use).
- The handwritten notes of img0417 (third block) are transcribed roughly; not measured.
No person has checked the references yet; a reader of medieval Latin abbreviations should.

## Abbreviations

Counted on the five reference pages, main text (5,000 words by the assistant's own pattern; the scorer counts 5,071):
- **1,288 words with an abbreviation sign (26%)**, not spread evenly: img0417 464, img0392 364, img0378 231, img0404 129, img0425 100.
- 992 of them with a stroke over a letter for missing letters: Cōtra and cōtra (47), cū (31), nō (17), aūt (15), aq̄ (14), etiā (13), autē, virtutē, decoctiōis; and the stroke on l (viol̓, cal̓a, dol̓).
- 296 with another sign: ꝫ for -m, -et, -ue (cuꝫ, habꝫ, quouſqꝫ, vſqꝫ), ꝰ for -us (meliꝰ, ſirupꝰ), ꝝ for -rum (zuccaꝝ, roſaꝝ), ꝙ (quod), qđ (quod), ħ (hoc), ꝑ and ꝓ (per, pro), ꝯ (con-, and ꝯ̄ for contra), ẜm (secundum), ꝗa (quia).
- The tironian sign ⁊ for "et", 436 times; the scorer leaves it out, as punctuation.
- Abbreviated plant names: "ro." (roſa, roſarum), "viol̓." (viola), "anti." (antimonium), "liquir.", "ſcariol̓." (ſcariola), "maſtic̄." (maſtix), "tapſi barƀ." (tapſus barbaſſus), "mirobal̓." (mirobalani).
Far more than in any other book of the project (Du Pinet 1561: 75 words in five pages; Mattioli 1568: about 19). The best model keeps most signs, but writes some otherwise (see "Scores"). Whether to expand them is decided later; for this book an extraction cannot work on the abbreviated text as it is: one word in four, and many plant names, would not be recognised.

## Speed

On the laptop (Intel Core Ultra 5 235U, no GPU; assumed the same machine as for the other reports), 8 threads, from the times of the files written by `tools/ocr_trial.py`: finding the lines about 22 s per page; reading with Latin Incunabula and Early Prints about 24 s per page, PP-OCRv6 (small) about 38 s, PP-OCRv6 (medium) about 100 s. The whole *Circa instans* (52 images) would take about 40 minutes with the Latin Incunabula model (assumed from these times).

## Proposal

**Not good enough by the threshold** with any ready-made model. The best, Latin Incunabula and Early Prints, has 1,622 main-text words wrong in 5,071 in Kraken's order (31.99%), 733 (14.45%) with the lines put back in column order; about 30 of its differences carry a record, 16 main-text lines are lost or garbled, and the chapter names are out of place.

Proposed, for the review of all reports (step 6 of the method):
- **Line finding and order first**, as for Du Pinet 1561 and Mattioli 1568: the columns are mixed on two pages of five, lines are drawn across the gutter, and the chapter openings (large name, short line beside it, woodcut initial, roman number) are split and misplaced. To compare: fine-tune the line finder on a few pages of this book, or a layout model (YALTAi, DocLayout-YOLO) that finds the columns and the chapter openings as regions. The book is short (52 pages): correcting the lines of every page by hand, with a tool such as eScriptorium, is also possible (assumed: not tried).
- **Model: Latin Incunabula and Early Prints**, the fewest wrong words, the most faithful to the abbreviation signs, and the fastest of the good ones.
- **Fine-tune it** on corrected pages of this book (not the sample pages): its letter errors are few, but it misses the slanted line-end hyphen about half the time, and it drops the bar of ħ, đ, ƀ. Joining a word cut at the line end could also be done after the reading, when the two halves make a known word (proposal, not tested).
- **Abbreviations**: this book is where the decision matters most. With one word in four abbreviated, the use records can only be taken from an expanded text. To compare: expand with a list of the abbreviations of this book (a few hundred forms; most recur: cōtra, cū, aq̄, ꝙ, qđ, ħ), or with a model trained to expand (assumed to exist for medieval Latin; not checked), or by a person for the plant names only. A reader of medieval Latin abbreviations is needed to check the expansions.
- Whether the scorer should set aside a stroke written as tilde or macron, and a combining mark inside a word (it now cuts the word in two), is to be decided with the other books; this report wrote the reference in the models' own notation instead (see "Reference").
