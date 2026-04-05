# CITADEL-X CS/AI Production Scan — Investigation Batch 1

**Date**: 2026-04-04
**Investigator**: CITADEL automated + manual verification
**Scope**: Top 4 suspect articles from CS/AI domain production scan

---

## Summary

| Article | DOI | Journal | Flagged/Total | GS Confirmed Fake | Verdict |
|---------|-----|---------|---------------|-------------------|---------|
| A | 10.1016/j.asoc.2025.113711 | Applied Soft Computing | 29/46 (63%) | ~15 of 29 | SUSPICIOUS — Chinese-language refs, many unverifiable |
| B | 10.1016/j.ins.2026.123423 | Information Sciences | 26/50 (52%) | 22-24 of 26 | **FABRICATED** — systematic LLM-generated references |
| C | 10.1016/j.eswa.2026.131840 | Expert Systems with Applications | 23/78 (29%) | ~10 of 23 | SUSPICIOUS — mix of paraphrased titles and invented refs |
| D | 10.1016/j.asoc.2026.114970 | Applied Soft Computing | 18/36 (50%) | 17 of 18 | **FABRICATED** — systematic LLM-generated references |

---

## Article A: Command and Control Network Architecture Optimization

**DOI**: 10.1016/j.asoc.2025.113711
**Title**: "Command and control network architecture optimization method based on dual-layer weighting and TOPSIS-GRA of indicators"
**Authors**: Jianwei Wang, Qing Zhang, Chengsheng Pan
**Journal**: Applied Soft Computing (Dec 2025)
**Refs**: 46 total, 29 flagged (63%)

### Investigation

This paper cites many Chinese-language defense/military journal articles, which are notoriously absent from CrossRef, OpenAlex, AND often Google Scholar. The topics (air defense networks, combat systems, UAV networks, command-and-control) are consistent with Chinese military research published in domestic Chinese journals.

**Google Scholar Results:**

| Category | Count | References |
|----------|-------|------------|
| **Confirmed found on GS** | 14 | "Command and control network architecture..." (sim=1.00), "Invulnerability optimization design..." (sim=1.00), "Aviation equipment suppliers evaluation..." (sim=0.99), "Research on enterprise financial performance..." (sim=1.00), "Application of AHP analytic hierarchy process..." (sim=1.00), "Summary of dimensionless methods..." (sim=1.00), "Coordination of functional safety..." (sim=0.72), "Combination weighting method..." (sim=1.00), "Index screening of system effectiveness..." (sim=1.00), "Research on network optimization of Shore-to-ship..." (sim=1.00), "Model and algorithm in threaten assessment..." (exact=1.00), "Dynamic improved topsis..." (exact=0.84), "An uncertain multi-attribute decision-making..." (exact=0.86), "Failure mode and effect analysis..." (exact=0.86) |
| **Not found on GS** | 15 | Mostly Chinese defense/military journal refs with formulaic "Research on X based on Y" titles |

**Key observations:**
- 14 of 29 flagged refs were confirmed real on Google Scholar (48%)
- The remaining 15 cite specific Chinese journals: *Firepower Command Control*, *Fire Command Control*, *J. Tianjin Univ. Technol.*, *J. Natl. Univ. Def. Technol.*, *J. Ordnance Equip. Eng.* — these are legitimate Chinese academic journals
- Chinese military/defense research is routinely NOT indexed in Western databases
- The paper topic (military C2 network optimization) is consistent with a Chinese defense research group
- The "Research on X based on Y" title pattern is standard Chinese academic phrasing, not necessarily LLM-generated

### Verdict: SUSPICIOUS BUT LIKELY FALSE POSITIVE

**Confidence: LOW (40%)**. The high flag rate (63%) is concerning, but the majority of flagged refs cite Chinese-language defense journals that are systematically absent from Western databases. 14 of 29 were confirmed real on GS. The remaining 15 could plausibly be genuine Chinese-language papers. This paper should be **deprioritized** for further action unless additional evidence surfaces.

---

## Article B: TumorNet — Brain Tumor Classification

**DOI**: 10.1016/j.ins.2026.123423
**Title**: "TumorNet: A hybrid lightweight framework for brain tumor classification and reasoning"
**Authors**: Hanxiang Wang, Muhammad Zaqeem, Muhammad Fayaz, Defu Qiu, Sajjad Ahadzadeh, Tan N. Nguyen, L.Minh Dang
**Journal**: Information Sciences (Aug 2026)
**Refs**: 50 total, 26 flagged (52%)

### Investigation

This paper has a massive number of fabricated references following a clear pattern: **"[Architecture] for brain tumor MRI classification"** with slight variations. Nearly all flagged titles are formulaic descriptions of applying a specific deep learning architecture (ResNet, DenseNet, VGG, EfficientNet, etc.) to brain tumor classification.

**Google Scholar Results:**

