# CITADEL-X: Non-Biomedical Citation Verification Pipeline Specification

**Version**: 1.0 (Draft)
**Date**: 2026-04-04
**Author**: Max Topaz / Claude Code
**Status**: Design specification -- not yet implemented

---

## 1. Overview and Motivation

The existing CITADEL pipeline detects fabricated citations in PubMed Central (PMC) papers using a PMID-centric approach: resolve claimed PMIDs via a local PubMed SQLite DB (40M records), compare claimed vs actual titles, classify mismatches, and verify through an LLM judge and Google Scholar. This pipeline achieves 91% precision with F1=0.941.

**CITADEL-X** extends fabrication detection beyond biomedicine to the social sciences, humanities, law, engineering, and other disciplines. These domains differ fundamentally from biomedicine in their citation practices:

| Property | Biomedical (CITADEL) | Non-Biomedical (CITADEL-X) |
|----------|---------------------|----------------------------|
| Primary identifier | PMID | DOI (when available) |
| Identifier coverage | ~95% of PMC refs have PMIDs | ~60-70% of CrossRef refs have DOIs |
| Reference format | Structured XML with tagged fields | Often unstructured text blobs |
| Verification DB | PubMed (40M articles, local SQLite) | OpenAlex (250M works, API) |
| Dominant citation types | Journal articles | Articles + books + chapters + proceedings + legal cases |
| Source of papers | PMC XML | CrossRef API (all domains) |

---

## 2. Architecture Overview

```
                        CrossRef API
                            |
                    [Article Discovery]
                            |
                    [Reference Extraction]
                            |
              +-------------+-------------+
              |                           |
        Structured refs             Unstructured refs
        (has title, DOI)            (raw text blob)
              |                           |
              |                    [Reference Parser]
              |                    (regex + LLM fallback)
              |                           |
              +-------------+-------------+
                            |
                    [Citation Type Router]
                            |
          +---------+-------+--------+---------+
          |         |                |          |
      DOI-based   Title-only   Legal case   Book/Chapter
          |         |                |          |
     [DOI Lookup]  [Title Search]  [Legal      [Book
      OpenAlex     OpenAlex API    Parser]     Verifier]
          |         |                |          |
          +----+----+          [skip/tag]  [OpenAlex +
               |                           ISBN lookup]
        [Title Similarity]                     |
               |                               |
        [Classification]<---------------------+
               |
        [LLM Judge] (Claude Haiku)
               |
        [Google Scholar Verify] (Serper.dev)
               |
           [Output DB]
```

---

## 3. Input Format

### 3A. Article Discovery Input (from CrossRef)

Each article to scan is discovered via the CrossRef API. The pipeline queries CrossRef for recently published articles in target domains.

```python
@dataclass
class CrossRefArticle:
    """A published article discovered via CrossRef."""
    doi: str                          # Article DOI (always present from CrossRef)
    title: str                        # Article title
    authors: List[str]                # Author list
    journal: str                      # Container title (journal, book, proceedings)
    publisher: str                    # Publisher name
    published_date: str               # Publication date (YYYY-MM-DD)
    subject_areas: List[str]          # CrossRef subject classifications
    type: str                         # "journal-article", "book-chapter", "proceedings-article", etc.
    references: List[CrossRefReference]  # Extracted references
    reference_count: int              # Total reference count (from metadata)
```

### 3B. Reference Input (from CrossRef reference list)

CrossRef returns references in two forms. The pipeline must handle both.

**Form 1: Structured reference** (has discrete fields)

```python
@dataclass
class CrossRefReference:
    """A single reference from a CrossRef article's reference list."""
    # Identifiers (may be empty)
    doi: str = ""                     # Reference DOI

    # Structured fields (may be partially populated)
    article_title: str = ""           # Article/chapter title
    volume_title: str = ""            # Book/proceedings title
    author: str = ""                  # First author (CrossRef format)
    year: str = ""                    # Publication year
    journal_title: str = ""           # Journal name
    volume: str = ""                  # Volume number
    issue: str = ""                   # Issue number
    first_page: str = ""             # First page

    # Raw text (when CrossRef couldn't parse the reference)
    unstructured: str = ""            # Full unstructured reference string

    # Pipeline metadata
    ref_key: str = ""                 # CrossRef's internal reference key
    ref_number: int = 0               # Sequential number in reference list

    @property
    def has_doi(self) -> bool:
        return bool(self.doi and self.doi.strip())

    @property
    def has_title(self) -> bool:
        return bool(self.article_title and self.article_title.strip())

    @property
    def is_unstructured(self) -> bool:
        """True if the reference is only available as raw text."""
        return bool(self.unstructured) and not self.has_title and not self.has_doi

    @property
    def citation_type(self) -> str:
        """Infer citation type from available fields."""
        if _is_legal_citation(self.unstructured or self.article_title):
            return "legal_case"
        if self.volume_title and not self.journal_title:
            return "book_chapter"
        if not self.journal_title and not self.volume_title:
            if self.unstructured and _looks_like_book(self.unstructured):
                return "book"
            return "unknown"
        return "journal_article"
```

**Form 2: Unstructured reference** (raw text blob)

Example inputs the parser must handle:

```
# Humanities
"Adams John 'A Dissertation on the Canon and Feudal Law' in C. Bradley Thompson (ed.) The Revolutionary Writings of John Adams (Liberty Fund 2000) 19-28"

# Law
"Brown v. Board of Education, 347 U.S. 483 (1954)"
"Roe v. Wade, 410 U.S. 113, 93 S.Ct. 705 (1973)"

# Social science
"Bourdieu, P. (1984). Distinction: A Social Critique of the Judgement of Taste. Cambridge, MA: Harvard University Press."

# Conference proceedings
"Smith, J. & Jones, K. (2023). 'Neural Approaches to Citation Verification.' In Proceedings of ACL 2023, pp. 1234-1245."

# Mixed with DOI
"10.1016/j.socscimed.2023.115432 Henderson, A. (2023) Social determinants of..."
```

---

## 4. Parsing Stage: Extracting Structured Fields from Unstructured References

### 4A. Parsing Strategy (Three-Tier)

**Tier 1: Regex-based parser** (fast, handles ~60% of unstructured refs)

The regex parser applies a cascade of patterns, each targeting a common citation style:

```python
CITATION_PATTERNS = [
    # APA style: Author, A. B. (2023). Title. Journal, vol(issue), pages.
    {
        "name": "apa",
        "pattern": r"^(?P<authors>[^(]+?)\s*\((?P<year>\d{4})\)\.\s*(?P<title>[^.]+(?:\.[^.]+)*?)\.\s*(?P<journal>[^,]+),\s*(?P<volume>\d+)",
        "priority": 1,
    },
    # Chicago/Turabian: Author. "Title." Journal vol, no. issue (year): pages.
    {
        "name": "chicago",
        "pattern": r'^(?P<authors>[^"]+?)\.\s*["\u201c](?P<title>[^"\u201d]+)["\u201d]\.\s*(?P<journal>[^,]+?)\s+(?P<volume>\d+)',
        "priority": 2,
    },
    # Harvard: Author (Year) Title, Journal, vol(issue), pp.
    {
        "name": "harvard",
        "pattern": r"^(?P<authors>[^(]+?)\s*\((?P<year>\d{4})\)\s+(?P<title>[^,]+),\s*(?P<journal>[^,]+),",
        "priority": 3,
    },
    # Book: Author (Year). Title. Place: Publisher.
    {
        "name": "book",
        "pattern": r"^(?P<authors>[^(]+?)\s*\((?P<year>\d{4})\)\.\s*(?P<title>[^.]+(?:\.[^.]+)*?)\.\s*(?P<place>[^:]+):\s*(?P<publisher>[^.]+)",
        "priority": 4,
    },
    # Book chapter: Author (Year). 'Chapter Title' in Editor (ed.) Book Title.
    {
        "name": "book_chapter",
        "pattern": r"^(?P<authors>[^(]+?)\s*\((?P<year>\d{4})\)\.\s*['\u2018](?P<title>[^'\u2019]+)['\u2019]\s+in\s+(?P<editor>[^(]+?)\s*\(ed",
        "priority": 5,
    },
    # Inline DOI extraction
    {
        "name": "doi_inline",
        "pattern": r"(?:https?://doi\.org/|doi:\s*)(?P<doi>10\.\d{4,}/[^\s]+)",
        "priority": 0,
    },
]
```

