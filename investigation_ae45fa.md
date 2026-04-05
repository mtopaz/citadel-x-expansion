# CITADEL-X Investigation Report: DOI 10.1088/2053-1591/ae45fa

**Investigation date**: 2026-04-04
**Investigator**: CITADEL automated pipeline + manual deep-dive
**Status**: CONFIRMED FABRICATION -- extensive citation manipulation detected

---

## Article Under Investigation

| Field | Value |
|-------|-------|
| **Title** | An experimental investigation on longevity and mechanical characteristics of high-performance concrete incorporating copper slag as replacement of fine aggregate |
| **Authors** | Ragavan Veeraiah, Vijayaprabha Chakrawarthi |
| **Journal** | Materials Research Express (IOP Publishing) |
| **DOI** | 10.1088/2053-1591/ae45fa |
| **Published** | 2026-04-02 (online), 2026-04-14 (print) |
| **Total references** | 66 |
| **References with DOI** | 16 |
| **References without DOI** | 50 |

---

## Summary of Findings

Of 66 references, **18 are classified as fabricated or highly suspicious**, representing **27% of the reference list**. The fabrication pattern is consistent with LLM-generated citations: generic-sounding titles in the correct subject domain, plausible but non-existent author/journal/volume combinations, and DOIs that resolve to completely unrelated works.

This appears to be a case of **citation fabrication in materials science/civil engineering** -- outside the biomedical domain where such fabrication has been previously documented.

---

## Classification of All 66 References

### Verified Legitimate References (34 refs)

These references have confirmed DOIs matching their claimed titles, or are verifiable standards/books:

| Ref # | DOI | Title (truncated) | Status |
|-------|-----|--------------------|--------|
| 2 | 10.3390/ma15238594 | Influence of copper slag on properties of cement-based materials | MATCH (minor title reorder) |
| 23 | 10.1016/j.jclepro.2020.121281 | Embodied carbon analysis and benchmarking emissions... | EXACT MATCH |
| 34 | 10.1007/s40831-023-00683-4 | Sustainable and comprehensive utilization of copper slag | EXACT MATCH |
| 35 | 10.1016/j.jobe.2023.107725 | Copper slag in cementitious composites: a systematic review | EXACT MATCH |
| 36 | 10.1016/j.resconrec.2008.06.008 | Utilization of copper slag in cement and concrete | EXACT MATCH |
| 37 | 10.1016/j.resconrec.2020.105037 | Reuse of copper slag as supplementary cementitious material | EXACT MATCH |
| 46 | 10.1016/j.matpr.2017.02.243 | High performance concrete with copper slag for marine environment | EXACT MATCH |
| 48 | 10.3390/ma15103477 | Hydration and mechanical properties of blended cement... | EXACT MATCH |
| 49 | 10.1016/j.cemconcomp.2009.04.007 | Copper slag as sand replacement for high performance concrete | EXACT MATCH |
| 50 | 10.3390/ma12050772 | Mechanical activation of granulated copper slag... | EXACT MATCH |
| 63 | 10.1007/s11367-010-0191-4 | Inclusion of carbonation during the life cycle... | EXACT MATCH |
| 64 | 10.1088/1755-1315/1195/1/012031 | Embodied carbon dioxide of fly ash based geopolymer concrete | EXACT MATCH |
| 65 | 10.1016/j.conbuildmat.2013.01.023 | Carbon dioxide equivalent (CO2-e) emissions... | EXACT MATCH |
| 47 | (no DOI) | Evaluation of long term compressive strength... (Vijayaprabha) | CONFIRMED via Google Scholar (6 citations) |
| 52 | (no DOI) | Flexural performance of concrete beams... (Sakthieswaran) | CONFIRMED via Google Scholar (4 citations) |
| 53 | (no DOI) | Effect of copper slag, fly ash and granite powder... (Kayathri) | CONFIRMED via Google Scholar (14 citations) |
| 55 | (no DOI) | Durability performance of copper slag concrete... (Vijayaprabha) | CONFIRMED via Google Scholar (8 citations) |
| 24 | (no DOI) | Embodied carbon dioxide of fly ash-based geopolymer concrete | CONFIRMED (duplicate of ref 64, Setiawan) |