| Category | Count | References |
|----------|-------|------------|
| **Confirmed found on GS** | 2 | "Efficient deep learning models for medical image analysis" (sim=0.85, real title: "Deep learning models in medical image analysis"), "Attention-augmented resnet for brain tumor MRI classification" (sim=0.72, real title: "Efficient attention-based Ghost-ResNet...") |
| **Not found on GS** | 22 | See pattern analysis below |
| **DOI mismatch** | 1 | DOI 10.1016/j.mri.2024.06.001 resolves to a Crohn's disease MRI study, not a brain tumor paper |
| **Borderline** | 1 | "Deep learning for brain MRI analysis" — generic title, GS returns similar but different papers |

**The fabrication pattern is unmistakable:**
- Titles follow formula: `[Architecture]-based [modifier] for [brain tumor MRI classification]`
- Examples of titles that DO NOT exist as real papers:
  - "Fine-tuned resnet50 for glioma grading using brats-2019 MRI dataset"
  - "Resnet50 with bigru and dual attention for multi-class brain tumor classification"
  - "Belief network-based fusion of resnet50 and vgg16 features for brain tumor classification"
  - "Regnety-based deep neural network for high-performance brain tumor MRI classification"
  - "EfficientNetV2-driven deep hybrid network for high-precision brain tumor MRI classification"
  - "Mobdensenet: densenet201-based hybrid architecture for high-accuracy brain tumor MRI classification"
