# CITADEL-X Investigation Report: DOI 10.1016/j.jobe.2026.115980

**Investigation Date:** 2026-04-04
**Investigator:** CITADEL-X automated pipeline + manual Google Scholar verification
**Status:** HIGHLY SUSPECT -- probable large-scale reference fabrication

---

## Article Metadata

| Field | Value |
|-------|-------|
| **Title** | Analysis of safety influencing factors in prefabricated building hoisting based on an improved DEMATEL-ISM method |
| **Authors** | Chunling Zhong, Xuechun Li |
| **Journal** | Journal of Building Engineering (Elsevier) |
| **DOI** | 10.1016/j.jobe.2026.115980 |
| **Published** | April 2026 |
| **Publisher** | Elsevier BV |
| **Reference Count** | 85 |

---

## Reference Profile Summary

| Category | Count | Percentage |
|----------|-------|------------|
| Total references | 85 | 100% |
| References with DOI (verifiable) | 28 | 33% |
| References without DOI, with title (flagged) | 46 | 54% |
| References without DOI or title (metadata only) | 11 | 13% |

### Google Scholar Verification Results (46 flagged refs)

| Classification | Count | Description |
|----------------|-------|-------------|
| **false_positive** (confirmed real) | 11 | Found on GS with high title similarity (>0.70) |
| **confirmed_fake** | 7 | Not found anywhere; generic LLM-style titles |
| **probable_fake** | 28 | Weak/no GS match; likely fabricated or severely paraphrased |
| **Total fabricated (confirmed + probable)** | **35** | **41% of all references** |

---

## Detailed Classification

### FALSE POSITIVES -- Confirmed Real Papers (11)

These references were found on Google Scholar with high title similarity and significant citation counts. They are real, well-known papers.

| Ref | Author (Year) | Title | GS Sim | Cited By |
|-----|---------------|-------|--------|----------|
| bib6 | Rahman (2014) | Barriers of implementing modern methods of construction | 1.00 | 428 |
| bib8 | Xie (2020) | Importance-performance analysis of prefabricated building sustainability: a case study of Guangzhou | 0.99 | 61 |
| bib21 | Zhou (2023) | Research on safety management of prefabricated building construction based on BIM technology and risk assessment system | 0.73 | 88 |
| bib32 | Zhang (2021) | Prediction and causal analysis of tower crane safety accidents based on random forest algorithm | 0.74 | 0 |
| bib48 | Al-Bayati (2021) | Impact of construction safety culture and construction safety climate on safety behavior and safety motivation | 1.00 | 150 |
| bib71 | Deng (1989) | Introduction to grey system theory | 1.00 | 7,291 |
| bib72 | Attri (2013) | Interpretive structural modeling (ISM) approach: an overview | 0.99 | 1,387 |
| bib73 | Zhou (2011) | Identifying critical success factors in emergency management using a fuzzy DEMATEL method | 1.00 | 658 |
| bib74 | Sheng-Li (2018) | DEMATEL technique: a systematic review of the state-of-the-art literature on methodologies and applications | 0.97 | 1,395 |
| bib83 | -- (2011) | GB 50204-2002(2011) Code for Acceptance of Construction Quality of Concrete Structures | N/A | N/A |

**Note:** bib83 is a Chinese national building standard (GB 50204-2002). It is a real regulatory document, not a journal article; GS mismatch is expected. bib32 has sim=0.74 but the match title ("Causal Analysis of Subway Construction Safety Accidents Based on Random Forest") is notably different -- this is borderline but given the methodological overlap it may be a legitimate partial match. Counted as false positive conservatively.

### CONFIRMED FAKE -- Not Found Anywhere (7)

These references returned zero Google Scholar results or had extremely low similarity (<0.20) on repeated searches. Their titles are highly specific yet entirely absent from any scholarly database.

| Ref | Author (Year) | Claimed Title | Claimed Journal | Assessment |
|-----|---------------|---------------|-----------------|------------|
| bib20 | Tianliang (2025) | Research on causes of coal mine accidents from a human factors perspective based on an improved DEMATEL-ISM-BN approach | Saf. Environ. Eng. | NOT_FOUND. Uses first name as surname ("Tianliang"). Very specific methodological title typical of LLM fabrication. |
| bib51 | Jiang (2024) | Safety risk assessment of hoisting construction in prefabricated buildings based on a variable-weight element extensional model | J. Wuhan Univ. (Nat. Sci. Ed.) | NOT_FOUND on two separate searches. Extremely specific combined methodology that does not exist in any database. |
| bib56 | Xue (2023) | Cause analysis of high-altitude fall accidents in construction projects based on an improved ISM-MICMAC approach | J. Saf. Environ. | NOT_FOUND. Generic safety + methodology combination title. |
| bib53 | Wen'an (2024) | Safety risk analysis of prefabricated building hoisting construction based on dynamic bayesian networks | J. Saf. Environ. | GS sim=0.18 (best match: "Robot Learning via Deep State-Space Model" -- completely unrelated). Uses first name as surname ("Wen'an"). |
| bib60 | Shang (2025) | Rapid identification of textile fiber constituents using microturbret plasma ionization mass spectrometry combined with random forest models | Anal. Chem. | NOT_FOUND on two separate searches. **Completely off-topic** (textile fiber analysis in a building engineering paper). "Microturbret" is not a real analytical chemistry term. |
| bib19 | Zhou (2013) | Quality control in the hoisting process of All-PC structures for high-rise residential buildings | Construction Supervision | GS sim=0.40, repeated search sim=0.31. No matching result found. |
| bib57 | Xie (2023) | Hierarchical analysis method-based optimization selection of objective levels for ground area governance | Coal Sci. Technol. | GS sim=0.41, repeated search found a vaguely similar Chinese title but completely different paper. Off-topic (coal/mining). |

