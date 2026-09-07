# OpenRichpedia Neo4j Course Project Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a reproducible OpenRichpedia-to-Neo4j course project with data fetching, preprocessing, validation, import scripts, visualization queries, tests, and Chinese documentation.

**Architecture:** A small Python CLI pipeline downloads a pinned OpenRichpedia subset, parses the upstream JavaScript data files into normalized graph CSV files, validates graph integrity, and imports them into Neo4j. Neo4j Browser is used for visual inspection and course screenshots; Markdown documentation explains every operation from installation to report writing.

**Tech Stack:** Python 3.10+, Python standard library, pytest, Neo4j Python Driver 6.x, Neo4j 5.26 LTS / Neo4j Desktop.

**Spec:** `docs/superpowers/specs/2026-09-07-openrichpedia-neo4j-design.md`

## Global Constraints

- Pin upstream OpenRichpedia data to commit `0ded4b2c9414160b5b39914d43e42168e4d0762c`.
- Do not download or commit the large image binary archives.
- All math in documentation must use LaTeX.
- Relationship types are limited to `HAS_SIGHT`, `HAS_IMAGE`, and `CONTAINS`.
- Python code must support Python 3.10+.
- Neo4j teaching baseline is 5.26 LTS; Python driver is 6.x.

---

### Task 1: Dataset parsers and normalization

**Files:**
- Create: `src/openrichpedia_kg/parsers.py`
- Create: `src/openrichpedia_kg/model.py`
- Test: `tests/test_parsers.py`

**Interfaces:**
- Produces `Node`, `Relationship`, `parse_city_hierarchy`, `parse_named_js_entities`, `parse_pair_relations`, `normalize_wikidata_id`.

- [ ] Write failing tests for city hierarchy parsing, named entity parsing, pair parsing, escaped labels, and ID normalization.
- [ ] Run `pytest tests/test_parsers.py -q` and confirm RED.
- [ ] Implement the minimal parser/model functions.
- [ ] Run the parser tests and confirm GREEN.
- [ ] Commit.

### Task 2: Graph builder and validation

**Files:**
- Create: `src/openrichpedia_kg/build.py`
- Create: `src/openrichpedia_kg/validate.py`
- Test: `tests/test_build.py`
- Test: `tests/test_validate.py`

**Interfaces:**
- Consumes parser results.
- Produces `build_graph(raw_dir) -> (nodes, relationships)` and `validate_graph(nodes, relationships) -> ValidationReport`.

- [ ] Write failing tests for node merge priority, relationship deduplication, auto-created image nodes, dangling endpoint detection, and duplicate detection.
- [ ] Run targeted tests and confirm RED.
- [ ] Implement graph construction and validation.
- [ ] Run targeted tests and confirm GREEN.
- [ ] Commit.

### Task 3: Fetching and CSV pipeline

**Files:**
- Create: `scripts/fetch_openrichpedia.py`
- Create: `scripts/preprocess.py`
- Create: `scripts/validate_processed.py`
- Create: `src/openrichpedia_kg/io.py`
- Test: `tests/test_io.py`

**Interfaces:**
- Fetches six pinned raw files.
- Writes `nodes.csv`, `relationships.csv`, `stats.json`.

- [ ] Write failing CSV/stats round-trip tests.
- [ ] Confirm RED.
- [ ] Implement CSV and stats I/O, then CLI scripts.
- [ ] Confirm GREEN for I/O tests and full suite.
- [ ] Commit.

### Task 4: Neo4j import and Cypher examples

**Files:**
- Create: `scripts/import_neo4j.py`
- Create: `cypher/01_constraints.cypher`
- Create: `cypher/02_load_csv.cypher`
- Create: `cypher/03_queries.cypher`
- Create: `.env.example`
- Create: `requirements.txt`

**Interfaces:**
- Imports normalized CSV to `:Entity` nodes and typed relationships.
- Uses environment variables `NEO4J_URI`, `NEO4J_USER`, `NEO4J_PASSWORD`, `NEO4J_DATABASE`.

- [ ] Write tests for relationship type whitelist and batch query generation.
- [ ] Confirm RED.
- [ ] Implement import helpers and CLI.
- [ ] Confirm GREEN.
- [ ] Commit.

### Task 5: Documentation and report

**Files:**
- Create: `README.md`
- Create: `docs/01-数据集分析.md`
- Create: `docs/02-Neo4j安装与配置.md`
- Create: `docs/03-数据预处理.md`
- Create: `docs/04-导入与可视化.md`
- Create: `docs/05-截图与答辩指南.md`
- Create: `docs/课程实验报告.md`
- Create: `DATA_LICENSE.md`

- [ ] Document the exact Windows/macOS commands.
- [ ] Explain the graph schema and mapping using LaTeX for formulas.
- [ ] Document all supplied Cypher queries and expected observations.
- [ ] Provide a report template with screenshot placeholders and analysis prompts.
- [ ] Commit.

### Task 6: Verification and release package

**Files:**
- Create: `data/raw/README.md`
- Create: `data/processed/README.md`
- Create: `Makefile`

- [ ] Run `pytest -q`.
- [ ] Run `python -m compileall src scripts`.
- [ ] Run preprocessing against fixture data and validate outputs.
- [ ] Scan documentation for stale placeholders and non-LaTeX formulas.
- [ ] Create a ZIP release of the repository.
- [ ] Commit final verification changes.