- Each fake ref is attributed to plausible-sounding authors (Singh, Patel, Ahmed, Ghassemi, etc.) in plausible venues (IEEE Access, Pattern Recognition, Computers in Biology and Medicine)
- The DOI mismatch (brain tumor paper claiming DOI for a Crohn's disease study) is a hallmark of automated reference fabrication
- Exact-phrase GS searches return either zero results or the article itself (TumorNet)

**DOI mismatch detail:**
- Claimed: "Transformer-based architecture for differentiating glioblastoma and CNS lymphoma"
- DOI 10.1016/j.mri.2024.06.001 resolves to: "Comparison of the value of adipose tissues in abdomen and lumbar vertebra for predicting disease activity in Crohn's disease: A preliminary study based on CSE-MRI"
- Completely unrelated — the DOI was likely randomly assigned or hallucinated by an LLM

### Verdict: **FABRICATED — HIGH CONFIDENCE**

**Confidence: 95%**. At least 22 of 26 flagged references appear to be fabricated. The systematic pattern (formulaic titles, plausible but non-existent venues, DOI pointing to unrelated paper) is consistent with LLM-generated reference lists. The 2 "found" refs had slightly modified titles of real papers, which is also consistent with LLM paraphrasing. **This paper warrants immediate editorial notification.**

---

## Article C: TNStream — Data Stream Clustering

**DOI**: 10.1016/j.eswa.2026.131840
**Title**: "TNStream: Applying tightest neighbors to micro-clusters to define multi-density clusters in streaming data"
**Authors**: Qifen Zeng, Haomin Bao, Yuanzhuo Hu, Zirui Zhang, Taichang Tian, Yuheng Zheng, Luosheng Wen
**Journal**: Expert Systems with Applications (Jul 2026)
**Refs**: 78 total, 23 flagged (29%)

### Investigation

This paper presents a mixed picture. Many flagged references cite real algorithms (StreamKM++, DGStream, I-HASTREAM, KD-AR Stream) but with **paraphrased/modified titles** that don't match the actual published titles. Others appear to be entirely invented.

**Google Scholar Results:**

| Category | Count | References |
|----------|-------|------------|
| **Real algorithm, wrong title** | 6 | StreamKM++ (real: "Streamkm++ a clustering algorithm for data streams", claimed: "StreamKM++: A stream clustering algorithm for large-scale data streams", sim=0.83), DGStream (real: "DGStream: High quality and efficiency...", sim=0.71), I-HASTREAM (sim=0.68), KD-AR Stream (sim=0.51), SWClustering (real: "Tracking clusters in evolving data streams over sliding windows"), EDMStream (real: "Clustering stream data by exploring the evolution of density mountain") |
| **Found via fuzzy match** | 8 | "Clustering in high-dimensional spaces..." (sim=0.74), "Data stream clustering in iot environments..." (sim=0.76), "Adaptive clustering for data streams" (sim=0.86), "Grid-based clustering algorithms..." (sim=0.79), "A density-based stream clustering algorithm..." (sim=0.78), "StreamSW" (sim=0.72) |
| **Not found on GS** | 7 | "DPClust: A novel data stream clustering algorithm...", "KD-stream: A real-time clustering approach...", "Akan: A new approach for real-time data stream clustering", "Comparison of K-D tree and ball tree...", "Similarity and social networks...", "Streaming clustering of high-dimensional data streams...", "High-dimensional data clustering: Techniques and challenges" |
| **DOI mismatch** | 1 | DOI 10.1007/s11390-019-1964-2 resolves to "DEMC: A Deep Dual-Encoder Network for Denoising Monte Carlo Rendering" — completely unrelated |

**Key observations:**
- ~6 references cite real algorithms but with paraphrased titles (a hallmark of LLM-generated text that "knows" the algorithm but fabricates the exact title)
- The DOI mismatch (stream clustering vs. Monte Carlo rendering) is a strong fabrication signal
- Several invented algorithm names: "DPClust", "KD-stream", "Akan" — no papers with these names exist on Google Scholar
- Lower flag rate (29%) — most of the reference list is legitimate
- The pattern suggests selective fabrication of gap-filling references

### Verdict: SUSPICIOUS — MODERATE CONFIDENCE

**Confidence: 70%**. Approximately 10 of 23 flagged references appear genuinely fabricated (including invented algorithm names and a DOI mismatch). Another 6 are real papers with paraphrased titles. The lower flag rate (29%) and presence of many real references suggests this may be a partially LLM-assisted paper where the authors used an LLM to help "fill in" some references they couldn't find or didn't bother to look up properly. **Worth monitoring; editorial notification recommended with caveat about title variants.**

---

## Article D: IT-2 General Fuzzy Automata

**DOI**: 10.1016/j.asoc.2026.114970
**Title**: "Design and optimization of minimization algorithms for IT-2 general fuzzy automata"
**Authors**: Kh. Abolpour, M. Shamsizadeh
**Journal**: Applied Soft Computing (Jun 2026)
**Refs**: 36 total, 18 flagged (50%)

### Investigation

This paper has a very high fabrication rate with a distinctive pattern: nearly all flagged titles are **generic descriptions of fuzzy control/optimization topics** that read like LLM-generated summaries of the field rather than actual paper titles.

**Google Scholar Results:**

| Category | Count | References |
|----------|-------|------------|
| **Confirmed found on GS** | 1 | "Fuzzy automata and their applications" — real title is "Fuzzy automata and languages: theory and applications" (sim=0.80, close enough to be a title variant) |
| **Not found on GS** | 17 | All remaining titles not found via exact-phrase or fuzzy matching |

**The fabrication pattern is clear:**
- Titles are descriptive/generic rather than specific:
  - "Interval type-2 fuzzy decision support systems in healthcare"
  - "A hybrid PSOGA algorithm for fuzzy system optimization"
  - "Genetic algorithm and metaheuristics in optimization of fuzzy systems"
  - "Hybrid metaheuristic optimization in fuzzy logic-based control systems"
  - "Shadowed type-2 fuzzy sets for intelligent control"
  - "Interval type-2 fuzzy logic systems for sentiment analysis"
- These read like topic descriptions or textbook chapter titles, not real research paper titles
- None have exact matches on Google Scholar
- The only borderline match ("Fuzzy automata and their applications") is likely a title variant of the classic Wee (1967) / Mordeson & Malik (2002) book
- The field (fuzzy logic, type-2 fuzzy systems) has a well-established literature that is well-indexed — there is no "Chinese journal" excuse here
- 50% flag rate with 17/18 not findable is extremely suspicious

### Verdict: **FABRICATED — HIGH CONFIDENCE**

**Confidence: 93%**. 17 of 18 flagged references do not exist on Google Scholar. The titles are formulaic and generic, consistent with LLM-generated descriptions of the field rather than actual paper titles. The one "found" reference is a title variant of a real book. **This paper warrants immediate editorial notification.**

---

## Overall Assessment

### Confirmed Fabricators (recommend editorial notification):
1. **Article B** (10.1016/j.ins.2026.123423) — TumorNet, Information Sciences — ~22 fabricated refs (52% of total)
2. **Article D** (10.1016/j.asoc.2026.114970) — IT-2 Fuzzy Automata, Applied Soft Computing — ~17 fabricated refs (50% of total)

### Requires Further Investigation:
3. **Article C** (10.1016/j.eswa.2026.131840) — TNStream, Expert Systems with Applications — ~10 fabricated + 6 paraphrased titles (29% of total)

### Likely False Positive:
4. **Article A** (10.1016/j.asoc.2025.113711) — C2 Network Optimization, Applied Soft Computing — Most flagged refs are Chinese defense journal articles not indexed in Western databases

### Common Fabrication Patterns Observed:
1. **Formulaic title templates**: "[Architecture] for [task] using [dataset/method]" (Article B)
2. **Generic topic descriptions as titles**: "X in Y" format (Article D)
3. **Real algorithms, fake titles**: Correct algorithm name but paraphrased/invented title (Article C)
4. **DOI mismatches to unrelated papers**: Articles B and C both have DOIs pointing to completely unrelated studies
5. **Plausible but non-existent venues**: Real journal names combined with fabricated paper titles
