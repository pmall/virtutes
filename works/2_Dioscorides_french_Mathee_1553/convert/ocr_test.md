# Reading test — Dioscorides, French, Mathée 1553

The test of how well ready-made Kraken models read this scan, on sample pages, done with the skill `test-scan-reading` (method: `docs/OCR_Kraken_approach.md`). Everything below was checked on the files unless marked otherwise.

## The book

One folio volume in French, *Les six livres de Pedacion Dioscoride*, translated by Martin Mathée, printed by Balthazar Arnoullet, 1553 (the colophon says Vienne). University of Toronto copy, via Internet Archive: one archive of 438 JPEG 2000 images, about 2,100 × 3,155 pixels (`metadata/note.txt`). The library's record says "page 24-295 is cut on bottom half"; on the 18 pages looked at to choose the sample (images 20 to 430, most of them in that range) no page is cut, so that remark was not confirmed.

Layout: two columns of 16th-century roman type, with a running head ("28 LE PREMIER LIVRE"; on some pages only the page number) and a catchword at the foot. Each chapter has a heading giving the plant's names ("De la Paſſefleur, que les Grecs, & Latins, & Italiens, appellent Anemone."), "CHAP. CLXIX.", Dioscorides' text in roman, then most chapters have Mathée's "ANNOTATIONS." in italic, in the same column. Chapters open with a drop capital two lines high. Many pages carry woodcuts of the plants, with an italic caption under each ("Crenouillette. 1. eſpece."); the text then runs in a narrow column beside the woodcut. The last part of the book (images 410 on) is Mathée's own description of simples not in Dioscorides, with italic headings.

What makes it hard: long s (ſ); letters with a stroke for a missing m or n (dãs, cõme, viẽnent) and the abbreviations ꝗ (que), q̃ (que), ꝑ (par); the italic of the annotations, with its ligatures (ct, ſs) and the ampersand written like "&" in a different shape; drop capitals; words set very close together; woodcut captions level with lines of text; on some pages broken or poorly inked type.

## Sample pages

Pages named by their image in the archive (`img0090` is image 90, `lessixlivresdepe00dios_0090.jp2`).

| Page | Printed page | Why |
|---|---|---|
| img0040 | 28 | Book 1, medicinal oils and ointments: recipes with quantities (five pounds of fenugreek in nine pounds of oil for seven days) and uses; three chapter openings, two annotations |
| img0090 | 78 | Book 1, the fig: a page of plant uses only, many preparations (fig with wax, with vinegar, with honey), roman type only |
| img0180 | 166 | Book 2, three woodcuts with captions and a narrow column beside them; anemone, its uses (juice up the nose, leaves cooked in barley water for milk) |
| img0270 | 254 | Book 4, alkanet, lycopsis and viper's bugloss: two long annotations in italic, two woodcuts with the narrow column |
| img0360 | 344 | Book 5, ceruse (white lead) and chrysocolla: a mineral, not a plant, taken as a page of book 5 with a long annotation at the top; recipes and uses still the same kind of text |
| img0410 | 394 | Mathée's supplement (cassia, rose of Jericho, sandalwood, musk): italic headings, short entries; broken type on the right column |

Five of the six carry uses of plants. Images taken from the archive unchanged with `tools/page_image.py`.

