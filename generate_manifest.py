"""
CITADEL-X Sampling Manifest Generator (CrossRef-based)
=======================================================
Generates a reproducible 5,000-article sampling frame:
  4 years x 5 domains x 250 articles = 5,000 total

Uses CrossRef ISSN-based sampling for reliable, reproducible results.
Each domain has 10 mid-tier journals. For each journal-year pair,
we pull articles with references and randomly sample to hit 250/cell.
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

# 5 domains x 10 journals each (mid-tier, IF<5 or unranked)
DOMAINS = {
    "stem": {
        "label": "STEM (materials, chemistry, engineering, physics)",
        "journals": [
            ("Materials Research Express", "2053-1591"),
            ("Construction and Building Materials", "0950-0618"),
            ("Journal of Building Engineering", "2352-7102"),
            ("Materials Today Communications", "2352-4928"),
            ("Case Studies in Construction Materials", "2214-5095"),
            ("RSC Advances", "2046-2069"),
            ("New Journal of Chemistry", "1144-0546"),
            ("Journal of Molecular Liquids", "0167-7322"),
            ("European Physical Journal Plus", "2190-5444"),
            ("Solid State Communications", "0038-1098"),
        ],
    },
    "cs_ai": {
        "label": "Computer Science / AI",
        "journals": [
            ("Expert Systems with Applications", "0957-4174"),
            ("Applied Soft Computing", "1568-4946"),
            ("Knowledge-Based Systems", "0950-7051"),
            ("Neurocomputing", "0925-2312"),
            ("Neural Computing and Applications", "0941-0643"),
            ("Pattern Recognition Letters", "0167-8655"),
            ("Information Sciences", "0020-0255"),
            ("Engineering Applications of Artificial Intelligence", "0952-1976"),
            ("Computers & Industrial Engineering", "0360-8352"),
            ("Journal of Computational Science", "1877-7503"),
        ],
    },
    "social_sciences": {
        "label": "Social Sciences",
        "journals": [
            ("Social Science Research", "0049-089X"),
            ("Social Forces", "0037-7732"),
            ("Political Studies", "0032-3217"),
            ("British Journal of Political Science", "0007-1234"),
            ("European Sociological Review", "0266-7215"),
            ("Applied Economics", "0003-6846"),
            ("Labour Economics", "0927-5371"),
            ("Social Indicators Research", "0303-8300"),
            ("Journal of European Social Policy", "0958-9287"),
            ("Regulation & Governance", "1748-5983"),
        ],
    },
    "law": {
        "label": "Law / Legal Scholarship",
        "journals": [
            ("Law and Social Inquiry", "0897-6546"),
            ("Journal of Legal Studies", "0047-2530"),
            ("Legal Studies", "0261-3875"),
            ("Journal of Law and Economics", "0022-2186"),
            ("Journal of Empirical Legal Studies", "1740-1453"),
            ("International Journal of Law and Psychiatry", "0160-2527"),
            ("Law & Society Review", "0023-9216"),
            ("Journal of Criminal Justice", "0047-2352"),
            ("Criminology", "0011-1384"),
            ("Regulation & Governance", "1748-5983"),
        ],
    },
    "history_humanities": {
        "label": "History / Humanities",
        "journals": [
            ("Journal of Modern History", "0022-2801"),
            ("Comparative Studies in Society and History", "0010-4175"),
            ("Journal of African History", "0021-8537"),
            ("Church History", "0009-6407"),
            ("Environmental History", "1084-5453"),
            ("Labor History", "0023-656X"),
            ("Medical History", "0025-7273"),
            ("French Historical Studies", "0016-1071"),
            ("Isis", "0021-1753"),
            ("Historical Methods", "0161-5440"),
        ],
    },
}


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
    except Exception as e:
        print(f"  [ERR] {issn} {year}: {e}", file=sys.stderr)
        return 0, []


def extract_article(item, domain, year):
    """Extract article metadata from CrossRef item. Returns dict or None."""
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

    # Get published year from item
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
    }


def main():
    random.seed(SEED)
    all_articles = []
    populations = defaultdict(int)  # (domain, year) -> count
    cell_articles = defaultdict(list)  # (domain, year) -> [articles]

    print("CITADEL-X Sampling Manifest Generator (CrossRef)")
    print(f"Target: {len(YEARS)} years x {len(DOMAINS)} domains x {ARTICLES_PER_CELL} = {len(YEARS)*len(DOMAINS)*ARTICLES_PER_CELL}")
    print(f"Seed: {SEED}")
    print("=" * 70)

    for domain_key, domain_info in DOMAINS.items():
        journals = domain_info["journals"]
        print(f"\n=== {domain_info['label']} ({len(journals)} journals) ===")

        for year in YEARS:
            cell_key = (domain_key, year)
            year_pool = []
            year_pop = 0

            for jname, issn in journals:
                total, items = fetch_crossref(issn, year, rows=50)
                time.sleep(0.3)

                year_pop += total

                for item in items:
                    art = extract_article(item, domain_key, year)
                    if art:
                        year_pool.append(art)

                # If we need more, fetch another page
                if total > 50 and len(year_pool) < ARTICLES_PER_CELL:
                    _, items2 = fetch_crossref(issn, year, rows=50, offset=50)
                    time.sleep(0.3)
                    for item in items2:
                        art = extract_article(item, domain_key, year)
                        if art:
                            year_pool.append(art)

            populations[cell_key] = year_pop

            # Deduplicate by DOI
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

            jname_safe = domain_key[:12]
            print(f"  {jname_safe:12s} {year}: pop={year_pop:>6,d}, pool={len(unique):>4d}, sampled={len(sample):>3d}")

    # Write CSV
    print(f"\n--- Writing {len(all_articles)} articles to {OUT_CSV} ---")
    with open(OUT_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["domain", "year", "doi", "journal", "title", "ref_count", "first_author"])
        writer.writeheader()
        for a in all_articles:
            writer.writerow(a)

    # Write sampling frame
    with open(OUT_FRAME, "w", encoding="utf-8") as f:
        f.write("# CITADEL-X Sampling Frame\n\n")
        f.write(f"Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Seed: {SEED}\n")
        f.write(f"Target: {ARTICLES_PER_CELL} articles per cell\n\n")

        f.write("## Population Sizes (CrossRef, peer-reviewed, mid-tier, >=10 refs)\n\n")
        f.write("| Domain | 2023 | 2024 | 2025 | 2026 | Total |\n")
        f.write("|--------|------|------|------|------|-------|\n")
        for dk in DOMAINS:
            row = [populations.get((dk, y), 0) for y in YEARS]
            total = sum(row)
            f.write(f"| {dk:20s} | {row[0]:>6,d} | {row[1]:>6,d} | {row[2]:>6,d} | {row[3]:>6,d} | {total:>8,d} |\n")
        col_totals = [sum(populations.get((dk, y), 0) for dk in DOMAINS) for y in YEARS]
        f.write(f"| {'**Total**':20s} | {col_totals[0]:>6,d} | {col_totals[1]:>6,d} | {col_totals[2]:>6,d} | {col_totals[3]:>6,d} | {sum(col_totals):>8,d} |\n")

        f.write(f"\n## Articles Sampled\n\n")
        f.write("| Domain | 2023 | 2024 | 2025 | 2026 | Total |\n")
        f.write("|--------|------|------|------|------|-------|\n")
        for dk in DOMAINS:
            row = [len(cell_articles.get((dk, y), [])) for y in YEARS]
            total = sum(row)
            f.write(f"| {dk:20s} | {row[0]:>4d} | {row[1]:>4d} | {row[2]:>4d} | {row[3]:>4d} | {total:>5d} |\n")
        col_s = [sum(len(cell_articles.get((dk, y), [])) for dk in DOMAINS) for y in YEARS]
        f.write(f"| {'**Total**':20s} | {col_s[0]:>4d} | {col_s[1]:>4d} | {col_s[2]:>4d} | {col_s[3]:>4d} | {sum(col_s):>5d} |\n")

    # Summary
    print(f"\n{'='*70}")
    print(f"MANIFEST COMPLETE: {len(all_articles)} articles")
    by_domain = defaultdict(int)
    by_year = defaultdict(int)
    for a in all_articles:
        by_domain[a["domain"]] += 1
        by_year[a["year"]] += 1
    print(f"By domain: {dict(sorted(by_domain.items()))}")
    print(f"By year: {dict(sorted(by_year.items()))}")
    avg_refs = sum(a["ref_count"] for a in all_articles) / max(1, len(all_articles))
    print(f"Avg refs/article: {avg_refs:.1f}")


if __name__ == "__main__":
    main()
