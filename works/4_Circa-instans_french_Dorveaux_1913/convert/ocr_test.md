# Reading test — *Circa instans*, French, Dorveaux 1913

The test of how well ready-made Kraken models read this scan, on sample pages, done with the skill `test-scan-reading` (method: `docs/OCR_Kraken_approach.md`). Everything below was checked on the files unless marked otherwise.

## The book

Paul Dorveaux's edition of *Le livre des simples médecines*, Paris, 1913: an Old French translation of the *Circa instans*, printed from one 13th-century manuscript. Wellcome Collection copy scanned by Internet Archive: 288 JPEG 2000 images of about 2,340 × 4,120 pixels (`source/b31364317_jp2.zip`). The Old French text fills images 0027 to 0218 (printed pages 1 to 192); before it the editor's preface, after it his glossary (two columns, images 0219 to 0278) and the list of authors. Only the Old French text is tested: the preface and the glossary are the editor's, not the source's, and carry no uses.

Layout of a text page: one column of modern roman type; the page number between dashes at the top (— 94 —); paragraphs numbered in bold, from 1 through the book; a heading in capitals for each simple (ACACIE, CASTORE); the editor's marks inside the text: the manuscript's folio, as "(Fol. 35 c)", and letters or words he added, in square brackets, often inside a word (es[t], eyg[u]e, d'un[e]); small raised note numbers; footnotes below, mostly the manuscript's readings where the editor corrected it. On some pages a printer's line at the foot ("Bull. Soc. fr. hist. méd., ..."); none on the sample pages.

The type is easy. What makes it hard: the Old French spelling (models trained on modern French may "correct" it), the square brackets inside words, and the raised note numbers, which sit close to the word before them.

## Sample pages

| Page | Image | Printed page | Why |
|---|---|---|---|
| img0030 | 30 | 4 | Early in the book; remedies of antimonium, chapter Acacie begins; three bracketed letters |
| img0076 | 76 | 50 | Chapters Cassielignee and Castore: preparations (boiled in oil, syrup with sugar), keeping time (.vij. anz) |
| img0120 | 120 | 94 | Chapters Galles, Galle muscate, Hermodaucles: preparations and effects; a line "Ici comencent li chapitres [de H]" |
| img0165 | 165 | 139 | Chapters Nitre, Nenuphar, Noiz muscates: many short remedies; note numbers on headings |
| img0207 | 207 | 181 | Chapters Siseleos, Soffre, end of a remedy; quantities (.iij. anz), roman numerals, many note numbers |

All five carry uses of plants or other simples. Images taken from the archive unchanged with `tools/page_image.py`.

## Models tried

One line finder (General segmentation model for print and handwriting) and nine reading models: the eight tried on Hort 1916 and Gallicorpora+, made for French prints of the 15th to 17th centuries. Each is pinned by DOI and checksum in `convert/ocr_models.csv`.

## Scores

`uv run tools/ocr_score.py` against the five reference pages (drafts, see "Reference"). The first column is the tool as it stands: a square bracket splits a word, so es[t] counts as two words "es" and "t". The second column takes the brackets out before comparing (es[t] counts as "est"), which is how the extraction should see the text; it was computed with a copy of the tool, not with the tool itself (see "Proposal").

| Reading | Main-text words wrong (tool, 1,361 words) | Main-text words wrong (brackets removed, 1,348 words) | CER (whole page) |
|---|---|---|---|
| PP-OCRv6 (medium) | 11 (0.81%) | 9 (0.67%) | 1.19% |
| PP-OCRv6 (small) | 18 (1.32%) | 15 (1.11%) | 1.42% |
| CATMuS-Print [Large] | 28 (2.06%) | 20 (1.48%) | 1.42% |
| CATMuS-Print [Small] | 28 (2.06%) | 38 (2.82%) | 1.84% |
| CATMuS-Print [Tiny] | 27 (1.98%) | 40 (2.97%) | 2.07% |
| PP-OCRv6 (tiny) | 47 (3.45%) | 42 (3.12%) | 1.51% |
| McCATMuS | 118 (8.67%) | 106 (7.86%) | 5.53% |
| Gallicorpora+ | 126 (9.26%) | 113 (8.38%) | 5.64% |
| A generalized model for English printed text (2019) | 1,627 (119.54%) | 1,613 (119.66%) | 82.25% |

Gallicorpora+ reads this 1913 type as an older one: f as s (long s), e as o, c as e ("sanc" as "sane", "et" as "el"). The English model drops every accent and splits words.

## Wrong main-text words of the two best models

Brackets removed (second column above). "Carries a record" means the word is a plant or simple, a part, a preparation, an effect or a quantity.

| Model | Page | Reference | Reading | Carries a record |
|---|---|---|---|---|
| PP-OCRv6 (medium) | img0030 | eyg[u]e (water, in "eygue rouse", rose water) | eyg[uje | **Yes**: an ingredient; the word is still guessable |
| PP-OCRv6 (medium) | img0030 | o (with) | 0 (a digit, so dropped) | No |
| PP-OCRv6 (medium) | img0120 | p[r]oz (good) | p[rjoz | No |
| PP-OCRv6 (medium) | img0120 | C'est | C est | No |
| PP-OCRv6 (medium) | img0165 | le | Ie | No |
| PP-OCRv6 (medium) | img0165 | color et | coloret | No (the colour of the flower) |
| PP-OCRv6 (medium) | img0207 | seches (dried, in "fies seches", dried figs) | sechés | **Yes**: a preparation; a brown speck over the e read as an accent; the word stays recognisable |
| PP-OCRv6 (small) | img0030 | eyg[u]e | eyg[ule | **Yes**: an ingredient |
| PP-OCRv6 (small) | img0076 | d'un[e] | d'unjel | No |
| PP-OCRv6 (small) | img0076 | afaitiez + note 4 | afaitiezt | No |
| PP-OCRv6 (small) | img0120 | C'est | Cest | No |
| PP-OCRv6 (small) | img0165 | chief et (head, in "pols del chief", head lice) | chiefet | **Yes**: the part of the body the remedy treats |
| PP-OCRv6 (small) | img0165 | le[e]s | le[els | No |
| PP-OCRv6 (small) | img0165 | color et | coloret | No |
| PP-OCRv6 (small) | img0207 | i + note 1 | il | No |
| PP-OCRv6 (small) | img0207 | n'en + note 4 | n'ent | No |
| PP-OCRv6 (small) | img0207 | SISELEOS + note 8 (chapter heading) | SISELEOSs | **Yes**: the name of the plant |
| PP-OCRv6 (small) | img0207 | seches | sechés | **Yes**: a preparation (as above) |
| PP-OCRv6 (small) | img0207 | es[t] | es[t] read with the bracket as a break, "es t" | No |

Most errors come from two things the edition adds to the text: the editor's square brackets, which the models read as j, l, i, ( or ), and the raised note numbers, which PP-OCRv6 (small) joins to the word before as a letter (4 as t, 1 as l, 8 as s). PP-OCRv6 (medium) keeps note numbers apart as digits, so the scorer leaves them out.

## Lines

Checked for PP-OCRv6 (medium) and (small) on all five pages, each main-text line of the reference matched with the reading:
- Lost: none in the main text.
- Cut in two: none in the main text.
- Out of order: none. Headings, paragraphs and notes come in page order.
- One extra empty line on img0030, among the footnotes: the line finder found something between two note lines; no text is missing.

## Reference

Drafted by the assistant from the images, then every line where one of the three best models (PP-OCRv6 medium and small, CATMuS-Print Tiny) read other words was looked at again on the line image (35 lines): no error found in the drafts. Points to note:
- img0120, "C'est une herbe": the apostrophe did not print (a gap with no mark); the reference keeps "C'est", the word the edition means.
- img0207, "fies seches": a brown speck above the e, not ink; the reference has "seches".
- Footnotes: the spacing and the dashes are close to the page, not exact; footnotes are not measured.
No person has checked the references yet.

## Abbreviations

No abbreviation signs: the editor expanded them. The main text keeps the roman numerals between points of the manuscript (.ij., .iij., .iiij., .vij.: 5 on the sample pages), all read right by PP-OCRv6 (medium). Other editorial marks in the main text of the sample pages: 14 square brackets and 7 folio marks "(Fol. ...)", the folio marks all read right by PP-OCRv6 (medium).

## Speed

On the laptop (Intel Core Ultra 5 235U, no GPU), 8 threads, one page (img0120), times including starting Kraken and loading the model: finding the lines 18 s; reading with PP-OCRv6 (small) 18 s, (medium) 40 s. The whole Old French text (192 pages) with PP-OCRv6 (medium): about 3 hours; with (small) about 2 hours (assumed from these times).

## Proposal

PP-OCRv6 (medium), the best reading: 0.67% of main-text words wrong with the brackets removed (0.81% as the tool counts), no main-text line lost. **Not good enough by the strict threshold**, which allows no wrong word that carries a record: two are wrong, "eyg[u]e" (an editor's bracket read as j) and "seches" (a speck read as an accent); both stay recognisable to a reader, but not to an exact name list.

To decide (step 6 of the method):
- **The editor's brackets.** Proposed: the scorer and the extraction take the brackets out of words (es[t] → est), as the second column does. A small correction after reading could also restore the shapes the models give a bracket inside a word ([uje, [ule, plr) → [u]); that would remove the first record word.
- **Specks read as accents.** The paper is spotted; a speck read as an accent (seches → sechés) may recur. When the whole book is read, the words found only once in the book, or not in the edition's glossary, would point to such cases (step 7 of the method).
- If neither is accepted, a short fine-tuning of PP-OCRv6 (medium) on a few corrected pages of this book, with brackets and note numbers in them.

PP-OCRv6 (small) is twice as fast but joins note numbers to words, which turned a plant name (SISELEOS) into another word; not proposed.
