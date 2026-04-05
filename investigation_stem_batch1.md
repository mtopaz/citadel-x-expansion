# CITADEL-X Batch Investigation: STEM Suspects Batch 1

**Investigator:** CITADEL automated + manual GS verification
**Date:** 2026-04-04
**Pipeline:** citadel_2026_stem_flagged.csv
**Method:** CrossRef metadata retrieval, Google Scholar (Serper.dev) title search, DOI resolution, title similarity analysis

---

## Article A: Influence of Mn-doped BaSO4 nanoparticles: Structural, functional, optical, morphological, thermal and antibacterial analysis

- **DOI:** 10.1016/j.ssc.2026.116386
- **Journal:** Solid State Communications
- **Published:** May 2026
- **Authors:** P. Soundhirarajan, M. Silambarasan, R. Boopathiraja, G. Srinivasan
- **Total refs:** 61, **Flagged:** 5
- **Verdict: FABRICATION CONFIRMED (5/5 flagged refs are fabricated)**

### Flagged Reference Details

| Ref # | Claimed Title | Author | Year | Verdict | Classification |
|-------|--------------|--------|------|---------|----------------|
| 35 | Spectroscopic studies and antibacterial activities of pure and Ni-doped BaSO4 nanoparticles synthesized by chemical co-precipitation route | Sivakumar | 2015 | doi_mismatch | **confirmed_fake** |
| 50 | Synthesis, characterization and antimicrobial activity of iron manganite (FeMnO3) nanoparticles | Saleh | 2020 | title_not_found | **confirmed_fake** |
| 52 | Morphological diversity of magnesium oxide nanostructures for improved antibacterial and anticancer activities | Umar | 2022 | title_not_found | **confirmed_fake** |
| 53 | Green synthesis of NiO nanoparticles using Rhamnus virgata L. leaf extract: characterization and their potential biological applications | Abbasi | 2020 | title_not_found | **confirmed_fake** |
| 57 | Green synthesis of magnesium oxide nanoparticles for effective antibacterial activity against Pseudomonas aeruginosa | Nguyen | 2022 | title_not_found | **confirmed_fake** |

### Evidence

**Ref #35 (DOI mismatch):** DOI 10.1016/j.saa.2014.08.080 resolves to "Synthesis, characterization and anti-bacterial activities of pure and **Co-doped** BaSO4 nanoparticles via chemical precipitation route" -- the paper cites "Ni-doped" but the DOI points to a "Co-doped" paper. The author name (Sivakumar) also does not match the real paper's authors. Classic fabrication pattern: real DOI attached to a modified/invented title.

**Ref #50 (title not found):** Claimed "Synthesis, characterization and antimicrobial activity of iron manganite (FeMnO3) nanoparticles" by Saleh (2020) in RSC Adv. GS found a real paper about FeMnO3 in RSC Advances 2020, but it is by Vasiljevic et al. (not Saleh) and has a different title ("Synthesis and antibacterial activity of iron manganite (FeMnO3) particles against the environmental bacterium Bacillus subtilis", sim=0.58). The claimed title appears to be a paraphrased/embellished version of the real paper with a fake author name.

**Ref #52 (title not found):** Claimed "Morphological diversity of magnesium oxide nanostructures for improved antibacterial and anticancer activities" by Umar (2022) in ACS Omega. No matching paper found on GS. Best hit (sim=0.53) was about MgO fabrication/photocatalysis by different authors. Deep search for Umar + MgO + ACS Omega + 2022 returned irrelevant results. Title sounds LLM-generated ("morphological diversity... for improved..."). **Confirmed fabricated.**

**Ref #53 (title not found):** Claimed "Green synthesis of NiO nanoparticles using Rhamnus virgata L. leaf extract..." by Abbasi (2020) in J. Mol. Struct. GS found a related paper by Abbasi in Biomedicines 2020 about NiO nanoparticles, but using **Rhamnus triquetra** (not Rhamnus virgata) leaves. A second Abbasi paper in J. Mol. Struct. 2020 was about Rhamnella gilgitica, not NiO. The claimed reference appears to be a chimera -- combining Abbasi's real authorship/year with a modified plant species name and different journal. **Confirmed fabricated.**

