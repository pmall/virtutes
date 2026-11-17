# What remains to do

In order; the first item is next. Done items are removed (history is in `git log`).

1. **Convert Pliny, Latin** — `3_Pliny_original_Mayhoff`.
   - Sections and paragraphs as `<milestone unit=…>`, two competing numberings; pages as `<pb xml:id="v.1.p.1"/>`; about 69,000 `<note>` holding variant readings (`apparatus`, not `note`).
2. **Convert Pliny, English** — `3_Pliny_english_Bostock-Riley_1855`.
   - `div1` book / `div2` chapter; pages as `<pb n="1001"/>` (probably volume 1, page 1); footnotes. Checked: the file does not parse as is with the standard library (undefined entity `&mdash;`); the three others do.
3. **Decide how to read the eight scans** — engine and transcription rules; `docs/OCR_Kraken_approach.md` is a proposal, nothing is installed. Needs the user and the specialists.
4. **Convert the eight scans**, once 3 is decided.
   - Theophrastus, English — the right-hand pages of `1_Theophrastus_original-english_Hort_1916` (its Greek is done).
   - Dioscorides, French — `2_Dioscorides_french_Mathee_1553`.
   - Pliny, French with its Latin — `3_Pliny_french_Poinsinet_1771-1782`.
   - *Circa instans*, Latin — `4_Circa-instans_original_Venice_1497`.
   - *Circa instans*, French — `4_Circa-instans_french_Dorveaux_1913`.
   - Mattioli, Italian — `5_Mattioli_original_Discorsi_1568`.
   - Mattioli, French — `5_Mattioli_french_DuPinet_1561`.
   - Petit Bauhin, French — `6_Petit-Bauhin_original_1671`.
5. **Define the steps after the text**: plant entries, translation, use records, classification (`docs/Project_context.md`, "The steps").
