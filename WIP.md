# What remains to do

In order; the first item is next. Done items are removed (history is in `git log`).

1. **Convert Pliny, Latin** — `3_Pliny_original_Mayhoff`.
   - Sections and paragraphs as `<milestone unit=…>`, two competing numberings; pages as `<pb xml:id="v.1.p.1"/>`; about 69,000 `<note>` holding variant readings (`apparatus`, not `note`).
2. **Convert Pliny, English** — `3_Pliny_english_Bostock-Riley_1855`.
   - `div1` book / `div2` chapter; pages as `<pb n="1001"/>` (probably volume 1, page 1); footnotes. Checked: the file does not parse as is with the standard library (undefined entity `&mdash;`); the three others do.
3. **Link the Theophrastus pages to the scan** — write `convert/images.py` of `1_Theophrastus_original-english_Hort_1916`.
   - Blocked: the scan `01_Theophraste_Hort_1916_grec-anglais.pdf` (md5 df3210d28e1a867f927caba43b3f478f) has no row in `works/Downloads_report.csv` (it was copied from the former pilot folder, not downloaded by our tools), so `require()` refuses it. Record it first.
   - Seen while checking the text: PDF page = printed page + 25 in volume 1; in volume 2, + 509 at the start (page 4) but + 513 by page 78 (page 88 checked by eye on PDF 601); assumed: four extra images somewhere between, not located.
4. **Decide how to read the eight scans** — engine and transcription rules; `docs/OCR_Kraken_approach.md` is a proposal, nothing is installed. Needs the user and the specialists.
5. **Convert the eight scans**, once 4 is decided.
6. **Define the steps after the text**: plant entries, translation, use records, classification (`docs/Project_context.md`, "The steps").