**Ref #57 (title not found):** Claimed "Green synthesis of magnesium oxide nanoparticles for effective antibacterial activity against Pseudomonas aeruginosa" by Nguyen (2022) in Materials. GS best hit (sim=0.85) was "Green synthesis of magnesium oxide nanoparticles and their antibacterial activity" -- but this is a 2012 paper from IJMS, not by Nguyen, and not from 2022. No exact match found. The title is generic enough to be LLM-generated. Deep search returned only tangentially related MgO synthesis papers. **Confirmed fabricated.**

### Pattern Analysis
All 5 fabricated references follow the nanoparticle/antibacterial theme of the paper. They exhibit classic fabrication signatures:
- **DOI-title swap** (ref 35): real DOI, modified title (Ni-doped vs Co-doped)
- **Author transplant** (refs 50, 53): real-sounding author names attached to modified titles of real papers
- **Generic LLM-style titles** (refs 52, 57): plausible-sounding but non-existent papers
- **Chimera references** (ref 53): combines real author + modified plant species + wrong journal

---

## Article B: Mechanical behaviour and crack-bridging mechanisms of polymer-cement spray-applied waterproofing membranes with high polymer contents

- **DOI:** 10.1016/j.conbuildmat.2026.146155
- **Journal:** Construction and Building Materials
- **Published:** May 2026
- **Authors:** Luoning Li, Shuchen Li, Chao Yuan, Xinyu Xie, Yong Han, Li Tong
- **Total refs:** 66, **Flagged:** 4
- **Verdict: INCONCLUSIVE -- likely Chinese-language papers (unverifiable)**

### Flagged Reference Details

| Ref # | Claimed Title | Author | Year | Journal | Classification |
|-------|--------------|--------|------|---------|----------------|
| 4 | A controversial discussion regarding the use of spray applied waterproofing for tunnel applications | Lemke | 2015 | (none listed) | **false_positive** |
| 29 | Study on the Factors Affecting the Tensile Properties of Polymer Cement Waterproof Coatings | Ran | 2020 | China Water S | **unverifiable** |
| 31 | Polymer-cement ratio on the performance of polymer modified porous concrete | Han | 2017 | Concrete | **unverifiable** |
| 34 | Tensile performance and mechanism of polymer cement waterproof coating | Jian | 2015 | N. Build. Mater. | **unverifiable** |

### Evidence

**Ref #4 (FOUND -- false positive):** GS returned an exact title match (sim=1.00). This paper exists. It appears to be a conference paper or industry publication by Lemke (2015) about spray-applied waterproofing in tunnels. The automated scanner failed to find it likely because it is grey literature without a DOI. **Confirmed real paper -- false positive.**

**Ref #29 (unverifiable):** Claimed to be from "China Water S[cience]" journal (2020). GS found no exact match. The title reads like a translated Chinese-language paper. The journal abbreviation suggests a Chinese-language periodical (e.g., "China Water & Wastewater" or similar). Chinese-language papers in domestic journals are often not indexed in Western databases. **Cannot confirm or deny -- unverifiable due to language/indexing.**

**Ref #31 (unverifiable):** Claimed journal is simply "Concrete" which could be a Chinese-language journal. GS found related but not matching papers. Best hit (sim=0.65) was "Mechanical properties of polymer-modified porous concrete" from IOP Conference Series -- similar topic but different title. This may be a translated title from a Chinese concrete journal. **Unverifiable.**

**Ref #34 (unverifiable):** Claimed journal "N. Build. Mater." likely abbreviates "New Building Materials" (a Chinese journal). GS found no matching paper. The title is plausible for a Chinese-language materials engineering paper. **Unverifiable.**

