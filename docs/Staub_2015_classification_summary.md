# Staub et al. 2015, classifying diseases and remedies — summary and what the project takes from it

From a full reading of the accepted manuscript (`references/Staub_2015_JEthnopharmacol.pdf`).

**Reference.** Staub P.O., Geck M.S., Weckerle C.S., Casu L., Leonti M. (2015). Classifying diseases and remedies in ethnomedicine and ethnopharmacology. *Journal of Ethnopharmacology*. doi:10.1016/j.jep.2015.08.051.

**What kind of article.** A short position paper, without new data. It compares three existing ways of sorting illnesses into categories and proposes a fourth. It is the methodological companion of the Mattioli study by the same group (Staub, Casu, Leonti 2016, `references/Staub_2016_Phytomedicine.pdf`), which the project uses as its benchmark: the 2016 study says it filed its 5,314 uses under 21 categories "largely following" the fourth scheme below.

Two terms used throughout: **emic** = in the terms of the culture or the text itself; **etic** = in the terms of an outside observer, here modern medicine.

## 1. What the article says

**The central claim.** There is no single correct way to sort illnesses and remedies into categories. The right scheme depends on the question asked. Whatever the scheme, its criteria must be written down so that anyone can apply them the same way.

**Three existing schemes, judged for field and historical data.**

| Scheme | Built for | Verdict of the article |
|---|---|---|
| ICD, International Classification of Diseases (WHO) | Hospitals; sorts by diagnosed disease and its cause | Needs a clinical diagnosis. A healer's account or an old text gives symptoms, not a diagnosis, so the ICD can hardly be applied |
| EBDCS, Economic Botany Data Collection Standard (Cook 1995) | Recording plant uses in botanical databases | Widely used but inconsistent: mixes illnesses and effects, puts chilblains under muscles and bones, treats "inflammation" as a category although it is a symptom of many conditions. Its own users found it hard to apply |
| ICPC, International Classification of Primary Care (WONCA, accepted by the WHO) | General practitioners; sorts by what the patient complains of | The closest to what informants and texts actually say: no diagnosis needed. 17 chapters, mostly by body system, plus psychological and social problems. Keeps apart what the others merge: urinary problems, women's problems, pregnancy and childbirth, men's problems |

**The proposal: one scheme per question.**

1. **To understand a medical tradition from the inside**: use the tradition's own categories. A ready-made modern scheme hides what is specific to it. Example given: the Popoluca of Mexico treat fever and headache with the same plants, the same way, and name them together; splitting them into "infections" and "pain" would misrepresent them.
2. **To compare traditions**: use the ICPC as a template, adapted where needed (for instance an added category for infectious diseases). Sort by its "symptoms and complaints" and its "medication, treatment" components.
3. **To look for new drugs**: use categories drawn from what approved plant-derived medicines are actually used for. The article derives 17 such categories from the 225 plant species behind approved or trial drugs listed by Zhu et al. 2011: antidote, andrology, cancer, cardiovascular, dermatology, eye, food, gastrointestinal, gynaecology, infections, metabolic, nervous system, parasites, poisons, respiratory, skeleto-muscular, urology.

**Other points made.**

- **"Culture-bound syndromes" do not need a category of their own.** Every illness is shaped by its culture. Fright illness (*susto*) can be filed with psychological complaints; a Maya syndrome turned out to match gallbladder disease. Sorting by symptom works for most of them.
- **How a remedy is given matters for sorting.** None of the three schemes takes it into account. Haemorrhoids treated with an ointment and haemorrhoids treated with a drink may belong to different categories (skin, circulation).
- **Counting use reports per category** gives a rough picture of which illnesses weighed most on a community.
- **Mattioli's own index.** The article notes that Mattioli, in the sixth book of his commentary, already grouped all remedies by body part, symptom and effect, from the head down to laxatives and emetics.

**A worked example on our own corpus.** The article sorts the uses of fennel in Mattioli's Dioscorides, each with its Italian quotation and page (p. 821):

