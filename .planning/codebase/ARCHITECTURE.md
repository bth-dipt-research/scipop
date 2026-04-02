# Architecture

**Analysis Date:** 2026-04-02

## Pattern Overview

**Overall:** Script-oriented pipeline architecture with two primary execution modes (batch extraction and interactive UI).

**Key Characteristics:**
- Top-level scripts execute end-to-end flows directly from module scope in `src/research_question_extractor.py` and `src/DIPT research topics-hierarchical TM.py`.
- File-based boundaries connect stages through CSV/PKL/XLSX/PDF artifacts under `data/` (for example `data/dipt_papers_2024/research_questions_0temp/results.csv`).
- External AI/ML tooling is integrated at the script layer without an internal service/repository abstraction (LangChain/OpenAI in `src/research_question_extractor.py`, BERTopic stack in `src/DIPT research topics-hierarchical TM.py`).

## Layers

**Interaction Layer (UI):**
- Purpose: Collect user inputs and step users through topic-model setup.
- Location: `src/DIPT research topics-hierarchical TM.py`
- Contains: Streamlit views, buttons, multiselects, upload workflow (`st.file_uploader`, `st.button`, `st.multiselect`).
- Depends on: Streamlit session state and pandas-loaded data.
- Used by: Human users running the Streamlit app.

**Orchestration Layer (Pipeline Scripts):**
- Purpose: Sequence data loading, model calls, and export.
- Location: `src/research_question_extractor.py`, `src/DIPT research topics-hierarchical TM.py`
- Contains: End-to-end control flow, loops over files, prompt/message assembly, export logic.
- Depends on: AI/ML adapters, local filesystem, prompt text embedded in script constants.
- Used by: CLI/script execution and Streamlit runtime.

**AI/ML Adapter Layer:**
- Purpose: Convert source material into structured model outputs.
- Location: `src/research_question_extractor.py` (LangChain + OpenAI), commented modeling pipeline in `src/DIPT research topics-hierarchical TM.py`.
- Contains: `ChatOpenAI(...).with_structured_output(...)`, `PyPDFLoader`, BERTopic component imports.
- Depends on: External model providers and Python ML libraries.
- Used by: Orchestration scripts.

**Persistence Layer (Filesystem Artifacts):**
- Purpose: Store inputs and outputs for downstream analysis.
- Location: `data/` (for example `data/dipt_papers_2024/pdfs/`, `data/dipt_papers_2024/research_questions_0temp/`, `data/dipt/*.csv`).
- Contains: PDFs, CSV exports, pickled extraction payloads, XLSX files, generated HTML.
- Depends on: Relative path conventions from script locations.
- Used by: Both scripts and notebook/manual analysis.

## Data Flow

**Research Question Extraction Flow:**

1. Discover PDF inputs from `data/dipt_papers_2024/pdfs/missed` via `get_file_names` in `src/research_question_extractor.py`.
2. Load each PDF into text (`pdf_to_text`) and wrap as `Document` with `paper_id` metadata in `src/research_question_extractor.py`.
3. Build `SystemMessage` + `HumanMessage`, call `completion_with_backoff` (retry wrapper), and parse structured `ResearchQuestions`.
4. Persist full extraction object to `data/dipt_papers_2024/research_questions_0temp/extraction_missed.pkl` and flattened rows to `data/dipt_papers_2024/research_questions_0temp/results_missed.csv`.

**Topic Modeling UI Flow:**

1. User uploads CSV/XLSX through Streamlit in `src/DIPT research topics-hierarchical TM.py`.
2. Script stores working DataFrame in `st.session_state.df` and advances step state via `goto()`.
3. User filters publication types and selects input columns; filtered data is written to `st.session_state.df_filtered`.
4. Downstream BERTopic operations are prepared in the same file (currently present mostly as commented workflow sections for training/export).

**State Management:**
- Streamlit flow state is kept in `st.session_state` keys (`step`, `uploaded`, `df_filtered`, `input`) in `src/DIPT research topics-hierarchical TM.py`.
- Batch extraction state is in in-memory lists/dicts (`results`, `extraction`) then serialized to files in `src/research_question_extractor.py`.

## Key Abstractions

**Structured Research Question Schema:**
- Purpose: Enforce normalized LLM output shape.
- Examples: `ResearchQuestion` and `ResearchQuestions` `TypedDict` declarations in `src/research_question_extractor.py`.
- Pattern: Type-annotated schema + LangChain structured output binding (`with_structured_output`).

**Document-Centric Processing Unit:**
- Purpose: Treat each paper as one processing unit with metadata.
- Examples: `Document(page_content=..., metadata={"paper_id": ...})` in `src/research_question_extractor.py`.
- Pattern: Convert files to unified document objects before model invocation.

**Step-Wizard UI Control:**
- Purpose: Keep Streamlit app navigation deterministic.
- Examples: `goto(step: int)`, `cancel_upload_cb()`, and step checks in `src/DIPT research topics-hierarchical TM.py`.
- Pattern: Small callback functions mutate session state, then rerun.

## Entry Points

**Batch extractor script:**
- Location: `src/research_question_extractor.py`
- Triggers: Run as a Python script from the project’s source context.
- Responsibilities: Load PDFs, query model with retries, write PKL/CSV outputs.

**Interactive topic model app:**
- Location: `src/DIPT research topics-hierarchical TM.py`
- Triggers: Run with Streamlit.
- Responsibilities: Upload/filter publication dataset and guide users through topic-model preparation.

**Project-level flow definition (documentation):**
- Location: `README.md`, `docs/loops.md`
- Triggers: Read by developers/operators.
- Responsibilities: Define conceptual pipeline loops and system stages that scripts implement operationally.

## Error Handling

**Strategy:** Minimal explicit error handling; resilience is concentrated around LLM calls.

**Patterns:**
- Retry with exponential backoff for model invocations via `@retry(...)` in `src/research_question_extractor.py`.
- Guarded UI progression through disabled Streamlit buttons and presence checks in `src/DIPT research topics-hierarchical TM.py`.

## Cross-Cutting Concerns

**Logging:** Lightweight console/UX logging with `print(...)` in `src/research_question_extractor.py` and status components (`st.success`, `st.badge`) in `src/DIPT research topics-hierarchical TM.py`.
**Validation:** Input validation is mostly implicit (file type checks and column presence checks) in `src/DIPT research topics-hierarchical TM.py`; no centralized schema validation module is present.
**Authentication:** API credential consumption occurs in `src/research_question_extractor.py` through `from keys import OPENAI_KEY`; credential storage file is excluded in `.gitignore` (`src/keys.py`).

---

*Architecture analysis: 2026-04-02*
