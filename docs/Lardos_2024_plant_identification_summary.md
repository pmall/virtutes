# Lardos et al. 2024, identifying the plants of historical texts — summary and what the project may take from it

From a full reading of the published article (`references/Lardos_2024_JEthnopharmacol.pdf`).

**Reference.** Lardos A., Patmore K., Allkin R., Lazarou R., Nesbitt M., Scott A.C., Zipser B. (2024). A systematic methodology to assess the identity of plants in historical texts: a case study based on the Byzantine pharmacy text John the Physician's Therapeutics. *Journal of Ethnopharmacology* 322, 117622. [doi:10.1016/j.jep.2023.117622](https://doi.org/10.1016/j.jep.2023.117622). Open access (CC BY).

**How to read this summary.** The article is an existing study in the project's field: one team's way of doing one part of the work, on one text. It is recorded here to be known, compared with and cited. It is not a procedure the project has to follow.

**What kind of article.** A method paper with a case study, by a team of seven (pharmacy, botany, history, philology, earth sciences; Zurich, Kew, Royal Holloway). The authors call their approach experimental. Its question: when a historical text names a plant, how sure can we be of the modern species that scholars have proposed for that name?

## 1. What the article says

**The problem.** Studies of old medical texts usually take the identity of each plant from a dictionary or a glossary. The authorities disagree with each other, some identities are doubtful, and the scientific names they give are often outdated or ambiguous. Taking them over without checking spreads the errors.

**The two texts.**

- The text studied is a Byzantine recipe book of the late 13th or early 14th century, probably from Cyprus: the *Therapeutics* of John the Physician, in its commentary version. It has 1,414 recipes naming 289 plants and 43 minerals. Like most recipe books it gives only the name of each plant, with no description.
- The descriptions are therefore taken from Dioscorides' *De materia medica*, the reference work of that tradition: the Greek plant names from Wellmann's edition, the botanical information from Beck's English translation (2005), with the Greek consulted for crucial passages.

**The method, in six stages.**

| Stage | What is done |
|---|---|
| 1. Data from the historical texts | Every word of the recipes is tagged by hand (plant, mineral, animal, mixed, other, unknown). The spelling variants of a plant name are grouped under one dictionary form. Each name is linked to its entry in Dioscorides (same name, synonym, product of that plant, unclear, no link). What Dioscorides says of the plant is recorded by feature: form, height, stem, leaf, flower, fruit, seed, root, habitat, distribution. The uses in the recipe book are recorded as use records |
| 2. Candidate species | Every species that the literature has proposed for the name is listed: 19th-century botanists of the Greek flora and modern field studies in Greece and Cyprus. The scientific names are validated and brought up to date with Kew's Medicinal Plant Names Services |
| 3. Data from modern sources | For each candidate: its description in two regional floras (Turkey, Cyprus); its uses in herbal medicine handbooks and field studies; its clinical trials |
| 4. Comparison | Feature by feature, the description in Dioscorides against the description in the floras: good match, partial match, no match, or no information. Use by use, the recipe book against the modern sources |
| 5. Scoring | The matches are added up per candidate, which ends as a **strong**, **moderate** or **weak** candidate. A second, separate score says how far the historical uses are also modern uses |
| 6. Review | The method and the results are reviewed by the whole team in a two-day workshop |

**A use record**, for the authors, is one mention in the recipe book of a plant substance with a medicinal use: the plant name, the part used, the use. Each use is filed under one of 21 groups by body part or system, following Staub et al. 2015 ([`Staub_2015_classification_summary.md`](Staub_2015_classification_summary.md)).

**The figures.**

| What was counted | Result |
|---|---|
| Plant names of the recipe book that have a link to a name in Dioscorides | 274 of 289 (95%); most are the very same name |
| Plants of Dioscorides these names lead to | 252 |
| Of these 252, how well Dioscorides describes the plant | 61 richly (24%), 74 moderately (29%), 117 poorly (47%) |
| Sample kept for the comparison | The 61 richly described plants, reached from 50 names of the recipe book |
| Species proposed in the literature for these 50 names | About five scientific names per name; about two once the names are validated; 130 species in all |
| Single features compared between Dioscorides and the floras | 1,213: good match 36%, partial 24%, no match 7%, no information in the flora 33% |
| Candidates by strength (141 name and candidate pairs) | Strong 26%, moderate 36%, weak 23%, not in the floras 14% |
| Names with several candidates where the method tells them apart | 27 of 33 |

**Other points made.**

