# Testing Patterns

**Analysis Date:** 2026-04-02

## Test Framework

**Runner:**
- Not detected (no `pytest.ini`, `pyproject.toml` test section, `tox.ini`, `jest.config.*`, or `vitest.config.*` found in `/home/mun/development/scipop`).
- Config: Not detected.

**Assertion Library:**
- Not detected (no automated test suite present).

**Run Commands:**
```bash
Not configured in repository              # Run all tests
Not configured in repository              # Watch mode
Not configured in repository              # Coverage
```

## Test File Organization

**Location:**
- No automated test directories or files detected (`tests/`, `test/`, `*.test.py`, `*.spec.py` not found).

**Naming:**
- Not detected. For new tests, use `test_<module>.py` to align with Python ecosystem defaults.

**Structure:**
```
Not applicable: test tree not present
```

## Test Structure

**Suite Organization:**
```python
# Not detected in current codebase.
# Existing validation is script- and UI-driven:
# - Batch script execution in `src/research_question_extractor.py`
# - Streamlit interaction flow in `src/DIPT research topics-hierarchical TM.py`
```

**Patterns:**
- Setup pattern: Manual environment setup in `README.md` (`conda create ...`, `pip install -r requirements.txt`).
- Teardown pattern: Not detected.
- Assertion pattern: Not detected.

## Mocking

**Framework:** Not detected.

**Patterns:**
```python
# No mocking patterns found in repository Python modules:
# - `src/research_question_extractor.py`
# - `src/DIPT research topics-hierarchical TM.py`
```

**What to Mock:**
- For future tests, mock external model/API calls from `ChatOpenAI` in `src/research_question_extractor.py` and PDF loading via `PyPDFLoader` to keep tests deterministic.

**What NOT to Mock:**
- Do not mock pure transformation logic (for example, `get_file_names` output filtering in `src/research_question_extractor.py`); validate with temporary filesystem fixtures.

## Fixtures and Factories

**Test Data:**
```python
# Not implemented.
# Candidate fixture inputs already exist under:
# - `data/dipt_papers_2024/pdfs/`
# - `data/dipt/*.csv`
```

**Location:**
- No dedicated fixture directory detected.

## Coverage

**Requirements:** None enforced.

**View Coverage:**
```bash
Not configured in repository
```

## Test Types

**Unit Tests:**
- Not implemented.
- Add first unit tests around pure helpers in `src/research_question_extractor.py` (`pdf_to_text` with mocked loader, `get_file_names` with temp files).

**Integration Tests:**
- Not implemented.
- Add integration tests for end-to-end extraction flow in `src/research_question_extractor.py` with controlled sample PDFs and mocked LLM responses.

**E2E Tests:**
- Not used.
- Streamlit UI in `src/DIPT research topics-hierarchical TM.py` currently relies on manual verification.

## Common Patterns

**Async Testing:**
```python
# Not detected (current source code is synchronous).
```

**Error Testing:**
```python
# Not detected.
# Recommended first cases for new tests:
# - API retry exhaustion in `completion_with_backoff` (`src/research_question_extractor.py`)
# - Missing/invalid upload columns in Streamlit flow (`src/DIPT research topics-hierarchical TM.py`)
```

---

*Testing analysis: 2026-04-02*
