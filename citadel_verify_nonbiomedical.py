#!/usr/bin/env python
"""
citadel_verify_nonbiomedical.py - CITADEL-X Core Verification Module
====================================================================
Non-biomedical citation verification for the CITADEL-X pipeline.

Verifies citations from social sciences, humanities, law, engineering,
and other non-biomedical domains using OpenAlex (primary), CrossRef (fallback),
and title similarity scoring.

Usage:
    # As a module:
    from citadel_verify_nonbiomedical import verify_citation, verify_article_references
    result = verify_citation({"article_title": "...", "doi": "..."})

    # Standalone self-test:
    python citadel_verify_nonbiomedical.py

Author: Max Topaz / Claude Code
Date: 2026-04-04
"""

import os
import re
import sys
import time
import json
import logging
import unicodedata
from dataclasses import dataclass, field, asdict
from difflib import SequenceMatcher
from typing import Optional, List, Dict, Any, Tuple
from datetime import datetime, date

import requests

# ============================================================================
# .env Loading (same pattern as google_scholar_verify.py)
# ============================================================================

_ENV_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env')
if os.path.exists(_ENV_PATH):
    with open(_ENV_PATH) as f:
        for line in f:
            line = line.strip()
            if '=' in line and not line.startswith('#'):
                key, val = line.split('=', 1)
                os.environ.setdefault(key.strip(), val.strip())

# ============================================================================
# Logging
# ============================================================================

logger = logging.getLogger("citadel_x")
if not logger.handlers:
    handler = logging.StreamHandler(sys.stderr)
    handler.setFormatter(logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    ))
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

# ============================================================================
# Constants
# ============================================================================

OPENALEX_BASE = "https://api.openalex.org"
OPENALEX_MAILTO = "mt3920@cumc.columbia.edu"
OPENALEX_DAILY_SEARCH_BUDGET = 100000  # Paid plan

CROSSREF_BASE = "https://api.crossref.org/works"
CROSSREF_USER_AGENT = (
    "CITADEL-X/1.0 (https://github.com/mtopaz/citadel; "
    "mailto:mt3920@cumc.columbia.edu)"
)

# Rate limit delays (seconds)
OPENALEX_DELAY = 0.15
CROSSREF_DELAY = 0.3

# Retry settings
MAX_RETRIES = 3
INITIAL_BACKOFF = 1.0  # seconds

# HTTP timeout
HTTP_TIMEOUT = 15  # seconds

# ============================================================================
# Domain-Specific Thresholds
# ============================================================================

DOMAIN_THRESHOLDS = {
    "stem":           {"match": 0.70, "mismatch": 0.35, "uncertain_low": 0.50},
    "social_science": {"match": 0.68, "mismatch": 0.33, "uncertain_low": 0.48},
    "humanities":     {"match": 0.65, "mismatch": 0.30, "uncertain_low": 0.45},
    "law":            {"match": 0.65, "mismatch": 0.30, "uncertain_low": 0.45},
    "general":        {"match": 0.70, "mismatch": 0.35, "uncertain_low": 0.50},
}


# ============================================================================
# Data Classes
# ============================================================================

@dataclass
class VerificationResult:
    """Result of verifying a single citation."""

    # Classification
    verdict: str = "unverifiable"
    # One of: verified, doi_mismatch, title_not_found, title_swap,
    #         unverifiable, book_unverifiable, legal_citation,
    #         uncertain, parsing_artifact, error
    confidence: float = 0.0  # 0.0 - 1.0

    # Evidence
    evidence: Dict[str, Any] = field(default_factory=dict)
    # Keys: similarity_score, source_checked, matched_title, matched_doi,
    #       matched_year, note, error_message, etc.

    # Fabrication flag
    fabrication_flag: bool = False
    # True only for doi_mismatch and title_not_found after verification

    def to_csv_row(self) -> Dict[str, str]:
        """Return a flat dict suitable for csv.DictWriter."""
        return {
            "verdict": self.verdict,
            "confidence": f"{self.confidence:.3f}",
            "fabrication_flag": str(self.fabrication_flag),
            "similarity_score": str(self.evidence.get("similarity_score", "")),
            "source_checked": str(self.evidence.get("source_checked", "")),
            "matched_title": str(self.evidence.get("matched_title", "")),
            "matched_doi": str(self.evidence.get("matched_doi", "")),
            "matched_year": str(self.evidence.get("matched_year", "")),
            "note": str(self.evidence.get("note", "")),
            "error_message": str(self.evidence.get("error_message", "")),
        }

    def to_dict(self) -> Dict[str, Any]:
        """Full serialization."""
        return {
            "verdict": self.verdict,
            "confidence": self.confidence,
            "fabrication_flag": self.fabrication_flag,
            "evidence": self.evidence,
        }


# ============================================================================
# Legal Citation Detection
# ============================================================================

LEGAL_CITATION_PATTERNS = [
    # US case law: "Party v. Party, Volume Reporter Page (Year)"
    re.compile(
        r'\b\w+\s+v\.?\s+\w+.*?\d+\s+(?:U\.?S\.?|S\.?\s*Ct\.?|F\.?\s*(?:2d|3d|4th)|'
        r'L\.?\s*Ed\.?|A\.?\s*(?:2d|3d)|N\.?[EWSY]\.?\s*(?:2d)?|P\.?\s*(?:2d|3d)|'
        r'So\.?\s*(?:2d|3d)|Cal\.?\s*(?:2d|3d|4th|5th))\s*\d+'
    ),
    # US statute: "42 U.S.C. ss 1983"
    re.compile(r'\d+\s+U\.?S\.?C\.?\s*(?:\u00a7|ss?\.?)\s*\d+'),
    # US Code of Federal Regulations
    re.compile(r'\d+\s+C\.?F\.?R\.?\s*(?:\u00a7|ss?\.?)\s*\d+'),
    # UK case law: "[2023] UKSC 12"
    re.compile(r'\[\d{4}\]\s+(?:UKSC|UKHL|EWCA|EWHC|AC|QB|Ch|WLR|All ER)'),
    # EU case law: "Case C-123/45"
    re.compile(r'Case\s+(?:C|T)-\d+/\d+'),
    # Generic "v." pattern with reporter volume
    re.compile(r'\b[A-Z][a-z]+\s+v\.\s+[A-Z].*?,\s+\d+\s+[A-Z]'),
]


def is_legal_citation(text: str) -> bool:
    """Detect if text is a legal case/statute citation."""
    if not text:
        return False
    for pat in LEGAL_CITATION_PATTERNS:
        if pat.search(text):
            return True
    return False


# ============================================================================
# Book Detection
# ============================================================================

