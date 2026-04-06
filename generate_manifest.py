"""
CITADEL-X Sampling Manifest Generator (CrossRef-based)
=======================================================
Two-stage stratified random sampling:
  Stage 1: 100 journals randomly selected from 764-journal universe
           (50 STEM + 50 CS/AI, stratified by impact tier)
  Stage 2: Articles randomly sampled within each journal-year cell

Uses sampled_journals.csv (from build_sampling_frame.py) as input.
Generates sampling_manifest.csv with article DOIs for scanning.
"""

import requests
import csv
import time
import random
import sys
from pathlib import Path
from collections import defaultdict

SEED = 42
ARTICLES_PER_CELL = 250
YEARS = [2023, 2024, 2025, 2026]
CROSSREF_BASE = "https://api.crossref.org/works"
HEADERS = {"User-Agent": "CITADEL/1.0 (mailto:mt3920@cumc.columbia.edu)"}

PROJECT_DIR = Path(__file__).parent
OUT_CSV = PROJECT_DIR / "sampling_manifest.csv"
OUT_FRAME = PROJECT_DIR / "sampling_frame.md"
SAMPLED_JOURNALS = PROJECT_DIR / "sampled_journals_v2.csv"


def load_sampled_journals():
    """Load randomly sampled journals from sampled_journals.csv."""
    domains = defaultdict(list)
    with open(SAMPLED_JOURNALS, encoding='utf-8') as f:
        for row in csv.DictReader(f):
            tier_str = row['tier'].replace('T', '')
            issn = row['issn'].split(';')[0].strip()  # Take first ISSN if multiple
            domains[row['domain']].append((row['journal'], issn, int(tier_str)))
    return dict(domains)


def fetch_crossref(issn, year, rows=50, offset=0):
    """Fetch articles from CrossRef by ISSN and year."""
    params = {
        "filter": f"type:journal-article,from-pub-date:{year}-01-01,until-pub-date:{year}-12-31,has-references:true,issn:{issn}",
        "rows": rows,
        "offset": offset,
        "select": "DOI,title,author,container-title,published,reference",
        "sort": "published",
        "order": "desc",
    }
    try:
        r = requests.get(CROSSREF_BASE, params=params, headers=HEADERS, timeout=30)
        if r.status_code == 200:
            data = r.json()
            total = data.get("message", {}).get("total-results", 0)
            items = data.get("message", {}).get("items", [])
            return total, items
        return 0, []
    except Exception:
        return 0, []


def extract_article(item, domain, year, tier):
    """Extract article metadata from CrossRef item."""
    doi = item.get("DOI", "")
    if not doi:
        return None
    titles = item.get("title", [])
    title = titles[0] if titles else ""
    containers = item.get("container-title", [])
    journal = containers[0] if containers else ""
    refs = item.get("reference", [])
    ref_count = len(refs)
    if ref_count < 10:
        return None
    if ref_count > 500:
        return None
    published = item.get("published", {})
    date_parts = published.get("date-parts", [[]])
    pub_year = date_parts[0][0] if date_parts and date_parts[0] else year
    authors = []
    for a in item.get("author", []):
        given = a.get("given", "")
        family = a.get("family", "")
        if family:
            authors.append(f"{given} {family}".strip() if given else family)
    return {
        "domain": domain,
        "year": pub_year,
        "doi": doi,
        "journal": journal,
        "title": title,
        "ref_count": ref_count,
        "first_author": authors[0] if authors else "",
        "tier": tier,
    }


