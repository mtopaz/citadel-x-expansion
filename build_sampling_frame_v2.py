#!/usr/bin/env python
"""
build_sampling_frame_v2.py  --  CITADEL-X Clean Sampling Frame Builder
======================================================================
Reads the raw journal universe (1,376 journals from CrossRef facets),
applies title-based include/exclude filters to remove contamination
(biomedical, neuroscience, ecology, etc.), enriches with ISSNs from
CrossRef /journals endpoint, tiers by total DOIs, and draws a
stratified random sample of 130 journals (65 per domain).

Output files:
  - journal_universe_clean.csv   (all journals surviving filters)
  - sampled_journals_v2.csv      (130 sampled journals)

Seed: 42 for reproducibility.
"""

import csv
import io
import os
import random
import re
import sys
import time
from pathlib import Path

import requests

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
BASE_DIR = Path(r"C:\Users\SON1\OneDrive - cumc.columbia.edu\Desktop\Grants_US\Claude_code\Fake_refernces")
RAW_CSV = BASE_DIR / "journal_universe_raw.csv"
CLEAN_CSV = BASE_DIR / "journal_universe_clean.csv"
SAMPLE_CSV = BASE_DIR / "sampled_journals_v2.csv"

SEED = 42
CROSSREF_TIMEOUT = 5  # seconds
CROSSREF_HEADERS = {
    "User-Agent": "CITADEL-X/1.0 (mailto:mt3920@cumc.columbia.edu)",
}

# ---------------------------------------------------------------------------
# Domain filter definitions
# ---------------------------------------------------------------------------

STEM_INCLUDE = [
    'materials', 'material', 'chemistry', 'chemical', 'physics', 'physical',
    'engineering', 'mechanics', 'mechanical', 'civil', 'structural',
    'polymer', 'ceramic', 'metallurg', 'alloy', 'composite', 'concrete',
    'construction', 'building', 'corrosion', 'coating', 'surface',
    'semiconductor', 'superconductor', 'magnet', 'optic', 'photon',
    'nanotechnol', 'nano', 'thin film', 'crystal', 'spectroscop',
    'electroch', 'catalys', 'energy', 'thermal', 'thermodynamic',
    'fluid', 'combustion', 'tribolog', 'manufactur', 'industrial',
    'applied science', 'rsc', 'acs', 'iop', 'phys rev', 'j phys',
]

STEM_EXCLUDE = [
    'medic', 'clinical', 'health', 'disease', 'cancer', 'neuro', 'neural',
    'pharmac', 'biolog', 'biotech', 'bioscience', 'genome', 'cell', 'immun',
    'pathol', 'surg', 'cardio', 'dent', 'nurs', 'psych', 'rehabilitat',
    'ocean', 'marine', 'earth', 'geolog', 'atmosph', 'ecolog',
    'environ', 'food', 'agric', 'veterinar', 'plant', 'animal', 'cereal',
]

CS_INCLUDE = [
    'computer', 'comput', 'software', 'artificial intelligence',
    'machine learning', 'neural', 'pattern recognition', 'data mining',
    'information science', 'information system', 'knowledge',
    'intelligent', 'fuzzy', 'expert system', 'deep learning',
    'natural language', 'image process', 'signal process',
    'cybersecur', 'network', 'algorithm', 'automat',
    'ieee trans', 'acm', 'aaai', 'ijcai',
]

CS_EXCLUDE = [
    'medic', 'clinical', 'health', 'biolog', 'bioscience', 'brain', 'cortex',
    'neuro',  # but NOT 'neurocomput' -- handled specially
    'genome', 'cell',
    'ocean', 'earth', 'atmosph', 'ecolog', 'geophys',
    'surg', 'cardio', 'dent', 'nurs', 'psych', 'pharmac',
    'immun', 'pathol', 'cancer', 'disease',
    'agric', 'food', 'veterinar', 'plant', 'animal', 'cereal',
    'biodata', 'biotechnol', 'rehabilitat', 'regenerat',
]