Main text, for the scores: the chapter headings and names, "CHAP." lines, "ANNOTATIONS." headings, Dioscorides' text and Mathée's annotations. The annotations are counted as main text because they carry uses and preparations of their own (img0040: how quince oil is made today; a proposal, as for Poinsinet's notes, to confirm). The woodcut captions are not counted: they only name the plant drawn, which the chapter heading names too; they are written in the third block of the reference, which is not measured (a choice, to confirm). Running head and catchword are not measured.

## Models tried

The same line finder and ten reading models as for Petit Bauhin 1671, pinned by DOI and checksum in `convert/ocr_models.csv`; the files were already in `models/` and were checked against the listed size and checksum without being fetched again. CATMuS Gothic Print was left out: the book is in roman and italic type.

Line finders compared on img0040 and img0090, both read with PP-OCRv6 (small): the general one (in `ocr_models.csv`) and the Kraken segmentation model for two-column prints (`seg_news_1.0.mlmodel`, 5,250,514 bytes, md5 6f7e68e826a44e810320c389a263bf0d, https://doi.org/10.5281/zenodo.10783346). With the two-column one, 128 main-text words wrong out of 1,428 (8.96%), against 43 (3.01%) with the general one; it cut lines at the start ("plique aux vlceres" for "quand on l'applique aux vlceres"). The general one is kept. It keeps the two columns apart on all six pages: no line crosses the gutter.

## Scores

`uv run tools/ocr_score.py` against the six reference pages (drafts, see "Reference"), 3,741 main-text words.

| Reading | Main-text words wrong | CER (whole page) |
|---|---|---|
| PP-OCRv6 (medium) | 94 (2.51%) | 2.82% |
| PP-OCRv6 (small) | 141 (3.77%) | 2.93% |
| CATMuS-Print [Large] | 162 (4.33%) | 6.41% |
| CATMuS-Print [Small] | 180 (4.81%) | 6.37% |
| Gallicorpora+ | 180 (4.81%) | 3.10% |
| CATMuS-Print [Tiny] | 226 (6.04%) | 6.62% |
| PP-OCRv6 (tiny) | 396 (10.59%) | 3.52% |
| McCATMuS | 427 (11.41%) | 6.87% |
| Latin Incunabula and Early Prints | 829 (22.16%) | 6.05% |
| A generalized model for English printed text | 3,785 (101.18%) | 96.51% |

Where the wrong words of PP-OCRv6 (medium) come from: the scorer lists 66 differences (a difference can count 1 or 2 words). Sorted by cause, from that list:
- 25 from the drop capitals. The big initial is not read with its line: "LOn prend" is read "On prend" (lon becomes on), "LA Ceruſe" is read "A Ceruſe" (la becomes a), and the L turns up at the start of the next line ("Lmenie", "Dainſi", "uinlaigre", "colgnue"). Every model does this.
- 14 from words set close together, read as one ("lamatrice", "laſecõdine", "ſeptiours", "Ilayde") or one word read as two ("tres bonne", "la rges").
- 9 on the broken type of img0410 (right column, lines 62 to 72): letters that are missing or deformed on the page ("doleu", "Sanal", "emplaſte", "medeciies", "lat" for "bat-tement"). The reference has the words as the sense requires (see "Reference").
- 4 from woodcut captions read inside lines of text (see "Lines").
- 3 from the italic ſs ligature read as ß ("außi", "dißemblable", "puißsant"): the scorer sets aside long s but not ß, which changes no word for the extraction either.
- 3 from a sign over a letter: a diaeresis left out (Auroëſne), a stroke read as an accent (principalemét for principalemẽt), a stroke lost (blache for blãche).
- 7 misreadings: Orchanette (l'Orchanette read "Porchanette"), ſiege read "fiege", excalfactif read "excalfaclif", liſle read "lifle", Matthioli read "Mathioli", teſfois read "tesſois", l' read "i'".
- 1 from the scorer: "Mace-" at the foot of a column followed by the catchword "doni"; the reading joins them, the reference has the catchword in its own block.

Set aside the drop capitals, the broken type, the captions, the ß and the scorer, and about 24 differences remain in 3,741 words, under 1%; assumed, from the list, not computed by the scorer.

## Wrong main-text words of the two best models

PP-OCRv6 (medium), the differences that carry a record (plant, part, preparation, effect, quantity); the other 50 do not (lon/on, la/a, de, qui, author names, spacing in words like "tres bonne", the ß):

| Page | Reference | Reading | Cause |
|---|---|---|---|
| img0040 | (par) ſept iours (macerated "for seven days") | ſeptiours | close-set words |
| img0040 | (enfleures du) ſiege (swellings of the anus) | fiege | long s read as f |
| img0040 | (provokes) la ſecõdine (the afterbirth) | laſecõdine | close-set words |
| img0040 | (aux) ſuffocatiõs (de la matrice) | auxſuf-focatiõs | close-set words |
| img0040 | (de) la matrice (the womb) | lamatrice | close-set words |
| img0180 | (effacent toutes les) taches (skin spots) | "ta Grenouillette. 1. eſpece. ches" | caption read into the line |
| img0270 | l'Orchanette (alkanet, a plant name) | Porchanette | italic l' read as P |
| img0360 | uinaigre (vinegar, a preparation) | uinlaigre | drop capital |
| img0360 | excalfactif (heating, a quality) | excalfaclif | italic ct ligature |
| img0410 | (pour la) doleur (de la teſte) | doleu | broken type |
| img0410 | l'eſtomac | l'eſtmac | broken type |
| img0410 | emplaſtre (a plaster) | emplaſte | broken type |
| img0410 | (pour le) cõforter (to strengthen) | ceiforter | broken type |
| img0410 | Sandal (sandalwood, a plant name) | Sanal | broken type |
| img0410 | conforte le (coeur) | conforteile | broken type |
| img0410 | (le) battement (du cœur) | lat-tement | broken type |

16 differences carry a record: 7 on the broken type of one column, 4 from close-set words, 3 misreadings, 1 drop capital, 1 caption. Plant names read right by PP-OCRv6 (medium) include Coings, Vigne ſauuage, Senegré, Calamus odoratus, Cyperus, Cardamomon, Mariolaine, Serpollet, Siſymbriõ, figues, Grenades, Grenouillette, Paſſefleur, Lycopſis, Anchuſa, Bugloſſe, Herbe à bouc, Ceruſe, Caſſe, Reubarbe, Amandes, Reigalice, Morelle, Ioubarbe, Pourpier. Two plant names are wrong: Orchanette once (of five times on its page) and Sandal once (of four).

PP-OCRv6 (small) makes most of the same errors; 51 of its 95 differences are not in the list of the medium model, among them long s read as f in five words (ſauuage, ſante, Ceruſa, Pſimmithion, Lycopſis read "fauuage", "fante", "Cerufa", "Pfim", "Lycopfis"), "Sampſucus" (a plant name) lost under the drop capital T, "aſtrictiue" (astringent) read "aſtrietiue", "lieux" read "licux", and more close-set words read as one ("tigeeſt", "racineeſt", "Orgeau"). Of these, Lycopſis, Sampſucus and aſtrictiue carry a record.

## Lines

Checked for PP-OCRv6 (medium) and (small) on all six pages: each main-text line of the reference matched with the reading, then the matches compared with the page images.
- Lost: none.
- Cut in two: none.
- Out of order: none. The left column is read before the right one on every page; the narrow column beside a woodcut is read in its place.
- Woodcut captions: read where they stand, among the lines of the narrow column; on img0180 the caption "Crenouillette. 1. eſpece." is on the same level as the line "ches, elles arra-" and the two are read as one line, which breaks the word "taches". The captions add 4 differences to the score and none is lost.
- Drop capitals: read as a separate letter at the start of the next line, or lost (see "Scores").
- Empty lines in the reading: 1 on img0180, 1 on img0270, 2 on img0410, none of them a main-text line (rules and blank space).

## Reference

Drafted by the assistant from the page images, cut in halves and quarters to read the small italic; then every line where one of the three best models (PP-OCRv6 medium, PP-OCRv6 small, CATMuS-Print Large) read other words was looked at again on the line image (127 lines). Four corrections of the draft: "qui vent au" (img0410: the page has vent, a misprint for vont, read right by the models), "liſle" (img0410: printed without apostrophe), "puiſsant" and "diſsemblable" (img0360: the italic ſs ligature, not two long s). Points settled by choice, or not settled:
- Broken type (img0410, right column, lines 62 to 72): the reference has the words the sense requires (meſlez, doleur, &, l'eſto-, emplaſtre, cõ-, Sandal, conforte le, medecines, bat-). The page shows letters missing or deformed; no model can read what the page does not show.
- Drop capitals are written with their line ("LOn prend", "LA Ceruſe"), as printed.
- Close-set words (ha vertu, la ſecõdine, la matrice, qui viennẽt, qui en) are written as two words, as the sense requires; "tresbonne" is written as one word, as printed.
- "Auroëſne" (img0040): the sign over the o and e may be a diaeresis or a broken letter; not settled.
- "principalemẽt" (img0360): the sign over the e looks like an acute accent; written as the stroke for a missing n, as the sense requires.
- "rement" (img0360, first line): the first letter is damaged; the word is the end of one begun on the page before, not checked.
- "Ae-ce" (img0270, Aetius) and "Mat-thioli" written as printed.
- The catchword "doni" (img0360) completes "Mace-" on the last line; it is written in the page-number block like the other catchwords (the next page begins "donique", checked).
No person has checked the references yet.

## Abbreviations

Checked on the six reference pages, main text (3,935 words counted by the assistant's own pattern):
- 103 words with an abbreviation sign: 94 with a stroke over a vowel for a missing m or n (dãs, cõme, viẽnent, Nitrũ, beſoĩg, Siſymbriõ), 8 with ꝗ or q̃ for "que", 1 with ꝑ for "par" (ꝑce que). They are not spread evenly: 35 on img0040, 4 on img0270, where the narrow columns and the italic use more of them.
- The ampersand (&) for "et", 194 times; the scorer leaves it out, as punctuation.
PP-OCRv6 (medium) keeps the stroke over the vowel except in three words of its list of errors (blache, principalemét, colgnue) and reads ꝗ, q̃ and ꝑ as printed; CATMuS-Print often drops the stroke (das, commece, effacet). Whether to expand them is decided later.

## Speed

On the laptop (Intel Core Ultra 5 235U, no GPU), 8 threads, one page (img0090), times including starting Kraken and loading the model: finding the lines 25 s; reading with PP-OCRv6 (medium) 69 s, PP-OCRv6 (small) 30 s. The whole book (438 images, front matter and index included) would take about 11 hours with PP-OCRv6 (medium) and about 7 hours with PP-OCRv6 (small) (assumed from these times).

## Proposal

**Not good enough by the threshold** with any ready-made model. The best, PP-OCRv6 (medium), has 94 main-text words wrong in 3,741 (2.51%), and 16 of its differences carry a record, 7 of them on one column of broken type. No main-text line is lost or out of order, and the two columns are kept apart by the general line finder.

Proposed, for the review of all reports (step 6 of the method):
- **Model: PP-OCRv6 (medium)**, the fewest wrong words, long s read right where the small model reads f, the abbreviation signs kept.
- **Fine-tune it** on corrected pages of this book (on the GPU server, not on the sample pages). Its errors are of the kinds a fine-tune learns: close-set words, the italic l' and ct, and the drop capitals; the same fine-tune may serve Du Pinet 1561, printed in Lyon eight years later (to see when that book is tested).
- **Drop capitals**: if the fine-tune does not cure them, a rule in `extract_fr.py` could put back a lone capital found at the start of the line after a chapter heading; to decide.
- **Set ß aside in the scorer** as ſs, like long s (a change to `tools/ocr_score.py`, to decide with the diaeresis proposed for Petit Bauhin).
- **Broken type**: the test does not say how many pages are like img0410 (one column of six pages). Step 7 of the method (lines with words found nowhere else in the book) should find them; another copy of the 1553 edition, or the 1559 printing, could be compared for those pages.
- Whether the annotations are main text and the captions are not, as counted here, is to be confirmed.
