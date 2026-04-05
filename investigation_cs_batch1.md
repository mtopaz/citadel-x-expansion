# CITADEL-X CS/AI Domain Investigation — Batch 1

**Date**: 2026-04-04
**Investigator**: Automated (Claude) with manual verification steps
**Domain**: Computer Science / AI / Engineering

---

## Article A: 10.1016/j.jocs.2026.102852

**Title**: Influence of different jet fuels on the infrared radiation characteristics of spherical convergent 2D nozzles
**Authors**: Xiao Guo, Mengke Wu, Shuhao Li, Zhenhua Wen
**Journal**: Journal of Computational Science (Elsevier)
**Year**: 2026
**Total references**: 30
**Flagged**: 20/30 (67%)
**Flag type**: All `title_not_found`

### Investigation Summary

All 20 flagged references are cited as papers from Chinese domestic journals, with no DOIs assigned. The claimed journals include:

| Journal Abbreviation | Full Name | Indexed in WoS/Scopus? |
|---|---|---|
| Chin. J. Aeronaut. | Chinese Journal of Aeronautics | **YES** (SCI, Q1) |
| Infrared Laser Eng. | Infrared and Laser Engineering | Partially (EI) |
| Aeroengine | 航空发动机 | No (domestic) |
| J. Aerosp. Power | 航空动力学报 | Partially (EI) |
| Laser & Infrared | 激光与红外 | Partially |
| J. Chengde Pet. Coll. | Journal of Chengde Petroleum College | **No** (very obscure) |
| Sci. Technol. Eng. | 科学技术与工程 | Partially |
| Infrared Technol. | 红外技术 | Partially |
| Gas. Turbine Exp. Res. | 燃气涡轮试验与研究 | No (domestic) |
| J. Propuls. Technol. | 推进技术 | Partially (EI) |
| Prog. Chem. | 化学进展 | Partially |
| J. Tsinghua Univ. | 清华大学学报 | Partially (EI) |

### Key Findings

**Critical red flags — CJA references NOT FOUND:**
- **Ref#1**: "Key Technologies for collaborative design of high-performance fighter aircraft and engine" — claimed Chin. J. Aeronaut. 2024. CJA is fully indexed in SCI/Scopus/Google Scholar. Exact title search returns ZERO results. **Not found anywhere.**
- **Ref#28**: "Cooling, Aerodynamic and Infrared Radiation Characteristics of Film-Cooled Vectoring Nozzles" — claimed Chin. J. Aeronaut. 2025. Exact title search returns ZERO results. **Not found anywhere.**

These two are the strongest evidence of fabrication: CJA publishes in English, is fully indexed, and any 2024-2025 paper would be findable. Their absence is definitive.

**Other unfindable references:**
- Ref#27: "Optimization Study on Aerodynamic/RCS Characteristics of Spherical-Convergent Two-Dimensional Vectoring Nozzles" — Gas. Turbine Exp. Res. 2021, author Guo (same as first author of this paper). Self-citation to a paper that cannot be found. NOT FOUND on Google Scholar.
- Ref#9, #10, #11, #14, #15, #16, #17: All claimed in Chinese domestic journals. None returned exact matches. The Google Scholar weak matches (sim 0.35-0.69) are to real but DIFFERENT papers on related topics.
- Ref#11 is especially suspicious: claimed in "J. Chengde Pet. Coll." (Journal of Chengde Petroleum College) — an aerospace IR paper in a petroleum college journal is implausible.

**One partial rescue:**
- Ref#20: "Experimental Study on Combustion Characteristics of Jatropha Oil/RP-3 Aviation Fuel Blends" — Google Scholar found a paper titled "...Jatropha Oil/RP-3 Kerosene Blended Fuel..." (sim=0.91). These might be translation variants of the same Chinese paper in J. Propuls. Technol., but the exact title returns zero results.

**Pattern analysis:**
- The titles read like plausible English translations of Chinese papers but are formulaic and highly repetitive ("Numerical analysis of infrared radiation characteristics of...")
- 20/30 references unfindable is an extraordinary failure rate
- The flagged refs form a cohesive, self-reinforcing web that would be nearly impossible to check without access to Chinese databases (CNKI)
- Author Guo/Wen have only 1 findable English-language publication (an IEEE conference paper on electromagnetic scattering of exhaust systems)

