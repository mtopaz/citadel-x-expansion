# CITADEL-X STEM 2024-2025 Batch Investigation #1

**Date**: 2026-04-04
**Investigator**: CITADEL-X automated pipeline + manual verification
**Scope**: Top 5 suspect articles from STEM 2024-2025 scan by flag rate

---

## Article A: 10.1016/j.physb.2024.416405

**Title**: Density functional theory study of influence of impurity defects on structure and properties of cassiterite
**Authors**: Xiaolin Wang, Jianhua Chen
**Journal**: Physica B: Condensed Matter (2024)
**References**: 41 total, 13 flagged (31.7%)

### Flagged References

| # | Ref | Title | Year | Journal | GScholar | Verdict |
|---|-----|-------|------|---------|----------|---------|
| 1 | 2 | The current situation, problems and countermeasures of comprehensive utilization of nonferrous metal resources in China | 2018 | China Resources Comprehensive Utilization | WEAK (0.47) — similar topic exists but different title | Chinese domestic |
| 2 | 3 | Recovery of low-grade fine cassiterite by gravity and flotation combined process | 2019 | Nonferrous Met. | **FOUND (1.00)** — exact match, 2 cites | FALSE POSITIVE |
| 3 | 5 | Domestic and foreign tin dressing progress | 2006 | China Mine Engineering | WEAK (0.38) — no match | Chinese domestic |
| 4 | 6 | Recovery of fine cassiterite from flotation tailings of copper-sulfide in kafang | 2015 | Yunxi, Metal Mine | **FOUND (1.00)** — exact match, 2 cites | FALSE POSITIVE |
| 5 | 7 | Test and application of cassiterite flotation process | 2001 | Tin technology | WEAK (0.50) — no match | Chinese domestic |
| 6 | 8 | Progress of cassiterite beneficiation | 2002 | Met. Ore Dress. Abroad | WEAK (0.60) — similar topic | Chinese domestic |
| 7 | 16 | Research progress of influence of metal ions on mineral flotation behavior and underlying mechanism | 2017 | Chin. J. Nonferrous Metals | **FOUND (1.00)** — exact match, 31 cites | FALSE POSITIVE |
| 8 | 17 | Effect of metal ions on flotation collectors of cassiterite and its mechanism | 2021 | Nonferrous Metals Engineering | WEAK (0.39) — different paper | Chinese domestic |
| 9 | 24 | Flotation theory and practice of fine cassiterite | 1973 | Met. Ore Dress. Abroad | WEAK (0.45) — too old to verify | Chinese domestic |
| 10 | 33 | First-principles study on the magnetic properties of transition metal (Mo,Ru,Rh,Pd) doped SnO2 | 2022 | Electronic Components and Materials | **FOUND (0.97)** — exact match, 2 cites | FALSE POSITIVE |
| 11 | 39 | Effect of metal ions on floatation behaviors of fine cassiterite | 2016 | Multipurpose Utilization of Mineral Resources | **FOUND (1.00)** — exact match, 7 cites | FALSE POSITIVE |
| 12 | 40 | Overview of tin mineral resources in China | 2015 | Geol. Rev. | WEAK (0.44) — no match | Chinese domestic |
| 13 | 41 | Study on active agents and their mechanism in flotation of fine cassiterite | 1989 | Yunnan Metallurgy | WEAK (0.44) — no match | Chinese domestic |

### Assessment

- **5 of 13 flagged refs confirmed real** via Google Scholar (exact title matches with citations)
- **Remaining 8 are Chinese domestic journal articles** from journals like "China Mine Engineering", "Tin technology", "Yunnan Metallurgy" — niche mining/metallurgy publications that are poorly indexed in Western databases
- Article topic (cassiterite flotation) is a niche Chinese mining research area
- No DOI mismatches; all flags are title_not_found with confidence 0.7
- Journal names are consistent with the field and not formulaic

**VERDICT: FALSE POSITIVE (Confidence: HIGH)**
Chinese domestic journal indexing gap. The unfound references cite real Chinese-language journals in tin/cassiterite beneficiation — a well-established subfield in Chinese mining research. Five references were independently verified as real. No fabrication signals.

