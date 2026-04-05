# CITADEL-X Error Log

## API Errors

### OpenAlex
- **2026-04-04 12:36**: Free tier budget exhausted ($0 remaining). All search calls returned 429. **Resolution**: Added paid API key (XV2Ly...), set budget to 100K/day. Added `_budget_exhausted` flag to skip search immediately on first 429 rather than retrying.
- **2026-04-04 14:04**: HTTP 400 on title search for non-ASCII titles (Chinese characters in filter query). **Resolution**: These fail gracefully — CrossRef fallback catches them. Non-ASCII title searches should URL-encode properly; logged as known limitation.

### CrossRef
- **2026-04-04 various**: HTTP 400 on `query.bibliographic` with certain special characters (quotes, brackets in titles). **Resolution**: Fails gracefully, ref classified as unverifiable. Consider adding character sanitization for title queries.
- **2026-04-04**: `to-pub-date` filter does not exist. **Resolution**: Fixed to `until-pub-date` across all extraction scripts.

### Serper.dev (Google Scholar)
- No errors encountered. Rate limit adequate for current volume.

## Encoding Errors
- **2026-04-04**: Windows cp1252 codec crashes on Polish/non-ASCII journal names. **Resolution**: All scripts now use `PYTHONIOENCODING=utf-8` and ASCII-replace for print output.
- **2026-04-04**: `urllib.parse.urlencode` encodes commas in CrossRef filter strings. **Resolution**: Switched to `requests` library for all HTTP calls.

## Pipeline Errors
- **2026-04-04**: MathML tags in OpenAlex titles break similarity scoring. **Resolution**: Added `strip_markup()` function to remove XML/HTML tags while preserving text content.
- **2026-04-04**: Unicode subscript characters (₃, ₂, ⁴⁺) in CrossRef titles vs ASCII in OpenAlex. **Resolution**: `normalize_text()` applies NFKC normalization which converts subscripts to ASCII.

## Known Limitations
1. Non-English titles (Chinese, Dutch, Turkish) frequently return title_not_found — these are false positives, not fabrication
2. Book citations in humanities have low verification rate (~30-40%) because CrossRef book coverage is incomplete
3. Legal case citations are detected and skipped but the regex may miss some non-US formats
4. Conference proceedings have inconsistent indexing in both OpenAlex and CrossRef