def main():
    random.seed(SEED)
    domains = load_sampled_journals()
    all_articles = []
    populations = defaultdict(int)
    cell_articles = defaultdict(list)

    total_journals = sum(len(v) for v in domains.values())
    print(f"CITADEL-X Manifest Generator (Two-Stage Stratified Random)")
    print(f"Journals: {total_journals} ({', '.join(f'{k}={len(v)}' for k,v in domains.items())})")
    print(f"Years: {YEARS}")
    print(f"Target: {ARTICLES_PER_CELL} articles per domain-year cell")
    print(f"Seed: {SEED}")
    print("=" * 70)

    for domain_key, journal_list in domains.items():
        print(f"\n=== {domain_key.upper()} ({len(journal_list)} journals) ===")

        for year in YEARS:
            cell_key = (domain_key, year)
            year_pool = []
            year_pop = 0

            for jname, issn, tier in journal_list:
                total, items = fetch_crossref(issn, year, rows=50)
                time.sleep(0.3)
                year_pop += total
                for item in items:
                    art = extract_article(item, domain_key, year, tier)
                    if art:
                        year_pool.append(art)
                # Fetch page 2 if needed
                if total > 50 and len(year_pool) < ARTICLES_PER_CELL:
                    _, items2 = fetch_crossref(issn, year, rows=50, offset=50)
                    time.sleep(0.3)
                    for item in items2:
                        art = extract_article(item, domain_key, year, tier)
                        if art:
                            year_pool.append(art)

            populations[cell_key] = year_pop

            # Deduplicate
            seen = set()
            unique = []
            for a in year_pool:
                if a["doi"] not in seen:
                    seen.add(a["doi"])
                    unique.append(a)

            # Random sample
            if len(unique) > ARTICLES_PER_CELL:
                sample = random.sample(unique, ARTICLES_PER_CELL)
            else:
                sample = unique

            cell_articles[cell_key] = sample
            all_articles.extend(sample)
            print(f"  {domain_key[:12]:12s} {year}: pop={year_pop:>6,d}, pool={len(unique):>4d}, sampled={len(sample):>3d}")

    # Write manifest CSV
    print(f"\n--- Writing {len(all_articles)} articles to {OUT_CSV} ---")
    with open(OUT_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["domain", "year", "doi", "journal", "title", "ref_count", "first_author", "tier"])
        writer.writeheader()
        for a in all_articles:
            writer.writerow(a)

    # Write sampling frame doc
    with open(OUT_FRAME, "w", encoding="utf-8") as f:
        f.write("# CITADEL-X Sampling Frame\n\n")
        f.write(f"Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Seed: {SEED}\n")
        f.write(f"Method: Two-stage stratified random sampling\n")
        f.write(f"Stage 1: {total_journals} journals randomly selected from 764-journal universe\n")
        f.write(f"Stage 2: Up to {ARTICLES_PER_CELL} articles randomly sampled per domain-year cell\n\n")

        f.write("## Population Sizes\n\n")
        f.write("| Domain | 2023 | 2024 | 2025 | 2026 | Total |\n")
        f.write("|--------|------|------|------|------|-------|\n")
        for dk in domains:
            row = [populations.get((dk, y), 0) for y in YEARS]
            f.write(f"| {dk:20s} | {row[0]:>6,d} | {row[1]:>6,d} | {row[2]:>6,d} | {row[3]:>6,d} | {sum(row):>8,d} |\n")

        f.write(f"\n## Articles Sampled\n\n")
        f.write("| Domain | 2023 | 2024 | 2025 | 2026 | Total |\n")
        f.write("|--------|------|------|------|------|-------|\n")
        for dk in domains:
            row = [len(cell_articles.get((dk, y), [])) for y in YEARS]
            f.write(f"| {dk:20s} | {row[0]:>4d} | {row[1]:>4d} | {row[2]:>4d} | {row[3]:>4d} | {sum(row):>5d} |\n")

    # Summary
    print(f"\n{'='*70}")
    print(f"MANIFEST COMPLETE: {len(all_articles)} articles")
    by_domain = defaultdict(int)
    by_year = defaultdict(int)
    by_tier = defaultdict(int)
    for a in all_articles:
        by_domain[a["domain"]] += 1
        by_year[a["year"]] += 1
        by_tier[a.get("tier", "?")] += 1
    print(f"By domain: {dict(sorted(by_domain.items()))}")
    print(f"By year: {dict(sorted(by_year.items()))}")
    print(f"By tier: {dict(sorted(by_tier.items()))}")
    avg_refs = sum(a["ref_count"] for a in all_articles) / max(1, len(all_articles))
    print(f"Avg refs/article: {avg_refs:.1f}")


if __name__ == "__main__":
    main()