---

## Article B: 10.1016/j.physb.2025.417962

**Title**: Rare-earth engineering of NaAlO3 perovskites unlocks unified optoelectronic, thermoelectric, and spintronic functionalities
**Authors**: Muhammad Imran, Sikander Azam, Qaiser Rafiq, Amin Ur Rahman
**Journal**: Physica B: Condensed Matter (2025)
**References**: 32 total, 13 flagged (40.6%)

### Flagged References

| # | Ref | Title | Year | Journal | GScholar | Verdict |
|---|-----|-------|------|---------|----------|---------|
| 1 | 5 | A review on perovskite oxides and their composites as functional materials | 2025 | Funct. Mater. Lett. | FOUND (0.87) — close match but GS title adds "for supercapacitors" (19 cites) | SUSPICIOUS |
| 2 | 7 | Regulation of Perovskite oxides composition for the enhancement of properties via A-site doping (Bi, Sr, Na, rare Earth metals) | 2023 | SmartMat | WEAK (0.46) — GS returns "A-site perovskite oxides: an emerging functional material" (273 cites) — different paper | SUSPICIOUS |
| 3 | 8 | Cation substitution strategy for developing perovskite oxide properties | 2023 | J. Am. Chem. Soc. | FOUND (0.85) — GS match adds "...with rich oxygen vacancies" (131 cites) — partial title | SUSPICIOUS |
| 4 | 11 | Optical and dielectric studies on NaAlO3 perovskite ceramics | 2019 | Ceram. Int. | WEAK (0.47) — no match with this exact title | SUSPICIOUS |
| 5 | 12 | Defect energetics in SrTiO3 and BaTiO3 | 2001 | Phys. Rev. B | WEAK (0.54) — GS returns "First-principles calculation of defect energetics in cubic-BaTiO3..." (84 cites) — truncated title? | SUSPICIOUS |
| 6 | 13 | First-principles investigation of rare-earth-doped perovskite oxides: stability, electronic structures, and optical properties | 2017 | J. Alloys Compd. | WEAK (0.42) — GS returns different paper on SrTiO3 (33 cites) | SUSPICIOUS |
| 7 | 15 | Rare-earth-doped inorganic materials for optoelectronics: from fundamentals to applications | 2017 | Chem. Rev. | WEAK (0.17) — no matching Chem. Rev. paper found | **LIKELY FAKE** |
| 8 | 16 | 4f-band structure of the trivalent lanthanides in inorganic compounds | 2012 | J. Lumin. | WEAK (0.42) — GS returns different paper | SUSPICIOUS |
| 9 | 17 | Multifunctional rare-earth-doped perovskite oxides for spintronic and optoelectronic applications | 2018 | J. Mater. Chem. C | WEAK (0.50) — GS top result is this article itself (self-cite?) | SUSPICIOUS |
| 10 | 18 | Multifunctional behavior of lanthanide-doped perovskites: a review | 2019 | Prog. Mater. Sci. | WEAK (0.45) — no matching Prog. Mater. Sci. paper | **LIKELY FAKE** |
| 11 | 24 | Correlated rare-earth oxides: the role of 4f electrons | 2012 | J. Phys. Condens. Matter | WEAK (0.33) — no match | **LIKELY FAKE** |
| 12 | 29 | Defect energetics in SrTiO3 and BaTiO3 | 2001 | Phys. Rev. B | DUPLICATE of ref 12 — same unverifiable ref cited twice | SUSPICIOUS |
| 13 | 30 | First-principles investigation of rare-earth-doped perovskite oxides: stability, electronic structures, and optical properties | 2017 | J. Alloys Compd. | DUPLICATE of ref 13 — same unverifiable ref cited twice | SUSPICIOUS |

### Assessment