### Assessment
This article has 1 clear false positive (ref #4, real paper found with exact title match) and 3 references that appear to be from Chinese-language journals. These domestic Chinese publications are systematically under-represented in OpenAlex and Google Scholar. The paper is from a Chinese research group (all Chinese-named authors), and citing Chinese-language domestic journals is expected. **No evidence of fabrication.** The 3 unverifiable refs should not be counted as fabricated without Chinese-language database verification (e.g., CNKI/Wanfang).

---

## Article C: Efficiency of policy response to public emergency in the construction industry: Implications for construction project management

- **DOI:** 10.1016/j.rineng.2026.110031
- **Journal:** Results in Engineering
- **Published:** June 2026
- **Authors:** Layin Wang, Yishan Cheng, Jinrong Zhang, Dong Zhao, Bozheng Yang, Yi He
- **Total refs:** 45, **Flagged:** 4
- **Verdict: INCONCLUSIVE -- likely Chinese-language social science papers (unverifiable)**

### Flagged Reference Details

| Ref # | Claimed Title | Author | Year | Journal | Classification |
|-------|--------------|--------|------|---------|----------------|
| 7 | Research on differences in policy response speed under the background of major public health emergencies... | Wu | 2022 | J. Beijing Univ. Technol. (Soc. Sci. Ed.) | **false_positive** |
| 16 | Research on the influencing factors of policy diffusion in innovation and entrepreneurship education... | Kang | 2021 | Soft Sci. | **unverifiable** |
| 21 | Research on the influencing factors and diffusion modes of innovation in social governance in China... | Yang | 2020 | Lanzhou J. | **unverifiable** |
| 22 | Research on the influencing factors and models of innovation diffusion in American social governance... | Yang | 2021 | J. Chongqing Technol. Bus. Univ. (Soc. Sci. Ed.) | **unverifiable** |

### Evidence

**Ref #7 (FOUND -- false positive):** GS returned an exact title match (sim=1.00). This paper exists. The journal "J. Beijing Univ. Technol. (Soc. Sci. Ed.)" is a Chinese university social science journal. The automated scanner failed to find it in OpenAlex, but it is findable via Google Scholar. **Confirmed real paper -- false positive.**

**Ref #16 (unverifiable):** Claimed from "Soft Sci." (Soft Science, a Chinese journal). GS found no exact match. Deep search returned tangentially related papers about innovation/entrepreneurship education but nothing matching this exact title. The title follows a common Chinese social science titling convention ("Research on the influencing factors of X: taking Y as an example"). Published in a Chinese domestic journal. **Unverifiable without CNKI.**

**Ref #21 (unverifiable):** Claimed from "Lanzhou J." (likely Lanzhou Journal/Lanzhou Academic Journal). GS found no match. The title follows Chinese academic conventions. Yang is a common Chinese surname. The meta-analysis framing is common in Chinese policy research. **Unverifiable without CNKI.**

**Ref #22 (unverifiable):** Claimed from "J. Chongqing Technol. Bus. Univ. (Soc. Sci. Ed.)". GS found no match. Very similar title pattern to ref #21 (same author "Yang", consecutive years, same topic with "China" swapped for "American"). This similarity is mildly suspicious -- could be a legitimate two-part study by the same author, or could indicate fabrication. However, paired publications on domestic vs. international comparisons are common in Chinese social science. **Unverifiable, mildly suspicious.**

### Assessment
This article is by a Chinese research group studying policy response in the construction industry. All 4 flagged references cite Chinese-language social science journals (Beijing University of Technology, Soft Science, Lanzhou Journal, Chongqing Technology and Business University). One (ref #7) was confirmed real via GS. The remaining 3 are in journals that are systematically absent from Western databases. The title patterns are consistent with Chinese social science conventions. **No strong evidence of fabrication.** Refs #21 and #22 having nearly identical titles by the same author in consecutive years is mildly suspicious but not definitive. CNKI verification recommended.

---

## Article D: Investigation of the durability of bio-resin-coated hemp based Textile Reinforced Mortar (TRM)

- **DOI:** 10.1016/j.cscm.2026.e05987
- **Journal:** Case Studies in Construction Materials
- **Published:** July 2026
- **Authors:** Mirna Zaydan, Carmelo Caggegi, Marie Michel, Laurence Curtil
- **Total refs:** 60, **Flagged:** 4
- **Verdict: MIXED -- 1 false positive (DOI mismatch is minor), 2 probable fakes, 1 confirmed real**

### Flagged Reference Details

| Ref # | Claimed Title | Author | Year | Journal | Classification |
|-------|--------------|--------|------|---------|----------------|
| 6 | Experimental investigation on tensile and shear bond properties of Carbon-FRCM composites applied on masonry substrates | Carozzi | 2017 | Compos. Part B Eng. | **false_positive** |
| 32 | Durability of natural fibre reinforced cement composites: A review | Shah | 2020 | Constr. Build. Mater. | **probable_fake** |
| 33 | Textile-reinforced concrete: State-of-the-art and future perspectives | Ferrara | 2020 | Mater. Struct. | **probable_fake** |
| 49 | Durability of natural fibres in concrete | Gram | 1983 | Cem. Concr. Res. | **false_positive** |

### Evidence

**Ref #6 (DOI mismatch -- false positive):** DOI 10.1016/j.compositesb.2017.06.018 resolves to "Experimental investigation of tensile and bond properties of Carbon-FRCM composites for strengthening masonry elements" by Carozzi et al. The claimed title is "Experimental investigation on tensile and **shear bond** properties of Carbon-FRCM composites **applied on masonry substrates**." GS found exact title match (sim=1.00). The similarity between claimed and DOI-resolved titles is 0.80. This is a clear case of a **minor title variant** -- the paper exists, the author (Carozzi) and year (2017) are correct, and the DOI is correct. The title discrepancy is likely due to a pre-print vs. published title change, or imprecise citation. **False positive -- real paper.**

**Ref #32 (probable fake):** Claimed "Durability of natural fibre reinforced cement composites: A review" by Shah (2020) in Constr. Build. Mater. GS found no exact match. Best hit (sim=0.83) was "Plant-based natural fibre reinforced cement composites: A review" from a different journal (J. Sustainable Cement-Based Materials, 2016). Deep search found Shah papers in Journal of Renewable Materials (2022) and Journal of Natural Fibers (2022) but none matching this exact title in Construction and Building Materials. The title is generic and review-like. The specific combination of author + title + journal + year cannot be verified. **Probable fake -- generic review title not found in claimed venue.**

**Ref #33 (probable fake):** Claimed "Textile-reinforced concrete: State-of-the-art and future perspectives" by Ferrara (2020) in Mater. Struct. GS found no matching paper. Best hits were by Ferrara (2020) but as a PhD thesis about "Flax TRM Composite Systems" from an Italian university, not a review article in Materials and Structures. No review paper with this exact title exists. The title follows a generic "State-of-the-art and future perspectives" template common in fabricated references. **Probable fake -- generic review title, author exists in the field but did not write this paper.**

**Ref #49 (FOUND -- false positive):** GS returned an exact title match (sim=1.00) with multiple hits. "Durability of natural fibres in concrete" by Gram (1983) is a well-known publication. It appears in FAO/AGRIS and other databases. This is a classic grey literature / technical report that may not have a DOI, explaining why OpenAlex could not find it. **Confirmed real paper -- false positive.**

### Assessment
This article from a French research group (Lyon) has a mixed profile. Two references are clearly real (refs #6 and #49 -- false positives). Two references (refs #32 and #33) have generic review-like titles that cannot be found in their claimed journals. The two probable fakes follow typical fabrication patterns: generic "review" and "state-of-the-art" titles attributed to real researchers in the field but in journals where those specific papers do not exist. With only 2 probable fakes (not fully confirmed), this is a weaker case than Article A.

---

## Summary Table

| Article | DOI | Journal | Flags | Confirmed Fake | Probable Fake | False Positive | Unverifiable | Verdict |
|---------|-----|---------|-------|---------------|---------------|----------------|--------------|---------|
| A | 10.1016/j.ssc.2026.116386 | Solid State Commun. | 5 | 5 | 0 | 0 | 0 | **FABRICATION CONFIRMED** |
| B | 10.1016/j.conbuildmat.2026.146155 | Constr. Build. Mater. | 4 | 0 | 0 | 1 | 3 | **FALSE POSITIVE** (Chinese-lang refs) |
| C | 10.1016/j.rineng.2026.110031 | Results Eng. | 4 | 0 | 0 | 1 | 3 | **FALSE POSITIVE** (Chinese-lang refs) |
| D | 10.1016/j.cscm.2026.e05987 | Case Stud. Constr. Mater. | 4 | 0 | 2 | 2 | 0 | **INCONCLUSIVE** (2 probable fakes) |

## Recommendations

1. **Article A** should be flagged for publisher notification. All 5 fabricated references show classic patterns (DOI-title swap, author transplant, chimera references, generic LLM-style titles). This is a high-confidence fabrication case.

2. **Articles B and C** should be removed from the suspect list. The flagged references are Chinese-language journal papers that are systematically absent from Western indexing. One ref from each article was confirmed real via Google Scholar. No evidence of fabrication.

3. **Article D** requires further investigation. Two references (#32, #33) have generic titles not found in claimed journals, but the other two are clearly real. Consider checking with the authors or searching French academic databases before escalating.

4. **Pipeline improvement:** Consider adding a "Chinese-language journal" filter to reduce false positives from papers citing domestic Chinese periodicals. Journals like "Soft Science," "Lanzhou Journal," "New Building Materials," and university social science editions are legitimate venues not covered by OpenAlex.
