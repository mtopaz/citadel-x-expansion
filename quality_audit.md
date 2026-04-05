# CITADEL-X Quality Audit Report

**Date**: 2026-04-05
**Auditor**: Quality re-verification of all confirmed/probable fabrication cases
**Method**: Re-checked strongest evidence per case via CrossRef DOI resolution and Google Scholar (Serper.dev) title search. Each DOI was re-resolved live; each title was re-searched with top-5 results examined for similarity.

---

## Summary

| Metric | Count |
|--------|-------|
| Cases audited | 12 |
| Upheld as HIGH confidence (>90%) | 6 |
| Upheld as MEDIUM confidence (60-90%) | 3 |
| Downgraded to LOW confidence (30-60%) | 2 |
| RETRACTED (false positive) | 1 |

**Overall finding**: 9 of 12 cases hold up under re-examination (6 HIGH + 3 MEDIUM). Two cases are weak but not dismissible. One case (Case 9) should be retracted from the confirmed list -- it has only a single DOI mismatch and most unverifiable refs are from legitimately obscure Chinese journals.

---

## Case-by-Case Review

### Case 1: MRE ae45fa -- Materials Research Express (17/66 refs)
**Article**: "An experimental investigation on longevity and mechanical characteristics of high-performance concrete incorporating copper slag as replacement of fine aggregate"

**Evidence re-checked**:
- **Ref 7 DOI (10.1007/978-981-19-5162-6)**: CONFIRMED -- still resolves to "Plant Fiber Reinforced Composites" (sim=0.28 vs claimed "Durability enhancement of HPC using mineral admixtures"). Completely different work. The DOI format (978-...) is a book ISBN-style DOI, incompatible with the claimed ASCE journal article.
- **Ref 8 DOI (10.3390/ma1621114)**: CONFIRMED -- still returns HTTP 404. This DOI does not exist in any format variation. The claimed paper cannot be found.
- **Ref 4 title ("Optimizing the use of SCMs in concrete")**: CONFIRMED NOT FOUND. Best GS match is "Optimizing the use of fly ash in concrete" (sim=0.89, 771 citations) -- a real paper by Thomas, but the claimed ref broadened "fly ash" to the generic "SCMs". This is a classic LLM paraphrase of a real paper.
- **Ref 6 title ("Effect of silica fume on durability and microstructure of HPC")**: CONFIRMED NOT FOUND. Best GS match is "Effect of ferrosilicon and silica fume on mechanical, durability, and microstructural properties..." (sim=0.62, 277 citations) -- different paper entirely.

**Evidence quality**:
- Strong evidence: 2 DOI mismatches (one resolves to unrelated book, one 404), 13 titles not found anywhere
- Weak evidence: 0
- False positives found: 0

**Revised confidence: HIGH (>95%)**
Two DOI mismatches are definitive. The 13 unfindable titles with generic formulaic patterns concentrated in refs 3-16 are highly consistent with LLM-generated literature review padding. No ambiguity.

---

### Case 2: J. Mol. Liquids 129534 -- (16/56 refs)
**Article**: "Comparative evaluation of surfactant and bile salt micelles mediated delivery of drugs to human serum albumin in aqueous media"

**Evidence re-checked**:
- **Ref 50 DOI (10.1083/jcb.200305137)**: CONFIRMED -- resolves to "p120 catenin associates with kinesin and facilitates the transport of cadherin-catenin complexes to intercellular junctions" (sim=0.32). Cell biology paper, completely unrelated to micelle chemistry.
- **Ref 52 DOI (10.1002/jps.10329)**: CONFIRMED -- resolves to "Separation and Characterization of the Colloidal Phases Produced on Digestion of..." (sim=0.03). Same author (Kossena), same journal, same year -- but completely fabricated title. Sophisticated fabrication using real metadata.
- **Ref 14 title ("Bile salt-induced permeation enhancement")**: CONFIRMED NOT FOUND. Best GS match (sim=0.46) is about bio-surfactants, not matching. No paper with this title by Maher in Pharmaceutics 2019 exists.
- **Ref 32 title ("Micelle formation and protein-surfactant interactions: a thermodynamic perspective")**: CONFIRMED NOT FOUND. Best GS match (sim=0.57) is "Polymer-surfactant and protein-surfactant interactions" -- different paper entirely.

