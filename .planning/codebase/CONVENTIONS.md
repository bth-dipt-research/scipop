# Coding Conventions

**Analysis Date:** 2026-04-02

## Naming Patterns

**Files:**
- Use `snake_case.py` for new Python modules (for example, `src/research_question_extractor.py`).
- Avoid spaces in new file names; `src/DIPT research topics-hierarchical TM.py` is a legacy-style filename and should not be copied for new modules.

**Functions:**
- Use `snake_case` for function names (for example, `pdf_to_text`, `get_file_names`, `completion_with_backoff` in `src/research_question_extractor.py`, and `cancel_upload_cb` in `src/DIPT research topics-hierarchical TM.py`).
- Use verb-oriented names for behavior (`goto`, `cancel_upload_cb`) and noun+verb for data transforms (`pdf_to_text`).

**Variables:**
- Use `snake_case` for local variables and module-level constants/parameters (for example, `paper_dir`, `output_dir`, `default_input_columns` in `src/research_question_extractor.py` and `src/DIPT research topics-hierarchical TM.py`).
- Use concise data-frame aliases (`df`) only for short-lived data processing blocks in `src/DIPT research topics-hierarchical TM.py`.

**Types:**
- Use `PascalCase` for typed schema objects (for example, `ResearchQuestion`, `ResearchQuestions` in `src/research_question_extractor.py`).
- Keep schema fields in `snake_case` (`research_question`) when serializing/deserializing model outputs in `src/research_question_extractor.py`.

## Code Style

**Formatting:**
- Tool used: Not detected (`pyproject.toml`, `setup.cfg`, `.flake8`, `.ruff.toml`, `.pre-commit-config.yaml` not detected in repo root).
- Use 4-space indentation and keep line continuations parenthesized, matching `src/research_question_extractor.py` imports and `ChatOpenAI(...)` initialization.

**Linting:**
- Tool used: Not detected (no Ruff/Flake8/Pylint config files detected).
- Use PEP 8 as baseline for new code to keep style consistent across `src/research_question_extractor.py` and `src/DIPT research topics-hierarchical TM.py`.

## Import Organization

**Order:**
1. Python standard library (`pickle`, `csv`, `pathlib`) as in `src/research_question_extractor.py`
2. Third-party libraries (`langchain_*`, `tenacity`, `streamlit`, `pandas`, BERTopic stack)
3. Local modules (`from keys import OPENAI_KEY` in `src/research_question_extractor.py`)

**Path Aliases:**
- Not detected. Use direct relative/local imports in `src/` modules.

## Error Handling

**Patterns:**
- Use retry-based resilience for external API calls with `tenacity.retry`, as shown by `completion_with_backoff` in `src/research_question_extractor.py`.
- Use guard conditions for UI state flow in Streamlit (`if st.session_state.step == ...`) in `src/DIPT research topics-hierarchical TM.py`.
- `try/except` blocks are not used in `src/`; for new I/O-heavy operations, add explicit exception handling around file and API boundaries.

## Logging

**Framework:** console (`print`)

**Patterns:**
- Use `print(...)` for progress logging in scripts (`print(f'Analyzing {paper_id}')` in `src/research_question_extractor.py`).
- Streamlit status output uses UI primitives (`st.success`, `st.write`) in `src/DIPT research topics-hierarchical TM.py`.

## Comments

**When to Comment:**
- Use comments to explain analysis intent and parameter rationale for ML/topic-modeling steps, as demonstrated in `src/DIPT research topics-hierarchical TM.py` (large explanatory comment blocks).
- Keep implementation comments near transformation stages when data assumptions are implicit.

**JSDoc/TSDoc:**
- Not applicable for this Python codebase.
- Python docstring usage is minimal; one concise docstring exists on `ResearchQuestion` in `src/research_question_extractor.py`.

## Function Design

**Size:**
- Use small utility functions for reusable operations (`pdf_to_text`, `get_file_names`) and keep orchestration logic at module scope for batch processing in `src/research_question_extractor.py`.

**Parameters:**
- Prefer typed parameters for file/data inputs (`pdf_file: Path`, `path: Path` in `src/research_question_extractor.py`).
- Use `st.session_state` instead of long parameter chains for Streamlit workflow steps in `src/DIPT research topics-hierarchical TM.py`.

**Return Values:**
- Return simple Python primitives/collections (`str`, `list[file]`) from helpers in `src/research_question_extractor.py`.
- Streamlit callback helpers mutate state and return `None` (`goto`, `cancel_upload_cb` in `src/DIPT research topics-hierarchical TM.py`).

## Module Design

**Exports:**
- Explicit export surfaces are not used. Modules are script-style and execute logic on import/run (`src/research_question_extractor.py`, `src/DIPT research topics-hierarchical TM.py`).

**Barrel Files:**
- Not used in this repository.

---

*Convention analysis: 2026-04-02*