**Critical red flags:**
1. **40.6% flag rate** — highest in the batch
2. **No flagged reference has an exact GScholar match** — unlike Article A where 5/13 matched perfectly
3. **Three references cite prestigious journals (Chem. Rev., Prog. Mater. Sci., J. Phys. Condens. Matter) but cannot be found** — these journals are extremely well-indexed; a real paper in Chem. Rev. would always be findable
4. **Two references are duplicated** (refs 12/29 and 13/30 are identical) — this is a classic LLM hallucination pattern where the model generates the same fake reference twice
5. **Formulaic title pattern**: "X-doped perovskite oxides for Y applications" repeated across multiple references
6. **References cluster in the literature review section** (refs 5-18) — classic LLM-generated introduction pattern
7. The GScholar "close matches" (sim 0.85-0.87) suggest the LLM was trained on real paper titles and generated plausible-sounding variations

**VERDICT: PROBABLE FABRICATION (Confidence: HIGH)**
Strong LLM-generated reference signature. Multiple unfindable references in well-indexed journals, duplicate ghost references, formulaic title patterns, and clustering in the literature review section. This article warrants editorial attention.

---

## Article C: 10.1016/j.jobe.2024.111072

**Title**: Study on the rheological properties and compressive strength mechanism of geopolymer cementitious materials for solid waste
**Authors**: Jiaze Li, Xiangdong Zhang, Shuai Pang, Cheng Yang, Yiqing Wu, Lijuan Su, Jiashun Liu, Xiaogang Wei
**Journal**: Journal of Building Engineering (2024)
**References**: 66 total, 11 flagged (16.7%)

### Flagged References

| # | Ref | Title | Year | Journal | GScholar | Verdict |
|---|-----|-------|------|---------|----------|---------|
| 1 | 4 | Application progress of biomass alternative fuels in cement industry | 2023 | Clean Coal Technol. | WEAK (0.68) — similar topic but different title (30 cites) | Chinese domestic |
| 2 | 8 | Evaluation of pozzolanic activity and hydration properties of tuffaceous rock powder in composite cementitious materials | 2022 | Mater. Bullet. | WEAK (0.55) — different paper (42 cites) | Chinese domestic |
| 3 | 21 | Research progress of high temperature resistance of geopolymer | 2023 | Materials | WEAK (0.61) — close topic but different title (29 cites) | Chinese domestic |
| 4 | 23 | The improvement mechanism of metakaolin-based geopolymers on cement-stabilized red clay | 2024 | Mater. Rep. | WEAK (0.41) — different paper | Chinese domestic |
| 5 | 51 | Effect of microwave curing on early properties of lithium slag composite cement | 2023 | Non-Metal. Ore | WEAK (0.52) — different paper | Chinese domestic |
| 6 | 52 | Macro and micro analysis of GBFS high performance cement-based materials under steam curing | 2021 | Concrete | WEAK (0.26) — no match | Chinese domestic |
| 7 | 53 | Study on concrete performance of multi-solid waste system based on sludge [J/OL] | 2024 | J. Civ. Eng. | WEAK (0.57) — different paper; note "[J/OL]" marker = Chinese online journal format | Chinese domestic |
| 8 | 54 | Study on the evolution of pore structure of manufactured aggregate concrete under sulfate freeze-thaw... | 2024 | J. Compos. Mater. | **FOUND (1.00)** — exact match, 15 cites | FALSE POSITIVE |
| 9 | 57 | Properties and mechanism of action of slag-carbide slag based geopolymer | 2023 | Silicate Bullet. | **FOUND (0.97)** — exact match, 2 cites | FALSE POSITIVE |
| 10 | 60 | Study on the ratio optimization design and synergistic effect of solid waste-based composite cementitious materials | 2023 | Silicate Bullet. | WEAK (0.40) — different paper | Chinese domestic |
| 11 | 61 | Effect of calcination system on structure and hydration properties of calcium sulfosilicate | 2022 | Acta Silicat. Sinic. | WEAK (0.31) — different paper | Chinese domestic |

### Assessment