# Journals containing "neural" that are neuroscience (not CS/AI)
# "neural network", "neural comput", "neural process", "neural system" = CS OK
# "neural transmission", "neural circuit", "neural engineering", "neural regenerat" = neuro, NOT OK
CS_NEURAL_OK_COMPOUNDS = [
    'neural network', 'neural comput', 'neural process', 'neural system',
    'neural inform',
]

# Additional broad/mega-journals and clearly off-domain titles to exclude
# from BOTH domains -- these are multidisciplinary or off-topic
GLOBAL_EXCLUDE_TITLES = {
    'scientific reports',
    'nature communications',
    'plos one',
    'ssrn electronic journal',
    'sustainability',
    'cureus',
    'data in brief',
    'scientific data',
    'applied sciences',  # too broad
    'mathematics',
    'science of the total environment',
    'science',
    'nature',
    'proceedings of the national academy of sciences',
}


def html_unescape(s: str) -> str:
    """Unescape HTML entities like &amp; -> &."""
    return (s.replace("&amp;", "&")
             .replace("&lt;", "<")
             .replace("&gt;", ">")
             .replace("&quot;", '"')
             .replace("&#39;", "'"))


def matches_any(title_lower: str, patterns: list[str]) -> bool:
    """Return True if title_lower contains any of the patterns."""
    return any(p in title_lower for p in patterns)


def passes_stem_filter(title: str) -> bool:
    """Return True if journal title qualifies for STEM domain."""
    t = title.lower()
    if t in GLOBAL_EXCLUDE_TITLES:
        return False
    if not matches_any(t, STEM_INCLUDE):
        return False
    if matches_any(t, STEM_EXCLUDE):
        return False
    return True


def passes_cs_filter(title: str) -> bool:
    """Return True if journal title qualifies for CS/AI domain."""
    t = title.lower()
    if t in GLOBAL_EXCLUDE_TITLES:
        return False
    if not matches_any(t, CS_INCLUDE):
        return False
    # Special handling: 'neurocomput' is OK, but 'neuro' alone is not
    for excl in CS_EXCLUDE:
        if excl in t:
            if excl == 'neuro' and 'neurocomput' in t:
                continue  # allow neurocomputing
            return False
    # Special handling for "neural": only allow CS-related neural compounds
    # e.g. "neural network", "neural computation" are CS;
    # "neural transmission", "neural circuit", "neural regeneration" are neuro
    if 'neural' in t:
        if not any(compound in t for compound in CS_NEURAL_OK_COMPOUNDS):
            return False
    return True


def load_raw_journals(path: Path) -> list[dict]:
    """Load the raw journal CSV."""
    journals = []
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            row["journal"] = html_unescape(row["journal"])
            row["article_count_2024plus"] = int(row["article_count_2024plus"])
            journals.append(row)
    print(f"  Loaded {len(journals)} raw journals "
          f"({sum(1 for j in journals if j['domain']=='stem')} STEM, "
          f"{sum(1 for j in journals if j['domain']=='cs_ai')} CS/AI)")
    return journals


def apply_filters(journals: list[dict]) -> list[dict]:
    """Apply include/exclude title filters to each domain."""
    clean = []
    dropped_stem = []
    dropped_cs = []

    for j in journals:
        title = j["journal"]
        domain = j["domain"]

        if domain == "stem":
            if passes_stem_filter(title):
                clean.append(j)
            else:
                dropped_stem.append(title)
        elif domain == "cs_ai":
            if passes_cs_filter(title):
                clean.append(j)
            else:
                dropped_cs.append(title)
        else:
            # Unknown domain -- skip
            pass

    stem_kept = sum(1 for j in clean if j["domain"] == "stem")
    cs_kept = sum(1 for j in clean if j["domain"] == "cs_ai")

    print(f"\n  After filtering:")
    print(f"    STEM:  {stem_kept} kept, {len(dropped_stem)} dropped")
    print(f"    CS/AI: {cs_kept} kept, {len(dropped_cs)} dropped")
    print(f"    Total: {len(clean)} clean journals")

    # Show some dropped examples
    print(f"\n  Example STEM drops (first 15):")
    for t in dropped_stem[:15]:
        print(f"    - {t}")
    print(f"\n  Example CS/AI drops (first 15):")
    for t in dropped_cs[:15]:
        print(f"    - {t}")

    return clean


