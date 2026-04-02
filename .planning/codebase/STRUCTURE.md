# Codebase Structure

**Analysis Date:** 2026-04-02

## Directory Layout

```text
scipop/
├── src/                    # Executable Python scripts (batch + Streamlit)
├── data/                   # Input corpora and generated analysis artifacts
├── experiments/            # Notebook-based exploratory analysis
├── prompts/                # Prompt definitions for GPT-driven synthesis/extraction
├── docs/                   # Process and loop documentation
├── .planning/codebase/     # Generated mapper reference documents
├── requirements.txt        # Python dependency pinning
├── README.md               # High-level system overview and setup
└── .gitignore              # Ignore rules (keys, cache, notebooks)
```

## Directory Purposes

**`src/`:**
- Purpose: House runnable application logic.
- Contains: Script-style Python modules such as `src/research_question_extractor.py` and `src/DIPT research topics-hierarchical TM.py`.
- Key files: `src/research_question_extractor.py`, `src/DIPT research topics-hierarchical TM.py`, `src/keys.py` (local secret file, gitignored).

**`data/`:**
- Purpose: Persist all pipeline inputs and outputs.
- Contains: Source PDFs, curated CSV/XLSX files, generated PKL/CSV/HTML artifacts.
- Key files: `data/dipt_papers_2024/pdfs/*.pdf`, `data/dipt_papers_2024/research_questions_0temp/results_missed.csv`, `data/dipt/topics.html`, `data/dipt/*.csv`.

**`experiments/`:**
- Purpose: Notebook experiments and ad hoc analysis.
- Contains: Jupyter notebooks.
- Key files: `experiments/DIPT research topics.ipynb`, `experiments/BTH research topics.ipynb`.

**`prompts/`:**
- Purpose: Store long-form prompt instructions used by GPT workflows.
- Contains: Text prompt files.
- Key files: `prompts/research-to-practice.txt`, `prompts/vision-builder.txt`.

**`docs/`:**
- Purpose: Document operational loops and process design.
- Contains: Markdown documentation.
- Key files: `docs/loops.md`.

## Key File Locations

**Entry Points:**
- `src/research_question_extractor.py`: Batch pipeline that extracts research questions from PDFs and writes serialized/tabular outputs.
- `src/DIPT research topics-hierarchical TM.py`: Streamlit UI entry point for dataset upload/filtering and topic-model preparation.
- `experiments/DIPT research topics.ipynb`: Notebook entry for exploratory DIPT topic modeling.

**Configuration:**
- `requirements.txt`: Dependency lock/pinning for Python runtime.
- `.gitignore`: Excludes runtime artifacts and local secret material (`src/keys.py`, `__pycache__`, notebooks pattern).
- `README.md`: Setup commands and conceptual flow map.

**Core Logic:**
- `src/research_question_extractor.py`: PDF loading, LLM invocation with retries, structured result persistence.
- `src/DIPT research topics-hierarchical TM.py`: Streamlit step management and dataset selection logic.

**Testing:**
- Not detected (`*.test.py` / `tests/` directories are not present in the current tree).

## Naming Conventions

**Files:**
- Primary Python modules usually follow snake_case (`src/research_question_extractor.py`).
- One script preserves notebook-export naming with spaces/hyphen (`src/DIPT research topics-hierarchical TM.py`); avoid introducing additional filenames with spaces for new modules.

**Directories:**
- Lowercase top-level names for functional grouping (`src/`, `data/`, `docs/`, `prompts/`, `experiments/`).
- Dataset-specific nested folders under `data/` (for example `data/dipt_papers_2024/`, `data/dipt/`).

## Where to Add New Code

**New Feature:**
- Primary code: Add a new module in `src/` (for example `src/<feature_name>.py`) and keep orchestration scripts thin by moving reusable functions into dedicated modules.
- Tests: Create `tests/` at project root (for example `tests/test_<feature_name>.py`) because no test location is currently established.

**New Component/Module:**
- Implementation: Place reusable domain logic in `src/` and keep entry-script responsibilities in `src/research_question_extractor.py` or Streamlit-specific UI logic in `src/DIPT research topics-hierarchical TM.py`.

**Utilities:**
- Shared helpers: Add `src/utils/` for filesystem, parsing, and serialization helpers currently embedded in scripts (for example extraction helpers now in `src/research_question_extractor.py`).

## Special Directories

**`data/dipt_papers_2024/research_questions_0temp/`:**
- Purpose: Intermediate/final extraction outputs (PKL + CSV).
- Generated: Yes.
- Committed: Yes (files are currently present in repository tree).

**`src/__pycache__/`:**
- Purpose: Python bytecode cache.
- Generated: Yes.
- Committed: No (ignored via `.gitignore`).

**`experiments/`:**
- Purpose: Notebook experimentation area.
- Generated: Partially (manual notebook outputs/checkpoints are typically generated during use).
- Committed: Not applicable as a stable target; `.gitignore` includes `*.ipynb*`, so treat notebooks as local unless ignore rules are changed.

---

*Structure analysis: 2026-04-02*
