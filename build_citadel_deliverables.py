"""
CITADEL-X Production Scan -- Final Deliverables Builder
Merges per-domain CSVs and builds summary statistics JSON.
"""

import pandas as pd
import json
from pathlib import Path

BASE = Path(r"C:/Users/SON1/OneDrive - cumc.columbia.edu/Desktop/Grants_US/Claude_code/Fake_refernces")

# ── Domain labels ──────────────────────────────────────────────────────────
DOMAINS = ["stem", "cs_ai", "social_sciences", "law", "history_humanities"]

VERIFIED_FILES = [BASE / f"citadel_{d}_verified.csv" for d in DOMAINS]
FLAGGED_FILES  = [BASE / f"citadel_{d}_flagged_prod.csv" for d in DOMAINS]

# ── TASK 1: Merge CSVs ────────────────────────────────────────────────────
print("=== TASK 1: Merging CSVs ===")

# Verified
dfs_v = [pd.read_csv(f, low_memory=False) for f in VERIFIED_FILES]
full_results = pd.concat(dfs_v, ignore_index=True)
out_verified = BASE / "citadel_full_results.csv"
full_results.to_csv(out_verified, index=False)
print(f"  citadel_full_results.csv  -> {len(full_results):,} rows")

# Flagged
dfs_f = [pd.read_csv(f, low_memory=False) for f in FLAGGED_FILES]
full_flagged = pd.concat(dfs_f, ignore_index=True)
out_flagged = BASE / "citadel_full_flagged.csv"
full_flagged.to_csv(out_flagged, index=False)
print(f"  citadel_full_flagged.csv  -> {len(full_flagged):,} rows")

# ── TASK 2: Build summary stats ──────────────────────────────────────────
print("\n=== TASK 2: Building summary stats ===")

# Scan-level totals (from known scan outputs)
domain_stats = {
    "stem":                {"articles": 1000, "refs": 56526, "flagged": 752},
    "cs_ai":               {"articles": 1000, "refs": 52761, "flagged": 603},
    "social_sciences":     {"articles": 1000, "refs": 66901, "flagged": 760},
    "law":                 {"articles":  962, "refs": 69598, "flagged": 854},
    "history_humanities":  {"articles":  818, "refs": 55680, "flagged": 1403},
}

total_articles = sum(d["articles"] for d in domain_stats.values())
total_refs     = sum(d["refs"]     for d in domain_stats.values())

# Year-level ref counts per domain (refs / flagged)
year_data = {
    "stem":   {2023: (13205, 160), 2024: (13176, 162), 2025: (14899, 199), 2026: (15246, 231)},
    "cs_ai":  {2023: (13179, 105), 2024: (13720,  86), 2025: (13031, 179), 2026: (12831, 233)},
    "social_sciences": {2023: (16221, 139), 2024: (17179, 169), 2025: (17056, 268), 2026: (16445, 184)},
    "law":    {2023: (16197, 175), 2024: (18534, 222), 2025: (19491, 238), 2026: (15376, 219)},
    "history_humanities": {2023: (17836, 284), 2024: (16914, 413), 2025: (16418, 527), 2026: (4512, 179)},
}

# Confirmed fakes (post quality-audit)
confirmed_cases = [
    {"doi": "10.1088/2053-1591/ae45fa",      "journal": "Materials Research Express",           "year": 2026, "domain": "stem",  "fake_refs": 17, "total_refs": 66,  "publisher": "IOP Publishing"},
    {"doi": "10.1016/j.molliq.2026.129534",   "journal": "Journal of Molecular Liquids",        "year": 2026, "domain": "stem",  "fake_refs": 16, "total_refs": 56,  "publisher": "Elsevier"},
    {"doi": "10.1016/j.jobe.2026.115980",     "journal": "Journal of Building Engineering",     "year": 2026, "domain": "stem",  "fake_refs": 35, "total_refs": 85,  "publisher": "Elsevier"},
    {"doi": "10.1016/j.ssc.2026.116386",      "journal": "Solid State Communications",          "year": 2026, "domain": "stem",  "fake_refs": 5,  "total_refs": 60,  "publisher": "Elsevier"},
    {"doi": "10.1016/j.jocs.2026.102852",     "journal": "Journal of Computational Science",    "year": 2026, "domain": "cs_ai", "fake_refs": 20, "total_refs": 30,  "publisher": "Elsevier"},
    {"doi": "10.1016/j.physb.2025.417962",    "journal": "Physica B",                           "year": 2025, "domain": "stem",  "fake_refs": 13, "total_refs": 32,  "publisher": "Elsevier"},
    {"doi": "10.1016/j.conbuildmat.2025.144502", "journal": "Construction and Building Materials", "year": 2025, "domain": "stem", "fake_refs": 14, "total_refs": 42, "publisher": "Elsevier"},
    {"doi": "10.1088/2053-1591/ae284b",       "journal": "Materials Research Express",           "year": 2025, "domain": "stem",  "fake_refs": 8,  "total_refs": 64,  "publisher": "IOP Publishing"},
    {"doi": "10.1016/j.ins.2026.123423",      "journal": "Information Sciences",                "year": 2026, "domain": "cs_ai", "fake_refs": 23, "total_refs": 50,  "publisher": "Elsevier"},
    {"doi": "10.1016/j.asoc.2026.114970",     "journal": "Applied Soft Computing",              "year": 2026, "domain": "cs_ai", "fake_refs": 17, "total_refs": 36,  "publisher": "Elsevier"},
    {"doi": "10.1016/j.eswa.2026.131840",     "journal": "Expert Systems with Applications",    "year": 2026, "domain": "cs_ai", "fake_refs": 13, "total_refs": 78,  "publisher": "Elsevier"},
]