def enrich_with_crossref(journals: list[dict]) -> list[dict]:
    """Query CrossRef /journals for ISSN and total_dois for each journal."""
    print(f"\n  Enriching {len(journals)} journals via CrossRef /journals endpoint...")
    enriched = []
    failures = 0
    session = requests.Session()
    session.headers.update(CROSSREF_HEADERS)

    for i, j in enumerate(journals):
        title = j["journal"]
        if (i + 1) % 50 == 0 or i == 0:
            print(f"    Progress: {i+1}/{len(journals)} "
                  f"({failures} failures so far)")

        # Search CrossRef /journals by query
        try:
            resp = session.get(
                "https://api.crossref.org/journals",
                params={"query": title, "rows": 3},
                timeout=CROSSREF_TIMEOUT,
            )
            if resp.status_code == 200:
                data = resp.json()
                items = data.get("message", {}).get("items", [])
                # Find best match by title similarity
                best = None
                best_score = 0
                for item in items:
                    cr_title = item.get("title", "").lower().strip()
                    j_title = title.lower().strip()
                    # Exact or close match
                    if cr_title == j_title:
                        best = item
                        best_score = 100
                        break
                    # Partial match score
                    words_j = set(j_title.split())
                    words_cr = set(cr_title.split())
                    if words_j and words_cr:
                        overlap = len(words_j & words_cr) / max(len(words_j), len(words_cr))
                        if overlap > best_score:
                            best_score = overlap
                            best = item

                if best and best_score >= 0.5:
                    j["issn"] = ";".join(best.get("ISSN", []))
                    j["total_dois"] = best.get("counts", {}).get("total-dois", 0)
                    j["crossref_title"] = best.get("title", "")
                else:
                    j["issn"] = ""
                    j["total_dois"] = j["article_count_2024plus"]  # fallback
                    j["crossref_title"] = ""
                    failures += 1
            else:
                j["issn"] = ""
                j["total_dois"] = j["article_count_2024plus"]
                j["crossref_title"] = ""
                failures += 1
        except (requests.RequestException, ValueError, KeyError) as e:
            j["issn"] = ""
            j["total_dois"] = j["article_count_2024plus"]
            j["crossref_title"] = ""
            failures += 1

        enriched.append(j)

        # Be polite: small delay between requests
        time.sleep(0.1)

    print(f"    Done. {failures} failures out of {len(journals)}.")
    return enriched


def assign_tiers(journals: list[dict], domain: str) -> list[dict]:
    """Assign T1/T2/T3 based on total_dois percentiles within domain."""
    domain_journals = [j for j in journals if j["domain"] == domain]
    domain_journals.sort(key=lambda x: x["total_dois"], reverse=True)
    n = len(domain_journals)
    t1_cutoff = int(n * 0.20)
    t2_cutoff = int(n * 0.60)

    for i, j in enumerate(domain_journals):
        if i < t1_cutoff:
            j["tier"] = "T1"
        elif i < t2_cutoff:
            j["tier"] = "T2"
        else:
            j["tier"] = "T3"

    return domain_journals


def draw_sample(journals: list[dict], domain: str, seed: int = SEED) -> list[dict]:
    """Stratified random sample: 15 T1 + 25 T2 + 25 T3 = 65."""
    rng = random.Random(seed)

    t1 = [j for j in journals if j["domain"] == domain and j["tier"] == "T1"]
    t2 = [j for j in journals if j["domain"] == domain and j["tier"] == "T2"]
    t3 = [j for j in journals if j["domain"] == domain and j["tier"] == "T3"]

    # Sample sizes (cap at tier size if tier is smaller)
    n_t1 = min(15, len(t1))
    n_t2 = min(25, len(t2))
    n_t3 = min(25, len(t3))

    sample = []
    sample.extend(rng.sample(t1, n_t1))
    sample.extend(rng.sample(t2, n_t2))
    sample.extend(rng.sample(t3, n_t3))

    return sample