**Tier 2: Heuristic field extraction** (handles ~25% more)

For references that don't match a clean regex pattern, use heuristic extraction:

```python
def heuristic_parse(raw_text: str) -> dict:
    """
    Extract fields from unstructured reference text using heuristics.

    Strategy:
    1. Extract year: look for (YYYY) or YYYY anywhere in string
    2. Extract DOI: look for 10.XXXX/ pattern
    3. Extract authors: text before the year (typically author block)
    4. Extract title: text between authors and journal/publisher
       - Quoted text is almost always the title
       - Text between year and next period is likely the title
    5. Extract journal/publisher: text after title, before page numbers
    """
    fields = {}

    # Year extraction
    year_match = re.search(r'\((\d{4})\)|,?\s*(\d{4})\s*[,.\)]', raw_text)
    if year_match:
        fields['year'] = year_match.group(1) or year_match.group(2)

    # DOI extraction
    doi_match = re.search(r'(10\.\d{4,9}/[^\s,;}\]]+)', raw_text)
    if doi_match:
        fields['doi'] = doi_match.group(1).rstrip('.')

    # Quoted title extraction (high confidence)
    quoted = re.search(r'["\u201c\u2018\'](.*?)["\u201d\u2019\']', raw_text)
    if quoted and len(quoted.group(1)) > 10:
        fields['title'] = quoted.group(1)

    # Author extraction (text before year, up to ~100 chars)
    if year_match:
        author_block = raw_text[:year_match.start()].strip().rstrip('(,.')
        if 5 < len(author_block) < 200:
            fields['authors'] = author_block

    return fields
```

**Tier 3: LLM-assisted parsing** (handles remaining ~15%, expensive)

For references that resist regex and heuristic parsing, use Claude Haiku as a structured extractor. This is reserved for high-value cases (e.g., when the article has many unstructured refs and is from a suspicious publisher).

```python
LLM_PARSE_PROMPT = """Extract structured citation fields from this reference string.
Return JSON with keys: title, authors, year, journal, volume, pages, publisher, doi, type.
If a field is not present, use null.
The "type" field should be one of: journal_article, book, book_chapter,
conference_paper, legal_case, thesis, report, other.

Reference: {raw_text}

JSON:"""
```

**Budget guard**: LLM parsing is limited to max 5 refs per article, max 200 per scan batch. If an article has >5 unparseable refs, flag the article for manual review rather than spending LLM budget.

### 4B. Legal Citation Detection

Legal citations have distinctive formats and must be detected early to avoid false positives (they will never match in OpenAlex).

```python
LEGAL_CITATION_PATTERNS = [
    # US case law: "Party v. Party, Volume Reporter Page (Year)"
    re.compile(r'\b\w+\s+v\.?\s+\w+.*?\d+\s+(?:U\.?S\.?|S\.?\s*Ct\.?|F\.?\s*(?:2d|3d|4th)|'
               r'L\.?\s*Ed\.?|A\.?\s*(?:2d|3d)|N\.?[EWSY]\.?\s*(?:2d)?|P\.?\s*(?:2d|3d)|'
               r'So\.?\s*(?:2d|3d)|Cal\.?\s*(?:2d|3d|4th|5th))\s*\d+'),
    # US statute: "42 U.S.C. ss 1983"
    re.compile(r'\d+\s+U\.?S\.?C\.?\s*(?:\u00a7|ss?\.?)\s*\d+'),
    # US Code of Federal Regulations
    re.compile(r'\d+\s+C\.?F\.?R\.?\s*(?:\u00a7|ss?\.?)\s*\d+'),
    # UK case law: "[2023] UKSC 12
    re.compile(r'\[\d{4}\]\s+(?:UKSC|UKHL|EWCA|EWHC|AC|QB|Ch|WLR|All ER)'),
    # EU case law: "Case C-123/45"
    re.compile(r'Case\s+(?:C|T)-\d+/\d+'),
    # Generic "v." pattern with reporter volume
    re.compile(r'\b[A-Z][a-z]+\s+v\.\s+[A-Z].*?,\s+\d+\s+[A-Z]'),
]

def _is_legal_citation(text: str) -> bool:
    """Detect if text is a legal case/statute citation."""
    if not text:
        return False
    for pat in LEGAL_CITATION_PATTERNS:
        if pat.search(text):
            return True
    return False
```

### 4C. Book Detection

```python
BOOK_INDICATORS = [
    re.compile(r'\b(?:University Press|Oxford UP|Cambridge UP|Harvard UP|MIT Press|'
               r'Princeton UP|Yale UP|Stanford UP|Chicago UP|Columbia UP|'
               r'Routledge|Springer|Wiley|Elsevier|Sage|Palgrave|Macmillan|'
               r'Penguin|Random House|HarperCollins|Norton|McGraw.Hill|'
               r'Academic Press|World Scientific|CRC Press)\b', re.IGNORECASE),
    re.compile(r'\b(?:eds?\.|edited by|translat(?:ed|ion) by)\b', re.IGNORECASE),
    re.compile(r'\b(?:pp?\.\s*\d+[-\u2013]\d+)\b'),  # Page ranges in book style
    re.compile(r'\b(?:Vol\.\s*\d+|Chapter\s+\d+)\b', re.IGNORECASE),
    # ISBN
    re.compile(r'(?:ISBN[:\s-]*)?(?:97[89][- ]?)?\d{1,5}[- ]?\d{1,7}[- ]?\d{1,7}[- ]?\d{1,7}[- ]?[\dXx]'),
]

def _looks_like_book(text: str) -> bool:
    """Heuristic: does this reference look like a book citation?"""
    if not text:
        return False
    score = sum(1 for pat in BOOK_INDICATORS if pat.search(text))
    return score >= 1
```

---

## 5. Identifier Resolution: DOI Lookup and Title Search

### 5A. Resolution Strategy (Decision Tree)

```
For each reference:

1. HAS DOI?
   YES -> Step 2
   NO  -> Step 5

2. DOI Lookup via OpenAlex: GET /works/doi:{doi}
   SUCCESS -> Step 3
   FAIL    -> Step 4

3. Compare claimed title vs OpenAlex title
   similarity >= 0.70 -> VERIFIED (titles match)
   similarity <  0.70 -> DOI_MISMATCH (DOI points to different paper)

4. DOI Fallback: try CrossRef /works/{doi}
   SUCCESS -> compare title (as Step 3)
   FAIL    -> treat as title-only (Step 5)

5. TITLE SEARCH via OpenAlex: GET /works?search={title}
   Has results?
   YES -> Step 6
   NO  -> Step 7

6. Compare best OpenAlex result to claimed metadata
   similarity >= 0.70 -> VERIFIED (title exists, no DOI or wrong DOI)
   similarity 0.50-0.69 -> UNCERTAIN (possible match, needs review)
   similarity <  0.50 -> TITLE_NOT_FOUND (no good match)

7. Fallback: Semantic Scholar API title search
   Has results?
   YES -> compare as Step 6
   NO  -> TITLE_NOT_FOUND (not in any database)
```

### 5B. OpenAlex Query Strategy