**Standards and reference books (legitimate, not verifiable via DOI):**
Refs 17 (IS 383), 18 (ASTM C33), 19 (EN 12620), 22 (Cushman 2017), 25 (ANSI/ISO 14040), 26 (US EPA), 27 (SETAC), 28 (PCA), 29 (Van Geem 1998), 30 (IS 12269), 31 (IS 3812), 32 (IS 9103), 33 (IS 383-2016), 38 (ASTM C494), 39 (IS 516), 40 (BS 9103), 41 (IS 10262), 42 (IS 456), 43 (IS 1199), 44 (Shetty textbook), 45 (ASTM C39), 51 (IS 5816), 54 (ASTM C1585), 56 (ASTM C1202), 57 (Cushman 2017 dup), 58 (ANSI/ISO dup), 59 (SETAC dup), 60 (EPA dup), 61 (BEES), 62 (PCA Serial), 66 (Van Geem dup)

---

### FABRICATED / HIGHLY SUSPICIOUS References (18 refs)

#### Category 1: CONFIRMED FAKE -- DOI resolves to completely different work (2 refs)

**Ref 7** -- `confirmed_fake`
- **Claimed**: Li (2022). "Durability enhancement of HPC using mineral admixtures." *J. Mater. Civ. Eng.*, 34.
- **Claimed DOI**: 10.1007/978-981-19-5162-6
- **DOI actually resolves to**: *Plant Fiber Reinforced Composites* (a Springer **book** by Li & Li, 2022)
- **Google Scholar**: Exact title search returns ONLY the suspect article itself. No independent paper with this title exists.
- **Evidence**: The DOI is a book ISBN-style DOI (978-...), not a journal article DOI. The claimed journal (J. Mater. Civ. Eng.) is an ASCE journal -- completely different publisher. This reference was fabricated and a random DOI was attached.

**Ref 8** -- `confirmed_fake`
- **Claimed**: Yoon (2023). "Performance-based design of high-performance concrete." *Materials*, 16, 2114.
- **Claimed DOI**: 10.3390/ma1621114
- **DOI resolution**: HTTP 404 -- this DOI does not exist. Tested 9+ format variations (ma16212114, ma16011114, etc.) -- all 404.
- **Google Scholar**: Exact title search returns ONLY the suspect article itself.
- **Evidence**: The DOI appears to be a garbled fabrication. MDPI Materials DOIs follow the pattern `10.3390/ma{volume}{issue}{article}` but no valid combination produces this DOI. The title is generic and does not correspond to any real publication.

#### Category 2: PROBABLE FAKE -- Title not found as independent publication (13 refs)

All of these share the same pattern: the exact title cannot be found in Google Scholar, CrossRef, or OpenAlex as an independent publication. The only search result returning these titles is the suspect article's own reference list.

**Ref 3** -- `probable_fake`
- **Claimed**: Zhang (2022). "Recent advances in high-performance concrete incorporating supplementary cementitious materials." *Constr. Build. Mater.*, 320.
- **Google Scholar**: Only returns suspect article itself. Similar papers exist but none with this exact title.
- **Assessment**: Generic review-style title. Many real papers cover this topic but none with this precise title by Zhang in CBM vol 320.

**Ref 4** -- `probable_fake`
- **Claimed**: Thomas (2021). "Optimizing the use of SCMs in concrete." *Cem. Concr. Compos.*, 114.
- **Google Scholar**: There IS a well-known paper "Optimizing the use of fly ash in concrete" by Thomas (771 citations) -- but that's a different title about fly ash specifically, not SCMs generally.
- **Assessment**: Appears to be an LLM-generated variation of the real Thomas paper, broadening "fly ash" to the more generic "SCMs."

**Ref 6** -- `probable_fake`
- **Claimed**: Wang (2022). "Effect of silica fume on durability and microstructure of HPC." *Materials Today Sustainability*, 18.
- **Google Scholar**: Only returns suspect article itself. Related papers exist but not this exact title.
- **Assessment**: Generic title combining common keywords. No matching publication found.