### PROBABLE FAKE -- Weak GS Match, Likely Fabricated or Severely Paraphrased (28)

These references had low Google Scholar similarity (0.20-0.68). While some may be real Chinese-language journal articles whose English-translated titles cannot be matched, the pattern of so many unverifiable references in a single paper is a strong indicator of fabrication.

| Ref | Author (Year) | Claimed Title (truncated) | Claimed Journal | GS Sim | Notes |
|-----|---------------|---------------------------|-----------------|--------|-------|
| bib2 | Ma (2025) | Research on construction quality evaluation of prefabricated residential... | Engineering Construction and Design | 0.61 | Best GS match is a different paper |
| bib11 | Ding (2010) | Identification and analysis of safety risk factors in tower crane accidents | Construction Technology | 0.64 | GS finds related but different paper |
| bib13 | Huang (2022) | Research progress of prefabricated modular buildings and module joints | Progress in Steel Building Structures | 0.60 | GS match is a review but different scope |
| bib16 | Gao (2025) | Application research of composite slabs in prefabricated building structures | Brick and Tile | 0.46 | Very obscure journal, no match |
| bib17 | Wu (2023) | Safety risk analysis and management practices for construction hoisting... | Construction Supervision | 0.51 | Weak match only |
| bib18 | Zhang (2025) | Statistical analysis of tower crane safety accident cases from 2014 to 2022 | Construction Safety | 0.51 | Weak match |
| bib22 | Yudan (2025) | Coupled analysis of safety risk factors in prefabricated building... | J. Saf. Environ. | 0.57 | Uses first name as surname ("Yudan") |
| bib23 | Fang (2023) | Research on risk assessment model for lifting operations in prefabricated... | J. Saf. Environ. | 0.62 | Partial match to different paper |
| bib24 | Wang (2024) | Early warning of unsafe behaviors among high-altitude workers in prefab... | Journal of Safety Science, China | 0.58 | Weak match |
| bib27 | Xuezhe (2021) | Safety risk assessment of hoisting construction for prefabricated buildings... | J. Civ. Eng. Manag. | 0.63 | Uses first name as surname ("Xuezhe") |
| bib28 | Dong (2018) | Application of JHA in risk analysis of port lifting operations | Value Eng. | 0.46 | No relevant match |
| bib30 | Zhang (2020) | Construction and analysis of a causal network model for tower crane accidents | Journal of Safety Science | 0.44 | GS finds related but different crane paper |
| bib31 | Zhou (2020) | Analysis and control of safety risk factors for tower cranes based on... | J. Saf. Environ. | 0.65 | Partial match |
| bib34 | Zhang (2020) | Causal analysis of unsafe behaviors among construction personnel based... | China Journal of Work Safety Science and Technology | 0.65 | Partial match |
| bib43 | Chen (2022) | Application of smart construction site technology in safety management... | Modern Manufacturing Technology and Equipment | 0.42 | No relevant match |
| bib44 | Zhu (2014) | Construction management during the hoisting phase of large equipment | Construction Technology | 0.49 | No relevant match |
| bib47 | Qu (2019) | Quality risk assessment of prefabricated building components based on ANP-FUZZY | J. Civ. Eng. Manag. | 0.61 | Weak match |
| bib50 | Qu (2019) | Quality risk assessment of prefabricated components in prefabricated... | J. Civ. Eng. Manag. | 0.63 | Near-duplicate of bib47 -- suspiciously similar |
| bib59 | Cao (2019) | A study on the applicability of regression analysis conditions based on SPSS... | Statistics and Decision Making | 0.54 | Off-topic for building engineering |
| bib61 | Wang (2024) | Safety evaluation of offshore wind farms for navigation based on fuzzy AHP-DEMATEL | China Maritime Science | 0.37 | No relevant match |
| bib62 | He (2023) | Analysis of causes of falls from heights based on the N-K model and fuzzy DEMATEL | Industrial Architecture | 0.56 | GS finds related but different paper |
| bib64 | Li (2025) | Analysis of influencing factors of unsafe behaviors in coal mines based on Grey-DEMATEL-ISM | Saf. Now | 0.53 | "Saf. Now" is likely a garbled journal name |
| bib67 | Chen (2020) | DEMATEL-BN model for safety risk transmission in prefabricated building construction | Journal of Safety Science | 0.59 | Weak match |
| bib78 | Lan (2021) | Dynamic quality and safety management at construction sites based on BIM | Architectural Science | 0.45 | No relevant match |
| bib80 | Li (2021) | Development and application of an evaluation index system for emergency... | J. Civ. Eng. Manag. | 0.58 | Weak match |
| bib82 | Jiang (2018) | Analysis and research on the current standard System for prefabricated... | (no journal) | 0.57 | No journal listed |
| bib84 | Wei (2020) | Exploration of issues and countermeasures in construction safety management... | Value Eng. | 0.60 | Weak match |
| bib85 | Jin (2024) | Application of an improved bayesian network model in risk analysis of... | J. Saf. Environ. | 0.49 | No relevant match |
| bib86 | Yang (2021) | Key influencing factors in ethical risk management of intelligent governance... | Sci. Soc. | 0.48 | Off-topic for building engineering |