OpenAlex is the primary verification database. Its API has two modes with very different cost profiles:

| Endpoint | Cost | Rate limit | Use case |
|----------|------|------------|----------|
| `/works/{id}` (DOI, OpenAlex ID) | Free (no budget) | 10 req/sec | DOI-based verification |
| `/works?search={title}` | $0.0001/query (10K free/day) | 10 req/sec | Title-based search |
| `/works?filter=title.search:{title}` | $0.0001/query | 10 req/sec | Exact title filter |

**Query optimization strategy**:

1. **DOI-first**: Always try `/works/doi:{doi}` first. This is free and returns full metadata.
2. **Title filter before search**: Use `filter=title.search:"{title}"` (quoted exact phrase) before the broader `search=` parameter. The filter is more precise and returns fewer false matches.
3. **Truncated title search**: If the full title gets no results, try the first 8-10 content words (handles subtitle variations).
4. **Author+year filter**: When title search returns multiple candidates, add `&filter=publication_year:{year},authorships.author.display_name.search:{first_author}` to narrow results.

```python
class OpenAlexVerifier:
    """OpenAlex-based citation verification."""

    BASE_URL = "https://api.openalex.org"

    def __init__(self, email: str):
        self.email = email  # Polite pool: include mailto for higher rate limit
        self.session = requests.Session()
        self.session.params = {"mailto": email}
        self.daily_search_count = 0
        self.DAILY_SEARCH_BUDGET = 8000  # Leave buffer under 10K free tier

    def lookup_by_doi(self, doi: str) -> Optional[dict]:
        """
        Direct DOI lookup. FREE (not counted against search budget).
        Returns OpenAlex work object or None.
        """
        url = f"{self.BASE_URL}/works/doi:{doi}"
        resp = self.session.get(url, timeout=15)
        if resp.status_code == 200:
            return resp.json()
        return None

    def search_by_title(self, title: str, year: str = None,
                        author: str = None) -> List[dict]:
        """
        Title search. Costs 1 search credit per call.
        Returns list of candidate works, sorted by relevance.
        """
        if self.daily_search_count >= self.DAILY_SEARCH_BUDGET:
            raise BudgetExhaustedError("Daily OpenAlex search budget exceeded")

        # Strategy 1: Exact title filter (most precise)
        params = {"filter": f'title.search:"{title[:200]}"'}
        if year:
            params["filter"] += f",publication_year:{year}"
        params["per_page"] = 5

        resp = self.session.get(f"{self.BASE_URL}/works", params=params, timeout=15)
        self.daily_search_count += 1

        if resp.status_code == 200:
            results = resp.json().get("results", [])
            if results:
                return results

        # Strategy 2: Broader search (if exact filter failed)
        # Use first 10 content words to handle subtitle variations
        words = _extract_content_words(title, max_words=10)
        search_query = " ".join(words)

        params = {"search": search_query, "per_page": 5}
        if year:
            params["filter"] = f"publication_year:{year}"

        resp = self.session.get(f"{self.BASE_URL}/works", params=params, timeout=15)
        self.daily_search_count += 1

        if resp.status_code == 200:
            return resp.json().get("results", [])

        return []
```

### 5C. Semantic Scholar Fallback

Semantic Scholar serves as the fallback for STEM references that OpenAlex may not have (especially recent conference papers).

```python
class SemanticScholarVerifier:
    """Fallback verification via Semantic Scholar API."""

    BASE_URL = "https://api.semanticscholar.org/graph/v1"

    def search_by_title(self, title: str) -> List[dict]:
        """
        Search S2 for a title. Rate limit: 1 req/sec (unauthenticated).
        With API key: 10 req/sec.
        """
        params = {
            "query": title[:200],
            "limit": 5,
            "fields": "title,authors,year,venue,externalIds,citationCount"
        }
        resp = requests.get(
            f"{self.BASE_URL}/paper/search",
            params=params, timeout=15
        )
        if resp.status_code == 200:
            return resp.json().get("data", [])
        return []
```

### 5D. Fallback Chain Summary

```
Reference with DOI:
  1. OpenAlex /works/doi:{doi}     [free, instant]
  2. CrossRef /works/{doi}          [free, ~200ms]
  3. Title search (if DOI not found)

Reference without DOI:
  1. OpenAlex title search          [1 credit, ~300ms]
  2. OpenAlex broader search        [1 credit, ~300ms]
  3. Semantic Scholar search         [free, ~500ms, STEM only]
  4. Google Scholar (Serper.dev)     [for flagged refs only, post-classification]
```

---

## 6. Verification Logic: Decision Tree

### 6A. Citation Type Router

Before verification, each reference is routed based on its detected type:

```python
def route_citation(ref: CrossRefReference) -> str:
    """
    Route a citation to the appropriate verification path.

    Returns one of:
    - "doi_verify"      -> Has DOI, verify via DOI lookup
    - "title_verify"    -> Has title but no DOI, search by title
    - "legal_skip"      -> Legal citation, skip verification
    - "book_verify"     -> Book/chapter, use book verification path
    - "unstructured"    -> Raw text, needs parsing first
    - "unverifiable"    -> Insufficient data to verify
    """
    # 1. Legal citations: skip entirely
    raw_text = ref.unstructured or ref.article_title or ""
    if _is_legal_citation(raw_text):
        return "legal_skip"

    # 2. Has DOI: verify via DOI
    if ref.has_doi:
        return "doi_verify"

    # 3. Has structured title: verify via title search
    if ref.has_title:
        if ref.citation_type == "book_chapter" or ref.citation_type == "book":
            return "book_verify"
        return "title_verify"

    # 4. Unstructured text: needs parsing
    if ref.is_unstructured:
        return "unstructured"

    # 5. Nothing to work with
    return "unverifiable"
```

### 6B. DOI Verification Path

```python
def verify_by_doi(ref: CrossRefReference, openalex: OpenAlexVerifier) -> VerificationResult:
    """
    Verify a reference that has a DOI.

    Decision tree:
    1. Look up DOI in OpenAlex
    2. If found: compare claimed title to OpenAlex title
       - Match (sim >= 0.70): VERIFIED
       - Mismatch (sim < 0.70): check for truncation/abbreviation
         - Truncation match: VERIFIED (with note)
         - Word overlap >= 0.65: VERIFIED (variant title)
         - Otherwise: DOI_MISMATCH
    3. If not found in OpenAlex: try CrossRef
    4. If not in CrossRef either: treat as title-only verification
    """
    work = openalex.lookup_by_doi(ref.doi)

    if work:
        actual_title = work.get("title", "")
        claimed_title = ref.article_title

        sim = combined_title_similarity(claimed_title, actual_title)

        if sim >= 0.70:
            return VerificationResult(
                category="verified",
                confidence="high",
                similarity_score=sim,
                actual_title=actual_title,
                source="openalex_doi"
            )

        # Check for truncation (CrossRef often has abbreviated titles)
        if _is_truncated_match(claimed_title, actual_title):
            return VerificationResult(
                category="verified",
                confidence="high",
                similarity_score=sim,
                actual_title=actual_title,
                source="openalex_doi",
                note="truncation_match"
            )

        # Check word overlap (catches paraphrased/translated titles)
        if _word_overlap_match(claimed_title, actual_title, min_recall=0.60):
            return VerificationResult(
                category="verified",
                confidence="medium",
                similarity_score=sim,
                actual_title=actual_title,
                source="openalex_doi",
                note="word_overlap_match"
            )

        # DOI resolves to a different title
        return VerificationResult(
            category="doi_mismatch",
            confidence="high",
            similarity_score=sim,
            actual_title=actual_title,
            source="openalex_doi"
        )

    # DOI not found in OpenAlex -- try CrossRef as fallback
    # (then fall through to title-only verification)
    return verify_by_title(ref, openalex)
```

