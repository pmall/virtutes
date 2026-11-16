# What remains to do

In order; the first item is next. Done items are removed (history is in `git log`).

On a fresh clone, `source/` holds only the libraries' small records: the typed texts and scans must be fetched again from `data/Downloads_report.csv` before a version can be converted (ask the user first).

1. **Convert Dioscorides** — `2_Dioscorides_original_Wellmann_1906-1914` (grc), skill `convert-version`. First real use of the text format (v0.1) and of `tools/vh_text.py`, both untested: expect to amend them, with the user's agreement.
   - First look, to verify: nested `div type="textpart"` (book, chapter, section); pages as `<pb n="228"/>` without volume; `<lb/>`, `<note>`, `<add>`, `<del>`, `<gap>`; one page marker out of order in volume 1.
2. **Convert Theophrastus** — `1_Theophrastus_original-english_Hort_1916`, Greek only (the English pages are a scan).
   - Same XML layout as Dioscorides; only even page numbers appear (Greek pages of a facing-page edition).
3. **Convert Pliny, Latin** — `3_Pliny_original_Mayhoff`.
   - Sections and paragraphs as `<milestone unit=…>`, two competing numberings; pages as `<pb xml:id="v.1.p.1"/>`; about 69,000 `<note>` holding variant readings (`apparatus`, not `note`).
4. **Convert Pliny, English** — `3_Pliny_english_Bostock-Riley_1855`.
   - `div1` book / `div2` chapter; pages as `<pb n="1001"/>` (probably volume 1, page 1); footnotes; named entities such as `&mdash;`.
5. **Decide how to read the eight scans** — engine and transcription rules; `docs/OCR_Kraken_approach.md` is a proposal, nothing is installed. Needs the user and the specialists.
6. **Convert the eight scans**, once 5 is decided.
7. **Define the steps after the text**: plant entries, translation, use records, classification (`docs/Project_context.md`, "The steps").

## Waiting for the user

- Put the typed XML sources (27 MB) in git, so that a clone can do items 1–4 without downloading?
