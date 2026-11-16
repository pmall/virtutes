# Mapping every version of a work — method

Virtutes Herbarum. Written 12 November 2026, after the first run on the six pilot works (result: `data/Pilot_works_all_versions.csv`, 529 versions). To be reused for any work of the catalogue.

**Aim:** for each work, an exhaustive view of every version that exists, whether or not we have it and whether or not it is online. Choosing which version to work from comes after, from this map.

## 1. The rule

**One row = one version = one edition (a distinct printing: year + place + printer or publisher), whatever languages it contains.**

- A bilingual book is **one** row.
- A multi-volume set published over several years is **one** row, with a year range (e.g. 1906-1914). If the volumes of one set carry different dates, or only one volume is known, say so in the note.
- A reprint or reissue with a new date is **its own** row, flagged "reprint of …" or "reissue" in the note.
- One printing sold the same year under several publishers' names is **one** row; the other names go in the note.
- Doubtful or probable "ghost" editions (known only from an old bibliography, likely misdated) are **kept**, flagged "doubtful" or "possible duplicate" in the note. Better a flagged row than a silent omission.
- **Manuscripts** are not listed one by one: one summary row per language tradition (approximate number of surviving manuscripts, the key ones, a source). Exception: a manuscript the project actually uses gets its own row (type `manuscript`).

## 2. The columns

UTF-8 CSV, exactly this header:

```
work_no,work,type,year,place,publisher_printer,editor_translator,language,contents,note,source_url,checked
```

| Column | Content |
|---|---|
| work_no | Number of the work, unique across all works (1, 2, 3 …) |
| work | Short name, identical on every row of the work |
| type | One of: `edition` (original language) · `translation` · `edition+translation` (bilingual) · `facsimile` · `derivative` (abridgement, adaptation or commentary built on the work — flagged, not the work itself) · `manuscripts` (summary row) · `manuscript` (single manuscript we use) |
| year | 1497 · 1906-1914 · c.1483 · c.1440-1450 |
| place | City of printing |
| publisher_printer | As in the catalogue record |
| editor_translator | Name(s); "(tr.)" for a translator if useful |
| language | Greek · Latin · Greek+English · Old French … |
| contents | complete · books I-V · vol. 1 only · etc. |
| note | Anything that helps: first edition, critical edition, reprint of X, doubtful, catalogue numbers (USTC, ISTC, VD16, SUDOC…), known digitised copies (identifiers only) |
| source_url | Link to the catalogue record or bibliography where the version was seen |
| checked | `yes` = seen in a catalogue record or a scholarly bibliography during the research · `no` = reported (memory, Wikipedia, a review, a bookseller) but not confirmed |

## 3. Scope decisions to take for each work, before starting

Write them down for each work; they change the size of the result a lot.

- **Which work exactly.** Name the original title and the language of first composition. Decide whether commentaries and translations-with-commentary count as versions (pilot: yes, flagged in the note), except when the commentary is itself a work of the catalogue (pilot: Mattioli's commentary on Dioscorides was mapped as its own work and appears only as one `derivative` row under Dioscorides).
- **Partial editions.** For very large works, keep only editions that contain the parts relevant to the project, and count the others without listing them. Pilot example: Pliny restricted to editions containing books XII–XXVII (plants and remedies); about 140 editions of other books only were counted, not listed.
- **Adaptations.** Decide which adaptations are recognised versions (pilot: the French *Arbolayre / Grant herbier* and English *Grete Herball* under *Circa instans*, as `derivative`) and which are only works using it as a source (excluded).
- **Period.** From the first manuscript or printing to today, translations still under copyright included.

## 4. Sources

| Period / kind | Sources | Remarks from the pilot run |
|---|---|---|
| Printed before 1501 | ISTC (data.cerl.org/istc), GW (Gesamtkatalog der Wiegendrucke) | ISTC blocks automated access; USTC and library records cite ISTC numbers |
| Printed 1450–1650 | **USTC** (ustc.ac.uk) — the main source; it includes EDIT16 (Italy), VD16 (Germany), BP16 (Paris) | Search many title variants (Latin, vernacular, author forms); ~20 variants were needed for Dioscorides |
| 17th c. | VD17, STCN (Netherlands), SBN (Italy), USTC | USTC thins out after 1650; VD17, STCN, SBN were not reached in the pilot — a known gap |
| 18th–21st c. | SUDOC, BnF catalogue, WorldCat, K10plus (Germany), NDL (Japan), national catalogues, publishers' pages | WorldCat, Gallica and HathiTrust often block automated access |
| Digitised copies | Internet Archive (archive.org/metadata/<id>, advancedsearch), Wellcome (api.wellcomecollection.org/catalogue/v2/works?query=…), Biodiversity Heritage Library, Google Books, Gallica, BIU Santé | Record identifiers only; never download |
| Manuscripts | Pinakes (Greek), Jonas (Old French, IRHT), Handschriftencensus (German), Mirabile, library catalogues | Jonas was down during the pilot |
| Scholarly bibliographies | *Catalogus Translationum et Commentariorum* (e.g. Riddle on Dioscorides, vol. IV), prefaces of critical editions (Hort, Wellmann, Mayhoff, Wölfel…), Pritzel's *Thesaurus literaturae botanicae*, specialist studies | Old bibliographies contain ghosts (e.g. Pritzel's "1683" Petit Bauhin) — confirm in a library record |

