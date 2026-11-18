# What remains to do

In order; the first item is next. Done items are removed (history is in `git log`).

1. **Hort 1916, English: decide whether the reading is good enough** (`docs/OCR_Kraken_approach.md`, "What good enough means": the threshold there is a proposal to confirm). On 5 sample pages (PDF 56, 226, 400, 760, 800; references in `works/1_Theophrastus_original-english_Hort_1916/convert/reference/`), PP-OCRv6 small gets 2 of 1,377 main-text words wrong, PP-OCRv6 medium 1, none carrying a record (`uv run tools/ocr_score.py --show ...` lists them). Then rename the reference files without `.draft`.
2. **Read all of Hort's English pages** with PP-OCRv6 small, run the checks of step 6 of the method, and write `extract_eng.py`.
3. **Convert the seven other scans** with the same method, starting with Mattioli 1568 (the hardest and the benchmark). For the older books, decide the transcription rules (abbreviations, long s, ligatures) with the specialists first.
   - Dioscorides, French — `2_Dioscorides_french_Mathee_1553`.
   - Pliny, French with its Latin — `3_Pliny_french_Poinsinet_1771-1782`.
   - *Circa instans*, Latin — `4_Circa-instans_original_Venice_1497`.
   - *Circa instans*, French — `4_Circa-instans_french_Dorveaux_1913`.
   - Mattioli, Italian — `5_Mattioli_original_Discorsi_1568`.
   - Mattioli, French — `5_Mattioli_french_DuPinet_1561`.
   - Petit Bauhin, French — `6_Petit-Bauhin_original_1671`.
4. **Define the steps after the text**: plant entries, translation, use records, classification (`docs/Project_context.md`, "The steps").