### 6C. Title-Only Verification Path

```python
def verify_by_title(ref: CrossRefReference, openalex: OpenAlexVerifier,
                    s2: SemanticScholarVerifier = None) -> VerificationResult:
    """
    Verify a reference by searching for its title.

    Decision tree:
    1. Search OpenAlex by title (+ year filter if available)
    2. Score each result against claimed metadata
    3. Best match:
       - sim >= 0.70: VERIFIED (title exists in literature)
       - sim 0.50-0.69: UNCERTAIN (may be a variant)
       - sim < 0.50 or no results: try Semantic Scholar
    4. If S2 also fails: TITLE_NOT_FOUND
    """
    claimed_title = ref.article_title
    if not claimed_title or len(claimed_title.strip()) < 10:
        return VerificationResult(category="unverifiable", confidence="low",
                                  note="title_too_short")

    # Search OpenAlex
    results = openalex.search_by_title(
        claimed_title,
        year=ref.year if ref.year else None
    )

    if results:
        best_sim = 0.0
        best_result = None
        for work in results:
            oa_title = work.get("title", "")
            sim = combined_title_similarity(claimed_title, oa_title)
            if sim > best_sim:
                best_sim = sim
                best_result = work

        if best_sim >= 0.70:
            return VerificationResult(
                category="verified",
                confidence="high" if best_sim >= 0.85 else "medium",
                similarity_score=best_sim,
                actual_title=best_result["title"],
                source="openalex_search"
            )

        if best_sim >= 0.50:
            # Check additional metadata for disambiguation
            if _metadata_corroborates(ref, best_result):
                return VerificationResult(
                    category="verified",
                    confidence="medium",
                    similarity_score=best_sim,
                    actual_title=best_result["title"],
                    source="openalex_search",
                    note="metadata_corroborated"
                )
            return VerificationResult(
                category="uncertain",
                confidence="low",
                similarity_score=best_sim,
                actual_title=best_result["title"],
                source="openalex_search"
            )

    # Fallback: Semantic Scholar (STEM refs)
    if s2:
        s2_results = s2.search_by_title(claimed_title)
        if s2_results:
            best_sim = 0.0
            best_result = None
            for paper in s2_results:
                sim = combined_title_similarity(claimed_title, paper.get("title", ""))
                if sim > best_sim:
                    best_sim = sim
                    best_result = paper

            if best_sim >= 0.70:
                return VerificationResult(
                    category="verified",
                    confidence="medium",
                    similarity_score=best_sim,
                    actual_title=best_result["title"],
                    source="semantic_scholar"
                )

    return VerificationResult(
        category="title_not_found",
        confidence="medium",
        similarity_score=0.0,
        source="all_searched"
    )
```

### 6D. Book Verification Path

```python
def verify_book(ref: CrossRefReference, openalex: OpenAlexVerifier) -> VerificationResult:
    """
    Verify a book or book chapter reference.

    Books are harder to verify because:
    - OpenAlex indexes many books but coverage is uneven for older works
    - Title matching is harder (subtitles, edition numbers, translations)
    - Chapter titles may not be indexed individually

    Strategy:
    1. If DOI present: standard DOI lookup
    2. Search for book title in OpenAlex (type=book filter)
    3. If chapter: search for chapter title, then book title
    4. If not found: BOOK_UNVERIFIABLE (not flagged as fake)
    """
    # Try DOI first (some books have DOIs)
    if ref.has_doi:
        result = verify_by_doi(ref, openalex)
        if result.category != "title_not_found":
            return result

    # For book chapters: search the chapter title
    if ref.article_title:
        results = openalex.search_by_title(ref.article_title, year=ref.year)
        if results:
            best = max(results, key=lambda w: combined_title_similarity(
                ref.article_title, w.get("title", "")))
            sim = combined_title_similarity(ref.article_title, best.get("title", ""))
            if sim >= 0.65:  # Slightly lower threshold for books
                return VerificationResult(
                    category="verified", confidence="medium",
                    similarity_score=sim, actual_title=best["title"],
                    source="openalex_search"
                )

    # Search the book/volume title
    if ref.volume_title:
        results = openalex.search_by_title(ref.volume_title, year=ref.year)
        if results:
            for work in results:
                if work.get("type") in ("book", "edited-book", "monograph"):
                    sim = combined_title_similarity(ref.volume_title, work.get("title", ""))
                    if sim >= 0.60:
                        return VerificationResult(
                            category="verified", confidence="medium",
                            similarity_score=sim,
                            actual_title=work["title"],
                            source="openalex_search",
                            note="book_title_match"
                        )

    # Book not found -- this is NOT evidence of fabrication
    return VerificationResult(
        category="book_unverifiable",
        confidence="low",
        note="book_not_in_openalex"
    )
```

### 6E. Legal Citation Path

```python
def handle_legal_citation(ref: CrossRefReference) -> VerificationResult:
    """
    Handle legal case citations. These are SKIPPED, not verified.

    Legal citations (e.g., "Brown v. Board of Education, 347 U.S. 483 (1954)")
    reference court decisions, not journal articles. They will never match in
    OpenAlex and should not be flagged as fabricated.

    Future enhancement: validate against legal databases (e.g., CourtListener API,
    Caselaw Access Project). For now, tag and skip.
    """
    raw = ref.unstructured or ref.article_title or ""

    # Extract case components for the record
    case_info = _parse_legal_citation(raw)

    return VerificationResult(
        category="legal_citation",
        confidence="high",
        note=f"Legal citation detected: {case_info.get('parties', 'unknown')}",
        source="legal_parser"
    )

def _parse_legal_citation(text: str) -> dict:
    """Extract basic components from a legal citation for logging."""
    info = {}
    # Parties: "X v. Y"
    parties = re.search(r'([\w\s.]+?)\s+v\.?\s+([\w\s.]+?)(?:,|\d)', text)
    if parties:
        info['parties'] = f"{parties.group(1).strip()} v. {parties.group(2).strip()}"
    # Reporter: "347 U.S. 483"
    reporter = re.search(r'(\d+)\s+([A-Z][A-Za-z.\s]+?)\s+(\d+)', text)
    if reporter:
        info['volume'] = reporter.group(1)
        info['reporter'] = reporter.group(2).strip()
        info['page'] = reporter.group(3)
    # Year: "(1954)"
    year = re.search(r'\((\d{4})\)', text)
    if year:
        info['year'] = year.group(1)
    return info
```

---

## 7. Similarity Scoring

### 7A. Algorithm

Reuse the existing `combined_title_similarity()` from `content_verifier.py`, which combines:
- **SequenceMatcher ratio** (edit distance-based)
- **Word overlap score** (Jaccard-like, ignoring stop words)
- **Containment check** (one title is a substring of the other)

The combined score is: `max(sequence_matcher, word_overlap, containment_bonus)`

### 7B. Domain-Specific Thresholds

Title characteristics vary by domain, requiring adjusted thresholds:

| Domain | Typical title length | Title characteristics | Match threshold | Mismatch threshold |
|--------|---------------------|----------------------|-----------------|-------------------|
| **STEM journals** | 10-15 words | Technical, specific | 0.70 | 0.35 |
| **Humanities** | 15-30 words | Descriptive, often with colons/subtitles | 0.65 | 0.30 |
| **Law review articles** | 8-20 words | Case names embedded, colons common | 0.65 | 0.30 |
| **Book titles** | 5-15 words | Short main + long subtitle | 0.60 | 0.30 |
| **Conference proceedings** | 10-20 words | Similar to STEM journals | 0.70 | 0.35 |

**Why lower thresholds for humanities/books**:
- Humanities titles frequently include subtitles separated by colons, and databases may index only the main title or the full title inconsistently.
- Book titles appear in many variant forms (different editions, translations, with/without subtitles).
- Legal article titles may include case names that are formatted differently across databases.