- **The names are stable.** Thirteen centuries after Dioscorides, the recipe book still uses his plant names. The authors take this as support for reading it with his descriptions.
- **One name can cover several plants.** 194 names lead to 252 plants: Dioscorides often describes two or three kinds under one name (a larger and a smaller plantain, three kinds of *khamaipitys*) and says they have the same properties. The users of the recipes probably did not distinguish them either.
- **Dioscorides often describes a plant by comparing it with another** (leaves like those of the leek, a flower like that of the rose), usually a common plant that he does not describe at all. Such descriptions cannot be compared with a flora directly.
- **Poorly described plants are mostly the common ones**: olive, fig, common herbs, imported spices. They needed no description.
- **Uses are weak evidence for identity.** Historical and modern uses of the same plant differ considerably, because uses change with time and place. The authors rank candidates by botany and give the uses score only as a complement. Two thirds of the candidates with a strong uses score are not strong botanically.
- **Practical advice** (their Table 3), among which: give every piece of data an identifier from the start and keep it in a database; have the text read by philologists and the uses by historians of medicine; fix the taxonomy at one dated state and keep the author's name with each species name; consider the whole flora of the region and not only the species already proposed.

**A worked example on our own corpus.** The chapter on cyclamen, κυκλάμινος, book II, chapter 164 in the article, `2.164` in our text of Wellmann's edition ([`works/2_Dioscorides_original_Wellmann_1906-1914`](../works/2_Dioscorides_original_Wellmann_1906-1914/)). Five species have been proposed for it; the uses score, from 0 to 3, is in brackets:

| Candidate species | Verdict on botany (uses) |
|---|---|
| *Cyclamen graecum* Link | Strong (0) |
| *Cyclamen hederifolium* Aiton | Strong (0) |
| *Cyclamen persicum* Mill. | Strong (3) |
| *Cyclamen cyprium* Kotschy | Weak (3) |
| *Cyclamen purpurascens* Mill. | Not in the two floras (0) |

Three species remain equally strong: the method narrows the choice, it does not always settle it.

## 2. What the project may take from it

Proposals for discussion with the pharmacology, history and linguistics colleagues; none is a decision.

| Point of the article | What it could mean for Virtutes Herbarum |
|---|---|
| An identification is a judgement with a level of confidence, and several species can remain | Matches the position already taken in the preliminary study: a plant name is linked to a modern species "with a confidence" ([`Project_context.md`](Project_context.md)). The record of a plant could hold several candidate species, each with its own level, instead of one species |
| Strong, moderate, weak | A possible scale for that confidence. Its thresholds are judgement calls of the authors, not tested values; the project may prefer another scale |
| One name, several plants; several names, one plant | The link between a name as written and a plant cannot be one to one. Dioscorides' "kinds" inside one chapter need their own place |
| Descriptions are compared feature by feature | Dioscorides, Mattioli and the Petit Bauhin describe their plants, so the same comparison is possible on the project's own texts, without going through a second text as the article had to |
| Names validated against one dated state of a taxonomy, with author names | Worth adopting whatever the method: it costs little and avoids confusing two species that share a name |
| Their data are public | The 50 names, their chapters in Dioscorides and the 130 rated candidates could serve as a test set for plant identification in Dioscorides, as Staub et al. 2016 serves for the uses in Mattioli. Not downloaded |
| Uses filed in the 21 groups of Staub et al. 2015 | A second study in the field using that classification, on a text of the same tradition: an argument for using it as the project's comparison layer, and results that could then be compared with theirs |

**Where the project differs, and should not copy.**

- **Scale.** Seven specialists assessed 50 plant names in one text, by hand. The pilot alone has six works and thousands of plant entries. The article's method cannot be applied as it stands; what part of it can be done by machine, and checked by people on a sample, is an open question for the project.
- **Kind of text.** The article treats a recipe book without descriptions. The pilot's works are herbals that describe their plants, some with woodcuts. The detour through a reference text is not needed, and the pictures are evidence the article did not have.
- **Aim.** The article wants the most likely species for each name. The project first wants what each text says, tied to its page; identification is a later layer that can be redone without touching the records.
- **Translation.** The article works from an English translation of Dioscorides and checks the Greek when needed. The project's position is to extract from the original language and use a translation as a control.

## 3. Limits and points not verified

Limits the authors state themselves:

- Only the richly described plants were assessed: a quarter of those met.
- Only species already proposed in the literature were compared, not the whole flora of the region; a species nobody proposed cannot come out.
- Only floras of Turkey and Cyprus were used; a plant imported from elsewhere is judged against the wrong flora.
- A third of the features Dioscorides gives had no counterpart in the floras, so a score can rest on few comparisons.
- The thresholds between strong, moderate and weak were set by overall judgement and "can be adjusted"; no statistical test was possible.
- The method assumes that the flora of the region has not changed much since Antiquity.

Not verified by us:

- The data files and the supplementary tables were not opened; what they contain is known only from the article's description.
- The licence and the conditions of use of Kew's Medicinal Plant Names Services.
- Whether the article's chapter numbers, taken from Beck's translation, always agree with those of our text of Wellmann's edition. Checked for one chapter only (cyclamen, 2.164).
- The article was not compared with other methods of plant identification; it is the only one read so far.
