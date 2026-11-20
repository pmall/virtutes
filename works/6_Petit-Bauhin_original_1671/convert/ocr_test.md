# Reading test — Petit Bauhin, *Histoire des plantes de l'Europe*, Lyon 1671

The test of how well ready-made Kraken models read this scan, on sample pages, done with the skill `test-scan-reading` (method: `docs/OCR_Kraken_approach.md`). Everything below was checked on the files unless marked otherwise.

## The book

Two small volumes (duodecimo), in French, Bayerische Staatsbibliothek copy: one archive of JPEG images per volume, about 970 × 1,815 pixels, 1,016 images in all (`metadata/note.txt`).

Layout of a plant entry: under the running head ("248 HISTOIRE DES PLANTES," with the page number), a line giving Gaspard Bauhin's Latin name ("G. Bauh. Ammi paruum foliis fœniculi."). Then a woodcut of the plant on the right and, to its left, a narrow column: the Latin name in capitals, the authors who describe it (abbreviated: "Matth. Ang. Lac."), the plant's names in French, Italian, Spanish and German (each after a label: "Fr.", "It.", "Eſp.", "All."), and its qualities ("QVALITEZ, ch. & ſeche": hot and dry). Then the text, in one column of 17th-century roman type with words in italic, in three paragraphs: "DESCR." (description), "LIEV." (where it grows), "PROPR." (properties: the uses). Some pages carry only text, the end of an entry, and a printer's ornament. A new section opens with a heading and a list of its plants.

What makes it hard: long s (ſ), letters with a tilde for a missing m or n (inflãmations, ſurgeõs), u and n hard to tell apart in the italic, ink blots and worn letters, headings in spaced capitals ("P R O P R."), and on some pages the inner edge of the text lost in the binding (see "Lines").

## Sample pages

Pages named by volume and image number in that volume's archive (`v2_img0200` is image 200 of volume 2, `bsb10300969_jpg.zip`).

| Page | Archive | Printed page | Why |
|---|---|---|---|
| v1_img0060 | bsb10300968_jpg.zip | 8 | Volume 1, early; Ægilops: a remedy (juice with honey, the herb pounded with flour against lachrymal fistulas); three words with a tilde |
| v1_img0300 | bsb10300968_jpg.zip | 248 | Ammi: a dose (one drachm of the powdered seed in wine, every other day, against sterility); a full names column |
| v1_img0400 | bsb10300968_jpg.zip | 348 | A page of text only (violet), many uses and quantities (3 or 4 spoonfuls of syrup, 2 drachms of powder), then an ornament |
| v2_img0060 | bsb10300969_jpg.zip | 494 | Volume 2; the opening of a section (heading and list of plants) and vervain with uses and quantities; the inner edge of the text runs into the binding |
| v2_img0200 | bsb10300969_jpg.zip | 634 | Aparine (cleavers): distilled water against dysentery and jaundice, leaves on wounds; the edge of the next page shows on the right |
| v2_img0300 | bsb10300969_jpg.zip | 734 | Sorb tree: uses of the fruit and its decoction; show-through from the back of the leaf |

