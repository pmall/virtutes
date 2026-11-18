# What remains to do

In order; the first item is next. Done items are removed (history is in `git log`).

1. **Test the reading of the seven other scans**, one at a time, with the skill `test-scan-reading` (method: `docs/OCR_Kraken_approach.md`). Each test ends with its report `convert/ocr_test.md`; the report of Hort 1916 is the model. Order, easiest first:
   1. *Circa instans*, French — `4_Circa-instans_french_Dorveaux_1913`.
   2. Pliny, French with its Latin — `3_Pliny_french_Poinsinet_1771-1782`.
   3. Petit Bauhin, French — `6_Petit-Bauhin_original_1671`.
   4. Dioscorides, French — `2_Dioscorides_french_Mathee_1553`.
   5. Mattioli, French — `5_Mattioli_french_DuPinet_1561` (two columns).
   6. Mattioli, Italian — `5_Mattioli_original_Discorsi_1568`.
   7. *Circa instans*, Latin — `4_Circa-instans_original_Venice_1497` (gothic type).

   The user has given the go-ahead to download these four models, besides the nine already in `models/` (67 MB in all; file, size and checksum to copy into each `convert/ocr_models.csv` that uses them):
   - CATMuS Gothic Print, `CATMuS-Gothic-Print-1.0.0.mlmodel`, 22,867,328 bytes, md5 a82371504c47403dc653495716eb149f, https://doi.org/10.5281/zenodo.10599911
   - Latin Incunabula and Early Prints, `reichenau_lat_cat_099218.mlmodel`, 22,892,687 bytes, md5 7ddd0d407472ffaaf699d1f6a8d877a5, https://doi.org/10.5281/zenodo.11113737
   - Gallicorpora+, `Gallicorpora+_best.mlmodel`, 16,216,786 bytes, md5 ff22c621126e2db524eb0315cd5ae808, https://doi.org/10.5281/zenodo.7410529
   - Kraken segmentation model for two-column prints, `seg_news_1.0.mlmodel`, 5,250,514 bytes, md5 6f7e68e826a44e810320c389a263bf0d, https://doi.org/10.5281/zenodo.10783346 (finding lines)
2. **Review all eight reports together**, the user with a larger AI model (`docs/OCR_Kraken_approach.md`, step 6 of the method): confirm the threshold of "good enough", choose a model per book, decide which books need another model or fine-tuning, and whether abbreviations are expanded. Accepted reference pages are renamed without `.draft`.
3. **Read each book in full** with its chosen model, run the checks of step 7 of the method, and write its `extract_<lang>.py` (skill `convert-version`). Fine-tuning, where decided, on the GPU server.
4. **Define the steps after the text**: plant entries, translation, use records, classification (`docs/Project_context.md`, "The steps").