### 7C. Domain Detection

```python
def detect_domain(article: CrossRefArticle) -> str:
    """
    Detect the broad domain of an article for threshold selection.
    Uses CrossRef subject areas and journal heuristics.
    """
    subjects = [s.lower() for s in article.subject_areas]
    journal = article.journal.lower() if article.journal else ""

    # Law
    if any(kw in journal for kw in ['law review', 'law journal', 'legal', 'jurisprudence']):
        return "law"
    if any('law' in s for s in subjects):
        return "law"

    # Humanities
    humanities_kw = ['philosophy', 'history', 'literature', 'linguistics', 'classics',
                     'religion', 'theology', 'arts', 'music', 'cultural studies']
    if any(any(kw in s for kw in humanities_kw) for s in subjects):
        return "humanities"

    # Social sciences
    social_kw = ['sociology', 'political', 'economics', 'psychology', 'anthropology',
                 'education', 'social work', 'public policy', 'geography']
    if any(any(kw in s for kw in social_kw) for s in subjects):
        return "social_science"

    # Engineering / CS
    stem_kw = ['engineering', 'computer science', 'physics', 'chemistry',
               'mathematics', 'materials', 'electrical', 'mechanical']
    if any(any(kw in s for kw in stem_kw) for s in subjects):
        return "stem"

    # Default
    return "general"

# Threshold lookup
DOMAIN_THRESHOLDS = {
    "stem":           {"match": 0.70, "mismatch": 0.35, "word_overlap_recall": 0.65},
    "social_science": {"match": 0.68, "mismatch": 0.33, "word_overlap_recall": 0.60},
    "humanities":     {"match": 0.65, "mismatch": 0.30, "word_overlap_recall": 0.55},
    "law":            {"match": 0.65, "mismatch": 0.30, "word_overlap_recall": 0.55},
    "general":        {"match": 0.70, "mismatch": 0.35, "word_overlap_recall": 0.65},
}
```

---

## 8. Classification Categories

### 8A. Category Definitions

```python
class VerificationCategory(Enum):
    """Classification categories for non-biomedical citation verification."""

    # === Positive outcomes ===
    VERIFIED = "verified"
    # Citation matches a real work in OpenAlex/S2/CrossRef.
    # Equivalent to biomedical "valid".

    # === Fabrication indicators ===
    DOI_MISMATCH = "doi_mismatch"
    # DOI resolves to a different title than claimed.
    # Equivalent to biomedical "wrong_pmid".
    # This is the strongest signal of fabrication.

    TITLE_NOT_FOUND = "title_not_found"
    # Title does not match any known work in OpenAlex, S2, or Google Scholar.
    # Equivalent to biomedical "fab_title".
    # Could be fabricated OR could be a work not indexed in any database.

    TITLE_SWAP = "title_swap"
    # DOI is valid and title exists, but DOI points to a different title than claimed.
    # Equivalent to biomedical "title_swap".
    # Strong evidence of deliberate manipulation.

    # === Inconclusive outcomes ===
    UNVERIFIABLE = "unverifiable"
    # Insufficient structured data to verify. No DOI, no parseable title,
    # or title too short/generic to search reliably.

    BOOK_UNVERIFIABLE = "book_unverifiable"
    # Book/chapter citation that could not be confirmed in OpenAlex.
    # NOT evidence of fabrication -- book coverage is incomplete.
    # Should not be flagged without additional evidence.

    UNCERTAIN = "uncertain"
    # Partial match found (similarity 0.50-0.69) but not confident enough
    # to classify as verified or title_not_found.

    # === Special categories ===
    LEGAL_CITATION = "legal_citation"
    # Recognized legal case/statute citation. Skipped, not verified.

    PARSING_ARTIFACT = "parsing_artifact"
    # Reference text is not a real citation (author names, URLs,
    # consortium names, etc. extracted from wrong field).

    # === Error ===
    ERROR = "error"
    # API failure or processing error.
```

### 8B. What Counts as "Fabricated"

Following the biomedical pipeline's multi-stage approach, a citation is counted as fabricated only after passing through all verification stages:

```
FABRICATED = (
    (category == "doi_mismatch" AND gs_verdict == "not_found")
    OR
    (category == "title_not_found" AND llm_verdict == "llm_confirmed_fake"
     AND gs_verdict == "not_found")
    OR
    (category == "title_swap" AND gs_verdict == "not_found")
)
AND rescue_pattern IS NULL
```

Categories explicitly excluded from fabrication counts:
- `book_unverifiable` -- coverage gap, not evidence of fabrication
- `legal_citation` -- different document type
- `unverifiable` -- insufficient data
- `uncertain` -- ambiguous match
- `parsing_artifact` -- data quality issue
- Any entry with a `rescue_pattern` set

---

## 9. Output Format

### 9A. Verification Result Data Class

```python
@dataclass
class VerificationResult:
    """Result of verifying a single citation."""

    # Classification
    category: str = "unverifiable"      # VerificationCategory value
    confidence: str = "low"             # "high", "medium", "low"

    # Similarity evidence
    similarity_score: float = -1.0      # Best title match score (0-1)
    actual_title: str = ""              # Title that the ID/search resolved to

    # Source tracking
    source: str = ""                    # "openalex_doi", "openalex_search",
                                        # "semantic_scholar", "crossref", "google_scholar"

    # Metadata comparison
    author_overlap: float = -1.0
    first_author_match: bool = False
    journal_match: bool = False
    year_match: bool = False
    year_diff: Optional[int] = None

    # Notes and evidence
    note: str = ""
    evidence_summary: str = ""

    # Post-classification fields (filled by LLM judge and GS verify)
    llm_verdict: str = ""               # "llm_confirmed_fake", "llm_false_positive", ""
    gs_verdict: str = ""                # "real_paper", "not_found", "citation_laundering", ""
    rescue_pattern: str = ""            # If set, entry is a rescued false positive
```

### 9B. Database Schema

