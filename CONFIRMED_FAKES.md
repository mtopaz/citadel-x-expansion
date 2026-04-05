# CITADEL-X Confirmed Fabrications

*Updated: 2026-04-05 T07:00 — 9 confirmed + 3 probable, ~200 fabricated refs*

## Case 1: Materials Research Express
- **Article**: "An experimental investigation on longevity and mechanical characteristics of high-performance concrete incorporating copper slag as replacement of fine aggregate"
- **Authors**: Ragavan Veeraiah & Vijayaprabha Chakrawarthi
- **Journal**: Materials Research Express (IOP Publishing)
- **Year**: 2026
- **DOI**: 10.1088/2053-1591/ae45fa
- **Fabricated**: 17 / 66 refs (26%)
- **Example fabricated titles**:
  1. "Durability enhancement of HPC using mineral admixtures" — DOI 10.1007/978-981-19-5162-6 resolves to "Plant Fiber Reinforced Composites" (sim=0.11)
  2. "Optimizing the use of SCMs in concrete" — not found in any database
  3. "Effect of silica fume on durability and microstructure of HPC" — not found in any database
- **Investigation**: investigation_ae45fa.md

## Case 2: Journal of Molecular Liquids
- **Article**: "Comparative evaluation of surfactant and bile salt micelles mediated delivery of drugs to human serum albumin in aqueous media"
- **Authors**: Syed, Behera, Choudhary
- **Journal**: Journal of Molecular Liquids (Elsevier)
- **Year**: 2026
- **DOI**: 10.1016/j.molliq.2026.129534
- **Fabricated**: 16 / 56 refs (28.6%)
- **Example fabricated titles**:
  1. "Cationic micelles enhance protein interactions with negatively charged membranes" — DOI 10.1083/jcb.200305137 resolves to a cell biology paper about p120 catenin (sim=0.15)
  2. "The physical chemistry of colloidal lipid systems" — not found in any database
  3. "Bile salt-induced permeation enhancement" — not found in any database
- **Investigation**: investigation_molliq_129534.md

## Case 3: Journal of Building Engineering
- **Article**: "Analysis of safety influencing factors in prefabricated building hoisting based on an improved DEMATEL-ISM method"
- **Authors**: Chunling Zhong & Xuechun Li
- **Journal**: Journal of Building Engineering (Elsevier)
- **Year**: 2026
- **DOI**: 10.1016/j.jobe.2026.115980
- **Fabricated**: 35 / 85 refs (41%)
- **Example fabricated titles**:
  1. "Research on construction quality evaluation of prefabricated residential buildings" — not found anywhere, first-name-as-surname author
  2. "Application research of composite slabs in prefabricated building structures" — not found, garbled journal "Saf. Now"
  3. Off-topic ref about textile fiber mass spectrometry using nonexistent term "microturbret"
- **Investigation**: investigation_jobe_115980.md

## Case 4: Solid State Communications
- **Article**: "Influence of Mn-doped BaSO4 nanoparticles: Structural, functional, optical, morphological, thermal and antimicrobial studies"
- **Journal**: Solid State Communications (Elsevier)
- **Year**: 2026
- **DOI**: 10.1016/j.ssc.2026.116386
- **Fabricated**: 5 / ~60 refs (8%)
- **Example fabricated titles**:
  1. "Spectroscopic studies and antibacterial activities of pure and Ni-doped BaSO4" — DOI 10.1016/j.saa.2014.08.080 resolves to "Co-doped" not "Ni-doped" (author transplant)
  2. "Green synthesis of magnesium oxide nanoparticles for effective antibacterial properties" — not found in any database
  3. "Morphological diversity of magnesium oxide nanostructures for improved catalytic activity" — chimera reference combining real author with modified subject
- **Investigation**: investigation_stem_batch1.md (Article A)

## Case 5: Journal of Computational Science
- **Article**: "Influence of different jet fuels on the infrared radiation characteristics of spherical convergent 2D nozzles"
- **Authors**: Xiao Guo et al.
- **Journal**: Journal of Computational Science (Elsevier)
- **Year**: 2026
- **DOI**: 10.1016/j.jocs.2026.102852
- **Fabricated**: ~20 / 30 refs (67%) — HIGHEST FABRICATION RATE
- **Domain**: CS/AI (computational engineering)
- **Example fabricated titles**:
  1. "Numerical analysis of infrared radiation characteristics of convergent-divergent nozzles" — claimed in Chinese Journal of Aeronautics (fully SCI-indexed, English-language) but non-existent
  2. "Infrared radiation characteristics of jet fuel exhaust under various atmospheric conditions" — not found in any database, formulaic LLM-style title
  3. Self-citation to unfindable paper by same first author in implausible venue
