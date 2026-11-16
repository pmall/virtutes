# What remains to do

In order; the first item is next. Done items are removed (history is in `git log`).

1. **Repair Dioscorides** — `2_Dioscorides_original_Wellmann_1906-1914` (grc), skill `convert-version` from step 4. `extract.py` is written; `repair.py` has no rule yet, so `text/` is still the raw text. The mistakes to repair are listed at the end of `extract.py`.
2. **Convert Theophrastus** — `1_Theophrastus_original-english_Hort_1916`, Greek only (the English pages are a scan).
   - Same XML layout as Dioscorides; only even page numbers appear (Greek pages of a facing-page edition).
3. **Convert Pliny, Latin** — `3_Pliny_original_Mayhoff`.
   - Sections and paragraphs as `<milestone unit=…>`, two competing numberings; pages as `<pb xml:id="v.1.p.1"/>`; about 69,000 `<note>` holding variant readings (`apparatus`, not `note`).
4. **Convert Pliny, English** — `3_Pliny_english_Bostock-Riley_1855`.
   - `div1` book / `div2` chapter; pages as `<pb n="1001"/>` (probably volume 1, page 1); footnotes. Checked: the file does not parse as is with the standard library (undefined entity `&mdash;`); the three others do.
5. **Decide how to read the eight scans** — engine and transcription rules; `docs/OCR_Kraken_approach.md` is a proposal, nothing is installed. Needs the user and the specialists.
6. **Convert the eight scans**, once 5 is decided.
7. **Define the steps after the text**: plant entries, translation, use records, classification (`docs/Project_context.md`, "The steps").