BOOK_INDICATORS = [
    re.compile(
        r'\b(?:University Press|Oxford UP|Cambridge UP|Harvard UP|MIT Press|'
        r'Princeton UP|Yale UP|Stanford UP|Chicago UP|Columbia UP|'
        r'Routledge|Springer|Wiley|Elsevier|Sage|Palgrave|Macmillan|'
        r'Penguin|Random House|HarperCollins|Norton|McGraw.Hill|'
        r'Academic Press|World Scientific|CRC Press)\b',
        re.IGNORECASE,
    ),
    re.compile(r'\b(?:eds?\.|edited by|translat(?:ed|ion) by)\b', re.IGNORECASE),
    re.compile(r'\b(?:pp?\.\s*\d+[-\u2013]\d+)\b'),
    re.compile(r'\b(?:Vol\.\s*\d+|Chapter\s+\d+)\b', re.IGNORECASE),
    re.compile(
        r'(?:ISBN[:\s-]*)?(?:97[89][- ]?)?\d{1,5}[- ]?\d{1,7}[- ]?\d{1,7}[- ]?\d{1,7}[- ]?[\dXx]'
    ),
    # Additional book indicators
    re.compile(r'\b(?:Press|Publishing|Publishers)\b', re.IGNORECASE),
    re.compile(
        r'\((?:London|New York|Cambridge|Oxford|Chicago|Princeton|Toronto|'
        r'Philadelphia|Boston|Berkeley|Edinburgh|Paris|Berlin|Amsterdam):',
        re.IGNORECASE,
    ),
]


def looks_like_book(text: str) -> bool:
    """Heuristic: does this reference look like a book citation?"""
    if not text:
        return False
    score = sum(1 for pat in BOOK_INDICATORS if pat.search(text))
    return score >= 1


# ============================================================================
# Reference Parser (Tier 1: Regex + Tier 2: Heuristic)
# ============================================================================

CITATION_PATTERNS = [
    # APA style: Author, A. B. (2023). Title. Journal, vol(issue), pages.
    {
        "name": "apa",
        "pattern": re.compile(
            r'^(?P<authors>[^(]+?)\s*\((?P<year>\d{4})\)\.\s*'
            r'(?P<title>[^.]+(?:\.[^.]+)*?)\.\s*'
            r'(?P<journal>[^,]+),\s*(?P<volume>\d+)'
        ),
        "priority": 1,
    },
    # Chicago/Turabian: Author. "Title." Journal vol, no. issue (year): pages.
    {
        "name": "chicago",
        "pattern": re.compile(
            r'^(?P<authors>[^"\u201c]+?)\.\s*'
            r'["\u201c](?P<title>[^"\u201d]+)["\u201d]\.\s*'
            r'(?P<journal>[^,]+?)\s+(?P<volume>\d+)'
        ),
        "priority": 2,
    },
    # Harvard: Author (Year) Title, Journal, vol(issue), pp.
    {
        "name": "harvard",
        "pattern": re.compile(
            r'^(?P<authors>[^(]+?)\s*\((?P<year>\d{4})\)\s+'
            r'(?P<title>[^,]+),\s*(?P<journal>[^,]+),'
        ),
        "priority": 3,
    },
    # Book: Author (Year). Title. Place: Publisher.
    {
        "name": "book",
        "pattern": re.compile(
            r'^(?P<authors>[^(]+?)\s*\((?P<year>\d{4})\)\.\s*'
            r'(?P<title>[^.]+(?:\.[^.]+)*?)\.\s*'
            r'(?P<place>[^:]+):\s*(?P<publisher>[^.]+)'
        ),
        "priority": 4,
    },
    # Book chapter: Author (Year). 'Chapter Title' in Editor (ed.) Book Title.
    {
        "name": "book_chapter",
        "pattern": re.compile(
            r"^(?P<authors>[^(]+?)\s*\((?P<year>\d{4})\)\.\s*"
            r"['\u2018](?P<title>[^'\u2019]+)['\u2019]\s+in\s+"
            r"(?P<editor>[^(]+?)\s*\(ed"
        ),
        "priority": 5,
    },
    # Inline DOI
    {
        "name": "doi_inline",
        "pattern": re.compile(
            r'(?:https?://doi\.org/|doi:\s*)(?P<doi>10\.\d{4,}/[^\s]+)'
        ),
        "priority": 0,
    },
]


def parse_reference_regex(raw_text: str) -> Optional[Dict[str, str]]:
    """
    Tier 1: Regex-based reference parsing.
    Returns extracted fields dict or None if no pattern matched.
    """
    if not raw_text or len(raw_text.strip()) < 10:
        return None

    # Sort by priority
    sorted_patterns = sorted(CITATION_PATTERNS, key=lambda p: p["priority"])

    for pat_info in sorted_patterns:
        m = pat_info["pattern"].search(raw_text)
        if m:
            fields = {k: v.strip() for k, v in m.groupdict().items() if v}
            fields["parse_method"] = f"regex_{pat_info['name']}"
            return fields

    return None


def parse_reference_heuristic(raw_text: str) -> Dict[str, str]:
    """
    Tier 2: Heuristic field extraction from unstructured reference text.
    Always returns a dict (possibly empty) with whatever fields could be extracted.
    """
    fields = {}
    if not raw_text:
        return fields

    # Year extraction
    year_match = re.search(r'\((\d{4})\)|,?\s*(\d{4})\s*[,.\)]', raw_text)
    if year_match:
        fields["year"] = year_match.group(1) or year_match.group(2)

    # DOI extraction
    doi_match = re.search(r'(10\.\d{4,9}/[^\s,;}\]]+)', raw_text)
    if doi_match:
        fields["doi"] = doi_match.group(1).rstrip(".")

    # Quoted title extraction (high confidence)
    quoted = re.search(r'["\u201c\u2018\'](.*?)["\u201d\u2019\']', raw_text)
    if quoted and len(quoted.group(1)) > 10:
        fields["title"] = quoted.group(1)

    # If no quoted title, try text between year and next period
    if "title" not in fields and year_match:
        after_year = raw_text[year_match.end():].strip().lstrip(").,: ")
        # Take text up to the next period followed by a space or journal-like pattern
        title_match = re.match(r'([^.]+(?:\.[^.]+)?)', after_year)
        if title_match and len(title_match.group(1).strip()) > 15:
            fields["title"] = title_match.group(1).strip()

    # Author extraction (text before year, up to ~200 chars)
    if year_match:
        author_block = raw_text[: year_match.start()].strip().rstrip("(,. ")
        if 5 < len(author_block) < 200:
            fields["authors"] = author_block

    if fields:
        fields["parse_method"] = "heuristic"

    return fields


def parse_reference(raw_text: str) -> Dict[str, str]:
    """
    Parse a raw reference string into structured fields.
    Tries Tier 1 (regex), then Tier 2 (heuristic).
    Flags references that need LLM parsing as needing_llm_parse.
    """
    if not raw_text or len(raw_text.strip()) < 10:
        return {"parse_method": "too_short", "needs_llm_parse": "true"}

    # Tier 1: Regex
    result = parse_reference_regex(raw_text)
    if result:
        return result

    # Tier 2: Heuristic
    result = parse_reference_heuristic(raw_text)
    if result and ("title" in result or "doi" in result):
        return result

    # Neither tier could extract enough -- flag for LLM parsing
    return {
        "raw_text": raw_text,
        "parse_method": "none",
        "needs_llm_parse": "true",
    }


