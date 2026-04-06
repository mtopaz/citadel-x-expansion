# CITADEL-X Sampling Strategy

## Two-Stage Stratified Random Sampling

### Stage 1: Journal Selection

**Universe definition**: All journals indexed in CrossRef that (a) deposit article references, (b) published ≥50 articles in 2024+, and (c) publish in STEM or CS/AI domains.

**Universe enumeration**: CrossRef faceted queries across 24 subject-area search terms (14 STEM + 10 CS/AI) returned all journals with articles matching each subject. Journals with <50 articles filtered out.

**Result**: 764 eligible journals (502 STEM, 262 CS/AI) with ISSN confirmed via CrossRef /journals endpoint.

**Stratification by impact**: Journals tiered by total DOI count in CrossRef (proxy for cumulative publication volume / impact):
- **Tier 1 (High impact)**: Top 20% — includes Nature-family, ACS, IEEE Transactions, etc.
- **Tier 2 (Mid-tier)**: 20th–60th percentile — solid discipline-specific journals
- **Tier 3 (Lower-tier)**: Bottom 40% — regional, newer, or niche journals

**Sampling allocation** (disproportionate stratified, oversampling high-risk tiers):
- Tier 1: 10 journals per domain (20% of sample — low expected fabrication, serves as control)
- Tier 2: 20 journals per domain (40%)
- Tier 3: 20 journals per domain (40%)
- Total: 50 journals per domain × 2 domains = **100 randomly selected journals**

**Random seed**: 42 (reproducible)

### Stage 2: Article Selection

For each sampled journal × year (2023, 2024, 2025, 2026):
- Query CrossRef for all articles with `has-references:true` and ≥10 references
- Draw up to N articles randomly (seed = 42 + batch × 1000)
- Exclude articles with >500 references (encyclopedias, special issues)

### Defensibility

1. **Reproducible**: Fixed seed, journal universe and sample saved as CSV
2. **Two-stage random**: Both journal selection and article selection use random sampling
3. **Stratified by impact tier**: Enables within-tier rate estimation; oversampling of high-risk tiers is standard epidemiological practice for case detection studies
4. **Universe documented**: All 764 eligible journals listed in `journal_universe.csv` with tier classification
5. **Domain focus justified**: STEM + CS/AI chosen because (a) DOI coverage enables verification (>80%), (b) prior evidence of LLM-driven fabrication in these domains, (c) social sciences/law/humanities have <50% verifiable references due to book/legal citation practices, making fabrication detection unreliable

### Limitations

1. Journal universe constructed from CrossRef subject-area queries, which depend on publisher-assigned subject tags. Some journals may be misclassified or missing.
2. Impact factor proxy (total DOIs) is imperfect — a high-volume journal could be either high-impact or predatory.
3. Tier boundaries (20/60/100 percentiles) are arbitrary; sensitivity analyses with different cutoffs should be reported.
4. Article selection within journal is not fully random for the initial production scan (sorted by publication date); subsequent batches use random seeds.

### Files

- `journal_universe.csv` — 764 journals with domain, tier, ISSN, volume
- `sampled_journals.csv` — 100 randomly selected journals
- `sampling_manifest.csv` — all sampled articles with DOIs