def save_clean_universe(journals: list[dict], path: Path):
    """Save the clean journal universe CSV."""
    fieldnames = ["journal", "domain", "tier", "issn", "total_dois",
                  "article_count_2024plus", "crossref_title"]
    with open(path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for j in sorted(journals, key=lambda x: (x["domain"], x["tier"],
                                                   -x["total_dois"])):
            writer.writerow(j)
    print(f"\n  Saved clean universe: {path}")
    print(f"    {len(journals)} journals total")


def save_sample(sample: list[dict], path: Path):
    """Save the sampled journals CSV."""
    fieldnames = ["journal", "domain", "tier", "issn", "total_dois",
                  "article_count_2024plus"]
    with open(path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for j in sorted(sample, key=lambda x: (x["domain"], x["tier"],
                                                 -x["total_dois"])):
            writer.writerow(j)
    print(f"  Saved sample: {path}")
    print(f"    {len(sample)} journals total")


def print_summary(sample: list[dict]):
    """Print a nice summary table."""
    print("\n" + "=" * 80)
    print("SAMPLING FRAME SUMMARY")
    print("=" * 80)

    for domain in ["stem", "cs_ai"]:
        domain_label = "STEM (Materials/Chemistry/Physics/Engineering)" if domain == "stem" else "CS/AI"
        d_sample = [j for j in sample if j["domain"] == domain]
        print(f"\n  {domain_label}: {len(d_sample)} journals sampled")
        print(f"  {'─' * 70}")

        for tier in ["T1", "T2", "T3"]:
            tier_journals = [j for j in d_sample if j["tier"] == tier]
            tier_label = {"T1": "High-impact (top 20%)",
                          "T2": "Mid-tier (20-60th pctl)",
                          "T3": "Lower-tier (bottom 40%)"}[tier]
            print(f"\n    {tier} — {tier_label}: {len(tier_journals)} journals")

            # Show top 5 by total_dois
            tier_journals.sort(key=lambda x: x["total_dois"], reverse=True)
            for j in tier_journals[:5]:
                print(f"      {j['journal'][:60]:<62} "
                      f"({j['total_dois']:>8,} DOIs)")
            if len(tier_journals) > 5:
                print(f"      ... and {len(tier_journals) - 5} more")

    print(f"\n  Total sampled: {len(sample)} journals")
    print("=" * 80)


def main():
    print("CITADEL-X Sampling Frame Builder v2")
    print("=" * 50)

    # Step 1: Load raw journals
    print("\n[1/6] Loading raw journal universe...")
    raw = load_raw_journals(RAW_CSV)

    # Step 2: Apply title-based filters
    print("\n[2/6] Applying domain-specific include/exclude filters...")
    clean = apply_filters(raw)

    # Step 3: Enrich via CrossRef
    print("\n[3/6] Enriching with CrossRef ISSN + total_dois...")
    enriched = enrich_with_crossref(clean)

    # Step 4: Assign tiers
    print("\n[4/6] Assigning tiers by total_dois percentile...")
    stem_tiered = assign_tiers(enriched, "stem")
    cs_tiered = assign_tiers(enriched, "cs_ai")
    all_tiered = stem_tiered + cs_tiered

    for domain, tiered in [("STEM", stem_tiered), ("CS/AI", cs_tiered)]:
        t1 = sum(1 for j in tiered if j["tier"] == "T1")
        t2 = sum(1 for j in tiered if j["tier"] == "T2")
        t3 = sum(1 for j in tiered if j["tier"] == "T3")
        print(f"    {domain}: T1={t1}, T2={t2}, T3={t3}, Total={len(tiered)}")

    # Step 5: Draw stratified sample
    print("\n[5/6] Drawing stratified random sample (seed=42)...")
    sample_stem = draw_sample(all_tiered, "stem", SEED)
    sample_cs = draw_sample(all_tiered, "cs_ai", SEED)
    full_sample = sample_stem + sample_cs
    print(f"    STEM: {len(sample_stem)} journals")
    print(f"    CS/AI: {len(sample_cs)} journals")
    print(f"    Total: {len(full_sample)} journals")

    # Step 6: Save files
    print("\n[6/6] Saving output files...")
    save_clean_universe(all_tiered, CLEAN_CSV)
    save_sample(full_sample, SAMPLE_CSV)

    # Summary
    print_summary(full_sample)


if __name__ == "__main__":
    main()
