# CITADEL-X Production Scan — Master Log

## NEW CANONICAL PLAN (started T23:00)

Systematic 5,000-article scan: 4 years x 5 domains x 250 articles, seed=42.
All prior ad-hoc scans superseded. Using CrossRef ISSN-based sampling.

Manifest: 4,780 articles (law 2026 and history 2026 have smaller populations).
Avg refs/article: 64.4 → expected ~308K total references.

5 parallel domain scans launched simultaneously.
Process IDs: bf0n9grne (STEM), bkuva9tg3 (CS/AI), b9ncx2uk5 (Social), b1z1kzif7 (Law), blr2wnsgb (History).

## 2026-04-04 Session Start

### Prior Work Summary
- **300 articles** scanned in pilot phases (100 cross-domain + 200 STEM)
- **18,636 references** verified
- **3 confirmed fabrication cases** (68 fabricated refs total)
- Pipeline: CrossRef (discovery) + OpenAlex (verification, paid $50) + Serper.dev GS (rescue, paid $50)
- Module: `citadel_verify_nonbiomedical.py` (~950 lines)

### Production Targets
| Domain | Target | Prior | Remaining |
|--------|--------|-------|-----------|
| STEM (materials, chem, eng, physics) | 2,000 | 250 | 1,750 |
| Social sciences | 1,000 | 75 | 925 |
| Law / legal | 750 | 75 | 675 |
| History / humanities | 750 | 75 | 675 |
| Computer science / AI | 500 | 0 | 500 |
| **Total** | **5,000** | **475** | **4,525** |

### Immediate Priority
1. Investigate 22 remaining suspect articles from prior scans
2. Begin parallel domain extraction + verification

### Current Task
Setting up production logging, then launching suspect investigations + domain scans.

---

## 2026-04-04 T15:30 — Suspect Triage

22 remaining suspect articles (3+ flags, not yet investigated):

**HIGH PRIORITY (5+ flags, likely fabrication):**
- 10.1017/lsi.2026.10134 — Law & Social Inquiry (11 flags)
- 10.1177/00323217261428857 — Political Studies (9 flags)
- 10.1080/0023656x.2026.2642136 — Labor History (6 flags)
- 10.1016/j.ssc.2026.116386 — Solid State Communications (5 flags)

**MEDIUM PRIORITY (4 flags):**
- 10.1016/j.conbuildmat.2026.146155 — Construction and Building Materials
- 10.1016/j.rineng.2026.110031 — Results in Engineering
- 10.1016/j.cscm.2026.e05987 — Case Studies in Construction Materials
- 10.1016/j.ijlp.2026.102222 — Intl J Law and Psychiatry

**LOW PRIORITY (3 flags, likely false positives):**
- 8 articles with 3 flags each from CSCM, Inorganic Chem, Physica B, SSC, Labor History, Social Forces, ESR

---

## 2026-04-04 T16:30 — Progress Checkpoint

- Articles scanned so far: 300
- References verified: 18,636
- Suspect articles (3+ flags): 22 (10 investigated, 12 remaining)
- Confirmed fabrications: **4** (MRE ae45fa: 17, J Mol Liq: 16, J Build Eng: 35, SSC: 5)
- Fabricated refs total: **73**
- Domain breakdown: law 75 | history 75 | STEM 250 | social 75 | CS 0
- API calls: OpenAlex ~15K | CrossRef ~12K | GoogleScholar ~500
- Errors: None critical (Chinese-language false positives identified)
- Current tasks:
  - Social/law suspect batch investigation (running)
  - STEM 2024-2025 extraction of 500 articles (running)
- Next: Launch remaining domain extractions

### STEM Batch 1 Investigation Results
| Article | Journal | Flags | Verdict |
|---------|---------|-------|---------|
| 10.1016/j.ssc.2026.116386 | Solid State Comm. | 5 | **CONFIRMED** (5 fake, DOI swap + chimera) |
| 10.1016/j.conbuildmat.2026.146155 | Constr. Build. Mat. | 4 | FALSE POSITIVE (Chinese journals) |
| 10.1016/j.rineng.2026.110031 | Results in Eng. | 4 | FALSE POSITIVE (Chinese journals) |
| 10.1016/j.cscm.2026.e05987 | Case Studies Constr. | 4 | INCONCLUSIVE (2 FP, 2 probable fake) |