**Evidence quality**:
- Strong evidence: 3 DOI mismatches (all resolve to completely different papers), 13 titles not found in any database
- Notable sophistication: Ref 52 and Ref 54 use real DOIs from same authors/journals but fabricated titles -- designed to pass cursory checks
- Weak evidence: 0
- False positives found: 0

**Revised confidence: HIGH (>95%)**
Three DOI mismatches with completely unrelated papers, plus 13 unfindable titles with a distinctive JPCB cluster (refs 34-36). The fabrication shows moderate sophistication (real metadata + fake titles). Extremely solid case.

---

### Case 3: J. Building Engineering 115980 -- (35/85 refs)
**Article**: "Analysis of safety influencing factors in prefabricated building hoisting based on an improved DEMATEL-ISM method"

**Evidence re-checked**:
- **bib60 ("Rapid identification of textile fiber constituents using microturbret plasma ionization mass spectrometry")**: CONFIRMED NOT FOUND AND OFF-TOPIC. GS returns only generic textile/mass-spec results (best sim=0.35). "Microturbret" is not a real analytical chemistry term. A textile fiber analysis paper in a building safety article has zero relevance.
- **bib51 ("Safety risk assessment of hoisting construction in prefabricated buildings based on a variable-weight element extensional model")**: CONFIRMED NOT FOUND. GS returned zero results. Completely empty search.
- **bib2 ("Research on construction quality evaluation of prefabricated residential buildings")**: NOT FOUND. Best GS match (sim=0.62) is a different paper.
- **bib64 journal "Saf. Now"**: CONFIRMED GARBLED. GS search for its title returned no match (best sim=0.45).

**Evidence quality**:
- Strong evidence: 7 confirmed fakes (bib60 off-topic + nonexistent term "microturbret"; bib51 zero GS results; 4 first-name-as-surname errors; near-duplicate bib47/bib50)
- Moderate evidence: 28 probable fakes with weak GS matches (sim 0.20-0.68)
- Weak evidence: Some of the 28 "probable fakes" may be legitimate Chinese-language journal articles poorly indexed in Western databases -- this is the main caveat