# ============================================================================
# Text Normalization & Title Similarity
# (ported from content_verifier.py combined_title_similarity approach)
# ============================================================================

def strip_markup(text: str) -> str:
    """Remove MathML, HTML tags, and XML entities from title strings."""
    if not text:
        return ""
    # Strip all XML/HTML/MathML tags, replace with space to preserve word boundaries
    text = re.sub(r'<[^>]+>', ' ', text)
    # Decode common entities
    text = text.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>')
    text = text.replace('&apos;', "'").replace('&quot;', '"')
    # Collapse spaces within chemical/math formulas: "Mo 3 Sb 7" → "Mo3Sb7"
    text = re.sub(r'(?<=[A-Za-z])\s+(?=\d)', '', text)
    text = re.sub(r'(?<=\d)\s+(?=[A-Za-z])', '', text)
    # Normalize whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def normalize_text(text: str) -> str:
    """Normalize text for comparison: lowercase, remove punctuation, normalize unicode."""
    if not text:
        return ""
    # Strip MathML/HTML markup first
    text = strip_markup(text)
    # Unicode normalization
    text = unicodedata.normalize("NFKC", text)
    # Lowercase
    text = text.lower()
    # Strip any remaining HTML tags
    text = re.sub(r'</?[a-zA-Z][^>]*>', '', text)
    # Remove punctuation except spaces
    text = re.sub(r'[^\w\s]', ' ', text)
    # Normalize whitespace
    text = ' '.join(text.split())
    return text


def sequence_similarity(s1: str, s2: str) -> float:
    """SequenceMatcher-based similarity (0-1)."""
    if not s1 and not s2:
        return 1.0
    if not s1 or not s2:
        return 0.0
    return SequenceMatcher(None, s1, s2).ratio()


def word_overlap_score(s1: str, s2: str) -> float:
    """Jaccard-like word overlap score (0-1)."""
    if not s1 and not s2:
        return 1.0
    if not s1 or not s2:
        return 0.0
    words1 = set(s1.split())
    words2 = set(s2.split())
    if not words1 or not words2:
        return 0.0
    intersection = len(words1 & words2)
    union = len(words1 | words2)
    return intersection / union if union > 0 else 0.0


def containment_score(s1: str, s2: str) -> float:
    """
    Check if one title is contained within the other.
    Returns a bonus score (0 or 0.85) when one string is a substantial
    substring of the other.
    """
    if not s1 or not s2:
        return 0.0
    # Only trigger containment for strings of reasonable length
    shorter = s1 if len(s1) <= len(s2) else s2
    longer = s2 if len(s1) <= len(s2) else s1
    if len(shorter) < 10:
        return 0.0
    if shorter in longer:
        return 0.85
    return 0.0


def combined_title_similarity(claimed: str, actual: str) -> float:
    """
    Combined title similarity using SequenceMatcher + word overlap + containment.
    Returns max of the three approaches.
    Ported from content_verifier.py with containment bonus added per spec.
    """
    # Strip MathML/HTML markup before normalization
    claimed_norm = normalize_text(strip_markup(claimed))
    actual_norm = normalize_text(strip_markup(actual))

    if not claimed_norm or not actual_norm:
        return 0.0

    seq_sim = sequence_similarity(claimed_norm, actual_norm)
    word_sim = word_overlap_score(claimed_norm, actual_norm)
    contain = containment_score(claimed_norm, actual_norm)

    # Combined: weighted blend of seq + word, then take max with containment
    # Weights follow content_verifier.py: 0.4 * levenshtein + 0.6 * jaccard
    blended = 0.4 * seq_sim + 0.6 * word_sim
    return max(blended, contain)


# ============================================================================
# API Helpers with Retry
# ============================================================================

def _retry_request(method: str, url: str, session: requests.Session,
                   max_retries: int = MAX_RETRIES,
                   **kwargs) -> Optional[requests.Response]:
    """
    Make an HTTP request with exponential backoff on 429 / 5xx.
    Returns the Response or None on exhausted retries.
    """
    kwargs.setdefault("timeout", HTTP_TIMEOUT)
    backoff = INITIAL_BACKOFF
    for attempt in range(max_retries + 1):
        try:
            resp = session.request(method, url, **kwargs)
            if resp.status_code == 200:
                return resp
            if resp.status_code == 404:
                return resp  # caller handles 404
            if resp.status_code == 429 or resp.status_code >= 500:
                if attempt < max_retries:
                    logger.warning(
                        "HTTP %d from %s, retrying in %.1fs (attempt %d/%d)",
                        resp.status_code, url, backoff, attempt + 1, max_retries
                    )
                    time.sleep(backoff)
                    backoff *= 2
                    continue
            # Other error codes
            logger.warning("HTTP %d from %s", resp.status_code, url)
            return resp
        except requests.exceptions.Timeout:
            if attempt < max_retries:
                logger.warning("Timeout on %s, retrying in %.1fs", url, backoff)
                time.sleep(backoff)
                backoff *= 2
                continue
            logger.error("Timeout on %s after %d retries", url, max_retries)
            return None
        except requests.exceptions.RequestException as exc:
            logger.error("Request error on %s: %s", url, exc)
            return None
    return None


# ============================================================================
# OpenAlex Verifier
# ============================================================================

class OpenAlexVerifier:
    """OpenAlex-based citation verification."""

    def __init__(self, email: str = OPENALEX_MAILTO):
        self.email = email
        self.session = requests.Session()
        api_key = os.environ.get('OPENALEX_API_KEY', '')
        if api_key:
            self.session.params = {"mailto": email, "api_key": api_key}  # type: ignore[assignment]
        else:
            self.session.params = {"mailto": email}  # type: ignore[assignment]
        self.daily_search_count = 0
        self._budget_exhausted = False  # Set True after first 429 on search

    @property
    def budget_remaining(self) -> int:
        return max(0, OPENALEX_DAILY_SEARCH_BUDGET - self.daily_search_count)

    def lookup_by_doi(self, doi: str) -> Optional[dict]:
        """
        Direct DOI lookup -- FREE, not counted against search budget.
        Returns OpenAlex work object or None.
        """
        doi = doi.strip().strip("/")
        url = f"{OPENALEX_BASE}/works/doi:{doi}"
        resp = _retry_request("GET", url, self.session)
        if resp is not None and resp.status_code == 200:
            try:
                return resp.json()
            except (ValueError, json.JSONDecodeError):
                return None
        return None

    def search_by_title(self, title: str, year: str = None,
                        per_page: int = 5) -> List[dict]:
        """
        Title search -- costs 1 search credit per call.
        Returns list of candidate work objects.
        Skips immediately if budget is known to be exhausted (avoids 429 retry storms).
        """
        if self._budget_exhausted:
            return []  # Skip -- caller will use CrossRef fallback

        if self.daily_search_count >= OPENALEX_DAILY_SEARCH_BUDGET:
            logger.warning("OpenAlex daily search budget exhausted (%d/%d)",
                           self.daily_search_count, OPENALEX_DAILY_SEARCH_BUDGET)
            self._budget_exhausted = True
            return []

        # Strategy 1: Exact title filter
        params: Dict[str, Any] = {
            "filter": f'title.search:"{title[:200]}"',
            "per_page": per_page,
        }
        if year:
            params["filter"] += f",publication_year:{year}"

        resp = _retry_request("GET", f"{OPENALEX_BASE}/works",
                              self.session, params=params)
        self.daily_search_count += 1
        time.sleep(OPENALEX_DELAY)

        # Detect budget exhaustion from 429 response
        if resp is not None and resp.status_code == 429:
            logger.info("OpenAlex search budget exhausted (got 429). Switching to CrossRef-only mode.")
            self._budget_exhausted = True
            return []

        if resp is not None and resp.status_code == 200:
            try:
                results = resp.json().get("results", [])
                if results:
                    return results
            except (ValueError, json.JSONDecodeError):
                pass

        # Strategy 2: Broader keyword search (first 10 content words)
        words = _extract_content_words(title, max_words=10)
        if not words:
            return []
        search_query = " ".join(words)

        params = {"search": search_query, "per_page": per_page}
        if year:
            params["filter"] = f"publication_year:{year}"

        resp = _retry_request("GET", f"{OPENALEX_BASE}/works",
                              self.session, params=params)
        self.daily_search_count += 1
        time.sleep(OPENALEX_DELAY)

        if resp is not None and resp.status_code == 429:
            self._budget_exhausted = True
            return []

        if resp is not None and resp.status_code == 200:
            try:
                return resp.json().get("results", [])
            except (ValueError, json.JSONDecodeError):
                pass

        return []