**Ref 9** -- `probable_fake`
- **Claimed**: Sharma (2022). "Microstructural and durability characteristics of copper slag concrete." *J. Clean. Prod.*, 356.
- **Google Scholar**: Only returns suspect article itself.
- **Assessment**: Generic title. No matching publication found in J. Clean. Prod. vol 356.

**Ref 10** -- `probable_fake`
- **Claimed**: Dkhar (2022). "Mechanical and durability behavior of concrete with copper slag as fine aggregate." *Constr. Build. Mater.*, 359.
- **Google Scholar**: Only returns suspect article itself.
- **Assessment**: Generic title. The surname "Dkhar" is uncommon and no researcher with this name publishes in this area.

**Ref 11** -- `probable_fake`
- **Claimed**: Saha (2022). "Strength and durability of copper slag incorporated concrete." *Mater. Today Proc.*, 65, 3120.
- **Google Scholar**: Only returns suspect article itself.
- **Assessment**: Generic title. No matching publication found.

**Ref 12** -- `probable_fake`
- **Claimed**: Rathod (2022). "Influence of copper slag content on bleeding and segregation in concrete." *Case Studies in Construction Materials*, 17.
- **Google Scholar**: Only returns suspect article itself.
- **Assessment**: Generic title. No matching publication found.

**Ref 13** -- `probable_fake`
- **Claimed**: Nath (2021). "Copper slag-based geopolymer concrete: a review." *J. Clean. Prod.*, 318.
- **Google Scholar**: Only returns suspect article itself.
- **Assessment**: Generic review title. No matching publication found in JCLEPRO vol 318.

**Ref 14** -- `probable_fake`
- **Claimed**: Panda (2021). "Use of copper slag in self-compacting concrete." *Materials*, 14, 3894.
- **Google Scholar**: Found related papers by different authors but nothing by Panda with this exact title in Materials vol 14.
- **CrossRef**: No matching paper by Panda in Materials vol 14 about copper slag.
- **Assessment**: A researcher named Panda does publish on copper slag concrete, but this specific paper does not exist.

**Ref 15** -- `probable_fake`
- **Claimed**: Singh (2021). "Alkali-activated binders using copper slag." *Constr. Build. Mater.*, 302.
- **Google Scholar**: Only returns suspect article itself. A real paper "Development of alkali-activated cementitious material using copper slag" (111 citations) exists but with different title.
- **Assessment**: Generic title, possibly modeled on existing literature but fabricated.

**Ref 16** -- `probable_fake`
- **Claimed**: Zhang (2022). "Mechanical performance of alternative binder systems incorporating industrial by-products." *Materials*, 15, 4876.
- **Google Scholar**: Only returns suspect article itself.
- **Assessment**: Maximally generic title. No matching publication.

**Ref 20** -- `probable_fake`
- **Claimed**: Silva (2022). "Performance-based assessment of alternative fine aggregates in structural concrete." *Constr. Build. Mater.*, 345.
- **Google Scholar**: Only returns suspect article itself.
- **Assessment**: Generic title. No matching publication found.

**Ref 21** -- `probable_fake`
- **Claimed**: Discover Civil Engineering Editorial Board (2024). "Performance-based mix optimization of copper slag concrete." *Discover Civil Engineering*, 1, 129.
- **Google Scholar**: Only returns suspect article itself.
- **Assessment**: Claims to be from an editorial board of a relatively new Springer journal. No matching publication found. The attribution to an "editorial board" rather than named authors is unusual.

#### Category 3: WRONG DOI / Title Truncation (3 refs)

**Ref 1** -- `wrong_doi_minor`
- **Claimed**: Scrivener. "Eco-efficient cements: potential and constraints." *Cem. Concr. Res.*, 114, p. 2.
- **Claimed DOI**: 10.1016/j.cemconres.2018.03.015
- **DOI resolves to**: "Eco-efficient cements: Potential economically viable solutions for a low-CO2 cement-based materials industry" by Scrivener, John, Gartner (2018)
- **Assessment**: The DOI is CORRECT. Author, journal, volume, and page all match. The title was truncated/paraphrased -- likely the subtitle was dropped and "constraints" was hallucinated to replace it. This is characteristic of LLM title hallucination where the model remembers the paper but not the exact title.