Wikipedia and booksellers' listings are leads only: a version seen only there gets `checked = no`.

## 5. How the research is run

1. **One researcher per work, in parallel** (AI sub-agents in the pilot run). Each gets the same brief (section 7), filled in for its work, and writes one CSV.
2. **Research only. Nothing is downloaded** — no scans, no books. Exception tolerated: an open-access bibliography read as a source, kept in a temporary folder, never in the project folder.
3. **Etiquette towards libraries:** low request rate, no bulk scraping, generic client name, no personal or project details in requests.
4. **Each researcher reports:** number of rows by type, how many `checked = yes / no`, and its main gaps or doubts.
5. **Check and merge** with `tools/merge_edition_maps.py` (section 6).
6. **Present the result as one table**, one line per work: versions, span of years, number confirmed. Then the gaps.

Cost of the pilot run, for planning: 6 researchers, 14–20 minutes each, in parallel; about 190,000–290,000 tokens each, 1.3 million in total.

## 6. Checking and merging

```
python3 tools/merge_edition_maps.py <folder with the per-work CSVs> <output.csv>
```

The script checks that every file has the exact header and 12 fields per row, normalises the `type` values, sorts by work, then manuscripts first, then year, writes one UTF-8 CSV that opens in Excel or LibreOffice, and prints the one-line-per-work summary.

After merging, check by hand that every version the project already uses or has listed appears in the map (pilot: all 14 versions known before the mapping were found).

## 7. Brief given to each researcher (template)

Replace the parts in `<…>`.

> You are building an exhaustive bibliographic map of ONE historical work, for a research team. Research only: look things up in library catalogues and bibliographies. Do NOT download scans or books.
>
> WORK: `<author, title in original language and usual translations, date of composition>`. Scope: every printed edition of the original text and every printed translation, in any language, from the first printing `<known first printing, if any>` to today. `<Scope decisions from section 3: commentaries, partial editions, adaptations, works mapped separately.>`
>
> RULE (must be applied strictly): one row = one version = one edition (a distinct printing: year + place + printer/publisher), whatever languages it contains. A bilingual book is ONE row. A multi-volume set published over several years is ONE row (give the year range). A reprint/reissue with a new date counts as its own row, flagged "reprint of …" or "reissue" in the note. Manuscripts: do NOT list individually — add one summary row of type "manuscripts" per language tradition with approximate counts and the key manuscripts, with a source. `<Manuscripts used by the project get their own row of type "manuscript": list them.>`
>
> COLUMNS — write a UTF-8 CSV with exactly this header:
> `work_no,work,type,year,place,publisher_printer,editor_translator,language,contents,note,source_url,checked`
> - work_no: `<n>` ; work: `<short name>`
> - type: one of: manuscripts | manuscript | edition | translation | edition+translation | facsimile | derivative
> - source_url: URL of a catalogue record or bibliography where you saw it `<suggested sources from section 4, plus specialist bibliographies for this work>`.
> - checked: yes = seen in a catalogue record or a bibliography during this task; no = known but not confirmed.
>
> `<Specific questions, if any: e.g. identify the edition of a given digitised copy.>`
>
> Etiquette: low request rate, no bulk scraping, no personal or project details in requests.
>
> OUTPUT: write the CSV to `<path>/<n>_<work>.csv` (quote fields containing commas), sorted by year. Then reply with: number of rows by type, checked = yes vs no, and the main gaps or doubts (3–6 lines). Be exhaustive within scope; better to include a row with checked = no than to omit a known edition.

## 8. Known limits of the pilot map (to revisit)

- Pliny: 17th-century Latin reprints probably incomplete (VD17, STCN, SBN not reached); several modern translations unconfirmed.
- Mattioli: EDIT16 not searched directly; post-1650 coverage thin; Ferri, Fausti and Raphael bibliographies not consulted.
- Dioscorides: Greek and Arabic manuscript counts not confirmed (Diels, Touwaide, Sezgin to check).
- *Circa instans*: about 8 possible duplicate 16th-century rows; Jonas unavailable for Old French manuscripts.
- Petit Bauhin: 1670 is the first edition (not 1683); authorship and the claimed derivation from Mattioli/Du Pinet (Magnin 1889, Persée doi:10.3406/linly.1889.4851) not read directly.
- Theophrastus: two doubtful Heinsius records kept; reprints of modern editions not exhaustive.
