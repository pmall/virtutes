# Selecting the versions of a work

Applies to every work of the catalogue.

**Starting point:** the map of all known versions of the work (see `Edition_mapping_method.md`).
**Result:** for each work, the versions to download, each of which will end as a typed text.

## The rules

1. **For each work, choose up to 3 versions:** original language, English, French.

2. **Everything ends as a typed text.** If a reliable typed text of the version exists, take it; if a scan of that same edition also exists, take it too (any complete copy; its sharpness does not matter), but the typed text is what we work from. Otherwise, take the scan and type it ourselves, keeping for each passage the page of the scan it comes from. All typed texts are brought to one format (`Unified_text_format.md`).

3. **A typed text is reliable** if it comes from a scholarly or institutional source, states its licence and the edition it was made from, and has been corrected: marked as checked or proofread, or made by a scholarly project that corrects its texts (Perseus, First1KGreek).

4. **A version is eligible only if:**
   - it is complete (not a selection or an abridgement);
   - its text is free of copyright;
   - it can be downloaded in full (not only viewed, lent or searched).

5. **Among eligible versions, choose in this order:**
   - **5.1** the edition used by a benchmark study we compare with, if its scan is sharp enough;
   - **5.2** a version with a reliable typed text;
   - **5.3** a printed book over a handwritten manuscript;
   - **5.4** a scholarly edition over an old printing;
   - **5.5** a bilingual book;
   - **5.6** among versions still equal, the earliest edition whose downloadable scan is sharp enough: at least about 225 pixels per inch of the printed page's height (so a small book needs fewer pixels than a folio).

6. **If no version is eligible,** leave the slot empty and say why.

## Applying the rules in order

**Candidates.** For each work and slot, the candidates are every version in the edition map in that language whose type is edition, translation, edition + translation or manuscript (a single manuscript, not a summary row). Facsimiles and derivatives are not candidates (a facsimile counts through the edition it reproduces).

**Procedure: best on paper first, then the next.**

1. **Rank the candidates on paper**, from the edition map and a search of the typed-text collections (Perseus, First1KGreek, Wikisource pages marked validated, Bibliothèques Virtuelles Humanistes, LacusCurtius, Corpus Corporum, EEBO-TCP, Gallica corrected text, and any collection specific to the work), using rule 5 in order: benchmark edition (5.1), reliable typed text (5.2), printed book over manuscript (5.3), scholarly edition over old printing (5.4; a scholarly edition is prepared by a named scholar with introduction, notes or critical apparatus), bilingual (5.5), earliest edition (5.6).
2. **Check the first candidate** against rule 4: complete, free of copyright (EU: editor and translator died 70 or more years ago), and downloadable in full; for a scan, also sharp enough. Look for its copies in the main libraries (Internet Archive, Gallica, Google Books, Bayerische Staatsbibliothek, BIU Santé, e-rara, Biodiversity Heritage Library, Wellcome, HathiTrust, and any library holding it).
3. **If it passes, it is chosen and the slot is decided.** If not, record why and check the next candidate.

A check that cannot be done (site blocked, server down) is retried another way (e.g. with a browser) or reported as open, never assumed.

**Record.** The candidates are the rows of the edition map; no separate table is kept. The selection file records, for each slot, the chosen version, the deciding rule, and why the better-ranked candidates were rejected (column why_not_others), with sources and dates.

## Presenting the result

One table, one row per work:

| Work | Original | English | French |
|---|---|---|---|

Each cell names the chosen version and says whether it comes as a typed text or as a scan to be typed, or why the slot is empty.

For each chosen version, also record: the copy chosen and its link, the image size (for scans), the rights, the size to download, and which rule decided.

## Reference points from the pilot

- "Sharp enough" (rules 5.1 and 5.6): the benchmark copy of Mattioli 1568, a folio scanned at 1899 × 3000 px per page, was judged sufficient; 225 pixels per inch of page height was set from it.
- Pilot result: `data/Pilot_selected_versions.csv`.