```sql
CREATE TABLE IF NOT EXISTS articles (
    doi TEXT PRIMARY KEY,
    title TEXT,
    journal TEXT,
    publisher TEXT,
    domain TEXT,                         -- "stem", "humanities", "law", etc.
    published_date TEXT,
    total_refs INTEGER,
    refs_with_dois INTEGER,
    refs_verified INTEGER DEFAULT 0,
    flagged_count INTEGER DEFAULT 0,
    fabricated_count INTEGER DEFAULT 0,
    scan_date TEXT,
    scanned_at TEXT
);

CREATE TABLE IF NOT EXISTS all_references (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    article_doi TEXT,                    -- Source article DOI
    ref_number INTEGER,

    -- Claimed metadata
    claimed_title TEXT,
    claimed_doi TEXT,
    claimed_authors TEXT,               -- Semicolon-separated
    claimed_venue TEXT,
    claimed_year TEXT,
    citation_type TEXT,                  -- "journal_article", "book", "legal_case", etc.
    raw_text TEXT,                       -- Original unstructured text (if any)

    -- Verification results
    category TEXT,                       -- VerificationCategory value
    confidence TEXT,
    similarity_score REAL,
    actual_title TEXT,
    verification_source TEXT,            -- "openalex_doi", "openalex_search", etc.

    -- Metadata forensics
    author_overlap REAL,
    first_author_match BOOLEAN,
    journal_match BOOLEAN,
    year_match BOOLEAN,
    year_diff INTEGER,

    -- Post-classification
    llm_verdict TEXT,
    gs_verdict TEXT,
    gs_best_title TEXT,
    gs_best_sim REAL,
    gs_best_url TEXT,
    rescue_pattern TEXT,

    -- Flags
    is_flagged BOOLEAN DEFAULT FALSE,
    is_fabricated BOOLEAN DEFAULT FALSE,

    evidence_summary TEXT,
    note TEXT,

    FOREIGN KEY (article_doi) REFERENCES articles(doi)
);

CREATE TABLE IF NOT EXISTS flagged (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    article_doi TEXT,
    article_title TEXT,
    journal TEXT,
    domain TEXT,
    ref_number INTEGER,
    claimed_title TEXT,
    claimed_doi TEXT,
    claimed_authors TEXT,
    claimed_venue TEXT,
    claimed_year TEXT,
    citation_type TEXT,
    raw_text TEXT,
    category TEXT,
    confidence TEXT,
    similarity_score REAL,
    actual_title TEXT,
    verification_source TEXT,
    llm_verdict TEXT,
    gs_verdict TEXT,
    rescue_pattern TEXT,
    evidence_summary TEXT,
    scan_date TEXT,
    FOREIGN KEY (article_doi) REFERENCES articles(doi)
);

CREATE TABLE IF NOT EXISTS scan_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    scan_date TEXT,
    domain_filter TEXT,                  -- Which domains were scanned
    status TEXT,
    articles_scanned INTEGER,
    total_refs INTEGER,
    refs_verified INTEGER,
    flagged_count INTEGER,
    fabricated_count INTEGER,
    openalex_searches_used INTEGER,
    elapsed_seconds REAL,
    started_at TEXT,
    finished_at TEXT,
    error TEXT
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_refs_article ON all_references(article_doi);
CREATE INDEX IF NOT EXISTS idx_refs_category ON all_references(category);
CREATE INDEX IF NOT EXISTS idx_refs_flagged ON all_references(is_flagged);
CREATE INDEX IF NOT EXISTS idx_flagged_article ON flagged(article_doi);
CREATE INDEX IF NOT EXISTS idx_flagged_category ON flagged(category);
CREATE INDEX IF NOT EXISTS idx_flagged_domain ON flagged(domain);
```

---

## 10. API Call Budget Estimates

### 10A. Per-Article Budget

Assume an average non-biomedical article has ~40 references, with the following distribution:

| Reference type | % of refs | Has DOI | Verification method | API calls |
|---------------|-----------|---------|--------------------:|----------:|
| Journal article with DOI | 45% (18 refs) | Yes | OpenAlex DOI lookup | 18 free |
| Journal article, no DOI | 20% (8 refs) | No | OpenAlex title search | 8-16 search credits |
| Book/chapter | 20% (8 refs) | Rare | OpenAlex title search | 8-16 search credits |
| Legal citation | 5% (2 refs) | No | Skip (legal parser) | 0 |
| Unverifiable | 10% (4 refs) | No | Tag as unverifiable | 0 |

**Per-article totals**:
- OpenAlex DOI lookups: ~18 (free)
- OpenAlex search queries: ~16-32 (at $0.0001 each = $0.0016-0.0032)
- Semantic Scholar fallback: ~2-4 (for title_not_found refs)
- LLM parse calls: ~2-4 (for unparseable unstructured refs)
- Google Scholar (Serper): ~1-3 (only for flagged refs)

**Cost per article**: ~$0.002-0.005 in OpenAlex search credits + ~$0.001 LLM + ~$0.003 Serper = ~$0.006-0.009 total.

### 10B. Per-Batch Budget (200 Articles)

| Resource | Per article | Per 200 articles | Daily free tier |
|----------|-----------|-----------------|----------------|
| OpenAlex DOI lookups | 18 | 3,600 | Unlimited (free) |
| OpenAlex search queries | 24 (avg) | 4,800 | 10,000/day |
| Semantic Scholar | 3 (avg) | 600 | ~5,000/day (with key) |
| Claude Haiku (LLM parse) | 3 (avg) | 600 | ~$0.15 |
| Claude Haiku (LLM judge) | 2 (avg) | 400 | ~$0.10 |
| Serper.dev (Google Scholar) | 2 (avg) | 400 | 2,500/month |

**200-article batch fits within daily free tiers**: 4,800 OpenAlex searches < 10,000/day limit.

**Daily throughput**: ~200 articles/day staying within free tiers. For larger scans, the OpenAlex premium tier ($500/month) provides 100K searches/day.

### 10C. Optimization: Skip Verified References

Following the biomedical pipeline's approach, only verify references that have checkable identifiers or titles:

```python
# Priority verification order:
# 1. Refs with DOIs (fastest, free) -- always verify
# 2. Refs with parsed titles (costs search credits) -- verify unless budget tight
# 3. Unstructured refs (costs parse + search) -- verify only if article is suspicious
# 4. Legal citations -- always skip
# 5. Very short/generic titles -- skip (parsing artifact)
```

---

## 11. Error Handling

### 11A. API Failure Modes

| Failure | Detection | Recovery |
|---------|-----------|----------|
| **OpenAlex rate limit** (429) | HTTP 429 response | Exponential backoff: 1s, 2s, 4s, 8s. Max 3 retries. |
| **OpenAlex down** (5xx) | HTTP 500-503 | Skip article, log error, retry in next scan. |
| **OpenAlex timeout** | No response in 15s | Retry once, then tag ref as "error". |
| **Semantic Scholar rate limit** | HTTP 429 | Back off 5s, reduce batch to 1 req/2s. |
| **Serper API limit** | HTTP 429 or 402 | Stop GS verification, continue with existing verdicts. |
| **CrossRef rate limit** | HTTP 429 | Back off 30s (CrossRef is aggressive about rate limits). |
| **LLM API error** | Anthropic 429/500 | Back off 10s, reduce concurrency to 1. |
| **Budget exhausted** | Daily search count >= 8,000 | Stop new title searches, DOI lookups still work. |

### 11B. Ambiguous Results

| Scenario | Resolution |
|----------|-----------|
| **Multiple OpenAlex matches, all low similarity** | Take best match. If best < 0.50, classify as title_not_found. |
| **Title matches but wrong year/author** | Log as "verified" but add forensic note about metadata mismatch. |
| **DOI resolves in CrossRef but not OpenAlex** | Use CrossRef metadata, tag source as "crossref". |
| **Unstructured ref partially parsed** | Use whatever fields were extracted. If title found, verify it. |
| **OpenAlex returns retracted paper** | Still counts as "verified" (the paper existed). Note retraction. |
| **Same title, multiple works** | Compare all metadata fields (year, author, venue) to pick best. |

### 11C. Graceful Degradation

```python
class VerificationPipeline:
    """
    Pipeline with graceful degradation.

    If a data source becomes unavailable, the pipeline continues with
    remaining sources rather than failing entirely.
    """

    def verify_with_fallbacks(self, ref: CrossRefReference) -> VerificationResult:
        # Level 1: Full verification (all sources)
        try:
            if ref.has_doi:
                result = self.openalex.lookup_by_doi(ref.doi)
                if result:
                    return self._evaluate_doi_result(ref, result)
        except APIError:
            self.log("OpenAlex DOI lookup failed, falling through to title search")

        # Level 2: Title search (OpenAlex)
        try:
            if ref.has_title:
                results = self.openalex.search_by_title(ref.article_title)
                if results:
                    return self._evaluate_search_results(ref, results)
        except (APIError, BudgetExhaustedError):
            self.log("OpenAlex search failed/exhausted, trying S2")

        # Level 3: Semantic Scholar fallback
        try:
            if ref.has_title and self.s2:
                results = self.s2.search_by_title(ref.article_title)
                if results:
                    return self._evaluate_s2_results(ref, results)
        except APIError:
            self.log("Semantic Scholar also failed")

        # Level 4: Cannot verify at all
        return VerificationResult(
            category="error",
            confidence="low",
            note="all_apis_failed"
        )
```

### 11D. Consecutive Error Circuit Breaker

Following the biomedical pipeline's pattern:

```python
MAX_CONSECUTIVE_ERRORS = 10
PAUSE_AFTER_CIRCUIT_BREAK = 60  # seconds

consecutive_errors = 0
for ref in references:
    try:
        result = verify(ref)
        consecutive_errors = 0
    except Exception as e:
        consecutive_errors += 1
        log(f"Error #{consecutive_errors}: {e}")
        if consecutive_errors >= MAX_CONSECUTIVE_ERRORS:
            log(f"Circuit breaker: {MAX_CONSECUTIVE_ERRORS} consecutive errors, "
                f"pausing {PAUSE_AFTER_CIRCUIT_BREAK}s")
            time.sleep(PAUSE_AFTER_CIRCUIT_BREAK)
            consecutive_errors = 0
```

---

## 12. Pipeline Stages (End-to-End)

### Stage 0: Article Discovery (CrossRef Harvester)

```python
def harvest_crossref_articles(
    domain_filter: str = None,     # e.g., "social-science", "humanities", "law"
    from_date: str = None,         # "YYYY-MM-DD"
    to_date: str = None,
    max_articles: int = 200,
    publisher_filter: str = None,  # Optional: target specific publishers
) -> Iterator[CrossRefArticle]:
    """
    Discover articles from CrossRef API with their reference lists.

    CrossRef API endpoint: /works
    Filters:
    - from-published-date, until-published-date
    - has-references=true (only articles that include reference data)
    - subject area (maps to CrossRef subject codes)

    Rate limit: 50 req/sec with polite pool (mailto header).
    """
```

**Domain-to-CrossRef subject mapping**:

| CITADEL-X Domain | CrossRef subject filter |
|-----------------|----------------------|
| Social sciences | `subject:social-science` |
| Humanities | `subject:humanities`, `subject:arts` |
| Law | `subject:law` |
| Engineering | `subject:engineering` |
| Computer science | `subject:computer-science` |
| Economics | `subject:economics` |
| Education | `subject:education` |
| All (exploratory) | `has-references=true` (no subject filter) |

### Stage 1: Reference Extraction and Parsing

For each discovered article:
1. Extract references from CrossRef metadata
2. Classify each reference by type (journal, book, legal, etc.)
3. Parse unstructured references (Tier 1-3)
4. Route each reference to the appropriate verification path

### Stage 2: Verification (DOI Lookup + Title Search)

Apply the verification logic from Section 6 to each reference.

### Stage 3: LLM Judge

For references classified as `title_not_found`, run them through Claude Haiku for triage. Reuse the existing `llm_judge.py` prompt structure with domain-specific adaptations:

```python
LLM_JUDGE_PROMPT_NONBIO = """You are a citation verification expert. A reference
from a {domain} paper claims the following title:

Claimed title: "{claimed_title}"
Claimed authors: {claimed_authors}
Claimed venue: {claimed_venue}
Claimed year: {claimed_year}

This title was NOT found in OpenAlex (250M works), Semantic Scholar, or CrossRef.

Possible explanations:
1. FABRICATED: The title was invented (common in paper mills).
   Signs: generic-sounding, combines trendy buzzwords, perfect grammar but no
   specificity, plausible but doesn't actually exist.
2. FALSE POSITIVE: The title is real but not indexed.
   Signs: very old work (pre-1990), government report, working paper,
   non-English publication, dissertation, conference workshop paper.
3. VARIANT TITLE: The work exists under a different/translated title.

For {domain} specifically, consider:
- {domain_specific_guidance}

Based on the evidence, classify as:
- "llm_confirmed_fake" — you believe this title was fabricated
- "llm_false_positive" — you believe this is a real work not indexed

Respond with JSON: {{"verdict": "...", "reasoning": "...", "confidence": "high|medium|low"}}
"""

DOMAIN_GUIDANCE = {
    "humanities": "Humanities works are frequently books, book chapters, or edited volumes "
                  "that may not be indexed in any database. Foreign-language works are common. "
                  "Be conservative about flagging as fabricated.",
    "law": "Legal scholarship includes law review articles, case notes, and statutory "
           "commentary. Many law reviews are not indexed in OpenAlex. Be very conservative.",
    "social_science": "Social science includes working papers, policy reports, and government "
                      "documents that may not be indexed. Gray literature is common.",
    "stem": "STEM papers are well-indexed. If a STEM title is not in OpenAlex or S2, "
            "it is more likely fabricated than in other domains.",
    "general": "Consider whether the title sounds plausible for its claimed venue. "
               "Generic, buzzword-heavy titles are suspicious.",
}
```

### Stage 4: Google Scholar Verification

Reuse the existing `google_scholar_verify.py` (Serper.dev backend) without modification. The search and classification logic is domain-agnostic.

### Stage 5: Rescue Patterns

Adapt the biomedical rescue patterns for non-biomedical domains:

| Pattern ID | Description | Domain relevance |
|-----------|-------------|-----------------|
| `NB-P1` | Title is a parsing artifact (author names, URLs, metadata) | All domains |
| `NB-P2` | Title too short (<3 content words) | All domains |
| `NB-P3` | Title is a translated variant of a verified work | Humanities, social science |
| `NB-P4` | Book edition/subtitle mismatch (same core title) | Humanities |
| `NB-P5` | Conference variant (workshop vs main, preprint vs proceedings) | STEM, CS |
| `NB-P6` | Government/institutional report (not indexed) | Social science, law |
| `NB-E1` | Publisher-specific formatting artifact | All domains |
| `NB-E2` | Non-English title where English translation exists | Humanities |

---

## 13. Conference Proceedings Verification

Conference proceedings present unique challenges:

### 13A. The Problem

- Proceedings are less consistently indexed than journal articles
- The same paper may appear as: preprint, workshop paper, main conference, extended version
- Conference names vary (ACL 2023 vs Proceedings of the 61st Annual Meeting...)
- Some conferences are indexed in DBLP/S2 but not OpenAlex

### 13B. Strategy

```python
def verify_proceedings(ref: CrossRefReference,
                       openalex: OpenAlexVerifier,
                       s2: SemanticScholarVerifier) -> VerificationResult:
    """
    Verify a conference proceedings citation.

    Strategy:
    1. If DOI present: standard DOI lookup (many proceedings have DOIs via ACM/IEEE/Springer)
    2. Title search in OpenAlex (has proceedings)
    3. Title search in Semantic Scholar (excellent CS/NLP proceedings coverage)
    4. If not found in either: classify as UNCERTAIN (not title_not_found)
       because proceedings coverage is spotty
    """
    # Step 1: DOI lookup
    if ref.has_doi:
        result = verify_by_doi(ref, openalex)
        if result.category == "verified":
            return result

    # Step 2: OpenAlex title search
    results = openalex.search_by_title(ref.article_title, year=ref.year)
    best_sim = _best_match_sim(ref.article_title, results)
    if best_sim >= 0.70:
        return VerificationResult(category="verified", confidence="medium",
                                  similarity_score=best_sim, source="openalex_search")

    # Step 3: Semantic Scholar (better proceedings coverage)
    s2_results = s2.search_by_title(ref.article_title)
    best_sim = _best_match_sim(ref.article_title, s2_results)
    if best_sim >= 0.70:
        return VerificationResult(category="verified", confidence="medium",
                                  similarity_score=best_sim, source="semantic_scholar")

    # Step 4: Not found -- but proceedings coverage is incomplete
    # Use UNCERTAIN rather than TITLE_NOT_FOUND to reduce false positives
    return VerificationResult(
        category="uncertain",
        confidence="low",
        note="proceedings_not_indexed"
    )
```

---

## 14. Implementation Roadmap