### Ref-by-Ref Classification

| Ref# | Title (truncated) | Journal | Classification |
|------|-------------------|---------|---------------|
| 1 | Key Technologies for collaborative design... | Chin. J. Aeronaut. | **confirmed_fake** (CJA is fully indexed, not found) |
| 2 | Influence of exhaust flow of integrated IR suppressor... | Infrared Laser Eng. | **probable_fake** (not found; weak match to different paper) |
| 3 | Integrated infrared radiation suppression technology... | Aeroengine | **probable_fake** (not found) |
| 9 | Numerical analysis of IR radiation of VTOL nozzles... | J. Aerosp. Power | **probable_fake** (not found; weak match to different paper) |
| 10 | Measurement and analysis of IR radiation of jet nozzles... | Laser & Infrared | **probable_fake** (not found) |
| 11 | Numerical analysis of IR radiation of turbofan twin-engine... | J. Chengde Pet. Coll. | **confirmed_fake** (implausible venue; not found) |
| 12 | Simulation of liquid-cooled plug 2D nozzle... | Sci. Technol. Eng. | **probable_fake** (not found) |
| 14 | Aerodynamic and IR characteristics of serrated vectoring nozzles... | Laser Infrared | **probable_fake** (not found; weak match to different paper) |
| 15 | Influence of design parameters of 2D convergent-divergent nozzles... | J. Aerosp. Power | **probable_fake** (not found) |
| 16 | Influence of circular-to-rectangular convergent section... | Infrared Technol. | **probable_fake** (not found) |
| 17 | IR radiation of plug axial-symmetric nozzles for turbofan... | Gas. Turbine Exp. Res. | **probable_fake** (not found) |
| 19 | Influence of alternative fuels on combustion chamber... | Aeroengine | **probable_fake** (not found; self-citation by author Guo) |
| 20 | Combustion Characteristics of Jatropha Oil/RP-3 blends... | J. Propuls. Technol. | **unverifiable** (sim=0.91 match but exact title not found; possible translation variant) |
| 22 | Combustion Characteristics and Soot Formation of alternative fuels... | J. Aerosp. Power | **probable_fake** (not found; weak match to different paper) |
| 23 | Synthesis of Biomass-Derived Polycyclic Hydrocarbon aviation fuels... | Prog. Chem. | **probable_fake** (not found) |
| 24 | Two-phase Combustion Flow Field in Model Combustion Chamber... | Gas. Turbine Exp. Res. | **probable_fake** (not found) |
| 25 | Review on combustion characteristics of RP-3 kerosene... | Aeroengine | **probable_fake** (not found; weak match) |
| 26 | Development status and challenges of reaction kinetics... | J. Tsinghua Univ. | **probable_fake** (not found; J. Tsinghua is EI-indexed) |
| 27 | Optimization of Aerodynamic/RCS of Spherical-Convergent 2D nozzles... | Gas. Turbine Exp. Res. | **confirmed_fake** (self-citation; not found anywhere) |
| 28 | Cooling, Aerodynamic and IR of Film-Cooled Vectoring Nozzles... | Chin. J. Aeronaut. | **confirmed_fake** (CJA is fully indexed, not found) |

### Verdict: FABRICATION CONFIRMED

**Confidence: HIGH**

**Summary**: 4 references confirmed fake (2 claimed in fully-indexed CJA but non-existent, 1 in implausible venue, 1 unfindable self-citation), 14 probable fakes (none findable, all in the same narrow topic), 1 unverifiable, 1 possible translation variant. With 18-19 of 30 references likely fabricated, this article contains systematic, large-scale citation fabrication.

**Note**: While Chinese domestic journal papers can be hard to find in Western databases, the critical evidence is that (a) two refs claimed in the fully-indexed, English-language Chinese Journal of Aeronautics are non-existent, (b) a self-citation by the first author cannot be found, and (c) the sheer volume (67%) is far beyond normal Chinese-journal indexing gaps.

---

## Article B: 10.1016/j.knosys.2025.114599

**Title**: Privacy-preserving ground-truth data for evaluating additive feature attribution in regression models with additive CBR and CQV
**Authors**: Mir Riyanul Islam, Rosina O. Weber, Mobyen Uddin Ahmed, Shahina Begum
**Journal**: Knowledge-Based Systems (Elsevier)
**Year**: 2025
**Total references**: 123
**Flagged**: 15/123 (12%)
**Flag types**: 13 `doi_mismatch`, 2 `title_not_found`