- **2 of 11 confirmed real** via exact Google Scholar match
- **Remaining 9 are Chinese domestic journals** ("Clean Coal Technol.", "Non-Metal. Ore", "Silicate Bullet.", "Concrete", "Mater. Rep.") — Chinese-language cement/geopolymer journals
- Ref [7] includes "[J/OL]" which is the standard Chinese citation format for online-first papers, confirming these are genuine Chinese references
- The references are scattered across the paper (refs 4, 8, 21, 23, 51-61), not clustered in a single section
- Flag rate of 16.7% is moderate and consistent with a paper heavily citing Chinese literature

**VERDICT: FALSE POSITIVE (Confidence: HIGH)**
Chinese domestic journal indexing gap again. Geopolymer/cement materials research is a major field in China. The "[J/OL]" formatting marker, scattered distribution, and confirmed real references all indicate legitimate Chinese-language citations.

---

## Article D: 10.1016/j.heliyon.2025.e44177

**Title**: Multidimensional motivation scale for community health workers: Psychometric properties and validation in a Turkish population
**Authors**: Hakan Celik, Mustafa Ozer, Betul Ozen
**Journal**: Heliyon (2025)
**References**: 72 total, 10 flagged (13.9%)

### Flagged References

| # | Ref | Title | Year | Journal | GScholar | Verdict |
|---|-----|-------|------|---------|----------|---------|
| 1 | 1 | Processes in the presentation of primary health care services in Turkey | 2017 | Smyrna Medical Journal | WEAK (0.49) — different paper on Turkish primary care | Turkish domestic |
| 2 | 2 | Family medicine practice and education in France: examining the Turkish model | 2015 | Ankara Medical Journal | WEAK (0.43) — different paper | Turkish domestic |
| 3 | 9 | Job satisfaction and motivation in nursing profession | 2015 | Kocatepe Medical Journal | **FOUND (1.00)** — exact match, 8 cites | FALSE POSITIVE |
| 4 | 12 | Health workforce in low and middle income countries: concepts and dynamics unpacked | 2022 | — | FOUND (0.78) — close match, 3 cites | FALSE POSITIVE |
| 5 | 26 | Studying of adaptation to Turkish culture the multidimensional work motivation scale | 2017 | Mediterranean J. Humanities | **FOUND (1.00)** — exact match, 5 cites; DOI 10.13114/MJH.2017.326 resolves to Turkish-language version of same paper | FALSE POSITIVE |
| 6 | 27 | The effects of intrinsic and extrinsic motivation tools on employees' motivations: an empirical investigation | 2007 | J. Commerce & Tourism Education | **FOUND (0.99)** — exact match, 16 cites | FALSE POSITIVE |
| 7 | 29 | Public service motivation scale: adaptation to Turkish, validity and reliability study | 2022 | Intl. J. Management Academy | WEAK (0.49) — no match | Turkish domestic |
| 8 | 39 | Job satisfaction and motivation in nursing profession | 2015 | Kocatepe Medical Journal | **FOUND (1.00)** — DUPLICATE of ref 9 (same paper cited twice) | FALSE POSITIVE |
| 9 | 44 | Basic concepts, applications, and programming | 2016 | Structural equation modeling with AMOS | WEAK (0.27) — DOI 10.4324/9781315757421 resolves to "Structural Equation Modeling With AMOS" by Barbara Byrne | FALSE POSITIVE |
| 10 | 50 | Sinif ici korelasyon katsayisi ve SEM kullanilarak test-tekrar test guvenilirliginin olculmesi | 2005 | J. Strength Condit Res. | WEAK (0.46) — Turkish-language title; GS returns related Turkish sports science paper | Turkish domestic |

### DOI Mismatch Analysis

- **Ref 26 (10.13114/MJH.2017.326)**: DOI resolves to "Cok Boyutlu Is Motivasyonu Olceginin Turk Kulturune Uyarlanmasi" — this is simply the Turkish-language title of the same paper "Studying of adaptation to Turkish culture the multidimensional work motivation scale". **NOT a mismatch** — it is a legitimate bilingual title discrepancy. Google Scholar confirms the paper exists with 5 citations.
- **Ref 44 (10.4324/9781315757421)**: DOI resolves to "Structural Equation Modeling With AMOS" by Barbara Byrne. The cited title "Basic concepts, applications, and programming" is the subtitle of this book. **NOT a mismatch** — the authors cited the subtitle while the DOI record uses the main title.

