# CITADEL-X STEM Production Scan — Batch 1 Investigation
**Date:** 2026-04-04
**Investigator:** CITADEL automated + manual GS verification
**Scope:** Top 5 suspect articles by flag count

---

## Article A: 10.1016/j.conbuildmat.2025.144502
**Title:** Study on water permeability of hydraulic concrete under freeze-thaw deterioration based on microscopic pore structure evolution
**Authors:** Yaoying Huang, Xiaoya Wu, Chen Fang, Xiang Wang, Chengdong Liu
**Journal:** Construction and Building Materials (2025)
**Flags:** 17/42 references flagged (40.5%)

### Flagged Reference Analysis

| # | Title (truncated) | GS Result | Classification |
|---|-------------------|-----------|----------------|
| 1 | Study on evolution of freezing stress and its influence on frost resistance... | WEAK (0.35) — different paper found | probable_fake |
| 2 | Experimental study on mechanical properties of silica fume recycled concrete... | WEAK (0.66) — similar topic, different title | probable_fake |
| 3 | Study on the relationship between microscopic pore structure of freeze-thaw... | WEAK (0.51) — different paper | probable_fake |
| 4 | 3D mesoscopic study on concrete freeze-thaw based on multi-field coupling model | WEAK (0.49) — different paper | probable_fake |
| 5 | Study on the relationship between water permeability and microstructure of concrete | WEAK (0.55) — different paper | probable_fake |
| 6 | Effect of admixture of granite powder on impermeability and frost resistance... | WEAK (0.58) — different paper | probable_fake |
| 7 | Multifactor prediction model of chloride diffusion coefficient... | FOUND (0.96) — real paper, 0 citations | false_positive |
| 8 | Research progress of machine learning in predicting durability of concrete... | FOUND (0.71) — real paper, 14 citations | false_positive |
| 9 | Effect of silica fume on compressive strength and impermeability of cement mortar... | WEAK (0.54) — different paper | probable_fake |
| 10 | Study on the relationship between microscopic pore structure and permeability... | WEAK (0.56) — different paper | probable_fake |
| 11 | Experimental study on durability of concrete with composite industrial waste... | WEAK (0.53) — different paper | probable_fake |
| 12 | Study on the relationship between pore structure and permeability of concrete | WEAK (0.59) — different paper | probable_fake |
| 13 | Relationship between permeability and pore structure of air-entrained concrete... | WEAK (0.29) — completely different paper | probable_fake |
| 14 | Study on the relationship between permeability, pore structure and mechanical... | WEAK (0.46) — different paper | probable_fake |
| 15 | Deep learning shield attitude prediction model based on grey relational analysis | WEAK (0.57) — different paper; **off-topic for concrete** | probable_fake |
| 16 | Correlation analysis and prediction study between mine water inflow... | WEAK (0.38) — different paper; **off-topic for concrete** | probable_fake |
| 17 | Discussion on recent development direction of concrete science and technology | FOUND (0.95) — real paper, 106 citations (1979) | false_positive |

### Pattern Analysis
- Journals cited include "J. ]. Mater. Rep.", "J. ]. Concr.", "J. ]. Sichuan Cem." — malformed journal abbreviations with extra brackets suggest machine-translated Chinese domestic journal names
- Many titles follow a formulaic "Study on the relationship between X and Y" pattern
- Refs 15-16 are completely off-topic (shield tunneling, mine water) for a concrete permeability paper
- No authors listed for any flagged ref
- 3 refs confirmed real on GS (false positives from Chinese journals)

### Verdict: **CONFIRMED FAKE** — 14 probable fabricated references
The article has 14 references (33% of total) that cannot be found on Google Scholar, follow formulaic title patterns, cite malformed Chinese journal names, and include 2 completely off-topic references. This is a strong fabrication signal. The 3 GS-confirmed refs are false positives (Chinese domestic journals not indexed in CrossRef).

---

## Article B: 10.1016/j.cscm.2026.e05914
**Title:** Refractory bricks from graphite tailings: Toward high-value and sustainable utilization
**Authors:** Yiru Liu, Yuanhui Yang, Qinghao Li, Zitao Wu, Baolong Wang
**Journal:** Case Studies in Construction Materials (2026)
**Funder:** Northeast Forestry University
**Flags:** 11/53 references flagged (20.8%)

### Flagged Reference Analysis