def _extract_content_words(title: str, max_words: int = 10) -> List[str]:
    """Extract content words from title, removing stop words."""
    stop_words = {
        'the', 'a', 'an', 'of', 'in', 'on', 'for', 'and', 'or', 'to', 'with',
        'by', 'from', 'its', 'their', 'is', 'are', 'was', 'were', 'been', 'be',
        'as', 'at', 'that', 'this', 'these', 'those', 'it', 'not', 'but', 'if',
        'than', 'into', 'through', 'during', 'between', 'after', 'before', 'using',
    }
    words = re.findall(r'\b[a-zA-Z]{2,}\b', title)
    content = [w for w in words if w.lower() not in stop_words]
    return content[:max_words]


# ============================================================================
# CrossRef DOI Fallback
# ============================================================================

class CrossRefFallback:
    """CrossRef DOI lookup as fallback when OpenAlex doesn't have the DOI."""

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": CROSSREF_USER_AGENT})

    def lookup_by_doi(self, doi: str) -> Optional[dict]:
        """
        Look up a DOI via CrossRef.
        Returns a work-like dict with 'title' key, or None.
        """
        doi = doi.strip().strip("/")
        url = f"{CROSSREF_BASE}/{doi}"
        resp = _retry_request("GET", url, self.session)
        time.sleep(CROSSREF_DELAY)

        if resp is not None and resp.status_code == 200:
            try:
                data = resp.json()
                msg = data.get("message", {})
                # Normalize to a simple dict matching OpenAlex pattern
                titles = msg.get("title", [])
                title = titles[0] if titles else ""
                return {
                    "title": title,
                    "doi": msg.get("DOI", doi),
                    "publication_year": (
                        msg.get("published-print", msg.get("published-online", {}))
                        .get("date-parts", [[None]])[0][0]
                    ),
                    "type": msg.get("type", ""),
                    "source": "crossref",
                }
            except (ValueError, json.JSONDecodeError, KeyError, IndexError,
                    TypeError, AttributeError):
                return None
        return None

    def search_by_title(self, title: str, year: str = None) -> List[dict]:
        """
        Search CrossRef by title. No budget limit, but slower (0.3s delay).
        Returns list of work-like dicts with 'title' key.
        """
        words = title.split()[:12]
        query = " ".join(words)
        params = {
            "query.bibliographic": query,
            "filter": "type:journal-article",
            "rows": 5,
            "select": "DOI,title,author,container-title,published",
        }
        if year:
            params["filter"] += f",from-pub-date:{year}-01-01,until-pub-date:{year}-12-31"

        resp = _retry_request("GET", CROSSREF_BASE, self.session, params=params)
        time.sleep(CROSSREF_DELAY)

        if resp is not None and resp.status_code == 200:
            try:
                items = resp.json().get("message", {}).get("items", [])
                results = []
                for item in items:
                    titles = item.get("title", [])
                    t = titles[0] if titles else ""
                    pub = item.get("published", {})
                    dp = pub.get("date-parts", [[None]])
                    yr = dp[0][0] if dp and dp[0] else None
                    results.append({
                        "title": t,
                        "doi": item.get("DOI", ""),
                        "publication_year": yr,
                        "source": "crossref",
                    })
                return results
            except (ValueError, json.JSONDecodeError, KeyError, IndexError):
                pass
        return []


# ============================================================================
# Google Scholar Verification via Serper.dev (last-resort before flagging)
# ============================================================================

SERPER_API_KEY = os.environ.get('SERPER_API_KEY', '')
SERPER_URL = 'https://google.serper.dev/scholar'

# Stop words for building GS query
_GS_STOP_WORDS = {
    'the', 'a', 'an', 'of', 'in', 'on', 'for', 'and', 'or', 'to', 'with',
    'by', 'from', 'its', 'their', 'is', 'are', 'was', 'were', 'been', 'be',
    'as', 'at', 'that', 'this', 'these', 'those', 'it', 'not', 'but', 'if',
    'than', 'into', 'through', 'during', 'between', 'after', 'before', 'using',
}


