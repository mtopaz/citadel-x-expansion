"""
CITADEL-X Production Scanner
=============================
Reads articles from sampling_manifest.csv for a specific domain,
fetches full references from CrossRef, runs verification, outputs results.

Usage:
    python citadel_production_scan.py --domain stem
    python citadel_production_scan.py --domain cs_ai
    python citadel_production_scan.py --domain social_sciences
    python citadel_production_scan.py --domain law
    python citadel_production_scan.py --domain history_humanities
"""

import csv
import json
import time
import sys
import os
import signal
import logging
import argparse
from pathlib import Path
from collections import Counter, defaultdict

import requests

# Global state for graceful shutdown on timeout
_all_rows = []
_out_results = None
_out_flagged = None
_csv_fields = None

def _write_partial_results(signum=None, frame=None):
    """Write whatever results we have so far (called on SIGTERM/timeout)."""
    global _all_rows, _out_results, _out_flagged, _csv_fields
    if not _all_rows or not _out_results or not _csv_fields:
        return
    log.info(f"Writing partial results ({len(_all_rows)} rows) before exit...")
    with open(_out_results, 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=_csv_fields)
        w.writeheader()
        w.writerows(_all_rows)
    flagged = [r for r in _all_rows if r.get('fabrication_flag')]
    with open(_out_flagged, 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=_csv_fields)
        w.writeheader()
        w.writerows(flagged)
    log.info(f"Partial results saved: {_out_results} ({len(_all_rows)} rows), {_out_flagged} ({len(flagged)} flagged)")
    if signum:
        sys.exit(0)

signal.signal(signal.SIGTERM, _write_partial_results)

# Setup
PROJECT_DIR = Path(__file__).parent
sys.path.insert(0, str(PROJECT_DIR))

# Load .env
if (PROJECT_DIR / '.env').exists():
    with open(PROJECT_DIR / '.env') as f:
        for line in f:
            line = line.strip()
            if '=' in line and not line.startswith('#'):
                k, v = line.split('=', 1)
                os.environ.setdefault(k.strip(), v.strip())

from citadel_verify_nonbiomedical import verify_citation, VerificationResult

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s [%(levelname)s] %(message)s',
                    datefmt='%H:%M:%S', stream=sys.stderr)
log = logging.getLogger('scan')

CROSSREF_BASE = "https://api.crossref.org/works"
CR_HEADERS = {"User-Agent": "CITADEL/1.0 (mailto:mt3920@cumc.columbia.edu)"}

DOMAIN_THRESH = {
    "stem": "stem",
    "cs_ai": "stem",
    "social_sciences": "social_sciences",
    "law": "law",
    "history_humanities": "humanities",
}

CSV_FIELDS = [
    'domain', 'year', 'article_doi', 'article_title', 'article_journal',
    'ref_number', 'ref_doi', 'ref_title', 'ref_author', 'ref_year',
    'ref_journal', 'ref_unstructured', 'verdict', 'confidence',
    'fabrication_flag', 'similarity_score', 'source_checked',
    'matched_title', 'matched_doi', 'evidence_note',
]


def fetch_references(doi):
    """Fetch full reference list for an article from CrossRef."""
    try:
        r = requests.get(f"{CROSSREF_BASE}/{doi}",
                        headers=CR_HEADERS, timeout=30)
        if r.status_code == 200:
            msg = r.json().get("message", {})
            refs = msg.get("reference", [])
            return refs
        return []
    except Exception:
        return []


def parse_ref(ref):
    """Parse a CrossRef reference into a citation dict."""
    return {
        'title': ref.get('article-title') or ref.get('volume-title'),
        'article_title': ref.get('article-title') or ref.get('volume-title'),
        'doi': ref.get('DOI'),
        'DOI': ref.get('DOI'),
        'author': ref.get('author'),
        'year': ref.get('year'),
        'journal': ref.get('journal-title') or ref.get('series-title'),
        'journal_title': ref.get('journal-title') or ref.get('series-title'),
        'unstructured': ref.get('unstructured'),
        'volume_title': ref.get('volume-title'),
        'key': ref.get('key', ''),
    }