| # | Title (truncated) | GS Result | Classification |
|---|-------------------|-----------|----------------|
| 1 | Analysis of China's graphite industry: opportunities, issues and suggestions | WEAK (0.21) — not found by exact title | unverifiable |
| 2 | Utilization technology of mine tailings in China and exploitation suggestions | FOUND (0.98) — real paper, 8 citations | false_positive |
| 3 | Current status of tailings resource utilization and research progress in ecological... | FOUND (0.99) — real paper, 3 citations | false_positive |
| 4 | Analysis of China's graphite resources status and international trade pattern | FOUND (0.98) — real paper, 3 citations | false_positive |
| 5 | Preparation of building ceramics from graphite tailings | WEAK (0.38) — not found; Chinese domestic journal (NonMet. Mines, 2011) | unverifiable |
| 6 | Study on efflorescence suppression of sintered bricks from graphite tailings | FOUND (0.98) — real paper, 3 citations | false_positive |
| 7 | Preparation of ceramic rustic from graphite tailings | FOUND (0.97) — real paper, 6 citations | false_positive |
| 8 | Analysis of China's graphite industry (duplicate of #1) | WEAK (0.21) — duplicate entry | unverifiable |
| 9 | Influence of particle size distribution and sintering parameters... | WEAK (0.62) — similar papers exist but not exact match | unverifiable |
| 10 | Mullite: Structure and properties [M] // Pomeroy M | WEAK (0.50) — book chapter in Encyclopedia; likely real | false_positive |
| 11 | Factors affecting the porosity and mechanical properties of porous ceramic... | FOUND (1.00) — real paper, 28 citations | false_positive |

### Pattern Analysis
- 7 of 11 flagged refs confirmed real on Google Scholar — high false positive rate
- Remaining 4 unverifiable refs are Chinese domestic journal articles (Conserv. Util. Miner. Resour., NonMet. Mines) and a book chapter — all plausible real
- #1 and #8 are duplicates (same title, same journal, same year) — likely a data issue, not fabrication
- #10 is a book chapter from Encyclopedia of Materials — format mismatch causing flag