def verify_via_google_scholar(claimed_title: str, serper_api_key: str = None) -> dict:
    """
    Search Google Scholar via Serper.dev for a claimed title.

    Returns
    -------
    dict with keys:
        verdict : str
            'real_paper' | 'citation_only' | 'uncertain' | 'not_found' | 'error'
        confidence : float
        best_match : dict or None
        reasoning : str
    """
    key = serper_api_key or SERPER_API_KEY
    if not key:
        return {
            'verdict': 'error',
            'confidence': 0.0,
            'best_match': None,
            'reasoning': 'SERPER_API_KEY not set',
        }

    # Build keyword query from the most distinctive words
    words = claimed_title.split()
    query_words = [
        w for w in words
        if w.lower().strip('.,;:()[]') not in _GS_STOP_WORDS
    ][:12]
    query = ' '.join(query_words)

    payload = {'q': query, 'num': 5}
    headers = {'X-API-KEY': key, 'Content-Type': 'application/json'}

    try:
        r = requests.post(SERPER_URL, json=payload, headers=headers, timeout=15)
        r.raise_for_status()
        data = r.json()
    except requests.exceptions.HTTPError as exc:
        return {
            'verdict': 'error',
            'confidence': 0.0,
            'best_match': None,
            'reasoning': f'Serper API error: {exc}',
        }
    except Exception as exc:
        return {
            'verdict': 'error',
            'confidence': 0.0,
            'best_match': None,
            'reasoning': f'Serper request failed: {exc}',
        }

    organic = data.get('organic', [])
    if not organic:
        time.sleep(0.5)
        return {
            'verdict': 'not_found',
            'confidence': 0.7,
            'best_match': None,
            'reasoning': 'No results returned from Google Scholar',
        }

    # Compare top results by title similarity
    best_sim = 0.0
    best_item = None
    for item in organic[:5]:
        result_title = item.get('title', '')
        sim = combined_title_similarity(claimed_title, result_title)
        if sim > best_sim:
            best_sim = sim
            best_item = item

    best_match = None
    if best_item:
        pub_url = best_item.get('link', '')
        num_citations = best_item.get('citedBy', 0)
        source_type = 'indexed' if pub_url else 'citation_only'
        best_match = {
            'title': best_item.get('title', ''),
            'similarity': best_sim,
            'pub_url': pub_url,
            'num_citations': num_citations,
            'source_type': source_type,
            'year': str(best_item.get('year', '')),
            'venue': best_item.get('publicationInfo', ''),
        }

    time.sleep(0.5)

    # Decision logic
    if best_sim >= 0.80:
        if best_match and best_match['source_type'] == 'indexed':
            return {
                'verdict': 'real_paper',
                'confidence': 0.85,
                'best_match': best_match,
                'reasoning': (
                    f'Found on Google Scholar with URL (sim={best_sim:.2f}, '
                    f'cited={best_match.get("num_citations", 0)}). '
                    f'Real paper, not fabrication.'
                ),
            }
        else:
            # Citation-only
            citations = best_match.get('num_citations', 0) if best_match else 0
            if citations >= 5:
                return {
                    'verdict': 'real_paper',
                    'confidence': 0.7,
                    'best_match': best_match,
                    'reasoning': (
                        f'Found as [CITATION] on GS (sim={best_sim:.2f}, '
                        f'cited={citations}). High citation count suggests real.'
                    ),
                }
            else:
                return {
                    'verdict': 'citation_only',
                    'confidence': 0.5,
                    'best_match': best_match,
                    'reasoning': (
                        f'Found as [CITATION] only on GS (sim={best_sim:.2f}, '
                        f'cited={citations}). Possible citation laundering.'
                    ),
                }

    if best_sim >= 0.60:
        return {
            'verdict': 'uncertain',
            'confidence': 0.4,
            'best_match': best_match,
            'reasoning': (
                f'Moderate match on GS (sim={best_sim:.2f}): '
                f'"{best_match["title"][:80] if best_match else "?"}"'
            ),
        }

    # No good match
    return {
        'verdict': 'not_found',
        'confidence': 0.8,
        'best_match': best_match,
        'reasoning': (
            f'Best match on GS has low similarity (sim={best_sim:.2f}). '
            f'Title likely fabricated.'
        ),
    }


# ============================================================================
# Core Verification Logic
# ============================================================================

# Module-level singletons (created lazily)
_openalex: Optional[OpenAlexVerifier] = None
_crossref: Optional[CrossRefFallback] = None


def _get_openalex() -> OpenAlexVerifier:
    global _openalex
    if _openalex is None:
        _openalex = OpenAlexVerifier()
    return _openalex


def _get_crossref() -> CrossRefFallback:
    global _crossref
    if _crossref is None:
        _crossref = CrossRefFallback()
    return _crossref


def _get_best_match(claimed_title: str, results: List[dict]
                    ) -> Tuple[float, Optional[dict]]:
    """Find the best title match from a list of API results."""
    best_sim = 0.0
    best_result = None
    for work in results:
        oa_title = work.get("title", "")
        if not oa_title:
            continue
        sim = combined_title_similarity(claimed_title, oa_title)
        if sim > best_sim:
            best_sim = sim
            best_result = work
    return best_sim, best_result


def _extract_doi_from_work(work: dict) -> str:
    """Extract DOI string from an OpenAlex or CrossRef work object."""
    doi = work.get("doi", "") or ""
    if doi.startswith("https://doi.org/"):
        doi = doi[len("https://doi.org/"):]
    return doi


def _detect_citation_type(citation: dict) -> str:
    """Detect the citation type from the citation dict fields."""
    raw_text = citation.get("unstructured", "") or citation.get("raw_text", "") or ""
    title = citation.get("article_title", "") or citation.get("title", "") or ""
    text_for_check = raw_text or title

    if is_legal_citation(text_for_check):
        return "legal_case"

    volume_title = citation.get("volume_title", "") or ""
    journal_title = citation.get("journal_title", "") or citation.get("journal", "") or ""
    claimed_doi = citation.get("doi", "") or citation.get("claimed_doi", "") or ""

    if volume_title and not journal_title:
        return "book_chapter"

    # Explicit book indicators in the text
    if looks_like_book(text_for_check):
        if not journal_title:
            return "book"
        # Even with a journal field, strong book indicators override
        # (some book refs have the publisher in the journal field)

    # No journal and no DOI — in humanities, almost always a book
    if not journal_title and not volume_title and not claimed_doi:
        if raw_text and len(raw_text) > 30:
            # Check for "in <Capitalized phrase>" pattern (book chapter indicator)
            if re.search(r'\bin\s+[A-Z][a-z]', raw_text):
                return "book_chapter"
            return "book"

    if journal_title:
        return "journal_article"
    return "unknown"


def _get_thresholds(domain: str = "general") -> dict:
    """Get similarity thresholds for a domain."""
    return DOMAIN_THRESHOLDS.get(domain, DOMAIN_THRESHOLDS["general"])


def verify_citation(citation: dict, domain: str = "general") -> VerificationResult:
    """
    Main entry point: verify a single citation.

    Parameters
    ----------
    citation : dict
        Citation dict with keys like:
        - article_title / title: claimed title
        - doi: claimed DOI
        - year / claimed_year: publication year
        - journal_title / journal / claimed_venue: journal name
        - authors / claimed_authors: author string
        - unstructured / raw_text: raw reference text
        - volume_title: for book chapters

    domain : str
        One of "stem", "social_science", "humanities", "law", "general".
        Controls similarity thresholds.

    Returns
    -------
    VerificationResult
    """
    try:
        return _verify_citation_inner(citation, domain)
    except Exception as exc:
        logger.error("Unexpected error verifying citation: %s", exc, exc_info=True)
        return VerificationResult(
            verdict="error",
            confidence=0.0,
            evidence={"error_message": str(exc)},
            fabrication_flag=False,
        )