| Quotation | ICPC chapter and code |
|---|---|
| "genera copiosamente latte" (makes plenty of milk) | Pregnancy, childbearing, family planning — W19 |
| "provoca ella l'orina" (provokes urine) | Urological — U29 |
| "conferisce a i dolori delle reni, & mali della vesica" (kidney pain, bladder troubles) | Urological — U14, U13 |
| "rompono le pietre" (breaks stones) | Urological — U95 |
| "provoca i mestrui" (brings on the menses) | Female genital — X05 |
| "purga le femine di parto" (purges women after childbirth) | Pregnancy, childbearing, family planning — W18 |

Under the ICD or the EBDCS all six would fall into one category, "genitourinary system disorders".

## 2. What the project takes from it

Proposals for discussion with the pharmacology, history and anthropology colleagues; none is a decision.

| Idea in the article | Transposed to Virtutes Herbarum |
|---|---|
| The text's own words and the modern reading are two different things | Three separate layers. (1) The **text** of each version, word for word, in the unified text format (`Unified_text_format.md`): it contains no interpretation at all. (2) The **use records**, each proven by a literal quotation from layer 1. (3) The **classifications**, attached to the records, never written into them. A classification can then be redone or replaced without touching the text or the records |
| No single scheme fits all questions | A record can carry several classifications side by side, one column per scheme. The project's five aims map onto the article's three: recording and tracing transmission → the texts' own categories; comparing across places and centuries → ICPC; confronting with science and exploring the untested → the therapy-based categories |
| Keep the tradition's own categories | Record the category the book itself uses, when it has one. Candidates in the pilot: the head-to-toe index in book six of Mattioli; the PROPR(iétés) heading of the Petit Bauhin; the qualities and degrees (hot, dry, in the second degree…) of *Circa instans* |
| Do not split what the source joins | When a text names several complaints in one breath for one preparation, keep one quotation and attach several codes to it, and keep the fact that they were named together |
| ICPC for comparison, adapted where needed | Use ICPC-2 codes as the comparison layer, at two depths: chapter (17 values) and code (e.g. U95). Record any adaptation in a table of our own, with the reason |
| Therapy-based categories for drug discovery | Use the 17 categories (21 in the 2016 study) as the "science" layer. Since the 2016 study classified Mattioli 1568 this way, our extraction from the same edition can be compared with theirs category by category |
| The way a remedy is given matters | The use record keeps route and form (drunk, applied, inhaled, fumigation…) as its own field; it is already in the project's draft list of fields |
| Criteria that anyone can follow | Each classification comes with a written rule sheet and worked examples (the fennel table is the model: quotation, page, code). Rule sheets are kept in this repository and versioned, so a change of rule is visible |
| Counting uses per category | Useful, with one caution specific to this corpus: later herbals copy earlier ones, so repeated uses are not independent witnesses |
| A quotation with its page for each use | Same requirement as the project's own rule. It is why the unified text format ties every passage to its page and forbids any silent change to the wording |

**Consequences for the work at hand.** The article confirms two choices made for the text format: the text layer stays free of interpretation, and it distinguishes the voice of the work from the voice of its commentator. The second point is decisive for Mattioli: the 2016 study extracted uses only from the chapters of Dioscorides (printed in roman type), not from Mattioli's commentary (in italics).

## 3. Limits and points not verified

- The file is the accepted manuscript, before the journal's copy-editing; the published version may differ in detail. Not compared.
- The article argues from examples; it does not test the schemes on a dataset (for instance by having two people classify the same records).
- Its Table 1 labels the 17 ICPC chapters A to Q in sequence. The codes in its own examples (A03, N01, P02, U95, W19, X05) use the real ICPC-2 chapter letters, which are not in sequence. To be read from the ICPC-2 itself, not from that table.
- **Not checked:** the licence of the ICPC-2 code list (owned by WONCA) and whether it may be copied into a public repository; whether a newer edition (ICPC-3) should be preferred; the contents of Zhu et al. 2011.
- **Not checked in our scan:** that the 1568 Discorsi we hold contains the head-to-toe index of book six described by the article (which cites a 1968–1970 facsimile).
- The examples of the article are field studies with living informants. A historical text cannot be questioned: where the wording is ambiguous, the record must say so rather than force a code.