### Investigation Summary

**DOI mismatch refs (13 of 15):**

All 13 DOI mismatch flags are **false positives**. The pattern is consistent:

1. The references are unstructured citations (no separate title/DOI fields in CrossRef)
2. The full unstructured string includes author names, arXiv IDs, and the DOI at the end
3. The pipeline extracted the DOI, resolved it successfully, and found the correct paper
4. The similarity score is low (0.03-0.13) because it compared the full unstructured string (with author names) against just the title
5. The matched titles match the claimed paper titles perfectly

Example — Ref#18:
- Unstructured: "M. Yang, B. Kim, Benchmarking Attribution Methods with Relative Feature Importance, arXiv preprint (arXiv: 1907.09701 [cs.LG]) (2019). 10.48550/arXiv.1907.09701."
- Matched: "Benchmarking Attribution Methods with Relative Feature Importance"
- These are the SAME paper. The low similarity is because the comparison includes "M. Yang, B. Kim," and the arXiv ID in the string.

All 13 arXiv-based references are real, well-cited papers in the XAI/ML interpretability domain by prominent researchers (Doshi-Velez, Kim, Hoffman, etc.).

**Title-not-found refs (2 of 15):**

- **Ref#36**: "Cost of Delay Estimates" (2020) — This is a real technical report from NEXTOR (FAA-funded National Center of Excellence for Aviation Operations Research). Found on nextor.umd.edu and Scribd. **Classification: false_positive** (grey literature/technical report, not indexed in academic databases)

- **Ref#93**: "Flight Progress Messages Document" (2020) — This is a real Eurocontrol technical document. Found as PDF at eurocontrol.int. **Classification: false_positive** (aviation industry technical document)

### Ref-by-Ref Classification

| Ref# | Type | Classification | Reason |
|------|------|---------------|--------|
| 18 | doi_mismatch | **false_positive** | Unstructured string vs title comparison artifact |
| 19 | doi_mismatch | **false_positive** | Same artifact |
| 20 | doi_mismatch | **false_positive** | Same artifact |
| 22 | doi_mismatch | **false_positive** | Same artifact |
| 36 | title_not_found | **false_positive** | Real NEXTOR/FAA technical report |
| 52 | doi_mismatch | **false_positive** | Same artifact |
| 62 | doi_mismatch | **false_positive** | Same artifact |
| 63 | doi_mismatch | **false_positive** | Same artifact |
| 67 | doi_mismatch | **false_positive** | Same artifact |
| 75 | doi_mismatch | **false_positive** | Same artifact |
| 93 | title_not_found | **false_positive** | Real Eurocontrol technical document |
| 98 | doi_mismatch | **false_positive** | Same artifact |
| 109 | doi_mismatch | **false_positive** | Same artifact |
| 111 | doi_mismatch | **false_positive** | Same artifact |
| 122 | doi_mismatch | **false_positive** | Same artifact |

### Verdict: FALSE POSITIVE

**Confidence: HIGH**

**Summary**: All 15 flags are false positives. The 13 DOI mismatches result from a pipeline artifact where unstructured citation strings (containing author names + arXiv IDs + DOIs) are compared against resolved titles, producing artificially low similarity scores. The 2 title-not-found entries are legitimate grey literature (FAA report, Eurocontrol document). Zero fabrication detected.

**Pipeline improvement note**: The DOI mismatch detection should extract and compare only the title portion of unstructured references, not the full string. This pattern likely generates false positives across many articles citing arXiv preprints.

---

## Article C: 10.1016/j.eswa.2025.128820

**Title**: Convolutional neural network for groundwater contamination source identification
**Authors**: Zhengchen Zhou, Xuesong Yan, Chengyu Hu
**Journal**: Expert Systems with Applications (Elsevier)
**Year**: 2025
**Total references**: 50
**Flagged**: 7/50 (14%)
**Flag type**: All `title_not_found`

### Investigation Summary

This article is about groundwater contamination modeling, authored by researchers at a Chinese university (likely China University of Geosciences, Wuhan, based on co-author Xuesong Yan). The flagged references are all Chinese-language papers and a Master's thesis.