def _verify_citation_inner(citation: dict, domain: str) -> VerificationResult:
    """Internal verification logic."""

    # --- Extract fields ---
    claimed_title = (
        citation.get("article_title")
        or citation.get("title")
        or citation.get("claimed_title")
        or ""
    ).strip()
    claimed_doi = (
        citation.get("doi")
        or citation.get("claimed_doi")
        or ""
    ).strip()
    claimed_year = str(
        citation.get("year")
        or citation.get("claimed_year")
        or ""
    ).strip()
    raw_text = (
        citation.get("unstructured")
        or citation.get("raw_text")
        or ""
    ).strip()

    # --- Early legal citation check on raw text (before parsing) ---
    # Must run before the parse branch so legal refs aren't misclassified
    if raw_text and is_legal_citation(raw_text):
        return VerificationResult(
            verdict="legal_citation",
            confidence=0.9,
            evidence={"note": "legal_citation_detected", "raw_text": raw_text[:200]},
        )

    # --- If unstructured and no title/doi, try parsing ---
    if not claimed_title and not claimed_doi and raw_text:
        parsed = parse_reference(raw_text)
        claimed_title = parsed.get("title", "")
        claimed_doi = parsed.get("doi", "")
        if not claimed_year:
            claimed_year = parsed.get("year", "")
        if parsed.get("needs_llm_parse") == "true" and not claimed_title and not claimed_doi:
            return VerificationResult(
                verdict="unverifiable",
                confidence=0.3,
                evidence={
                    "note": "needs_llm_parse",
                    "raw_text": raw_text[:300],
                },
            )

    # --- Detect citation type ---
    ctype = _detect_citation_type(citation)

    # --- Legal citation: skip ---
    text_for_legal = raw_text or claimed_title
    if is_legal_citation(text_for_legal) or ctype == "legal_case":
        return VerificationResult(
            verdict="legal_citation",
            confidence=0.9,
            evidence={"note": "legal_citation_detected", "raw_text": text_for_legal[:200]},
        )

    # --- Parsing artifact check ---
    if claimed_title and len(claimed_title.split()) < 3 and not claimed_doi:
        return VerificationResult(
            verdict="parsing_artifact",
            confidence=0.6,
            evidence={"note": "title_too_short", "claimed_title": claimed_title},
        )

    # --- Nothing to verify ---
    if not claimed_title and not claimed_doi:
        return VerificationResult(
            verdict="unverifiable",
            confidence=0.2,
            evidence={"note": "no_title_no_doi"},
        )

    thresholds = _get_thresholds(domain)
    match_threshold = thresholds["match"]
    uncertain_low = thresholds["uncertain_low"]

    openalex = _get_openalex()
    crossref = _get_crossref()

    # ================================================================
    # PATH 1: Has DOI -- DOI verification
    # ================================================================
    if claimed_doi:
        # Clean DOI
        claimed_doi = re.sub(r'^https?://doi\.org/', '', claimed_doi).strip()

        # Step 1: OpenAlex DOI lookup (free)
        work = openalex.lookup_by_doi(claimed_doi)
        if work:
            actual_title = work.get("title", "") or ""
            matched_doi = _extract_doi_from_work(work)

            if claimed_title:
                sim = combined_title_similarity(claimed_title, actual_title)
                if sim >= match_threshold:
                    return VerificationResult(
                        verdict="verified",
                        confidence=min(0.95, 0.7 + sim * 0.3),
                        evidence={
                            "similarity_score": round(sim, 4),
                            "source_checked": "openalex_doi",
                            "matched_title": actual_title,
                            "matched_doi": matched_doi,
                        },
                    )
                else:
                    # Containment check: subtitle handling
                    # e.g. "Assetization" vs "Assetization: Turning Things into Assets..."
                    claimed_norm = normalize_text(strip_markup(claimed_title))
                    actual_norm = normalize_text(strip_markup(actual_title))
                    shorter = claimed_norm if len(claimed_norm) <= len(actual_norm) else actual_norm
                    longer = actual_norm if len(claimed_norm) <= len(actual_norm) else claimed_norm
                    if len(shorter) >= 10 and shorter in longer:
                        return VerificationResult(
                            verdict="verified",
                            confidence=min(0.90, 0.7 + len(shorter) / len(longer) * 0.25),
                            evidence={
                                "similarity_score": round(sim, 4),
                                "source_checked": "openalex_doi",
                                "matched_title": actual_title,
                                "matched_doi": matched_doi,
                                "note": "subtitle_containment_match",
                            },
                        )
                    # Before flagging as doi_mismatch, try Google Scholar
                    if SERPER_API_KEY:
                        gs_result = verify_via_google_scholar(claimed_title)
                        if gs_result['verdict'] == 'real_paper':
                            return VerificationResult(
                                verdict="verified",
                                confidence=gs_result['confidence'],
                                evidence={
                                    "similarity_score": round(
                                        gs_result.get('best_match', {}).get('similarity', 0), 4
                                    ) if gs_result.get('best_match') else 0.0,
                                    "source_checked": "google_scholar_serper",
                                    "matched_title": (
                                        gs_result.get('best_match', {}).get('title', '')
                                        if gs_result.get('best_match') else ''
                                    ),
                                    "rescued_by": "google_scholar",
                                    "gs_reasoning": gs_result['reasoning'],
                                    "claimed_title": claimed_title,
                                    "original_doi_title": actual_title,
                                },
                            )
                    # DOI resolves to a different title
                    return VerificationResult(
                        verdict="doi_mismatch",
                        confidence=0.85,
                        fabrication_flag=True,
                        evidence={
                            "similarity_score": round(sim, 4),
                            "source_checked": "openalex_doi",
                            "matched_title": actual_title,
                            "matched_doi": matched_doi,
                            "claimed_title": claimed_title,
                            "note": "DOI points to a different title",
                        },
                    )
            else:
                # No claimed title, but DOI resolves -- verified by DOI alone
                return VerificationResult(
                    verdict="verified",
                    confidence=0.7,
                    evidence={
                        "source_checked": "openalex_doi",
                        "matched_title": actual_title,
                        "matched_doi": matched_doi,
                        "note": "verified_by_doi_only",
                    },
                )

        # Step 2: CrossRef fallback for DOI
        cr_work = crossref.lookup_by_doi(claimed_doi)
        if cr_work:
            actual_title = cr_work.get("title", "") or ""
            if claimed_title and actual_title:
                sim = combined_title_similarity(claimed_title, actual_title)
                if sim >= match_threshold:
                    return VerificationResult(
                        verdict="verified",
                        confidence=min(0.90, 0.65 + sim * 0.3),
                        evidence={
                            "similarity_score": round(sim, 4),
                            "source_checked": "crossref_doi",
                            "matched_title": actual_title,
                            "matched_doi": claimed_doi,
                        },
                    )
                else:
                    # Containment check: subtitle handling (CrossRef)
                    claimed_norm = normalize_text(strip_markup(claimed_title))
                    actual_norm = normalize_text(strip_markup(actual_title))
                    shorter = claimed_norm if len(claimed_norm) <= len(actual_norm) else actual_norm
                    longer = actual_norm if len(claimed_norm) <= len(actual_norm) else claimed_norm
                    if len(shorter) >= 10 and shorter in longer:
                        return VerificationResult(
                            verdict="verified",
                            confidence=min(0.85, 0.65 + len(shorter) / len(longer) * 0.25),
                            evidence={
                                "similarity_score": round(sim, 4),
                                "source_checked": "crossref_doi",
                                "matched_title": actual_title,
                                "matched_doi": claimed_doi,
                                "note": "subtitle_containment_match",
                            },
                        )
                    # Before flagging as doi_mismatch, try Google Scholar
                    if SERPER_API_KEY:
                        gs_result = verify_via_google_scholar(claimed_title)
                        if gs_result['verdict'] == 'real_paper':
                            return VerificationResult(
                                verdict="verified",
                                confidence=gs_result['confidence'],
                                evidence={
                                    "similarity_score": round(
                                        gs_result.get('best_match', {}).get('similarity', 0), 4
                                    ) if gs_result.get('best_match') else 0.0,
                                    "source_checked": "google_scholar_serper",
                                    "matched_title": (
                                        gs_result.get('best_match', {}).get('title', '')
                                        if gs_result.get('best_match') else ''
                                    ),
                                    "rescued_by": "google_scholar",
                                    "gs_reasoning": gs_result['reasoning'],
                                    "claimed_title": claimed_title,
                                    "original_doi_title": actual_title,
                                },
                            )
                    return VerificationResult(
                        verdict="doi_mismatch",
                        confidence=0.80,
                        fabrication_flag=True,
                        evidence={
                            "similarity_score": round(sim, 4),
                            "source_checked": "crossref_doi",
                            "matched_title": actual_title,
                            "matched_doi": claimed_doi,
                            "claimed_title": claimed_title,
                            "note": "DOI points to different title (CrossRef)",
                        },
                    )
            elif actual_title:
                return VerificationResult(
                    verdict="verified",
                    confidence=0.65,
                    evidence={
                        "source_checked": "crossref_doi",
                        "matched_title": actual_title,
                        "matched_doi": claimed_doi,
                        "note": "verified_by_doi_only_crossref",
                    },
                )

        # DOI not found anywhere -- fall through to title search
        logger.debug("DOI %s not found in OpenAlex or CrossRef, trying title search",
                      claimed_doi)

    # ================================================================
    # PATH 2: Title-only verification (or DOI not found)
    # ================================================================
    if not claimed_title:
        return VerificationResult(
            verdict="unverifiable",
            confidence=0.2,
            evidence={
                "note": "doi_not_found_no_title",
                "claimed_doi": claimed_doi,
            },
        )

    # Book / book chapter -- use lower thresholds, special outcome
    if ctype in ("book", "book_chapter"):
        return _verify_book(claimed_title, claimed_year, ctype, openalex)

    # Title search: try OpenAlex first, then CrossRef fallback
    source_checked = "openalex_search"
    results = openalex.search_by_title(claimed_title, year=claimed_year or None)

    # If OpenAlex returned nothing (likely 429 budget exhaustion), try CrossRef
    if not results:
        cr_results = crossref.search_by_title(claimed_title, year=claimed_year or None)
        if cr_results:
            results = cr_results
            source_checked = "crossref_search"

    if results:
        best_sim, best_work = _get_best_match(claimed_title, results)
        if best_work:
            matched_title = best_work.get("title", "")
            matched_doi = _extract_doi_from_work(best_work)
            matched_year = str(best_work.get("publication_year", ""))

            if best_sim >= match_threshold:
                return VerificationResult(
                    verdict="verified",
                    confidence=min(0.90, 0.6 + best_sim * 0.35),
                    evidence={
                        "similarity_score": round(best_sim, 4),
                        "source_checked": source_checked,
                        "matched_title": matched_title,
                        "matched_doi": matched_doi,
                        "matched_year": matched_year,
                    },
                )

            if best_sim >= uncertain_low:
                return VerificationResult(
                    verdict="uncertain",
                    confidence=0.4,
                    evidence={
                        "similarity_score": round(best_sim, 4),
                        "source_checked": source_checked,
                        "matched_title": matched_title,
                        "matched_doi": matched_doi,
                        "matched_year": matched_year,
                        "note": "partial_match",
                    },
                )

    # Before returning fabrication verdict, check Google Scholar as last resort
    if SERPER_API_KEY:
        gs_result = verify_via_google_scholar(claimed_title)
        if gs_result['verdict'] == 'real_paper':
            return VerificationResult(
                verdict="verified",
                confidence=gs_result['confidence'],
                evidence={
                    "similarity_score": round(
                        gs_result.get('best_match', {}).get('similarity', 0), 4
                    ) if gs_result.get('best_match') else 0.0,
                    "source_checked": "google_scholar_serper",
                    "matched_title": (
                        gs_result.get('best_match', {}).get('title', '')
                        if gs_result.get('best_match') else ''
                    ),
                    "rescued_by": "google_scholar",
                    "gs_reasoning": gs_result['reasoning'],
                    "claimed_title": claimed_title,
                },
            )

    # Title not found in any source
    return VerificationResult(
        verdict="title_not_found",
        confidence=0.7,
        fabrication_flag=True,
        evidence={
            "similarity_score": 0.0,
            "source_checked": source_checked,
            "claimed_title": claimed_title,
            "note": "not_found_in_any_source",
        },
    )


