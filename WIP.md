# What remains to do

In order; the first item is next. Done items are removed (history is in `git log`).

1. **Hort 1916, English: confirm the 5 reference pages** (`works/1_Theophrastus_original-english_Hort_1916/convert/reference/*.draft.txt`, PDF pages 56, 226, 400, 760, 800). The assistant drafted them, then checked every line where one of the three best models disagreed (62 lines) against a zoomed image: no error found in the drafts. Three points remain open, for a reader of Greek or for the transcription rules: PDF 56, note 6, the accent printed over the ο of τούτοις (as printed: τόυτοις); PDF 760, "UMP₂Ald.", a low mark after P read as subscript 2 (the models read a comma); PDF 760, the note number after "motive" looks like 8 but is 3 by the order of the notes. Whether the assistant's check is enough for the English, or a person must still read every line, is for the user to decide (`docs/OCR_Kraken_approach.md`, "Who does what"). Then rename the files without `.draft`, score the 8 models again with `tools/ocr_score.py` and choose. On the drafts, PP-OCRv6 (small) is best (1.5% character errors with typography set aside); the errors left are in note numbers and Greek notes, and one note line lost by the line finder.
2. **Decide the transcription rules** for the reference pages (spacing before `;` and note numbers, quotes, dashes; for older books abbreviations, long s, ligatures); the drafts follow provisional rules (`docs/OCR_Kraken_approach.md`). Needs the user and the specialists.
3. **Read all of Hort's English pages** with the chosen model and write its `extract_eng.py`; decide whether the Greek notes need their own treatment.
4. **Convert the seven other scans**, once 1–3 are done.
   - Dioscorides, French — `2_Dioscorides_french_Mathee_1553`.
   - Pliny, French with its Latin — `3_Pliny_french_Poinsinet_1771-1782`.
   - *Circa instans*, Latin — `4_Circa-instans_original_Venice_1497`.
   - *Circa instans*, French — `4_Circa-instans_french_Dorveaux_1913`.
   - Mattioli, Italian — `5_Mattioli_original_Discorsi_1568`.
   - Mattioli, French — `5_Mattioli_french_DuPinet_1561`.
   - Petit Bauhin, French — `6_Petit-Bauhin_original_1671`.
5. **Define the steps after the text**: plant entries, translation, use records, classification (`docs/Project_context.md`, "The steps").