confirmed_fake_articles = len(confirmed_cases)
confirmed_fake_refs     = sum(c["fake_refs"] for c in confirmed_cases)

# ── Rate per 10K refs ─────────────────────────────────────────────────────
overall_rate = round(confirmed_fake_refs / total_refs * 10000, 1)

# Rate by domain: fake refs in that domain / total refs in that domain * 10K
domain_fake_refs = {}
for c in confirmed_cases:
    domain_fake_refs[c["domain"]] = domain_fake_refs.get(c["domain"], 0) + c["fake_refs"]

rate_by_domain = {}
for d in DOMAINS:
    fr = domain_fake_refs.get(d, 0)
    tr = domain_stats[d]["refs"]
    rate_by_domain[d] = round(fr / tr * 10000, 1) if tr else 0

# Rate by year: fake refs in that year / total refs scanned in that year * 10K
year_total_refs = {}
for d, ydict in year_data.items():
    for yr, (refs, _flagged) in ydict.items():
        year_total_refs[yr] = year_total_refs.get(yr, 0) + refs

year_fake_refs = {}
for c in confirmed_cases:
    year_fake_refs[c["year"]] = year_fake_refs.get(c["year"], 0) + c["fake_refs"]

rate_by_year = {}
for yr in sorted(year_total_refs):
    fr = year_fake_refs.get(yr, 0)
    tr = year_total_refs[yr]
    rate_by_year[str(yr)] = round(fr / tr * 10000, 1) if tr else 0

# Rate by domain x year
rate_by_domain_year = {}
for d in DOMAINS:
    for yr in sorted(year_data[d]):
        key = f"{d}_{yr}"
        refs_in_cell = year_data[d][yr][0]
        fakes_in_cell = sum(
            c["fake_refs"] for c in confirmed_cases
            if c["domain"] == d and c["year"] == yr
        )
        rate_by_domain_year[key] = round(fakes_in_cell / refs_in_cell * 10000, 1) if refs_in_cell else 0

# Top 10 worst articles (by fake ref count desc, then fake fraction desc)
top10 = sorted(confirmed_cases, key=lambda c: (-c["fake_refs"], -c["fake_refs"]/c["total_refs"]))[:10]
top10_out = []
for rank, c in enumerate(top10, 1):
    top10_out.append({
        "rank": rank,
        "doi": c["doi"],
        "journal": c["journal"],
        "year": c["year"],
        "domain": c["domain"],
        "fake_refs": c["fake_refs"],
        "total_refs": c["total_refs"],
        "fake_fraction": round(c["fake_refs"] / c["total_refs"], 3),
    })

# Publisher concentration
publisher_counts = {}
for c in confirmed_cases:
    publisher_counts[c["publisher"]] = publisher_counts.get(c["publisher"], 0) + 1

# ── Assemble JSON ─────────────────────────────────────────────────────────
summary = {
    "scan_name": "CITADEL-X Production Scan",
    "scan_date": "2026-04-04",
    "total_articles": total_articles,
    "total_refs": total_refs,
    "total_flagged_refs": sum(d["flagged"] for d in domain_stats.values()),
    "confirmed_fake_articles": confirmed_fake_articles,
    "confirmed_fake_refs": confirmed_fake_refs,
    "overall_fake_rate_per_10K": overall_rate,
    "rate_by_domain": rate_by_domain,
    "rate_by_year": rate_by_year,
    "rate_by_domain_year": rate_by_domain_year,
    "top_10_worst_articles": top10_out,
    "publisher_concentration": publisher_counts,
    "domain_scan_details": {
        d: {
            "articles": domain_stats[d]["articles"],
            "refs": domain_stats[d]["refs"],
            "flagged": domain_stats[d]["flagged"],
            "confirmed_fakes": domain_fake_refs.get(d, 0),
        }
        for d in DOMAINS
    },
}

out_json = BASE / "citadel_summary_stats.json"
with open(out_json, "w") as f:
    json.dump(summary, f, indent=2)

print(f"\n  citadel_summary_stats.json written.")

# ── Print key numbers ─────────────────────────────────────────────────────
print(f"\n{'='*60}")
print(f"  Total articles scanned:      {total_articles:,}")
print(f"  Total refs checked:          {total_refs:,}")
print(f"  Total flagged refs:          {summary['total_flagged_refs']:,}")
print(f"  Confirmed fake articles:     {confirmed_fake_articles}")
print(f"  Confirmed fake refs:         {confirmed_fake_refs}")
print(f"  Overall fake rate per 10K:   {overall_rate}")
print(f"  Rate by domain:              {rate_by_domain}")
print(f"  Rate by year:                {rate_by_year}")
print(f"  Publisher concentration:     {publisher_counts}")
print(f"{'='*60}")
print("Done.")
