# CITADEL — Citation Integrity Detection and Evaluation Library

## What This Project Is
Automated pipeline to detect fabricated citations in PubMed Central (PMC) papers. Collaboration between Max Topaz (Columbia) and Nir Roguin. Two complementary tools:
- **CITADEL** (Max's pipeline): Scans PMC XML, extracts references, resolves PMIDs/DOIs, compares claimed vs actual titles
- **ARGUS** (Nir's tool): Scans ALL of PMC, compares PMIDs to claimed titles

For the paper, present as ONE unified system — don't mention two separate tools.

## Project Root
`C:\Users\SON1\OneDrive - cumc.columbia.edu\Desktop\Grants_US\Claude_code\Fake_refernces\`

## Current State (2026-02-24) — Paper submitted, pipeline formalized & running
- **Paper submitted** to Lancet Comment/Viewpoint (2026-02-24)
- **Paper snapshot frozen** at `results/paper_snapshot_20260224/` (49 GB, all 13 DBs)
- **Paper numbers** (through Feb 18, 2026): 4,046 fabricated citations, 2,112 rescued, 2,810 affected papers
- **Live pipeline numbers** (through Feb 24, 2026): 3,880 fabricated, 2,315 rescued across 2,474,301 papers
- **Post-paper additions** (Feb 18-24): 8 new fabricated citations (2 rescued from 10 flagged)
- **Precision: 91%** (500-sample, 3 reviewers, Fleiss' kappa = 0.71)
- **Pipeline formalized**: single orchestrator (`citadel_pipeline.py`), weekly automation
- See `HANDOFF.md`, `PIPELINE_README.md`, and `results/FINAL_RESULTS.json` for full details

## Architecture — Production Pipeline (v2.0)

**Single entry point**: `python citadel_pipeline.py --days 7 --stage all`

| Stage | Module | What it does |
|-------|--------|-------------|
| 0. PubMed Update | `core/pubmed_updater.py` | Download daily PubMed XML updates into local DB |
| 1. Scanner | `core/scanner.py` -> `scan_v2.py` | Extract refs from PMC XML, resolve PMIDs, compare titles |
| 2. LLM Judge | `core/llm_judge_runner.py` -> `llm_judge.py` | Claude Haiku triage of fab_title/title_swap |
| 3. GS Verify | `core/gs_verifier.py` | Serper.dev verification (both fab_title AND wrong_pmid) |
| 4. Rescue | `core/rescue.py` | Apply all rescue patterns (builtin + eyeball + LLM artifact) |

**Config**: `citadel_config.yaml` (all thresholds, API settings, paths in one file)
**Automation**: `weekly_run.bat` via Windows Task Scheduler (Sunday 2 AM)

### Legacy Pipeline (pre-formalization)
1. **Scanner** (`scan_v2.py`): Extract refs from PMC XML, resolve PMID/DOI, compare titles
2. **Classifier** (`classifier.py`): Categorize as wrong_pmid, fab_title, title_swap, valid
3. **LLM Judge** (`llm_judge.py`): Triage fab_title entries
4. **Google Scholar** (`google_scholar_verify.py`): Check LLM fakes
5. **Rescue passes**: Multiple separate scripts (see `legacy/DEPRECATED.md`)
6. **Human Review** (Streamlit/Railway apps): Final validation

## Key Database Schema
Each year-quarter has its own DB: `results/scan_{year}_{Q1-Q4}/citadel_v2.db`
Table: `flagged`

**Important columns:**
- `pmc_id`, `ref_number` — unique key for each flagged reference
- `claimed_title`, `claimed_authors`, `claimed_venue`, `claimed_year` — what the paper claims
- `claimed_pmid`, `claimed_doi` — identifiers the paper provides
- `actual_title_pmid`, `actual_title_doi` — what those identifiers actually resolve to
- `category` — wrong_pmid | fab_title | llm_confirmed_fake | title_swap | valid
- `gs_verdict` — for fab_title pipeline: real_paper | not_found | citation_laundering
- `wp_gs_verdict` — for wrong_pmid pipeline: real_paper | not_found | citation_laundering
- `rescue_pattern` — if set, entry is a rescued false positive (not counted as fabricated)
- `journal` — the PMC paper that contains this reference

**What counts as "fabricated":**
- `category = 'wrong_pmid' AND wp_gs_verdict = 'not_found' AND (rescue_pattern IS NULL OR rescue_pattern = '')`
- `category IN ('llm_confirmed_fake', 'fab_title') AND gs_verdict = 'not_found' AND (rescue_pattern IS NULL OR rescue_pattern = '')`

## Key Files

### Production Pipeline (use these)
| File | Purpose |
|------|---------|
| `citadel_pipeline.py` | **Main orchestrator** -- single entry point for all stages |
| `citadel_config.yaml` | All configuration (thresholds, API settings, paths) |
| `weekly_run.bat` | Windows Task Scheduler target for weekly automation |
| `core/config.py` | Config loader (YAML + .env + env vars) |
| `core/db_manager.py` | Quarterly DB path resolution + migrations |
| `core/scanner.py` | Scanner wrapper (routes to correct quarterly DB) |
| `core/pubmed_updater.py` | Auto-update local PubMed DB with daily files |
| `core/llm_judge_runner.py` | LLM judge wrapper (configurable model) |
| `core/gs_verifier.py` | Unified GS verify (fab_title + wrong_pmid) |
| `core/rescue.py` | Unified rescue (builtin + eyeball + LLM artifact) |

### Core Modules (imported by pipeline, still standalone-runnable)
| File | Purpose |
|------|---------|
| `scan_v2.py` | Scanner engine -- extracts refs from PMC XML |
| `classifier.py` | Classification engine (FTS5 + word overlap) |
| `llm_judge.py` | Claude Haiku triage functions + prompt |
| `google_scholar_verify.py` | Serper.dev search functions |
| `rescue_patterns.py` | Builtin rescue patterns P1-P6 |
| `eyeball_scan.py` | Eyeball rescue patterns E1-E19 |
| `pubmed_local.py` | Build/query local PubMed DB (40M articles) |

### Deprecated (see `legacy/DEPRECATED.md`)
| File | Replaced By |
|------|-------------|
| `continuous_pipeline.py` | `citadel_pipeline.py` |
| `gs_verify_all_wrong_pmid.py` | `core/gs_verifier.py` |
| `apply_rescues.py` | `core/rescue.py` |
| `check_status.py` | `citadel_pipeline.py --status` |

## Critical Technical Notes
- **Python on Windows**: Use `python` not `python3`
- **Paths**: Use forward slashes `C:/Users/...` in bash to avoid EOF errors
- **PYTHONUNBUFFERED=1**: Required for real-time background output
- **SQLite**: WAL mode + busy_timeout for concurrent access
- **LLM judge**: 1 worker at a time (>2 parallel causes API errors)
- **Serper API key**: In `.env` as `SERPER_API_KEY`
- **PubMed local DB**: Has NO authors column — only title, journal, year
- **DB table**: Named `flagged` (NOT `flagged_references`)

## User Preferences
- Max types quickly with typos — interpret intent, don't ask clarification
- Prefers progress numbers and actionable next steps
- Wants minimal permission interruptions
- Paper approach: ONE unified system, 3-year window (2023-2025)

## Rescue Pattern Reference
Entries with `rescue_pattern` set are excluded from fabrication counts:
- `P1-P6_*` — Round 1 regex QC (526 entries)
- `llm_fp_*` — Round 2 GPT-4o-mini rescue (362 entries)
- `sandy_pattern:*` — Round 3a parsing artifacts (163 entries)
- `metadata_rescue:*` — Round 3b title similarity rescue (335 entries)
- `eyeball:*` — Round 4a eyeball patterns (158 entries)
- `eyeball3:*` — Round 4b eyeball batch 3 (53 entries)
- `llm_eyeball:gpt4omini` — Round 5a GPT artifact detection (510 entries)
- `nir_eyeball:manual` — Round 5b Nir manual rescue (5 entries)

## Railway Deployment
- **Live**: https://web-production-2c35b.up.railway.app
- **GitHub**: mtopaz/citadel-review
- **Deploy dir**: `citadel-review-deploy/`
- Round 5 deployed, Pallavi complete (83% precision)

## Running the Pipeline

```bash
# Weekly scan (all stages, last 7 days)
python citadel_pipeline.py --days 7

# Individual stages
python citadel_pipeline.py --stage scan --days 7
python citadel_pipeline.py --stage llm
python citadel_pipeline.py --stage gs
python citadel_pipeline.py --stage rescue

# Status dashboard
python citadel_pipeline.py --status

# Quick test (1 day, 5 papers max)
python citadel_pipeline.py --days 1 --max-papers 5

# Skip PubMed update
python citadel_pipeline.py --days 7 --no-pubmed-update
```

## What's Next
1. **Paper under review** at Lancet (submitted 2026-02-24)
2. **Weekly monitoring** via `weekly_run.bat` (Task Scheduler, Sunday 2 AM)
3. **Respond to reviewer feedback** when it comes