All six carry uses of plants. Images taken from the archives unchanged with `tools/page_image.py` (which now also takes this library's image names, `0060.jpg`).

Main text, for the scores: everything but the running head with its page number: the Bauhin line, the names column, the qualities, the section heading and the three paragraphs. The names column and the qualities are counted because they carry plant names in five languages, which the extraction needs to identify the plant (a proposal: Poinsinet and the others have no such column). The library's stamps in the margin of v1_img0300 are left out. There are no notes.

## Models tried

The three models of every reading in this report: layout model, none; line finder, Kraken's general one, unless said otherwise; reading model, the one named in each row.

The same line finder and nine reading models as for Poinsinet 1771–1782, plus Latin Incunabula and Early Prints (made for print up to the 16th century, the closest to this book of the models already in `models/`); all pinned by DOI and checksum in `convert/ocr_models.csv`. CATMuS Gothic Print was left out: the book is in roman type. The files were already in `models/` and were checked against the listed size and checksum without being fetched again. The pages are in one column, so the two-column line finder was not tried.

## Scores

`uv run tools/ocr_score.py` against the six reference pages (drafts, see "Reference"), 947 main-text words.

| Reading | Main-text words wrong | CER (whole page) |
|---|---|---|
| PP-OCRv6 (medium) | 33 (3.48%) | 3.11% |
| Gallicorpora+ | 44 (4.65%) | 2.45% |
| PP-OCRv6 (small) | 47 (4.96%) | 2.39% |
| CATMuS-Print [Large] | 48 (5.07%) | 4.95% |
| CATMuS-Print [Small] | 59 (6.23%) | 5.50% |
| CATMuS-Print [Tiny] | 62 (6.55%) | 5.76% |
| PP-OCRv6 (tiny) | 103 (10.88%) | 3.15% |
| McCATMuS | 135 (14.26%) | 6.46% |
| Latin Incunabula and Early Prints | 308 (32.52%) | 6.94% |
| A generalized model for English printed text | 965 (101.90%) | 91.06% |

Where the 33 wrong words of PP-OCRv6 (medium) come from (from the list below):
- 8 on the inner edge of v2_img0060, where letters are lost in the binding of this copy: every model misses them.
- 4 from a diaeresis left out (feuïlles read feuilles, menuë read menue). The scorer sets aside long s, u/v and i/j but not the diaeresis, which changes no word for the extraction either.
- 4 from a heading in spaced capitals read as two words ("DE SCR.", "PR OPR.") or two words run together.
- 4 from one line out of order, counted once where it is missing and once where it is added.
- 4 from two words run together (la tige, a speck between fleurs and blanches).
- 9 misreadings, 3 of them under an ink blot or on a worn letter.

The scorer counts a word split in two or two words joined as 2. Page by page: 3, 13, 1, 10, 2 and 4 wrong (v1_img0300 carries the line out of order; v2_img0060 the binding).

Set aside the diaeresis and the binding, and it is about 21 in 947 (2.2%); assumed, from the list, not computed by the scorer.

## Wrong main-text words of the two best models

PP-OCRv6 (medium):

| Page | Reference | Reading | Carries a record |
|---|---|---|---|
| v1_img0060 | Ital, (label of the Italian name) | Inal (a blot on the t) | No: the name after it, Egilopa, is right |
| v1_img0060 | la tige (the juice "of the stem") | latige (the two words almost touch on the page) | **Yes**: a part of the plant |
| v1_img0300 | Cæſ. (an author's name, worn) | Caſ. | No |
| v1_img0300 | Allem. Ammey. | read after the qualities, not lost | No (order only) |
| v1_img0300 | au 3. D. (dry "in the 3rd degree") | au z. D. | **Yes**: the degree of a quality |
| v1_img0300 | feuïlles, menuë | feuilles, menue | No (diaeresis) |
| v1_img0300 | fleurs blanches | fleurs'blanches (a speck between the words) | No: the scorer counts it as one word; the extraction would see both |
| v1_img0300 | PROPR. | PR OPR. | No, but the extraction may look for this heading |
| v1_img0300 | prendre (an ink blot over the r) | prendrs | No |
| v1_img0400 | cuiëllerées (spoonfuls) | cuiellerées | No (diaeresis) |
| v2_img0060 | Eiſenkraut (German name of vervain) | Eiſenxraut | **Yes**: a plant name |
| v2_img0060 | quelques-fois, au-tre, tige, coudée, feüilles, à | quelques fois, au tre, tig, coudé, feüille, (missing) | tige: **yes** (a part), the others no; all on the edge lost in the binding |
| v2_img0060 | Iuin (distilled "in June") | luin | No: when the water is made, not what it does |
| v2_img0200 | ſiue ("or") | ſine (u and n alike in the italic) | No |
| v2_img0200 | feüilles | feuilles | No (diaeresis) |
| v2_img0300 | o ("Sorbolero o Sorboles") | (missing) | No |
| v2_img0300 | DESCR. | DE SCR. | No |
| v2_img0300 | preſque | prefque | No |

Gallicorpora+ makes most of the same errors (latige, the order on v1_img0300, the binding edge, ſine) and others of its own, 3 of them in plant names of the names column (Klebkraut read RlebEraut, Eiſenkraut read Ei enxraut, hirſutis read birſuris in Bauhin's Latin name); it reads the 3 right but loses a tilde (oſtãt read oſtat). It writes the diaeresis as printed, which PP-OCRv6 (medium) does not.

Every plant name of the main paragraphs (Coquiole, Ægilops, Ammi, violette, Aparine, Lentilles, Sorbes, Neffles, Sorbier, Freſne...) is read right by PP-OCRv6 (medium). Its errors that carry a record are in the names column and the qualities (Eiſenkraut, 3), and in "tige" twice: once from two words run together, once from the binding.

## Lines

Checked for PP-OCRv6 (medium) and Gallicorpora+ on all six pages: each main-text line of the reference matched with the reading.
- Lost: none.
- Cut in two: none.
- Out of order: one. On v1_img0300 the line "Allem. Ammey." of the names column is read after the three lines of qualities, not before; still above the text. The names column itself is read before the text on every page, the woodcut gives no lines, and the ornament of v1_img0400 gives none either.
- v2_img0060: the right edge of the text runs into the binding of this copy; the last letters of 9 lines are lost or half visible (tige, au-, coudée, feüilles, à, &, chaſteaux, bon-, elle, L'eau, le, épanche-). The line finder keeps the lines whole; what is lost is on the image. The test does not say how many pages of the book are like this (the contact sheet of 12 pages made to choose the sample showed one).
- Two empty lines in the reading of v2_img0060 (the rules under the running head), outside the main text.

## Reference

Drafted by the assistant from the images, then every line where one of the three best models (PP-OCRv6 medium, Gallicorpora+, PP-OCRv6 small) read other words was looked at again on the line image (48 lines). Four errors of the draft corrected: "ondurcies" and "iettte" are as printed (misprints of the book, read right by the models), "Scabieuſe" and "Caruleo" are as printed (the draft had "Scabienſe" and "Cæruleo"). Points not settled, or settled by choice:
- Words under an ink blot or worn, kept as the sense requires: "Ital" (v1_img0060), "prendre" (v1_img0300), "Cæſ." (v1_img0300, an author's abbreviation; the æ is not clear).
- "ſiue" (v2_img0200): the italic u looks like n; kept as the sense requires.
- The edge lost in the binding (v2_img0060): the reference has the whole words, as the sense and the half-letters give them, and the line-end hyphens that are not visible.
- "la tige" (v1_img0060): the space between the two words is very narrow; the reference keeps two words.
- "PROPR." on v2_img0300 where the sense needs "LIEV." (a misprint of the book): kept as printed.
No person has checked the references yet.

## Abbreviations

Checked on the six reference pages, main text:
- 6 words with a tilde for a missing m or n: inflãmations, grãd, l'ẽpeſcher, oſtãt (v1_img0060), ſurgeõs, perſõnes (v1_img0300). PP-OCRv6 (medium) reads all six with their tilde.
- About 74 words cut short with a full stop (counted by pattern, then by eye): the paragraph headings (DESCR., LIEV., PROPR.), the authors (Matth., Ang., Lac., Lugd., Dod., Lob.), the language labels (Fr., Franç., It., Ital., Eſp., All., Allem., Apoth.) and the qualities (ch., fr., ſech., gr., D. for "degré").
- The ampersand (&) for "et", 52 times; the scorer leaves it out, as punctuation.
The cut-short words are a closed list that could be expanded by a table; whether to expand them is decided later.

## Speed

On the laptop (Intel Core Ultra 5 235U, no GPU), 8 threads, one page (v1_img0400), times including starting Kraken and loading the model: finding the lines 18 s; reading with PP-OCRv6 (medium) 24 s, Gallicorpora+ 14 s, PP-OCRv6 (small) 15 s. The whole book (1,016 images, front matter and index included) would take about 12 hours with PP-OCRv6 (medium) and about 9 hours with Gallicorpora+ (assumed from these times).

## Proposal

**Not good enough by the threshold** with any ready-made model. The best, PP-OCRv6 (medium), has 33 main-text words wrong in 947 (3.48%), about 2.2% once the diaeresis and the binding are set aside, and 4 of its wrong words carry a record (Eiſenkraut, a quality degree, "tige" twice). No main-text line is lost; one is out of order within the names column.

Proposed, for the review of all reports (step 6 of the method):
- **Model: PP-OCRv6 (medium)**, the fewest wrong words, every plant name of the paragraphs right, the tildes kept. Gallicorpora+ is second and faster, but loses more plant names in the names column.
- **Fine-tune it** on corrected pages of this book (on the GPU server, not on the sample pages). Its errors are of the kinds a fine-tune learns: the italic k and u/n, spaced capitals, the old-style 3, words set close together.
- **Set the diaeresis aside in the scorer**, like long s (a change to `tools/ocr_score.py`, to decide): it changes no word for the extraction, and it accounts for 4 of the 33.
- **The binding**: count the pages whose edge is lost (step 7 of the method: lines whose last word is found nowhere else in the book). If they are many, look for another copy of the 1671 edition for those pages; no model can read what the scan does not show.
- Whether the names column and the qualities are main text, as counted here, is to be confirmed.
