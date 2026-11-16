---
name: map-editions
description: Build the exhaustive list of every edition and translation of one historical work (the edition map). Use when a new work enters the project or its map must be completed.
---

# Task: map every version of a work

**Goal.** One CSV listing every known edition and translation of one work, following `docs/Edition_mapping_method.md` (read it first: the rule, the columns, the scope decisions, the sources).

## Steps

1. **Settle the scope with the user** before starting: the scope decisions of section 3 of the method, written down for this work.
2. **One researcher per work.** For several works, run one sub-agent per work in parallel, each with the brief below and its own output file. Order of magnitude from the pilot: 15 to 20 minutes and 200,000 to 300,000 tokens per work.
3. **Research only.** No scan or book is downloaded. An open-access bibliography read as a source goes to a temporary folder outside the repository.
4. **Check and merge**: `python3 tools/merge_edition_maps.py <folder with the per-work CSVs> <output.csv>`.
5. **Check by hand** that every version the project already uses or has listed appears in the map.
6. **Report** as one table, one line per work: number of versions by type, span of years, how many are `checked = yes`; then the gaps and doubts. Add the gaps to the "Known limits" section of the method document.

## Brief for each researcher

Replace the parts in `<…>`.

> You are building an exhaustive bibliographic map of ONE historical work, for a research team. Research only: look things up in library catalogues and bibliographies. Do NOT download scans or books.
>
> WORK: `<author, title in original language and usual translations, date of composition>`. Scope: every printed edition of the original text and every printed translation, in any language, from the first printing `<known first printing, if any>` to today. `<Scope decisions: commentaries, partial editions, adaptations, works mapped separately.>`
>
> RULE (must be applied strictly): one row = one version = one edition (a distinct printing: year + place + printer/publisher), whatever languages it contains. A bilingual book is ONE row. A multi-volume set published over several years is ONE row (give the year range). A reprint/reissue with a new date counts as its own row, flagged "reprint of …" or "reissue" in the note. Manuscripts: do NOT list individually — add one summary row of type "manuscripts" per language tradition with approximate counts and the key manuscripts, with a source. `<Manuscripts used by the project get their own row of type "manuscript": list them.>`
>
> COLUMNS — write a UTF-8 CSV with exactly this header:
> `work_no,work,type,year,place,publisher_printer,editor_translator,language,contents,note,source_url,checked`
> - work_no: `<n>` ; work: `<short name>`
> - type: one of: manuscripts | manuscript | edition | translation | edition+translation | facsimile | derivative
> - source_url: URL of a catalogue record or bibliography where you saw it `<suggested sources from section 4 of the method, plus specialist bibliographies for this work>`.
> - checked: yes = seen in a catalogue record or a bibliography during this task; no = known but not confirmed.
>
> `<Specific questions, if any: e.g. identify the edition of a given digitised copy.>`
>
> Etiquette: at most one request every two seconds, no bulk scraping, generic client name, no personal or project details in requests.
>
> OUTPUT: write the CSV to `<path>/<n>_<work>.csv` (quote fields containing commas), sorted by year. Then reply with: number of rows by type, checked = yes vs no, and the main gaps or doubts (3–6 lines). Be exhaustive within scope; better to include a row with checked = no than to omit a known edition.