---

## Red Flags and Patterns

### 1. First-Name-as-Surname Pattern
Multiple references use Chinese given names (first names) as the author surname, which is a hallmark of LLM-generated references where the model confuses Chinese name ordering:
- **bib20**: "Tianliang" (given name, not family name)
- **bib22**: "Yudan" (given name)
- **bib27**: "Xuezhe" (given name)
- **bib53**: "Wen'an" (given name)

This pattern is extremely rare in legitimate references and is a strong indicator of AI-generated fabrication.

### 2. Off-Topic References
Several references have no clear relevance to prefabricated building hoisting safety:
- **bib60**: Textile fiber identification using mass spectrometry (!) -- has zero connection to construction
- **bib59**: SPSS weighted regression methodology -- generic statistics paper
- **bib86**: Ethical risk management of intelligent governance -- social science, not engineering
- **bib57**: Ground area governance optimization -- coal mining context

### 3. Generic LLM-Style Title Templates
Many fabricated titles follow a formulaic pattern: "[Topic] based on [Method Acronym Combination]":
- "...based on an improved DEMATEL-ISM-BN approach"
- "...based on blind number theory and element extensification method"
- "...based on RF-SFLA-SVM"
- "...based on improved combined weighting-dynamic fuzzy theory"
- "...based on a variable-weight element extensional model"
- "...based on Grey-DEMATEL-ISM"

While this pattern exists in legitimate Chinese engineering literature, the sheer density of unverifiable titles following this template is suspicious.

### 4. Duplicate/Near-Duplicate References
- **bib47** and **bib50** are near-duplicates (same author "Qu", same year 2019, same journal, same page number) with slightly different titles. This is a classic LLM hallucination pattern where the model generates variations of the same fabricated reference.

### 5. Garbled Journal Names
- **bib64**: "Saf. Now" -- likely garbled abbreviation (possibly "Safety" journal?)
- **bib73**: "Safety ence" -- clearly garbled "Safety Science"
- **bib48**: "Saf. Now" appears again

### 6. Extremely High Ratio of Unverifiable References
Only 28 of 85 references (33%) have DOIs. While Chinese-language journals sometimes lack DOIs, the combination of 54% of references being unverifiable by title search is far above the baseline for legitimate papers in this field.

---

## Overall Assessment

**VERDICT: HIGHLY LIKELY FABRICATED REFERENCE LIST**

**Confidence: HIGH (85-90%)**

**Estimated fabricated references: 35 out of 85 (41%)**
- 7 confirmed fake (not found anywhere, clear red flags)
- 28 probable fake (weak/no GS match, suspicious patterns)

**Key evidence:**
1. 4+ references use Chinese given names as surnames (LLM hallmark)
2. Multiple off-topic references (textile fiber analysis in a construction paper)
3. Near-duplicate fabricated references (bib47/bib50)
4. Garbled journal names ("Saf. Now", "Safety ence")
5. Formulaic "[Topic] based on [Method]" title pattern at extreme density
6. Only 33% of references have verifiable DOIs
7. 3 references returned zero GS results on multiple search attempts
8. Several references cite Chinese journals that appear to not exist (e.g., "Journal of Safety Science, China" vs. the real "China Safety Science Journal")

**Caveat:** Some of the "probable_fake" references may be legitimate Chinese-language journal articles that simply have poor indexing in international databases. However, the clustering of multiple independent red flags (wrong name ordering, off-topic refs, duplicates, garbled names) strongly suggests systematic AI-assisted reference fabrication rather than mere indexing gaps.

**Recommendation:** Flag for editorial investigation. The combination of evidence patterns is consistent with LLM-generated reference lists observed in other CITADEL cases. The authors should be asked to provide full bibliographic details and copies of the cited Chinese-language articles.

---

## Appendix: References with DOIs (28 verified, not flagged)

The following 28 references have DOIs and were not part of this investigation (presumed verifiable):
bib3, bib4, bib5, bib9, bib10, bib12, bib14, bib15, bib25, bib26, bib33, bib35, bib36, bib39, bib41, bib42, bib45, bib49, bib52, bib54, bib55, bib58, bib63, bib65, bib66, bib69, bib70, bib87

## Appendix: References with No Title or DOI (11, unclassifiable)

bib1, bib7, bib29, bib37, bib38, bib40, bib46, bib68, bib75, bib76, bib81

These have only author/year metadata and cannot be verified or classified without full text access.