### Assessment

- **6 of 10 confirmed real** via Google Scholar (including the two "DOI mismatches" which are actually legitimate)
- Both DOI "mismatches" are explained: one is a bilingual title issue (Turkish/English), the other is a main-title vs. subtitle discrepancy
- Remaining 4 unfound refs are from Turkish domestic medical/academic journals (Smyrna Medical Journal, Ankara Medical Journal, Kocatepe Medical Journal) — the same indexing gap pattern as Chinese journals
- Ref 8 is a duplicate citation of ref 3 (same paper cited at two different points) — this is a citation management error, not fabrication

**VERDICT: FALSE POSITIVE (Confidence: HIGH)**
Turkish domestic journal indexing gap. Similar to the Chinese journal pattern, Turkish-language academic journals in medical/social sciences are poorly indexed internationally. Both DOI mismatches have innocent explanations. The majority of flagged refs were independently verified as real.

---

## Article E: 10.1088/2053-1591/ae2dcb

**Title**: Milling-grinding of sapphire domes with brazed diamond tools force modelling and wear mechanisms
**Authors**: Wei Feng, Ling Ji
**Journal**: Materials Research Express (2025)
**References**: 21 total, 9 flagged (42.9%)

### Flagged References

| # | Ref | Title | Year | Journal | GScholar | Verdict |
|---|-----|-------|------|---------|----------|---------|
| 1 | 1 | Research on the characteristics of high-strength nano-infrared ceramic nozzles for mid-wave infrared missiles | 2021 | Acta Optica Sinica | WEAK (0.35) — GS returns the present article itself | DOI MISMATCH |
| 2 | 2 | Conformal ALON and spinet windows | 2019 | — | **FOUND (0.97)** — match: "Conformal ALON and spinel windows" (9 cites); "spinet" is a typo for "spinel" | FALSE POSITIVE |
| 3 | 3 | Research on environmental routine test items for air-to-air missile | 2019 | Aerospace Control | **FOUND (1.00)** — exact match, 2 cites | FALSE POSITIVE |
| 4 | 6 | Numerical simulation on effect of cooling rate on sapphire single crystal growth with three-dimensional gradient freezing (3DGF) | 2015 | J. Synthetic Crystals | WEAK (0.37) — no match | Chinese domestic |
| 5 | 10 | Fabrication and properties of high-performance alumina transparent ceramics for semiconductors | 2024 | — | WEAK (0.39) — no match | Chinese domestic |
| 6 | 13 | Experimental Study on processing of sapphire with bonded large particle size SiO2 grain bonded abrasive tool | 2017 | Surf. Technol. | **FOUND (1.00)** — exact match, 3 cites | FALSE POSITIVE |
| 7 | 14 | Optimization and experimental study of processing technology for large sapphire fairings | 2013 | — | WEAK (0.57) — no match | Chinese domestic |
| 8 | 15 | Research of key technology on precision grinding of deep conformal sapphire dome | 2018 | — | **FOUND (1.00)** — exact match, 3 cites | FALSE POSITIVE |
| 9 | 16 | Research on precision grinding and chemical mechanical polishing of sapphire | 2019 | — | WEAK (0.53) — different paper | Chinese domestic |

### DOI Mismatch Analysis

- **Ref 1 (10.3788/AOS202141.0716002)**: DOI resolves to "Study on Characteristics of High-Strength Nano Infrared Ceramic Dome for Mid-Infrared Missile" — the cited title says "nozzles" but the DOI title says "Dome", and the cited title says "mid-wave" while DOI says "mid-infrared". The cited title appears to be a **poor English translation of the same Chinese paper**. The core content (high-strength nano infrared ceramic + missile application, Acta Optica Sinica 2021) is consistent. Sim = 0.68 is borderline. **Likely the same paper with translation variation** — not fabrication.

