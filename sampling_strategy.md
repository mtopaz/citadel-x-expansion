# CITADEL-X Sampling Strategy (v2 — Clean Frame)

## Overview

Two-stage stratified random sampling from a curated, contamination-free journal universe. Version 2 replaces the original CrossRef-facet-based universe (764 journals, contaminated with biomedical/ecology titles) with a title-filtered universe of 795 journals.

## Problem with v1

CrossRef subject-area queries are imprecise — publisher-assigned subject tags pulled in neuroscience journals (e.g., "The Journal of Neuroscience"), medical journals (e.g., "Cureus", "European Heart Journal - Digital Health"), biology journals (e.g., "International Journal of Biological Macromolecules"), and mega-journals (e.g., "PLOS One", "Scientific Reports") into both STEM and CS/AI domains. This contamination undermined the claim of domain-specific sampling.

## v2 Approach: Title-Based Include/Exclude Filtering

### Source Data

Starting universe: 1,376 journals from CrossRef faceted queries (853 STEM, 523 CS/AI) stored in `journal_universe_raw.csv`.

### STEM Domain (Materials, Chemistry, Physics, Engineering)

**Include** if journal title contains any of: materials, material, chemistry, chemical, physics, physical, engineering, mechanics, mechanical, civil, structural, polymer, ceramic, metallurg, alloy, composite, concrete, construction, building, corrosion, coating, surface, semiconductor, superconductor, magnet, optic, photon, nanotechnol, nano, thin film, crystal, spectroscop, electroch, catalys, energy, thermal, thermodynamic, fluid, combustion, tribolog, manufactur, industrial, applied science, RSC, ACS, IOP, Phys Rev, J Phys.

**Exclude** if title also contains any of: medic, clinical, health, disease, cancer, neuro, neural, pharmac, biolog, biotech, bioscience, genome, cell, immun, pathol, surg, cardio, dent, nurs, psych, rehabilitat, ocean, marine, earth, geolog, atmosph, ecolog, environ, food, agric, veterinar, plant, animal, cereal.

### CS/AI Domain

**Include** if title contains any of: computer, comput, software, artificial intelligence, machine learning, neural, pattern recognition, data mining, information science, information system, knowledge, intelligent, fuzzy, expert system, deep learning, natural language, image process, signal process, cybersecur, network, algorithm, automat, IEEE Trans, ACM, AAAI, IJCAI.

**Exclude** if title also contains any of: medic, clinical, health, biolog, bioscience, brain, cortex, neuro (except "neurocomput"), genome, cell, ocean, earth, atmosph, ecolog, geophys, surg, cardio, dent, nurs, psych, pharmac, immun, pathol, cancer, disease, agric, food, veterinar, plant, animal, cereal, biodata, biotechnol, rehabilitat, regenerat.

**Special "neural" handling**: Journals containing "neural" are only retained if they also contain a CS-relevant compound ("neural network", "neural comput", "neural process", "neural system", "neural inform"). This excludes neuroscience journals like "Journal of Neural Transmission" and "Frontiers in Neural Circuits" while keeping "Neural Networks", "Neural Computing and Applications", etc.

### Global Exclusions (both domains)

Mega-journals and multidisciplinary titles excluded regardless of keyword match: Scientific Reports, Nature Communications, PLOS One, SSRN Electronic Journal, Sustainability, Cureus, Data in Brief, Scientific Data, Applied Sciences, Mathematics, Science of The Total Environment, Science, Nature, PNAS.

### Filtering Result

| Domain | Raw | Clean | Dropped |
|--------|-----|-------|---------|
| STEM | 853 | 571 | 282 |
| CS/AI | 523 | 224 | 299 |
| **Total** | **1,376** | **795** | **581** |

## Stage 1: Journal Selection

### ISSN Enrichment

Each of the 795 clean journals queried against CrossRef `/journals` endpoint to obtain ISSN(s) and cumulative DOI count (`total_dois`). Timeout: 5 seconds per request. Failures (54/795) fell back to `article_count_2024plus` as the volume proxy.

### Stratification by Impact

Within each domain, journals ranked by `total_dois` (cumulative DOIs registered in CrossRef — proxy for publication volume and longevity):

- **Tier 1 (High impact)**: Top 20% by total DOIs
- **Tier 2 (Mid-tier)**: 20th–60th percentile
- **Tier 3 (Lower-tier)**: Bottom 40%

| Domain | T1 | T2 | T3 | Total |
|--------|-----|-----|-----|-------|
| STEM | 114 | 228 | 229 | 571 |
| CS/AI | 44 | 90 | 90 | 224 |

### Sampling Allocation

Disproportionate stratified random sampling (seed = 42):

- Tier 1: 15 journals per domain
- Tier 2: 25 journals per domain
- Tier 3: 25 journals per domain
- **Total: 65 journals per domain x 2 = 130 randomly selected journals**

Oversampling mid- and lower-tier journals is standard epidemiological practice: these tiers have higher expected fabrication rates, and the design maximizes case detection while retaining high-impact journals as comparators.

## Stage 2: Article Selection

For each sampled journal x year (2023, 2024, 2025, 2026):
- Query CrossRef for all articles with `has-references:true` and >= 10 references
- Draw up to N articles randomly (seed = 42 + batch x 1000)
- Exclude articles with >500 references (encyclopedias, special issues)

## Defensibility

1. **Reproducible**: Fixed seed (42), all code in `build_sampling_frame_v2.py`, universe and sample saved as CSV
2. **Clean domain boundaries**: Title-based include/exclude filters remove biomedical, ecological, and off-domain contamination that CrossRef subject tags introduced
3. **Transparent exclusion criteria**: Every include and exclude term documented; mega-journal exclusions justified (multidisciplinary scope makes domain attribution impossible)
4. **Two-stage random**: Both journal selection and article selection use seeded random sampling
5. **Stratified by impact tier**: Enables within-tier rate estimation with disproportionate allocation for case detection
6. **Universe documented**: All 795 eligible journals listed in `journal_universe_clean.csv` with tier, ISSN, and volume data
7. **Domain focus justified**: STEM + CS/AI chosen because (a) DOI coverage enables reference verification (>80% resolvable), (b) prior evidence of LLM-driven citation fabrication in these domains, (c) social sciences/law/humanities have <50% verifiable references due to book/legal citation practices

## Limitations

1. Title-based filtering may miss journals with ambiguous names or exclude valid edge cases (e.g., "Advanced Science" excluded as too broad despite publishing materials science)
2. CrossRef `total_dois` as impact proxy is imperfect — high-volume journals may be either high-impact or predatory
3. Tier boundaries (20/60/100 percentiles) are arbitrary; sensitivity analyses with different cutoffs should be reported
4. 54 of 795 journals (7%) failed CrossRef ISSN lookup and used fallback volume estimates
5. Mega-journal exclusion (Scientific Reports, Nature Communications, etc.) means these high-volume venues are not represented

## Files

| File | Description |
|------|-------------|
| `journal_universe_raw.csv` | 1,376 raw journals from CrossRef facets (contaminated) |
| `journal_universe_clean.csv` | 795 journals after title-based filtering (v2) |
| `sampled_journals_v2.csv` | 130 randomly selected journals (65 per domain) |
| `build_sampling_frame_v2.py` | Script that produces the above (reproducible) |
| `sampling_manifest.csv` | All sampled articles with DOIs (produced by article sampling stage) |