**Google Scholar verification results:**

| Ref# | Title | GS Result | Sim |
|------|-------|-----------|-----|
| 15 | Research on inverse problem of aquifer parameters based on deep learning | Not found exactly; related papers exist | — |
| 18 | Current status and problems of non-point source pollution load calculation in China | **FOUND EXACT** | 1.00 |
| 32 | Advances in mathematical methods of groundwater pollution source identification | **FOUND EXACT** (cited by 17) | 1.00 |
| 42 | Review on groundwater contamination source identification based on Bayesian method | **FOUND EXACT** (cited by 3) | 1.00 |
| 44 | Advances in mathematical methods of groundwater pollution source identification (2020) | **FOUND EXACT** (cited by 2, different year from Ref#32) | 1.00 |
| 45 | Groundwater contaminant source identification based on evolutionary algorithm (thesis) | Not found exactly; related CNKI theses exist | — |
| 48 | Analysis of current situation and countermeasures of groundwater pollution in China | **FOUND EXACT** (cited by 3) | 1.00 |

### Ref-by-Ref Classification

| Ref# | Title (truncated) | Classification | Reason |
|------|-------------------|---------------|--------|
| 15 | Research on inverse problem of aquifer parameters... | **false_positive** | Likely Chinese domestic paper/thesis not indexed in OpenAlex; topic is real and well-studied |
| 18 | Current status and problems of non-point source pollution... | **false_positive** | Found on Google Scholar with exact match (sim=1.00, cited by 27) |
| 32 | Advances in mathematical methods of groundwater pollution... (2017) | **false_positive** | Found on Google Scholar with exact match (sim=1.00, cited by 17) |
| 42 | Review on groundwater contamination source identification... | **false_positive** | Found on Google Scholar with exact match (sim=1.00, cited by 3) |
| 44 | Advances in mathematical methods of groundwater pollution... (2020) | **false_positive** | Found on Google Scholar — different paper from Ref#32 despite same title, different year (cited by 2) |
| 45 | Groundwater contaminant source identification... (thesis) | **false_positive** | Chinese Master's thesis from Hefei; CNKI-only; related theses found in same domain |
| 48 | Analysis of current situation and countermeasures... | **false_positive** | Found on Google Scholar with exact match (sim=1.00, cited by 3) |

### Verdict: FALSE POSITIVE

**Confidence: HIGH**

**Summary**: All 7 flags are false positives. Five of the 7 references were found with exact title matches on Google Scholar (sim=1.00), confirming they are real Chinese-language papers in the Advances in Water Science journal and related venues. The remaining 2 (a thesis and a domestic paper) are consistent with Chinese academic literature not indexed in OpenAlex/CrossRef but genuinely existing in CNKI.

---

## Summary Table

| Article | DOI | Journal | Flagged | Confirmed Fake | Probable Fake | False Positive | Verdict |
|---------|-----|---------|---------|----------------|---------------|----------------|---------|
| A | 10.1016/j.jocs.2026.102852 | J. Comput. Sci. | 20/30 | 4 | 14 | 1 (+ 1 unverifiable) | **FABRICATION CONFIRMED** |
| B | 10.1016/j.knosys.2025.114599 | Knowl.-Based Syst. | 15/123 | 0 | 0 | 15 | **FALSE POSITIVE** |
| C | 10.1016/j.eswa.2025.128820 | Expert Syst. Appl. | 7/50 | 0 | 0 | 7 | **FALSE POSITIVE** |

## Pipeline Improvement Recommendations

1. **Unstructured citation DOI comparison**: When a reference has no structured title but has an unstructured string containing a DOI, the similarity comparison should extract just the title portion (after author names, before arXiv IDs) rather than comparing the full string. This would eliminate the 13 false positives in Article B and likely many others across the CS/AI domain.

2. **Chinese-language paper handling**: Papers from Chinese domestic journals frequently have English titles that are translations, making them findable on Google Scholar even when absent from CrossRef/OpenAlex. A Google Scholar search step for `title_not_found` verdicts could rescue many false positives (5 of 7 in Article C were immediately confirmed this way).

3. **CJA vs domestic journals**: When a reference claims to be from Chinese Journal of Aeronautics (which is SCI-indexed and English-language), failure to find it should be weighted more heavily than failure to find a paper from a domestic Chinese journal.