def _verify_book(claimed_title: str, claimed_year: str, ctype: str,
                 openalex: OpenAlexVerifier) -> VerificationResult:
    """Verify a book or book chapter reference."""
    source = "openalex_search"
    results = openalex.search_by_title(claimed_title, year=claimed_year or None)

    # CrossRef fallback for books too
    if not results:
        crossref = _get_crossref()
        cr_results = crossref.search_by_title(claimed_title, year=claimed_year or None)
        if cr_results:
            results = cr_results
            source = "crossref_search"

    if results:
        best_sim, best_work = _get_best_match(claimed_title, results)
        if best_work and best_sim >= 0.60:
            return VerificationResult(
                verdict="verified",
                confidence=min(0.80, 0.5 + best_sim * 0.35),
                evidence={
                    "similarity_score": round(best_sim, 4),
                    "source_checked": source,
                    "matched_title": best_work.get("title", ""),
                    "matched_doi": _extract_doi_from_work(best_work),
                    "citation_type": ctype,
                },
            )

    # Books have incomplete coverage -- not evidence of fabrication
    return VerificationResult(
        verdict="book_unverifiable",
        confidence=0.3,
        evidence={
            "note": "book_not_found",
            "citation_type": ctype,
            "claimed_title": claimed_title,
        },
    )


# ============================================================================
# Batch Verification
# ============================================================================

def verify_article_references(article: dict,
                              domain: str = "general") -> List[VerificationResult]:
    """
    Verify all references in an article dict (from JSONL files).

    Parameters
    ----------
    article : dict
        Must have a 'references' key containing a list of citation dicts.
        May also have 'doi', 'title', 'subject_areas', etc.

    domain : str
        Domain for threshold selection. If "auto", attempts detection from
        article metadata.

    Returns
    -------
    list of VerificationResult, one per reference.
    """
    refs = article.get("references", article.get("reference", []))
    if not refs:
        logger.info("No references found in article")
        return []

    if isinstance(refs, dict):
        # Sometimes CrossRef returns a single ref as a dict
        refs = [refs]

    results = []
    openalex = _get_openalex()
    budget_at_start = openalex.daily_search_count

    for i, ref in enumerate(refs):
        if not isinstance(ref, dict):
            results.append(VerificationResult(
                verdict="error",
                confidence=0.0,
                evidence={"error_message": "reference is not a dict", "ref_index": i},
            ))
            continue

        logger.debug("Verifying ref %d/%d", i + 1, len(refs))
        result = verify_citation(ref, domain=domain)
        results.append(result)

        # Check budget
        if openalex.budget_remaining <= 0:
            logger.warning(
                "OpenAlex search budget exhausted after ref %d/%d. "
                "Remaining refs will only get DOI lookups (free).",
                i + 1, len(refs)
            )

    searches_used = openalex.daily_search_count - budget_at_start
    logger.info(
        "Verified %d references (%d OpenAlex searches used, %d remaining)",
        len(results), searches_used, openalex.budget_remaining
    )

    return results


