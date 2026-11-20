# Reading test — Theophrastus, Hort 1916, English pages

The test of how well ready-made Kraken models read this scan, on sample pages, done with the skill `test-scan-reading` (method: `docs/OCR_Kraken_approach.md`). Everything below was checked on the files unless marked otherwise.

## The book

Loeb edition, 1916, two volumes in one PDF of 1,014 pages (`source/Theophrastus_Enquiry_Plants_Loeb.pdf`). Greek on the left-hand pages, English translation on the right-hand pages; only the English pages are read here (the Greek is typed, from First1KGreek). Pages stored as black-and-white images at 600 dpi, about 2,500 × 3,780 pixels.

Layout of an English page: one column of modern roman type; a running head with the book and chapter numbers in small capitals; italic side headings inside the text; small raised note numbers; footnotes below, mostly variant readings of the Greek, with Greek words and Latin quotations; the page number at the foot. The difficulty is low for the type; the footnotes, with their Greek and their small print, are the hard part.

The PDF also carries an invisible text layer made by automatic reading (Internet Archive), scored below as one more reading.

## Sample pages

| Page | PDF page | Printed page | Why |
|---|---|---|---|
| pdf0056 | 56 | vol. 1, p. 31 | Book I, general description of plants; early in volume 1 |
| pdf0226 | 226 | vol. 1, p. 201 | Book III, galls of the oak; long footnotes with Greek and Latin |
| pdf0400 | 400 | vol. 1, p. 375 | Book IV, the reed of Lake Copais; place names |
| pdf0760 | 760 | vol. 2, p. 247 | Book IX, balsam and aromatic plants; an italic side heading |
| pdf0800 | 800 | vol. 2, p. 287 | Book IX, medicinal roots: uses of plants (purging, amulet), quantities in years |

Page images taken out of the PDF unchanged with `pdfimages -png`.

## Models tried

The three models of every reading in this report: layout model, none; line finder, Kraken's general one, unless said otherwise; reading model, the one named in each row.

One line finder (General segmentation model for print and handwriting) and eight reading models; each pinned by DOI and checksum in `convert/ocr_models.csv`.

## Scores

`uv run tools/ocr_score.py` against the five reference pages (drafts, see "Reference"). Main-text words: 1,377.

| Reading | Main-text words wrong | CER (whole page) |
|---|---|---|
| PP-OCRv6 (medium) | 1 (0.07%) | 2.73% |
| PP-OCRv6 (small) | 2 (0.15%) | 2.14% |
| PP-OCRv6 (tiny) | 9 (0.65%) | 3.29% |
| CATMuS-Print [Large] | 9 (0.65%) | 4.18% |
| PDF text layer (Internet Archive) | 12 (0.87%) | 4.05% |
| CATMuS-Print [Small] | 17 (1.23%) | 3.84% |
| CATMuS-Print [Tiny] | 19 (1.38%) | 4.13% |
| McCATMuS | 67 (4.87%) | 6.17% |
| A generalized model for English printed text (2019) | 693 (50.33%) | 30.39% |

The whole-page character error rate is higher than the main-text rate because of the footnotes: the models read Greek letters as Latin ones (σομφώδης as "gouoóòns") and misread small note numbers.

## Wrong main-text words of the two best models

| Model | Page | Reference | Reading | Carries a record |
|---|---|---|---|---|
| PP-OCRv6 (medium) | pdf0800 | years | vears | No (a quantity of years, but "vears" is read as "years" by any reader; the number "thirty" around it is right) |
| PP-OCRv6 (small) | pdf0760 | (note number 5) | o | No |
| PP-OCRv6 (small) | pdf0800 | lamp 11 | lampil | No |

## Lines

- Lost: one footnote line on pdf0800 ("9 A manufactured drug. cf. 9. 9. 4."): the line finder found it but could not draw its outline (warning "Polygonizer failed"), so every model read it as empty. No main-text line was lost on the five pages.
- Cut in two: two short footnote lines (pdf0226 "eius pilulas. 5 ἢ ins. St.", pdf0760 "4 Plin. 12. 104 and 105. 5 cf. C.P. 6. 18. 2."); both pieces are read, the second one placed after the rest of the notes.
- Out of order: none in the main text.

## Reference

Drafted by the assistant from the images, then every line where one of the three best models read other words was looked at again on a zoomed image (62 lines): no error found in the drafts. Not settled, all in the footnotes:
- pdf0056, note 6: the accent of τούτοις is printed over the ο (τόυτοις); the reference has the correct form τούτοις.
- pdf0760, note 3: "UMP₂Ald.", a low mark after P read as a subscript 2 (a manuscript siglum); the models read a comma.
- pdf0760: the note number after "motive" looks like an 8 on the image; written 3 because the notes of the page are 3, 4, 5.
No person has checked the references yet.

## Abbreviations

None in the main text beyond ordinary ones (cf., i.e.); not relevant for this book.

## Speed

On the laptop's CPU (no GPU), 8 threads: finding the lines about 11 s a page; reading with PP-OCRv6 (small) about 10 s a page, (medium) about 35 s. All English pages (about 500) with PP-OCRv6 (small): about 3 hours (assumed from these times).

## Reproducibility

Run twice, the second time from scratch with `tools/ocr_trial.py`: the readings of all eight models were identical, file for file.

## Proposal

PP-OCRv6 (small). Good enough by the proposed threshold: under 1 main-text word in 100 wrong (0.15%), none carrying a record, no main-text line lost. It is about three times faster than PP-OCRv6 (medium) for the same result on the main text. The footnotes are read badly where they hold Greek; they are variant readings of the Greek and carry no uses, so this does not matter for extraction. When the whole book is read, look for lines lost by the line finder (empty lines), since one footnote line was lost on five pages.