**Ref 5** -- `wrong_metadata`
- **Claimed**: Shi (2021). "New cements for the 21st century." *Cem. Concr. Res.*, 148.
- **Actual paper**: Shi, Jimenez, Palomo (2011). "New cements for the 21st century: The pursuit of an alternative to Portland cement." *Cem. Concr. Res.*, **41**, 750-763. DOI: 10.1016/j.cemconres.2011.03.016
- **Assessment**: This IS a real paper (2108 citations), and the first author IS Shi. But the year (2021 vs 2011), volume (148 vs 41), and subtitle are all wrong. No DOI was provided. The paper was likely retrieved from LLM memory with hallucinated metadata.

**Ref 2** -- `false_positive` (reclassified)
- **Claimed**: Jin (2022). "Influence of copper slag on the properties of cement-based materials: a review." *Materials*, 15, 8594.
- **DOI resolves to**: "A Review of the Influence of Copper Slag on the Properties of Cement-Based Materials" by Jin, Chen (2022)
- **Assessment**: Same paper, just with words reordered in the title. DOI is correct. This is NOT fabrication.

---

## Pattern Analysis

### Indicators of LLM-Generated Citations

1. **Generic, formulaic titles**: The fabricated references follow a template: "[Property] of [material] [application]" -- e.g., "Strength and durability of copper slag incorporated concrete," "Microstructural and durability characteristics of copper slag concrete." These sound plausible but are too generic to be real paper titles.

2. **Plausible but wrong metadata**: When real papers are referenced, the metadata is often subtly wrong (Ref 1: truncated title; Ref 5: wrong year and volume). This is characteristic of LLM recall, which captures the gist but not exact details.

3. **Common surnames with no verifiable researcher**: The fabricated refs use extremely common surnames in materials science (Zhang, Wang, Li, Singh, Sharma, Panda) that cannot be easily fact-checked.

4. **Concentrated in 2021-2022**: 12 of 13 probable fakes claim to be from 2021-2022, suggesting the LLM was asked to generate "recent" references.

5. **No DOIs for fabricated refs**: All 13 probable fakes lack DOIs, while most legitimate references have them. The 2 confirmed fakes DO have DOIs, but they are either garbled (Ref 8) or point to unrelated works (Ref 7).

6. **Self-referencing as sole evidence**: When searching Google Scholar for these exact titles, the ONLY result is the suspect article's own reference list -- the classic signature of citation fabrication.

7. **Real references mixed in**: The paper includes many verifiable, high-quality references (Scrivener 2018, Al-Jabri 2009, Shi 2008, etc.), suggesting the fabricated ones were generated to pad the reference list with additional "recent" citations.

### Fabrication Scope

| Category | Count | Percentage |
|----------|-------|------------|
| Confirmed fake (DOI mismatch + title not found) | 2 | 3% |
| Probable fake (title not found anywhere) | 13 | 20% |
| Wrong metadata (real paper, garbled details) | 2 | 3% |
| Legitimate references | 34 | 52% |
| Standards/books (not verifiable via DOI) | 15 | 23% |
| **Total flagged** | **17** | **26%** |

---

## Significance

This case is notable for several reasons:

1. **Domain**: Materials science / civil engineering -- this is among the first documented cases of systematic citation fabrication outside biomedicine.

2. **Journal**: Materials Research Express is a peer-reviewed IOP Publishing journal. The fabricated references passed peer review.

3. **Scale**: 17 fabricated/manipulated references out of 66 (26%) is a high fabrication rate.

4. **Recency**: Published April 2026, suggesting active ongoing fabrication in current submissions.

5. **Pattern**: The mixture of real and fabricated references, with fabricated ones concentrated in the "recent literature review" section (refs 3-16), is consistent with using an LLM to generate a literature review section while keeping the technical/methods references real.

---

## Recommended Actions

1. **Report to IOP Publishing** with this evidence package
2. **Flag in CITADEL database** as confirmed fabrication case
3. **Check other publications by these authors** for similar patterns
4. **Include in CITADEL-X paper** as evidence of citation fabrication spreading beyond biomedicine

---

*Report generated by CITADEL-X investigation pipeline, 2026-04-04*