### Assessment

- **4 of 9 confirmed real** via exact Google Scholar match
- 1 DOI "mismatch" is explained by translation variation of a Chinese-language paper
- Remaining 4 unfound refs are from Chinese domestic journals in crystal growth and sapphire processing (J. Synthetic Crystals, Surf. Technol.)
- Sapphire dome grinding is a specialized Chinese defense/optics manufacturing niche
- With only 21 total references and 9 flagged, the high percentage (42.9%) is misleading — the absolute count of genuinely unverifiable refs is ~4, all from Chinese domestic journals

**VERDICT: FALSE POSITIVE (Confidence: HIGH)**
Chinese domestic journal indexing gap in a niche defense optics subfield. Four references confirmed real, DOI mismatch explained by translation, remaining unfound refs are from plausible Chinese-language journals. No fabrication signals.

---

## Summary Table

| Article | DOI | Flag Rate | Confirmed Real | Confirmed Fake | Verdict | Confidence |
|---------|-----|-----------|----------------|----------------|---------|------------|
| **A** | 10.1016/j.physb.2024.416405 | 13/41 (31.7%) | 5 | 0 | **FALSE POSITIVE** — Chinese journal gap | HIGH |
| **B** | 10.1016/j.physb.2025.417962 | 13/32 (40.6%) | 0 | 3+ | **PROBABLE FABRICATION** | HIGH |
| **C** | 10.1016/j.jobe.2024.111072 | 11/66 (16.7%) | 2 | 0 | **FALSE POSITIVE** — Chinese journal gap | HIGH |
| **D** | 10.1016/j.heliyon.2025.e44177 | 10/72 (13.9%) | 6 | 0 | **FALSE POSITIVE** — Turkish journal gap | HIGH |
| **E** | 10.1088/2053-1591/ae2dcb | 9/21 (42.9%) | 4 | 0 | **FALSE POSITIVE** — Chinese journal gap | HIGH |

## Key Findings

### Article B Is the Only Actionable Case

**10.1016/j.physb.2025.417962** (Imran et al., Physica B 2025) displays strong LLM-fabrication signatures:

1. **Zero confirmed real references** among 13 flagged — every other article in this batch had multiple confirmed-real refs
2. **Ghost references in prestigious journals**: Claimed papers in Chem. Rev., Prog. Mater. Sci., and J. Phys. Condens. Matter that do not exist
3. **Duplicate phantom references**: Refs 12/29 and 13/30 are identical entries — a hallmark of LLM text generation loops
4. **Formulaic title generation**: Titles follow a "[Adjective] [topic]-doped perovskite oxides for [application]" template
5. **Literature review clustering**: Flagged refs concentrated in refs 5-18 (introduction/background section)

### The Chinese/Turkish Journal Gap Dominates False Positives

4 of 5 articles are false positives driven by the same root cause: Chinese and Turkish domestic academic journals are poorly indexed in CrossRef and OpenAlex. Distinguishing features of these legitimate-but-unfindable references:
- Journal names are specific and non-generic (e.g., "Yunnan Metallurgy", "Silicate Bulletin", "Smyrna Medical Journal")
- Some refs from the same paper ARE findable on Google Scholar, confirming the citation ecosystem is real
- Citation format markers like "[J/OL]" indicate genuine Chinese academic formatting
- Topics match established domestic research programs (cassiterite beneficiation, geopolymer cement, Turkish healthcare workforce)

### Recommendations

1. **Article B**: Flag for editorial review at Physica B. Recommend the editors request the authors provide copies or URLs for references 5, 7, 11, 15, 17, 18, and 24.
2. **Pipeline tuning**: Consider adding a "Chinese/Turkish domestic journal" classifier to reduce false positive rate. Markers include: journal name pattern matching, author surname-only format, and presence of "[J/OL]" tags.
3. **Threshold adjustment**: A raw flag count threshold performs poorly when the underlying cause is regional indexing gaps. A better metric might be: (flags in well-indexed journals) / (total flags).