# ============================================================================
# Self-Test (__main__)
# ============================================================================

def _run_self_test():
    """Run quick self-tests with hardcoded citations."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%H:%M:%S",
    )

    separator = "=" * 72

    print(separator)
    print("CITADEL-X Verification Module -- Self-Test")
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(separator)

    # --- Test 1: Legal citation detection ---
    print("\n[Test 1] Legal citation detection")
    legal_tests = [
        ("Brown v. Board of Education, 347 U.S. 483 (1954)", True),
        ("42 U.S.C. ss 1983", True),
        ("Roe v. Wade, 410 U.S. 113, 93 S.Ct. 705 (1973)", True),
        ("[2023] UKSC 12", True),
        ("Case C-123/45, Commission v. Italy", True),
        ("Smith, J. (2023). A study of law. Legal Journal, 5(2), 1-10.", False),
    ]
    legal_pass = 0
    for text, expected in legal_tests:
        got = is_legal_citation(text)
        status = "PASS" if got == expected else "FAIL"
        if got == expected:
            legal_pass += 1
        print(f"  {status}: is_legal_citation({text[:50]}...) = {got} (expected {expected})")
    print(f"  Legal detection: {legal_pass}/{len(legal_tests)} passed")

    # --- Test 2: Reference parsing ---
    print("\n[Test 2] Reference parsing")
    parse_tests = [
        (
            'Bourdieu, P. (1984). Distinction: A Social Critique of the Judgement of Taste. '
            'Cambridge, MA: Harvard University Press.',
            "book",
        ),
        (
            'Smith, J. & Jones, K. (2023). Neural Approaches to Citation Verification. '
            'Journal of AI, 45(2), 100-115.',
            "apa",
        ),
        (
            '10.1016/j.socscimed.2023.115432 Henderson, A. (2023) Social determinants of health.',
            "doi_inline",
        ),
    ]
    for raw, expected_method in parse_tests:
        result = parse_reference(raw)
        method = result.get("parse_method", "none")
        has_match = expected_method in method or (expected_method == "doi_inline" and "doi" in result)
        status = "PASS" if has_match else "INFO"
        print(f"  {status}: parse({raw[:50]}...) -> method={method}, fields={list(result.keys())}")

    # --- Test 3: Title similarity ---
    print("\n[Test 3] Title similarity")
    sim_tests = [
        (
            "Effects of climate change on biodiversity",
            "Effects of climate change on biodiversity",
            0.95,  # Expect near-perfect
        ),
        (
            "Effects of climate change on biodiversity",
            "Climate change impacts on global biodiversity patterns",
            0.40,  # Expect moderate
        ),
        (
            "A completely different title about economics",
            "Neural networks for image classification",
            0.0,  # Expect very low
        ),
    ]
    for t1, t2, min_expected in sim_tests:
        sim = combined_title_similarity(t1, t2)
        status = "PASS" if sim >= min_expected else "WARN"
        print(f"  {status}: sim({t1[:30]}..., {t2[:30]}...) = {sim:.3f} (min expected {min_expected})")

    # --- Test 4: Verify real citation via API ---
    print("\n[Test 4] API verification -- real paper with DOI")
    real_citation = {
        "article_title": "Attention Is All You Need",
        "doi": "10.48550/arXiv.1706.03762",
        "year": "2017",
    }
    print(f"  Verifying: {real_citation['article_title']}")
    print(f"  DOI: {real_citation['doi']}")
    result = verify_citation(real_citation, domain="stem")
    print(f"  Verdict: {result.verdict}")
    print(f"  Confidence: {result.confidence:.3f}")
    print(f"  Fabrication flag: {result.fabrication_flag}")
    print(f"  Evidence: { {k: str(v)[:80] for k, v in result.evidence.items()} }")

    # --- Test 5: Verify citation by title search ---
    print("\n[Test 5] API verification -- title search (no DOI)")
    title_citation = {
        "article_title": "The Structure of Scientific Revolutions",
        "year": "1962",
    }
    print(f"  Verifying: {title_citation['article_title']}")
    result = verify_citation(title_citation, domain="humanities")
    print(f"  Verdict: {result.verdict}")
    print(f"  Confidence: {result.confidence:.3f}")
    print(f"  Fabrication flag: {result.fabrication_flag}")
    print(f"  Evidence: { {k: str(v)[:80] for k, v in result.evidence.items()} }")

    # --- Test 6: Verify a legal citation (should be skipped) ---
    print("\n[Test 6] Legal citation (should be skipped)")
    legal_citation = {
        "unstructured": "Brown v. Board of Education, 347 U.S. 483 (1954)",
    }
    result = verify_citation(legal_citation)
    print(f"  Verdict: {result.verdict}")
    expected_verdict = "legal_citation"
    status = "PASS" if result.verdict == expected_verdict else "FAIL"
    print(f"  {status}: expected '{expected_verdict}', got '{result.verdict}'")

    # --- Test 7: Verify likely fabricated citation ---
    print("\n[Test 7] Likely fabricated title (nonsense)")
    fake_citation = {
        "article_title": "Quantum Blockchain Synergy for Sustainable Nanoparticle "
                         "Optimization in Smart Agricultural Ecosystems",
        "year": "2024",
        "journal": "Journal of Advanced Multidisciplinary Research",
    }
    print(f"  Verifying: {fake_citation['article_title'][:60]}...")
    result = verify_citation(fake_citation, domain="stem")
    print(f"  Verdict: {result.verdict}")
    print(f"  Confidence: {result.confidence:.3f}")
    print(f"  Fabrication flag: {result.fabrication_flag}")
    print(f"  Evidence: { {k: str(v)[:80] for k, v in result.evidence.items()} }")

    # --- Test 8: CSV row export ---
    print("\n[Test 8] CSV row export")
    row = result.to_csv_row()
    print(f"  CSV columns: {list(row.keys())}")
    print(f"  CSV verdict: {row['verdict']}")

    # --- Summary ---
    print(f"\n{separator}")
    print("Self-test complete.")
    openalex = _get_openalex()
    print(f"OpenAlex searches used: {openalex.daily_search_count}")
    print(f"OpenAlex budget remaining: {openalex.budget_remaining}")
    print(separator)


if __name__ == "__main__":
    _run_self_test()