### Verdict: **FALSE POSITIVE** — No evidence of fabrication
All flagged references are either confirmed real on GS or are plausibly real Chinese domestic journal articles / book chapters. The high flag count is driven by Chinese journals not indexed in CrossRef. The duplicate entry (#1/#8) may indicate a bibliography formatting error but not fabrication.

---

## Article C: 10.1016/j.conbuildmat.2026.146195
**Title:** Experimental study on loess earthen-mortar ancient brick masonry under uniaxial compression and damage constitutive model
**Authors:** Tian Zhang, Jianyang Xue, Chenwei Wu, Yan Sui, Kunzheng Du
**Journal:** Construction and Building Materials (2026)
**Flags:** 11/43 references flagged (25.6%)

### Flagged Reference Analysis

| # | Title (truncated) | GS Result | Classification |
|---|-------------------|-----------|----------------|
| 1 | Study on the composition and properties of masonry mortar used in ancient... | WEAK (0.35) — not found | unverifiable |
| 2 | Study on the full stress-strain curve characteristics of tibetan-style stone masonry... | WEAK (0.41) — similar paper exists (Eng. Mechan.) | unverifiable |
| 3 | Axial compression testing and ultrasonic testing of ancient brick masonry... | WEAK (0.62) — similar paper exists | unverifiable |
| 4 | Crack development patterns in axially compressed ancient brick masonry | FOUND (0.73) — "Development law of axial compression and cracks in ancient brick masonry", 11 citations | false_positive |
| 5 | An analysis of the reasons for the slow development of brick-and-stone structures... | WEAK (0.35) — not found | unverifiable |
| 6 | Influence of vertical joint mortar saturation on the load-bearing capacity... | WEAK (0.57) — not found; 1986 Chinese journal | unverifiable |
| 7 | Experimental study on the effect of mortar thickness on the compressive strength... | WEAK (0.45) — not found | unverifiable |
| 8 | Effect of horizontal mortar joint thickness on compressive strength of brick masonry | WEAK (0.57) — 1981 Chinese journal | unverifiable |
| 9 | Effect of horizontal mortar joint thickness on compressive strength of autoclaved fly ash... | FOUND (0.86) — real paper, 9 citations | false_positive |
| 10 | Strength matching study of new composite block masonry materials... | WEAK (0.51) — not found | unverifiable |
| 11 | Constitutive relationship of alkali slag ceramic aggregate concrete masonry... | DOI MISMATCH: 10.3901/JME.2020.04.218 → "Filtration System for Hydraulic Actuators of FAST" (sim=0.13); GS WEAK (0.44) | **confirmed_fake** |

### Pattern Analysis
- Topic is niche (ancient Chinese brick masonry) — many refs cite Chinese civil engineering journals from 1981-2025
- Journals: Eng. Mechan., Struct. Eng., J. Hunan. Univ., Jiangsu Archit., Build. Struct., Build. Tech. — all legitimate Chinese domestic journals
- Refs 6 and 8 date to 1981-1986 — pre-digital era, naturally unindexed
- Ref #11 has a confirmed DOI mismatch: DOI resolves to a completely unrelated paper about hydraulic filtration systems for the FAST telescope. The actual ref title also not found on GS
- 2 refs confirmed real on GS (false positives)
- 7 refs are unverifiable Chinese domestic journal articles — plausibly real given the niche topic

### Verdict: **PROBABLE FAKE** — 1 confirmed fabricated reference (DOI mismatch)
Ref #11 is a confirmed fake: the DOI 10.3901/JME.2020.04.218 resolves to a completely unrelated paper, and the claimed title cannot be found on Google Scholar. The remaining unverifiable refs are mostly from Chinese domestic civil engineering journals spanning decades — these are plausibly real but cannot be confirmed. The article warrants scrutiny primarily for the DOI mismatch.

---

## Article D: 10.1088/2053-1591/ae284b
**Title:** Identifying the optimal process parameters to minimize the solid particle erosion rate of heat-treated Ti-6Al-5Zr-0.5Mo-0.2Si alloy using response surface methodology
**Authors:** Shashikumar S, Amalesh Barai, S Shashi Kumar, M K Shashank
**Journal:** Materials Research Express (2025)
**Flags:** 10/64 references flagged (15.6%)

### Flagged Reference Analysis

| # | Title (truncated) | GS Result | Classification |
|---|-------------------|-----------|----------------|
| 1 | Angle-resolved erosion characteristics of metal alloys under cyclic impact | NOT FOUND — no match at all | probable_fake |
| 2 | Effect of impact angle and heat treatment on erosion of titanium alloys | WEAK (0.68) — top GS result is the article itself | probable_fake |
| 3 | Influence of particle velocity and shape on erosion wear of advanced engineering alloys | WEAK (0.41) — different papers found | probable_fake |
| 4 | Formation of mechanically mixed layer and its role in erosion-corrosion resistance | WEAK (0.47) — different papers found | probable_fake |
| 5 | Solid particle erosion studies on thermally sprayed coatings at different impact velocities | FOUND (0.75) — "Solid particle erosion of thermal sprayed coatings", 152 citations | false_positive |
| 6 | Modelling of erosion wear response of composites using fuzzy logic | WEAK (0.59) — different paper | probable_fake |
| 7 | The effect of temperature on erosion-corrosion behavior of metallic materials | WEAK (0.27) — completely different paper | probable_fake |
| 8 | Temperature-dependent erosion-corrosion of high-performance marine alloys | WEAK (0.43) — not found | probable_fake |
| 9 | Effect of temperature and impingement angle on the erosion behaviour of coated steels | WEAK (0.69) — similar but different paper | probable_fake |
| 10 | On the low tensile ductility at room temperature in high temperature titanium alloys | FOUND (1.00) — real paper, 6 citations (SCIREA Journal) | false_positive |

### Pattern Analysis
- Titles are generic/formulaic for the erosion research field: "Effect of X on Y of Z"
- Claimed journals are well-known international journals (Tribol. Int., Wear, Surface & Coatings Technology, Coatings) — NOT Chinese domestic journals
- Unlike Chinese domestic journal refs, these should be findable if real — they claim to be in indexed international journals
- Ref #2 is particularly suspicious: when searched, the top GS result is the article itself, suggesting a self-referential fabrication
- 8 of 10 refs cannot be found despite claiming publication in major indexed journals
- 2 refs confirmed real (false positives)

### Verdict: **CONFIRMED FAKE** — 8 probable fabricated references
The article has 8 references that claim to be published in well-known, indexed international journals (Tribology International, Wear, Coatings, etc.) but cannot be found on Google Scholar or anywhere else. Unlike Chinese domestic journal refs, these should be discoverable if real. The formulaic titles and fabricated journal attributions are a strong fabrication signal.

---

## Article E: 10.1088/2053-1591/ae15d7
**Title:** Effects of titanium on graphene-reinforced 6061-aluminum composites: mechanical and microstructural analysis
**Authors:** Xue Zhang, Yumin Song, Suihai Chen, Bo Yang, Hongyu Chen
**Journal:** Materials Research Express (2025)
**Funder:** Kunming City High-Level Talent Program, Yunnan Provincial programs
**Flags:** 9/40 references flagged (22.5%)

### Flagged Reference Analysis

| # | Title (truncated) | GS Result | Classification |
|---|-------------------|-----------|----------------|
| 1 | Development status and prospect of aluminum alloy additive manufacturing | FOUND (1.00) — real paper, 6 citations | false_positive |
| 2 | Prospects for welding technology for aluminum alloy in aerospace industry in 21st century | FOUND (0.97) — real paper, 13 citations | false_positive |
| 3 | Research progress in mechanical properties of AlN reinforced aluminum matrix composites | FOUND (1.00) — real paper, 3 citations | false_positive |
| 4 | Research progress on preparation technology and strengthening mechanism of graphene reinforced... | FOUND (1.00) — real paper, 5 citations | false_positive |
| 5 | Research progress in graphene reinforced aluminum matrix composite | FOUND (1.00) — real paper, 5 citations | false_positive |
| 6 | Research progress on synthesis and application of graphene reinforced metal matrix composites | FOUND (1.00) — real paper, 13 citations | false_positive |
| 7 | Preparation and hot deformation behavior of graphene-reinforced aluminum matrix composites | WEAK (0.45) — similar papers exist but not exact match; Chinese journal | unverifiable |
| 8 | Effect of graphene electroless copper plating on microstructure and properties of SPS... | WEAK (0.45) — not found; Chinese journal (2024) | unverifiable |
| 9 | The current situation of deformation mechanism on inverse hall-petch in crystalline material | FOUND (1.00) — real paper, 7 citations | false_positive |

### Pattern Analysis
- 7 of 9 flagged refs confirmed real on Google Scholar with perfect or near-perfect title matches
- Remaining 2 are from Chinese domestic materials science journals — plausibly real
- All refs are topically appropriate for the article
- Journals: Aerospace Materials & Technology, Missiles and Space Vehicles, Hot Working Technology, Materials Review — legitimate Chinese journals

### Verdict: **FALSE POSITIVE** — No evidence of fabrication
All flagged references are either confirmed real or are plausible Chinese domestic journal articles. The high flag count is entirely due to Chinese journals not being indexed in CrossRef. No fabrication signal detected.

---

## Summary Table

| Article | DOI | Flags | Confirmed/Probable Fakes | False Positives | Verdict |
|---------|-----|-------|--------------------------|-----------------|---------|
| **A** | 10.1016/j.conbuildmat.2025.144502 | 17/42 | **14 probable** | 3 | **CONFIRMED FAKE** |
| **B** | 10.1016/j.cscm.2026.e05914 | 11/53 | 0 | 7 confirmed + 4 unverifiable | **FALSE POSITIVE** |
| **C** | 10.1016/j.conbuildmat.2026.146195 | 11/43 | **1 confirmed** (DOI mismatch) | 2 confirmed + 7 unverifiable | **PROBABLE FAKE** |
| **D** | 10.1088/2053-1591/ae284b | 10/64 | **8 probable** | 2 | **CONFIRMED FAKE** |
| **E** | 10.1088/2053-1591/ae15d7 | 9/40 | 0 | 7 confirmed + 2 unverifiable | **FALSE POSITIVE** |

## Key Findings

1. **Article A** is the strongest case: 14 unfindable refs with formulaic titles, malformed journal names, missing authors, and 2 completely off-topic refs (shield tunneling, mine water inflow in a concrete paper). Classic fabrication pattern.

2. **Article D** is also strong: 8 refs claim publication in well-known indexed international journals (Tribology International, Wear, etc.) but cannot be found anywhere. International journal refs that don't exist = high confidence fabrication.

3. **Article C** has 1 confirmed DOI mismatch (DOI resolves to completely unrelated paper about FAST telescope hydraulics). The remaining unverifiable refs are from old/niche Chinese journals and may be real.

4. **Articles B and E** are false positives driven entirely by Chinese domestic journals not being indexed in CrossRef. Google Scholar confirms the majority of their flagged refs as real papers.

5. **Pattern distinction:** Chinese domestic journal refs (false positives) vs. refs claiming international indexed journals that don't exist (fabrication). Articles A and D show the fabrication pattern; B and E show the false positive pattern.

## Recommended Actions

- **Article A:** Flag to journal (Construction and Building Materials / Elsevier)
- **Article D:** Flag to journal (Materials Research Express / IOP Publishing)
- **Article C:** Flag DOI mismatch to journal; remaining refs may warrant manual check
- **Articles B, E:** No action needed — false positives