**Revised confidence: HIGH (85-90%)**
The first-name-as-surname pattern (Tianliang, Yudan, Xuezhe, Wen'an), the off-topic textile fiber ref with fabricated terminology, garbled journal names ("Saf. Now", "Safety ence"), and near-duplicate refs are all strong independent signals. Even if half the "probable fakes" turned out to be real Chinese papers, 7 confirmed fakes plus the multiple red-flag patterns make this a solid case. Slight downgrade from 95% due to the Chinese-journal caveat.

---

### Case 4: Solid State Communications 116386 -- (5/60 refs)
**Article**: "Influence of Mn-doped BaSO4 nanoparticles: Structural, functional, optical, morphological, thermal and antimicrobial studies"

**Evidence re-checked**:
- **Ref 35 DOI (10.1016/j.saa.2014.08.080)**: CONFIRMED DOI MISMATCH. Resolves to "Synthesis, characterization and anti-bacterial activities of pure and **Co-doped** BaSO4..." (sim=0.67). The claimed title says "Ni-doped" but the real paper is "Co-doped". Author name also doesn't match. Classic DOI-title swap with element substitution.
- **Ref 57 title ("Green synthesis of magnesium oxide nanoparticles for effective antibacterial activity against Pseudomonas aeruginosa")**: CONFIRMED NOT FOUND. Best GS match (sim=0.74) is "Green synthesis of magnesium oxide nanoparticles and their antibacterial activity" -- a 2012 paper from IJMS, not by Nguyen, not from 2022, different journal.
- **Ref 52 title ("Morphological diversity of magnesium oxide nanostructures for improved antibacterial and anticancer activities")**: CONFIRMED NOT FOUND. Best GS match (sim=0.60) is about MgO fabrication/photocatalysis -- different paper entirely.

**Evidence quality**:
- Strong evidence: 1 DOI mismatch (Ni-doped vs Co-doped -- clear element substitution fabrication), 4 titles not found
- Weak evidence: 0
- False positives found: 0
- Note: Lower absolute count (5 fakes) but all 5 are confirmed

**Revised confidence: HIGH (>90%)**
All 5 flagged refs confirmed fake. The DOI element-substitution trick (Co->Ni) is a distinctive and deliberate fabrication. The chimera reference (ref 53: real author + wrong plant species + wrong journal) shows sophistication. Small number of fakes but 100% hit rate on flags.

---

### Case 5: J. Computational Science 102852 -- (~20/30 refs, 67%)
**Article**: "Influence of different jet fuels on the infrared radiation characteristics of spherical convergent 2D nozzles"

**Evidence re-checked**:
- **Ref 1 ("Key Technologies for collaborative design of high-performance fighter aircraft and engine", claimed Chin. J. Aeronaut. 2024)**: CONFIRMED NOT FOUND. GS returns unrelated results (best sim=0.45). CJA is fully SCI-indexed and English-language. Any 2024 paper would be findable. Definitive.
- **Ref 28 ("Cooling, Aerodynamic and Infrared Radiation Characteristics of Film-Cooled Vectoring Nozzles", claimed Chin. J. Aeronaut. 2025)**: CONFIRMED NOT FOUND. Best GS match (sim=0.60) is a related but different paper. CJA would have this if it existed. Definitive.
- **Ref 27 (self-citation, claimed Gas. Turbine Exp. Res. 2021)**: CONFIRMED NOT FOUND. GS returned the present article itself as second hit (sim=0.53). First author Guo cannot have published this unfindable paper.

**Evidence quality**:
- Strong evidence: 4 confirmed fakes (2 in fully-indexed CJA that don't exist, 1 unfindable self-citation, 1 in implausible venue "J. Chengde Pet. Coll.")
- Moderate evidence: 14 probable fakes in Chinese domestic journals -- more defensible here than Case 3 because (a) the confirmed CJA fakes prove fabrication intent, (b) 67% fabrication rate is extreme, (c) formulaic title templates are dense
- Weak evidence: 1 possible translation variant (ref 20, sim=0.91)
- False positives found: 0

**Revised confidence: HIGH (>95%)**
The CJA evidence is the linchpin: these are claimed to be in a fully-indexed, English-language journal and simply do not exist. Combined with unfindable self-citation, the highest fabrication rate in the dataset (67%), and implausible venue assignments (aerospace paper in petroleum college journal). Ironclad case.

---

### Case 6: Physica B 417962 -- (~13/32 refs, 41%) [PROBABLE]
**Article**: "Rare-earth engineering of NaAlO3 perovskites unlocks unified optoelectronic, thermoelectric, and spintronic functionalities"

**Evidence re-checked**:
- **Ref 15 ("Rare-earth-doped inorganic materials for optoelectronics: from fundamentals to applications", claimed Chem. Rev. 2017)**: CONFIRMED NOT FOUND. Best GS match (sim=0.48) is "Rare-earth doping in nanostructured inorganic materials" in Chem. Rev. (1055 citations) -- a real review, but with a completely different title and published in 2021 not 2017. The claimed paper does not exist in Chem. Rev. A ghost reference in one of chemistry's most prestigious journals.
- **Ref 18 ("Multifunctional behavior of lanthanide-doped perovskites: a review", claimed Prog. Mater. Sci. 2019)**: CONFIRMED NOT FOUND. Best GS match (sim=0.49) is about lanthanide-doped halide perovskite nanocrystals -- different topic, different journal. No such review exists in Progress in Materials Science.
- **Ref 24 ("Correlated rare-earth oxides: the role of 4f electrons", claimed J. Phys. Condens. Matter 2012)**: CONFIRMED NOT FOUND. Best GS match (sim=0.38) is about 4f levels by high-energy spectroscopy (140 citations, 1979) -- completely different paper.

**Evidence quality**:
- Strong evidence: 3 ghost references in highly prestigious, perfectly indexed journals (Chem. Rev., Prog. Mater. Sci., J. Phys. Condens. Matter) -- these journals have near-100% indexing coverage, so absence is definitive
- Strong evidence: Duplicate phantom references (refs 12/29 and 13/30 are identical) -- hallmark of LLM generation loops
- Moderate evidence: Formulaic titles clustered in literature review section (refs 5-18)
- Weak evidence: Some refs with sim 0.85-0.87 could be paraphrases of real papers
- False positives found: 0

**Revised confidence: HIGH (90%)**
Upgraded from PROBABLE to HIGH. The ghost references in Chem. Rev. and Prog. Mater. Sci. are definitive -- these are among the world's most well-indexed journals. Combined with duplicate phantom references (identical entries at two different positions), this is strong evidence. Upgrading to confirmed.

---

### Case 7: Construction and Building Materials 144502 -- (~14/42 refs, 33%)
**Article**: "Study on water permeability of hydraulic concrete under freeze-thaw deterioration based on microscopic pore structure evolution"

**Evidence re-checked**:
- **Ref 15 ("Deep learning shield attitude prediction model based on grey relational analysis")**: CONFIRMED NOT FOUND AND OFF-TOPIC. Best GS match (sim=0.59) is about shield tunneling prediction -- completely unrelated to concrete permeability. This is a shield tunneling / mining reference in a concrete paper.
- **Ref 16 ("Correlation analysis and prediction study between mine water inflow and rainfall")**: CONFIRMED NOT FOUND AND OFF-TOPIC. GS matches are about mine water inflow modeling (sim=0.38-0.40) -- completely unrelated to concrete. Two consecutive off-topic refs from different domains.
- **Ref 1 ("Study on evolution of freezing stress and its influence on frost resistance of concrete")**: CONFIRMED NOT FOUND. Best GS match (sim=0.63) is a related but different paper.
- **Ref 10 ("Study on the relationship between microscopic pore structure and permeability of concrete")**: CONFIRMED NOT FOUND. Best GS match (sim=0.59) is a different paper on pore structure.

**Evidence quality**:
- Strong evidence: 2 completely off-topic refs (shield tunneling + mine water in a concrete paper), malformed journal abbreviations ("J. ]. Mater. Rep.", "J. ]. Concr."), 14 unfindable titles
- Moderate evidence: Formulaic "Study on the relationship between X and Y" title pattern
- Weak evidence: Some of the 14 may be Chinese domestic journal papers, though the malformed abbreviations suggest machine-generated rather than manually cited refs
- False positives found: 3 (confirmed real on GS)

**Revised confidence: MEDIUM (75%)**
The two off-topic references and malformed journal names are strong signals. However, this paper cites many Chinese domestic journals and the "Study on X" title pattern is genuinely common in Chinese academic literature (not just LLM-generated). The case would be stronger with DOI mismatch evidence. Keeping at MEDIUM because evidence relies primarily on title-not-found + off-topic refs, without the harder DOI evidence seen in stronger cases.

---

### Case 8: Materials Research Express ae284b -- (~8/64 refs, 13%)
**Article**: "Identifying the optimal process parameters to minimize the solid particle erosion rate of heat-treated Ti-6Al-5Zr-0.5Mo-0.2Si alloy using response surface methodology"

**Evidence re-checked**:
- **Ref 1 ("Angle-resolved erosion characteristics of metal alloys under cyclic impact")**: CONFIRMED NOT FOUND. Best GS match (sim=0.50) is about angle-resolved secondary ion mass spectrometry -- completely unrelated. Zero relevant erosion papers with this title.
- **Ref 2 ("Effect of impact angle and heat treatment on erosion of titanium alloys")**: CONFIRMED NOT FOUND. Best GS match (sim=0.68) is "Effect of heat treatment on erosive wear behaviour of Ti6Al4V alloy" -- similar topic but different title and scope.
- **Ref 3 ("Influence of particle velocity and shape on erosion wear of advanced engineering alloys")**: CONFIRMED NOT FOUND. Best GS match (sim=0.59) is "Influence of material hardness and particle velocity on erosive wear rate" -- different paper with 13 citations.

**Evidence quality**:
- Strong evidence: 8 refs claim well-indexed international journals (Tribology International, Wear, Surface & Coatings Technology) but cannot be found. These journals have excellent indexing -- real papers would be findable. This distinguishes these from Chinese domestic journal false positives.
- Moderate evidence: Formulaic "Effect of X on Y" title pattern, though this is common in erosion literature
- Weak evidence: Ref 2 has a sim=0.68 GS match that could potentially be a title variant (but different enough to be a distinct paper)
- False positives found: 2 (confirmed real on GS)

**Revised confidence: MEDIUM (70%)**
The key distinction is that these refs claim to be in well-indexed international journals (not Chinese domestic). Real papers in Tribology International and Wear would be found on GS. However, the lower fabrication rate (13%) and the absence of DOI mismatches or other hard evidence (no off-topic refs, no garbled journals, no name errors) makes this a weaker case than most. The titles, while formulaic, are not dramatically outside normal erosion research titling conventions. Keeping at MEDIUM.

---

### Case 9: Construction and Building Materials 146195 -- (1 confirmed/43 refs) [PROBABLE]
**Article**: "Experimental study on loess earthen-mortar ancient brick masonry under uniaxial compression and damage constitutive model"

**Evidence re-checked**:
- **Ref 11 DOI (10.3901/JME.2020.04.218)**: CONFIRMED DOI MISMATCH. Resolves to "Filtration System for Hydraulic Actuators of FAST" (sim=0.26). This is about the FAST radio telescope's hydraulic filtration system -- completely unrelated to ancient brick masonry. Definitive fabrication for this single reference.
- **Ref 11 title ("Constitutive relationship of alkali slag ceramic aggregate concrete masonry")**: CONFIRMED NOT FOUND on GS. Best match (sim=0.49) is about alkali-activated mortars -- different paper.

**Evidence quality**:
- Strong evidence: 1 DOI mismatch (definitive for that single ref)
- Moderate evidence: 0
- Weak evidence: 7 other unverifiable refs are from Chinese domestic civil engineering journals spanning 1981-2025 (pre-digital era). The article topic (ancient Chinese brick masonry) is a niche field that naturally cites old, poorly-indexed Chinese literature.
- False positives found: 2 (confirmed real on GS)

**Revised confidence: RETRACT from confirmed list**
One DOI mismatch proves one reference is fabricated. But a single wrong DOI in a paper about ancient Chinese masonry -- citing many legitimately obscure Chinese domestic journals from the 1980s -- does not meet the threshold for "confirmed fabrication case." This could be a copy-paste error or a metadata mistake rather than systematic LLM-generated fabrication. There are no other corroborating signals: no formulaic titles, no off-topic refs, no garbled journals, no name errors, no duplicate refs. The remaining 7 unverifiable refs are exactly what you'd expect from a paper on ancient Chinese masonry. **Recommendation: Downgrade to "single DOI error noted" and remove from the confirmed fabrication list.** If we are claiming publication-quality evidence of systematic fabrication, this case does not meet that bar.

---

### Case 10: Information Sciences 123423 (TumorNet) -- (22-24/50 refs, 44-48%)
**Article**: "TumorNet: A hybrid lightweight framework for brain tumor classification and reasoning"

**Evidence re-checked**:
- **DOI mismatch (10.1016/j.mri.2024.06.001)**: CONFIRMED. Resolves to "Comparison of the value of adipose tissues in abdomen and lumbar vertebra for predicting disease activity in Crohn's disease..." (sim=0.17). A Crohn's disease MRI study, completely unrelated to brain tumors.
- **"Fine-tuned resnet50 for glioma grading using brats-2019 MRI dataset"**: CONFIRMED NOT FOUND. Best GS match (sim=0.46) is about vision transformers for brain tumor classification -- completely different paper.
- **"Resnet50 with bigru and dual attention for multi-class brain tumor classification"**: CONFIRMED NOT FOUND. Best GS match (sim=0.33) is about ResNet50 with convolutional block attention -- different paper.
- **"EfficientNetV2-driven deep hybrid network for high-precision brain tumor MRI classification"**: CONFIRMED NOT FOUND. GS returned zero results. Complete absence.

**Evidence quality**:
- Strong evidence: 1 DOI mismatch (Crohn's disease vs brain tumors), 22+ titles not found, systematic formulaic template "[Architecture]-based [modifier] for brain tumor MRI classification"
- The template-generation pattern is unmistakable: the LLM generated a reference for each major deep learning architecture (ResNet, VGG, DenseNet, EfficientNet, RegNet, MobileNet) applied to brain tumor classification, each with plausible-sounding but non-existent titles
- False positives found: 0 (the 2 "found" refs were paraphrases of real papers with modified titles -- still fabricated in form)

**Revised confidence: HIGH (>95%)**
One of the strongest cases in the dataset. The systematic template pattern, DOI mismatch to a completely unrelated medical field, and the sheer number of unfindable refs (22+) leave no room for doubt. The formulaic title-generation pattern is a textbook example of LLM reference hallucination.

---

### Case 11: Applied Soft Computing 114970 (IT-2 Fuzzy Automata) -- (17/36 refs, 47%)
**Article**: "Design and optimization of minimization algorithms for IT-2 general fuzzy automata"

**Evidence re-checked**:
- **"Interval type-2 fuzzy decision support systems in healthcare"**: CONFIRMED NOT FOUND. Best GS match (sim=0.57) is "An interval type-2 fuzzy multi-criteria decision-making approach for patient bed allocation" -- related topic but different paper entirely.
- **"A hybrid PSOGA algorithm for fuzzy system optimization"**: CONFIRMED NOT FOUND. Best GS match (sim=0.77) is "A hybrid PSO-GA algorithm for constrained optimization problems" (967 citations) -- a real paper on PSO-GA but NOT about fuzzy systems. The claimed title appears to paraphrase this real paper's title while adding "fuzzy system".
- **"Shadowed type-2 fuzzy sets for intelligent control"**: CONFIRMED NOT FOUND. Best GS match (sim=0.61) is "Shadowed type-2 fuzzy logic systems" (17 citations) -- a real paper by Mendel, but different title and not about "intelligent control." The claimed ref paraphrases this real paper with added scope.

**Evidence quality**:
- Strong evidence: 17 of 18 flagged refs not found on GS. The titles read like LLM topic descriptions ("X in Y" format) rather than real paper titles. The fuzzy logic field is well-indexed in Western databases -- there is no Chinese/Turkish journal excuse.
- The "hybrid PSOGA" example is instructive: the LLM clearly drew from the real, highly-cited PSO-GA paper but fabricated a fuzzy-systems version of it
- Weak evidence: 1 title variant of a real book (Mordeson & Malik)
- False positives found: 0

**Revised confidence: HIGH (93%)**
Well-indexed field with no regional indexing excuse. 17/18 unfindable titles with a consistent LLM-descriptive-title pattern. The "topic description as paper title" pattern is distinctive -- these sound like textbook sections, not research papers. Strong case.

---

### Case 12: Expert Systems with Applications 131840 (TNStream) -- (~10-16/78 refs, 13-21%) [PROBABLE]
**Article**: "TNStream: Applying tightest neighbors to micro-clusters to define multi-density clusters in streaming data"

**Evidence re-checked**:
- **DOI mismatch (10.1007/s11390-019-1964-2)**: CONFIRMED. Resolves to "DEMC: A Deep Dual-Encoder Network for Denoising Monte Carlo Rendering" (sim=0.21). Monte Carlo rendering vs stream clustering -- completely unrelated.
- **"DPClust: A novel data stream clustering algorithm"**: CONFIRMED NOT FOUND. Best GS match (sim=0.64) is a review paper. No algorithm named "DPClust" exists in the stream clustering literature.
- **"Akan: A new approach for real-time data stream clustering"**: CONFIRMED NOT FOUND. GS returned Turkish-language results (sim=0.16) and generic stream processing papers. No algorithm named "Akan" exists.
- **"KD-stream: A real-time clustering approach"**: CONFIRMED NOT FOUND. GS returned zero results.

**Evidence quality**:
- Strong evidence: 1 DOI mismatch, 3+ invented algorithm names (DPClust, KD-stream, Akan -- these algorithm names do not exist in the literature), ~7 fully fabricated titles
- Moderate evidence: ~6 refs cite real algorithms (StreamKM++, DGStream, I-HASTREAM) but with paraphrased/modified titles (sim 0.51-0.83) -- this is fabrication of titles even when the cited work is real
- Weak evidence: Some paraphrased titles could be alternative phrasings or conference versions
- False positives found: 0

**Revised confidence: MEDIUM (70%)**
The DOI mismatch and invented algorithm names are definitive evidence of some fabrication. The paraphrased-title pattern (real algorithms, wrong titles) suggests partial LLM assistance rather than wholesale fabrication. The lower flag rate (29%) and mixed nature of evidence place this below the strongest cases. Keeping as PROBABLE is appropriate, though the evidence is credible.

---

## Consolidated Results

| # | Case | DOI | Fabricated Refs | Key Evidence | Evidence Quality | Revised Confidence |
|---|------|-----|----------------|--------------|------------------|--------------------|
| 1 | MRE ae45fa | 10.1088/2053-1591/ae45fa | 17/66 (26%) | 2 DOI mismatches + 13 unfindable titles | STRONG | **HIGH (>95%)** |
| 2 | J. Mol. Liq. 129534 | 10.1016/j.molliq.2026.129534 | 16/56 (29%) | 3 DOI mismatches + 13 unfindable titles | STRONG | **HIGH (>95%)** |
| 3 | J. Build. Eng. 115980 | 10.1016/j.jobe.2026.115980 | 35/85 (41%) | Off-topic ref + nonexistent term + name errors + duplicates | STRONG | **HIGH (85-90%)** |
| 4 | Solid State Commun. 116386 | 10.1016/j.ssc.2026.116386 | 5/60 (8%) | 1 DOI mismatch (element swap) + 4 unfindable | STRONG | **HIGH (>90%)** |
| 5 | J. Comput. Sci. 102852 | 10.1016/j.jocs.2026.102852 | ~20/30 (67%) | 2 CJA ghost refs + unfindable self-cite | STRONG | **HIGH (>95%)** |
| 6 | Physica B 417962 | 10.1016/j.physb.2025.417962 | ~13/32 (41%) | Ghost refs in Chem. Rev./PMS + duplicate phantoms | STRONG | **HIGH (90%)** |
| 7 | Constr. Build. Mater. 144502 | 10.1016/j.conbuildmat.2025.144502 | ~14/42 (33%) | 2 off-topic refs + malformed journal abbrevs | MODERATE | **MEDIUM (75%)** |
| 8 | MRE ae284b | 10.1088/2053-1591/ae284b | ~8/64 (13%) | 8 unfindable in indexed intl journals | MODERATE | **MEDIUM (70%)** |
| 9 | Constr. Build. Mater. 146195 | 10.1016/j.conbuildmat.2026.146195 | 1/43 (2%) | 1 DOI mismatch only | WEAK | **RETRACT** |
| 10 | Info. Sci. 123423 | 10.1016/j.ins.2026.123423 | 22-24/50 (44-48%) | DOI mismatch + template-generated titles | STRONG | **HIGH (>95%)** |
| 11 | Appl. Soft Comput. 114970 | 10.1016/j.asoc.2026.114970 | 17/36 (47%) | 17/18 unfindable in well-indexed field | STRONG | **HIGH (93%)** |
| 12 | Expert Syst. Appl. 131840 | 10.1016/j.eswa.2026.131840 | ~10-16/78 (13-21%) | DOI mismatch + invented algorithm names | MODERATE | **MEDIUM (70%)** |

---

## Recommendations for the Paper

### Cases suitable for publication as confirmed fabrications (HIGH confidence, N=8):
1. **Case 1** (MRE ae45fa) -- Materials science, 26% fake, DOI + title evidence
2. **Case 2** (J. Mol. Liq.) -- Chemistry, 29% fake, DOI + title evidence, sophisticated fabrication
3. **Case 3** (J. Build. Eng.) -- Construction, 41% fake, multiple independent red flags
4. **Case 4** (Solid State Commun.) -- Materials science, 8% fake, element-swap DOI trick
5. **Case 5** (J. Comput. Sci.) -- Aerospace engineering, 67% fake, CJA ghost refs
6. **Case 6** (Physica B) -- Condensed matter, 41% fake, ghost refs in top journals + duplicates (upgraded from PROBABLE)
7. **Case 10** (Info. Sci., TumorNet) -- CS/AI, 44-48% fake, template-generated refs
8. **Case 11** (Appl. Soft Comput., Fuzzy) -- CS/AI, 47% fake, topic-description-as-title pattern

### Cases to present with caveats (MEDIUM confidence, N=3):
9. **Case 7** (Constr. Build. Mater. 2025) -- 33% fake, off-topic refs but Chinese journal caveat
10. **Case 8** (MRE ae284b) -- 13% fake, unfindable in indexed journals but no DOI evidence
11. **Case 12** (Expert Syst. Appl., TNStream) -- 13-21% fake, mixed fabrication + paraphrasing

### Case to remove from confirmed list (N=1):
12. **Case 9** (Constr. Build. Mater. 2026) -- Single DOI error insufficient for "confirmed fabrication"; may be metadata error rather than systematic fabrication

---

## Methodological Notes

### What constitutes STRONG evidence of fabrication:
1. **DOI resolves to completely different paper** (sim < 0.30) -- the gold standard
2. **Title claimed in fully-indexed journal but absent** (e.g., CJA, Chem. Rev., Tribology International) -- these journals have near-100% GS/CrossRef coverage
3. **Multiple independent red flags in one paper** -- off-topic refs, garbled journal names, first-name-as-surname, duplicate phantom refs, nonexistent terminology ("microturbret")
4. **Template-generated title patterns** -- systematic formulaic variation across multiple refs (e.g., "[Architecture] for brain tumor MRI classification")

### What does NOT constitute strong evidence:
1. **Title not found + Chinese/Turkish domestic journal** -- many legitimate journals are poorly indexed in Western databases
2. **Single DOI error** without corroborating signals -- could be copy-paste mistake
3. **Formulaic-sounding title alone** -- the "Research on X based on Y" pattern is standard Chinese academic phrasing

### Estimated total fabricated references across all cases:
- HIGH confidence cases (8): ~145 fabricated references
- MEDIUM confidence cases (3): ~32 fabricated references
- Combined: ~177 fabricated references across 11 articles (excluding Case 9)

---

*Quality audit performed 2026-04-05 using live CrossRef DOI resolution and Google Scholar (Serper.dev) re-verification.*