### Social/Law Batch 1 Investigation Results
All 4 articles CLEARED -- 30/30 flags are false positives (non-English citations):
| Article | Journal | Flags | Verdict |
|---------|---------|-------|---------|
| 10.1017/lsi.2026.10134 | Law & Social Inquiry | 11 | FALSE POSITIVE (Chinese legal journals) |
| 10.1177/00323217261428857 | Political Studies | 9 | FALSE POSITIVE (Chinese polisci) |
| 10.1080/0023656x.2026.2642136 | Labor History | 6 | FALSE POSITIVE (19th-c primary sources) |
| 10.1016/j.ijlp.2026.102222 | Intl J Law & Psych | 4 | FALSE POSITIVE (Polish journals) |

**Key insight**: Fabrication concentrates in mid-tier STEM. Non-STEM flags are nearly all non-English citation gaps.

---

## 2026-04-04 T21:00 — Progress Checkpoint

- Articles scanned so far: 500 (300 prior + 200 CS/AI)
- References verified: 29,114
- Confirmed fabrications: **5** (73 + 20 = **93 fabricated refs**)
- New confirmed: J Computational Science (10.1016/j.jocs.2026.102852) — 20/30 refs fabricated (67%)
- Domain breakdown: law 75 | history 75 | STEM 250 | social 75 | CS 200
- Running: STEM 2024-2025 scan (500 articles), social+law+history scan (600 articles)
- CS/AI scan complete: 200 articles, 10,478 refs, 108 flagged (1.0%), 10 suspect articles
  - Top 3 investigated: 1 confirmed fabrication, 2 false positives
  - Pipeline finding: arXiv-style unstructured citations cause DOI mismatch false positives — needs title extraction fix
- Next: Await STEM + social/law/history scans, investigate new suspects

### CS/AI Investigation Results
| Article | Journal | Flags | Verdict |
|---------|---------|-------|---------|
| 10.1016/j.jocs.2026.102852 | J Computational Science | 20/30 | **CONFIRMED** (67% fake, formulaic titles, Chinese journal fakes) |
| 10.1016/j.knosys.2025.114599 | Knowledge-Based Systems | 15/123 | FALSE POSITIVE (arXiv citation format issue) |
| 10.1016/j.eswa.2025.128820 | Expert Systems w/ Apps | 7/50 | FALSE POSITIVE (found on GS) |

---

## 2026-04-04 T22:30 — Progress Checkpoint

- Articles scanned so far: 1,000 (300 prior + 200 CS/AI + 500 STEM 2024-2025)
- References verified: 55,762
- Confirmed fabrications: **5 confirmed + 1 probable = 6 cases**
- Fabricated refs total: **~106**
- Domain breakdown: law 75 | history 75 | STEM 750 | social 75 | CS 200
- Running: Social+law+history scan (600 articles, social science near completion)
- STEM 2024-2025 results: 500 articles, 26,648 refs, 306 flagged (1.1%)
  - Year comparison: 2024=1.10%, 2025=1.20% — stable, no acceleration
  - 24 suspect articles; top 5 investigated: 1 probable fake, 4 false positives
  - Most false positives = Chinese domestic journal citations

### STEM 2024-2025 Investigation Results
| Article | Journal | Year | Flags | Verdict |
|---------|---------|------|-------|---------|
| 10.1016/j.physb.2025.417962 | Physica B | 2025 | 13/32 | **PROBABLE FAKE** (0/13 found on GS, duplicate refs, ghost journal entries) |
| 10.1016/j.physb.2024.416405 | Physica B | 2024 | 13/41 | FALSE POSITIVE (Chinese mining journals) |
| 10.1016/j.jobe.2024.111072 | J Build Eng | 2024 | 11/66 | FALSE POSITIVE (Chinese cement journals) |
| 10.1016/j.heliyon.2025.e44177 | Heliyon | 2025 | 10/72 | FALSE POSITIVE (Turkish medical journals) |
| 10.1088/2053-1591/ae2dcb | MRE | 2025 | 9/21 | FALSE POSITIVE (Chinese optics journals) |

### Emerging Pattern: False Positive Root Causes
1. **Chinese domestic journals** (70% of false positives) — CNKI-only indexed, absent from OpenAlex/CrossRef/GS
2. **Turkish medical journals** — similar indexing gap
3. **arXiv unstructured citations** — format causes DOI mismatch artifacts
4. **Historical primary sources** — newspapers, government docs
5. **Non-English book titles** — Polish, Dutch, Turkish

### Running Fabrication Rate by Year (STEM only)
| Year | Articles | Flag Rate | Confirmed/Probable Fakes | Fab Rate |
|------|----------|-----------|--------------------------|----------|
| 2024 | 260 | 1.10% | 0 confirmed | 0.0% |
| 2025 | 240 | 1.20% | 1 probable | ~0.4% |
| 2026 | 250 | 1.70% | 4 confirmed | 1.6% |

Fabrication rate appears to be **increasing** from 2024 to 2026, though sample sizes need to grow.

---

---