### Phase 1: Core Infrastructure (Week 1-2)
- [ ] `crossref_harvester.py` -- Article discovery and reference extraction from CrossRef
- [ ] `reference_parser.py` -- Regex + heuristic parsing of unstructured references
- [ ] `citation_type_router.py` -- Route references by type (journal, book, legal, etc.)
- [ ] `legal_citation_detector.py` -- Legal citation pattern matching

### Phase 2: Verification Engine (Week 2-3)
- [ ] `openalex_verifier.py` -- DOI lookup + title search via OpenAlex API
- [ ] `semantic_scholar_verifier.py` -- S2 fallback for STEM
- [ ] `nonbio_classifier.py` -- Classification logic with domain-specific thresholds
- [ ] `similarity.py` -- Reuse/adapt `combined_title_similarity()` from content_verifier.py

### Phase 3: Classification Pipeline (Week 3-4)
- [ ] `nonbio_llm_judge.py` -- Domain-adapted LLM judge prompt
- [ ] Integrate existing `google_scholar_verify.py` (Serper backend, no changes needed)
- [ ] `nonbio_rescue.py` -- Non-biomedical rescue patterns
- [ ] `nonbio_scan.py` -- Main scan orchestrator (equivalent to scan_v2.py)

### Phase 4: Database and Output (Week 4)
- [ ] SQLite schema creation and migration
- [ ] Scan logging and status reporting
- [ ] Output CSV/JSON generation for analysis

### Phase 5: Validation (Week 5-6)
- [ ] Select 200 articles from each target domain (social science, humanities, law, STEM)
- [ ] Run pipeline, review flagged citations manually
- [ ] Calculate precision and recall per domain
- [ ] Tune thresholds based on validation results
- [ ] Document domain-specific false positive patterns

---

## 15. Key Design Decisions and Rationale

### 15.1. Why OpenAlex as Primary (Not CrossRef)?

| Factor | OpenAlex | CrossRef |
|--------|----------|---------|
| Coverage | 250M works (includes books, proceedings) | 150M works (DOI-centric) |
| Non-DOI content | Yes (has MAG-derived records) | No (DOI required) |
| Title search quality | Excellent (full-text search) | Limited (metadata-only search) |
| Cost | 10K free searches/day | Free but slow, limited search |
| Author metadata | Full author disambiguation | Basic author strings |
| Concept tagging | Yes (domain classification) | Subject codes only |

OpenAlex subsumes CrossRef's content AND adds 100M works without DOIs from the Microsoft Academic Graph. This is critical for humanities and older works.

### 15.2. Why Not Build a Local DB (Like PubMed Local)?

The biomedical pipeline uses a local PubMed SQLite DB (40M records) for instant lookups. For CITADEL-X, this approach is impractical because:

1. **Scale**: 250M works vs 40M -- would require ~500GB+ of SQLite with FTS5 index
2. **Update frequency**: OpenAlex updates weekly with ~500K new works; PubMed daily updates are smaller
3. **Initial load**: Downloading the full OpenAlex snapshot takes ~300GB of compressed data and days to process
4. **API is fast enough**: OpenAlex DOI lookups are free and take ~100ms. Title searches take ~300ms. This is adequate for batch processing 200 articles/day.

**Future optimization**: If throughput needs exceed 1,000 articles/day, consider building a local OpenAlex mirror using the official data snapshot. OpenAlex provides a full data dump updated weekly in Parquet format.

### 15.3. Why Separate Legal Citations?

Legal citations reference court opinions and statutes, not academic publications. They follow a completely different citation format (reporter-based) and are not indexed in any academic database. Flagging "Brown v. Board of Education, 347 U.S. 483 (1954)" as a fabricated reference would be a 100% false positive. The legal citation detector prevents this.

**Future enhancement**: Integrate with the Caselaw Access Project (CAP) API or CourtListener to actually verify legal citations. This would enable detecting fabricated case citations (e.g., citing a case number that doesn't exist).

### 15.4. Conservative Approach to Books

Books are the most under-indexed reference type. Many books, especially:
- Older works (pre-2000)
- Non-English publications
- Small press / independent publishers
- Government publications
- Textbooks without DOIs

...will not appear in OpenAlex. Classifying a missing book as `book_unverifiable` rather than `title_not_found` prevents massive false positive inflation in humanities and social sciences where books dominate the reference list.

### 15.5. Why Three-Tier Parsing?

Unstructured reference parsing is the single biggest technical risk in this pipeline. CrossRef returns ~30-40% of non-biomedical references as raw text blobs. The three-tier approach balances cost and accuracy:

- **Tier 1 (regex)**: Fast, free, handles standardized citation styles. Covers ~60%.
- **Tier 2 (heuristic)**: Still fast, handles non-standard formatting. Covers ~25% more.
- **Tier 3 (LLM)**: Expensive ($0.001/ref) but handles anything. Reserved for the ~15% that resist parsing.

Budget guard: max 5 LLM parse calls per article, max 200 per batch. If an article has many unparseable refs, it's likely a formatting issue rather than a verification target.

---

## 16. Comparison: Biomedical vs Non-Biomedical Pipeline

| Component | CITADEL (Biomedical) | CITADEL-X (Non-Biomedical) |
|-----------|---------------------|----------------------------|
| Source | PMC XML (NCBI E-utilities) | CrossRef API |
| Discovery | PMC date range search | CrossRef subject/date filter |
| References | Structured XML (`<ref>` tags) | Structured JSON + unstructured text |
| Primary ID | PMID | DOI |
| ID coverage | ~95% of refs have PMIDs | ~60-70% have DOIs |
| Verification DB | Local PubMed SQLite (40M) | OpenAlex API (250M) |
| Local DB? | Yes (instant lookups) | No (API-based, ~100-300ms) |
| Fallback | DOI via CrossRef | Semantic Scholar + Google Scholar |
| Parsing needed? | No (XML is structured) | Yes (unstructured text blobs) |
| Legal citations? | N/A (biomedical) | Must detect and skip |
| Book citations? | Rare in PMC | Common in humanities |
| LLM judge | Claude Haiku (same) | Claude Haiku (domain-adapted prompt) |
| GS verify | Serper.dev (same) | Serper.dev (same, no changes) |
| Similarity threshold | 0.35 mismatch / 0.50 match | Domain-dependent (0.30-0.35 / 0.60-0.70) |
| Classification | 7 categories | 10 categories |
| Throughput | ~1,000 papers/hour | ~200 articles/day (API-limited) |
| Cost | ~$0 (local DB + free APIs) | ~$1-2/day (OpenAlex + Serper) |

---

## 17. Open Questions for Validation

1. **Fabrication rate by domain**: Is the ~1-1.5% biomedical fabrication rate consistent across domains? Humanities may be lower (less paper mill activity), law may be different (more opportunity for case citation fabrication).

2. **Unstructured reference parsing accuracy**: What fraction of Tier 1+2 parsed references have correct title extraction? Need to validate on a sample of 200 unstructured refs across domains.

3. **OpenAlex coverage by domain**: What fraction of legitimate references in each domain are actually in OpenAlex? High false-negative rates in underindexed domains (e.g., law reviews) could make the pipeline impractical.

4. **Book verification feasibility**: Is `book_unverifiable` a useful category, or does it mask too many potentially fabricated book citations? Need to validate on a sample of 100 book references.

5. **Legal citation detection precision**: How often do the legal citation regexes false-positive on non-legal text? (E.g., "State v. Federal Oversight: A Policy Analysis" is an article title, not a case.)

6. **Cross-domain threshold tuning**: Do the proposed domain-specific thresholds (Section 7B) need per-publisher or per-journal adjustment?

7. **Proceedings gap**: For CS/engineering, how much does Semantic Scholar add over OpenAlex for proceedings verification? Is DBLP integration worth the effort?

---

*End of specification. This document should be treated as a living design doc, updated as validation results inform threshold and strategy adjustments.*