def run_domain_scan(domain):
    """Run full scan for one domain."""
    manifest = PROJECT_DIR / "sampling_manifest.csv"
    out_results = PROJECT_DIR / f"citadel_{domain}_verified.csv"
    out_flagged = PROJECT_DIR / f"citadel_{domain}_flagged_prod.csv"
    out_jsonl = PROJECT_DIR / f"citadel_{domain}_verified.jsonl"

    # Read manifest
    articles = []
    with open(manifest, encoding='utf-8') as f:
        for row in csv.DictReader(f):
            if row['domain'] == domain:
                articles.append(row)

    log.info(f"=== {domain.upper()} SCAN: {len(articles)} articles ===")
    thresh = DOMAIN_THRESH.get(domain, "general")

    # Set globals for graceful shutdown
    global _all_rows, _out_results, _out_flagged, _csv_fields
    _out_results = out_results
    _out_flagged = out_flagged
    _csv_fields = CSV_FIELDS

    start = time.time()
    all_rows = []
    _all_rows = all_rows  # point global to same list
    stats = {'total': 0, 'verified': 0, 'flagged': 0, 'unverifiable': 0}
    article_flags = {}
    by_year = defaultdict(lambda: {'total': 0, 'flagged': 0})

    for i, art in enumerate(articles):
        doi = art['doi']
        year = int(art['year'])
        journal = art['journal']
        title = art['title'][:80]

        # Fetch references from CrossRef
        refs_raw = fetch_references(doi)
        time.sleep(0.3)

        if not refs_raw or len(refs_raw) < 10:
            log.info(f"  [{i+1}/{len(articles)}] {journal[:35]} ({year}) | SKIP ({len(refs_raw)} refs)")
            continue

        if len(refs_raw) > 500:
            log.info(f"  [{i+1}/{len(articles)}] {journal[:35]} ({year}) | SKIP outlier ({len(refs_raw)} refs)")
            continue

        log.info(f"  [{i+1}/{len(articles)}] {journal[:35]} ({year}) | {len(refs_raw)} refs")

        art_flagged = 0
        art_results = []

        for j, ref_raw in enumerate(refs_raw):
            stats['total'] += 1
            by_year[year]['total'] += 1
            citation = parse_ref(ref_raw)

            try:
                result = verify_citation(citation, domain=thresh)
            except Exception as e:
                result = VerificationResult(verdict='error', confidence=0.0,
                                           evidence={'error': str(e)})

            ev = result.evidence or {}
            row = {
                'domain': domain, 'year': year,
                'article_doi': doi, 'article_title': title,
                'article_journal': journal,
                'ref_number': j + 1,
                'ref_doi': citation.get('doi') or '',
                'ref_title': (citation.get('title') or '')[:200],
                'ref_author': citation.get('author') or '',
                'ref_year': citation.get('year') or '',
                'ref_journal': citation.get('journal') or '',
                'ref_unstructured': (citation.get('unstructured') or '')[:300],
                'verdict': result.verdict,
                'confidence': round(result.confidence, 3),
                'fabrication_flag': result.fabrication_flag,
                'similarity_score': ev.get('similarity_score', ''),
                'source_checked': ev.get('source_checked', ''),
                'matched_title': (ev.get('matched_title') or '')[:200],
                'matched_doi': ev.get('matched_doi', ''),
                'evidence_note': ev.get('note', ''),
            }
            all_rows.append(row)
            art_results.append(row)

            if result.verdict == 'verified':
                stats['verified'] += 1
            elif result.fabrication_flag:
                stats['flagged'] += 1
                by_year[year]['flagged'] += 1
                art_flagged += 1
            else:
                stats['unverifiable'] += 1

        if art_flagged >= 3:
            article_flags[doi] = (journal, year, art_flagged, len(refs_raw))

        # Progress every 25 articles
        if (i + 1) % 25 == 0:
            elapsed = time.time() - start
            log.info(f"    === {stats['total']} refs, {stats['flagged']} flagged, "
                    f"{len(article_flags)} suspects, {elapsed:.0f}s ===")

    # Write results
    with open(out_results, 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=CSV_FIELDS)
        w.writeheader()
        w.writerows(all_rows)

    flagged_rows = [r for r in all_rows if r['fabrication_flag']]
    with open(out_flagged, 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=CSV_FIELDS)
        w.writeheader()
        w.writerows(flagged_rows)

    # Write JSONL (article-level summary)
    with open(out_jsonl, 'w', encoding='utf-8') as f:
        for doi_key, (jnl, yr, cnt, total) in article_flags.items():
            f.write(json.dumps({
                'doi': doi_key, 'journal': jnl, 'year': yr,
                'flagged_refs': cnt, 'total_refs': total,
                'domain': domain,
            }) + '\n')

    elapsed = time.time() - start
    print(f"\n{'='*70}")
    print(f"{domain.upper()} SCAN COMPLETE")
    print(f"{'='*70}")
    print(f"Time: {elapsed:.0f}s ({elapsed/60:.1f} min)")
    print(f"Articles: {len(articles)} | Refs: {stats['total']}")
    print(f"Verified: {stats['verified']} ({100*stats['verified']/max(1,stats['total']):.1f}%)")
    print(f"Flagged: {stats['flagged']} ({100*stats['flagged']/max(1,stats['total']):.1f}%)")
    print(f"Unverifiable: {stats['unverifiable']} ({100*stats['unverifiable']/max(1,stats['total']):.1f}%)")

    print(f"\nBy year:")
    for y in sorted(by_year.keys()):
        d = by_year[y]
        pct = 100 * d['flagged'] / max(1, d['total'])
        print(f"  {y}: {d['total']} refs, {d['flagged']} flagged ({pct:.2f}%)")

    print(f"\nSuspect articles (3+ flags):")
    for d, (j, y, c, t) in sorted(article_flags.items(), key=lambda x: -x[1][2]):
        jn = j[:40].encode('ascii', 'replace').decode()
        print(f"  {c:3d}/{t:3d}: {jn} ({y}) | {d}")

    print(f"\nOutput: {out_results} ({len(all_rows)} rows)")
    print(f"Flagged: {out_flagged} ({len(flagged_rows)} rows)")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--domain", required=True,
                       choices=list(DOMAIN_THRESH.keys()))
    args = parser.parse_args()
    run_domain_scan(args.domain)