- **Investigation**: investigation_cs_batch1.md (Article A)

## Case 6 (Probable): Physica B
- **Article**: Imran et al. — Physica B: Condensed Matter
- **Year**: 2025
- **DOI**: 10.1016/j.physb.2025.417962
- **Fabricated**: ~13 / 32 refs (41%) — PROBABLE (not fully confirmed)
- **Evidence**:
  1. Zero of 13 flagged refs found on Google Scholar (every other investigated article had multiple confirmed-real refs)
  2. Ghost references attributed to well-indexed journals (Chem. Rev., Prog. Mater. Sci.) that don't exist
  3. Two references duplicated verbatim (refs 12/29 and 13/30) — classic LLM hallucination loop
  4. Formulaic titles clustered in literature review section
- **Investigation**: investigation_stem_2024_2025_batch1.md (Article B)

## Case 7: Construction and Building Materials (2025)
- **Article**: (title from investigation)
- **Journal**: Construction and Building Materials (Elsevier)
- **Year**: 2025
- **DOI**: 10.1016/j.conbuildmat.2025.144502
- **Fabricated**: ~14 / 42 refs (33%)
- **Evidence**:
  1. 14 probable fakes with formulaic titles not found on Google Scholar
  2. Malformed journal abbreviations
  3. Two off-topic refs: shield tunneling + mine water treatment in a concrete paper
- **Investigation**: investigation_stem_prod_batch1.md (Article A)

## Case 8: Materials Research Express (2025, ae284b)
- **Article**: (materials science / tribology)
- **Journal**: Materials Research Express (IOP Publishing)
- **Year**: 2025
- **DOI**: 10.1088/2053-1591/ae284b
- **Fabricated**: ~8 / 64 refs (13%)
- **Evidence**:
  1. 8 probable fakes claiming to be in well-indexed journals (Tribology International, Wear, Coatings) but not findable anywhere
  2. Unfindable in Google Scholar despite these journals having near-complete GS coverage
- **Investigation**: investigation_stem_prod_batch1.md (Article D)

## Case 9 (Probable): Construction and Building Materials (2026)
- **Journal**: Construction and Building Materials (Elsevier)
- **Year**: 2026
- **DOI**: 10.1016/j.conbuildmat.2026.146195
- **Fabricated**: 1 confirmed + possible more / 43 refs
- **Evidence**: DOI 10.3901/JME.2020.04.218 resolves to "Filtration System for Hydraulic Actuators of FAST" — completely unrelated to the article's topic
- **Investigation**: investigation_stem_prod_batch1.md (Article C)

## Case 10: Information Sciences (2026)
- **Article**: "TumorNet" — brain tumor MRI classification
- **Journal**: Information Sciences (Elsevier)
- **Year**: 2026
- **DOI**: 10.1016/j.ins.2026.123423
- **Domain**: CS/AI
- **Fabricated**: 22-24 / 50 refs (44-48%)
- **Evidence**:
  1. Formulaic titles: "[Architecture]-based [modifier] for brain tumor MRI classification" — template-generated
  2. One DOI resolves to a Crohn's disease paper (completely unrelated)
  3. Only 2 of 26 flagged refs had any Google Scholar match (paraphrased real papers)
  4. 95% confidence
- **Investigation**: investigation_csai_prod_batch1.md (Article B)

## Case 11: Applied Soft Computing (2026)
- **Article**: "IT-2 General Fuzzy Automata"
- **Journal**: Applied Soft Computing (Elsevier)
- **Year**: 2026
- **DOI**: 10.1016/j.asoc.2026.114970
- **Domain**: CS/AI
- **Fabricated**: 17 / 36 refs (47%)
- **Evidence**:
  1. Titles read like LLM topic descriptions rather than real paper titles ("Interval type-2 fuzzy decision support systems in healthcare")
  2. Zero exact matches on Google Scholar for any of 17 flagged refs
  3. 93% confidence
- **Investigation**: investigation_csai_prod_batch1.md (Article D)

## Case 12 (Probable): Expert Systems with Applications (2026)
- **Article**: "TNStream" — data stream clustering
- **Journal**: Expert Systems with Applications (Elsevier)
- **Year**: 2026
- **DOI**: 10.1016/j.eswa.2026.131840
- **Domain**: CS/AI
- **Fabricated**: ~10-16 / 78 refs (13-21%)
- **Evidence**: Mixed — ~6 paraphrased real algorithm names, ~10 fully invented, 1 DOI to unrelated Monte Carlo paper
- **Investigation**: investigation_csai_prod_batch1.md (Article C)
