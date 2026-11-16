# Work in progress

Rewritten at each session; not a history (see `git log`). Rules for this file: `AGENTS.md`.

## Where the work stands

- Six pilot works: versions mapped, chosen, downloaded and checked (11 version folders).
- Unified text format v0.1 and its checker are written but **not yet tried on a real text**. The checker was tested only on a four-line sample.
- No version converted. No `convert/`, `work/` or `text/` folder exists yet.

## Next

Convert the four typed texts, one per session, following `instructions/convert_version.md`. Suggested order, simplest first:

1. `2_Dioscorides_original_Wellmann_1906-1914` (grc)
2. `1_Theophrastus_original-english_Hort_1916` (grc only; the English pages are a scan)
3. `3_Pliny_original_Mayhoff` (lat)
4. `3_Pliny_english_Bostock-Riley_1855` (eng)

The first conversion is also the test of the format and of the checker: expect to amend both, with the user's agreement.

## Hints from a first look at the four XML files (to verify; they belong in each `convert.py` once written)

- Dioscorides and Theophrastus (First1KGreek): nested `div type="textpart"` for book, chapter, section; pages as `<pb n="228"/>` with the printed number and no volume; `<lb/>`, `<note>`, `<add>`, `<del>`, `<gap>`. Theophrastus shows only even page numbers (the Greek pages of a facing-page edition). Dioscorides volume 1 has a page marker out of order (84 after 89, per its note.txt).
- Pliny Latin (Perseus): `div type="textpart"`; sections and paragraphs as `<milestone unit="section|paragraph" n=…/>`, two competing numberings; pages as `<pb xml:id="v.1.p.1"/>`; about 69,000 `<note>` holding the variant readings (so `apparatus`, not `note`); about 228,000 `<hi>`.
- Pliny English (Perseus): older layout, `div1 type="book"` / `div2 type="chapter"`; pages as `<pb n="1001"/>` (probably volume 1, page 1); footnotes as `<note anchored="yes" place="foot">`; named entities such as `&mdash;`.

## Open questions for the user

- Should the typed XML sources (27 MB in all) be in git, so that a clone can rebuild the texts without downloading?
- Reading engine and transcription rules for the eight scans: `docs/OCR_Kraken_approach.md` is still a proposal; nothing is installed.
