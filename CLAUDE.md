<!-- GSD:project-start source:PROJECT.md -->
## Project

**Static scipop**

Static scipop is a public, static website that publishes expert-reviewed synthesis texts derived from clustered research areas. It is designed for a general audience to browse research area summaries without needing to run notebooks, scripts, or local tooling. The MVP focuses on clear publication and navigation of finalized synthesis content, not generation automation.

**Core Value:** Anyone can reliably access and understand the approved research syntheses through a simple, shareable public website.

### Constraints

- **Hosting**: GitHub Pages — required for initial deployment target and sharing simplicity
- **Content Source**: Markdown-first — finalized syntheses are currently stored in markdown files
- **Scope**: MVP publication only — no planning/execution for end-to-end automation yet
- **Audience**: General public — content presentation should be readable beyond domain experts
- **Delivery Model**: Static site architecture — avoid backend/runtime complexity in v1
<!-- GSD:project-end -->

<!-- GSD:stack-start source:codebase/STACK.md -->
## Technology Stack

## Languages
- Python 3.12 - Main application and data-processing code in `src/research_question_extractor.py` and `src/DIPT research topics-hierarchical TM.py`.
- Markdown - Project documentation in `README.md`.
- Plain text prompts - LLM prompt assets in `prompts/research-to-practice.txt` and `prompts/vision-builder.txt`.
## Runtime
- CPython 3.12 (explicitly documented via conda setup in `README.md` line 27).
- pip (usage documented in `README.md` line 32; pinned as dependency `pip==24.2` in `requirements.txt` line 10).
- Lockfile: missing (dependency pinning is done only in `requirements.txt`).
## Frameworks
- Streamlit 1.50.0 - Interactive UI for topic modeling workflow in `src/DIPT research topics-hierarchical TM.py`.
- LangChain Community 0.3.14 + LangChain OpenAI 0.3.0 - PDF loading and LLM orchestration in `src/research_question_extractor.py` (`PyPDFLoader`, `ChatOpenAI`).
- BERTopic 0.16.4 - Topic modeling pipeline in `src/DIPT research topics-hierarchical TM.py`.
- Not detected (no `tests/` directory, no `pytest`/`unittest` test files, and no dedicated test config files found).
- Conda environment workflow documented in `README.md` (`conda create --name scipop python=3.12 pip`).
- Jupyter notebook experimentation present in `experiments/DIPT research topics.ipynb` and `experiments/BTH research topics.ipynb`.
## Key Dependencies
- `langchain-openai==0.3.0` (`requirements.txt`) - Connects extraction flow to GPT models via `ChatOpenAI` in `src/research_question_extractor.py`.
- `langchain-community==0.3.14` (`requirements.txt`) - Provides `PyPDFLoader` for ingesting local PDF papers in `src/research_question_extractor.py`.
- `bertopic==0.16.4` (`requirements.txt`) - Core topic discovery engine used in `src/DIPT research topics-hierarchical TM.py`.
- `streamlit==1.50.0` (`requirements.txt`) - Front-end runtime for upload/filter/topic-model UI in `src/DIPT research topics-hierarchical TM.py`.
- `openpyxl==3.1.5` and `xlrd==2.0.1` (`requirements.txt`) - Excel ingestion/export support used by pandas workflows in `src/DIPT research topics-hierarchical TM.py`.
- `PyMuPDF==1.25.1` and `pypdf==5.1.0` (`requirements.txt`) - PDF processing dependencies supporting paper ingestion flows centered in `src/research_question_extractor.py`.
- `nltk==3.9.1` (`requirements.txt`) - Sentence tokenization via `sent_tokenize` in `src/DIPT research topics-hierarchical TM.py`.
## Configuration
- Runtime parameters are configured in code, not via environment files (for example `model = "gpt-4o-mini"` and `temperature = 0` in `src/research_question_extractor.py`).
- API credential is imported from `src/keys.py` (`from keys import OPENAI_KEY` in `src/research_question_extractor.py`).
- `.gitignore` excludes `src/keys.py` (line 2), indicating local-only secret handling.
- Dependency configuration: `requirements.txt`.
- Developer setup instructions: `README.md`.
- No CI build config (`.github/workflows/*` not detected) and no container build files (`Dockerfile*` not detected).
## Platform Requirements
- Conda + Python 3.12 + pip workflow as documented in `README.md`.
- Local data files expected under `data/` and consumed by scripts in `src/` (for example `../data/dipt_papers_2024` in `src/research_question_extractor.py`).
- Not detected as a packaged/deployed service.
- Current execution targets are local script runs (`src/research_question_extractor.py`) and local Streamlit app sessions (`src/DIPT research topics-hierarchical TM.py`).
<!-- GSD:stack-end -->

<!-- GSD:conventions-start source:CONVENTIONS.md -->
## Conventions

## Naming Patterns
- Use `snake_case.py` for new Python modules (for example, `src/research_question_extractor.py`).
- Avoid spaces in new file names; `src/DIPT research topics-hierarchical TM.py` is a legacy-style filename and should not be copied for new modules.
- Use `snake_case` for function names (for example, `pdf_to_text`, `get_file_names`, `completion_with_backoff` in `src/research_question_extractor.py`, and `cancel_upload_cb` in `src/DIPT research topics-hierarchical TM.py`).
- Use verb-oriented names for behavior (`goto`, `cancel_upload_cb`) and noun+verb for data transforms (`pdf_to_text`).
- Use `snake_case` for local variables and module-level constants/parameters (for example, `paper_dir`, `output_dir`, `default_input_columns` in `src/research_question_extractor.py` and `src/DIPT research topics-hierarchical TM.py`).
- Use concise data-frame aliases (`df`) only for short-lived data processing blocks in `src/DIPT research topics-hierarchical TM.py`.
- Use `PascalCase` for typed schema objects (for example, `ResearchQuestion`, `ResearchQuestions` in `src/research_question_extractor.py`).
- Keep schema fields in `snake_case` (`research_question`) when serializing/deserializing model outputs in `src/research_question_extractor.py`.
## Code Style
- Tool used: Not detected (`pyproject.toml`, `setup.cfg`, `.flake8`, `.ruff.toml`, `.pre-commit-config.yaml` not detected in repo root).
- Use 4-space indentation and keep line continuations parenthesized, matching `src/research_question_extractor.py` imports and `ChatOpenAI(...)` initialization.
- Tool used: Not detected (no Ruff/Flake8/Pylint config files detected).
- Use PEP 8 as baseline for new code to keep style consistent across `src/research_question_extractor.py` and `src/DIPT research topics-hierarchical TM.py`.
## Import Organization
- Not detected. Use direct relative/local imports in `src/` modules.
## Error Handling
- Use retry-based resilience for external API calls with `tenacity.retry`, as shown by `completion_with_backoff` in `src/research_question_extractor.py`.
- Use guard conditions for UI state flow in Streamlit (`if st.session_state.step == ...`) in `src/DIPT research topics-hierarchical TM.py`.
- `try/except` blocks are not used in `src/`; for new I/O-heavy operations, add explicit exception handling around file and API boundaries.
## Logging
- Use `print(...)` for progress logging in scripts (`print(f'Analyzing {paper_id}')` in `src/research_question_extractor.py`).
- Streamlit status output uses UI primitives (`st.success`, `st.write`) in `src/DIPT research topics-hierarchical TM.py`.
## Comments
- Use comments to explain analysis intent and parameter rationale for ML/topic-modeling steps, as demonstrated in `src/DIPT research topics-hierarchical TM.py` (large explanatory comment blocks).
- Keep implementation comments near transformation stages when data assumptions are implicit.
- Not applicable for this Python codebase.
- Python docstring usage is minimal; one concise docstring exists on `ResearchQuestion` in `src/research_question_extractor.py`.
## Function Design
- Use small utility functions for reusable operations (`pdf_to_text`, `get_file_names`) and keep orchestration logic at module scope for batch processing in `src/research_question_extractor.py`.
- Prefer typed parameters for file/data inputs (`pdf_file: Path`, `path: Path` in `src/research_question_extractor.py`).
- Use `st.session_state` instead of long parameter chains for Streamlit workflow steps in `src/DIPT research topics-hierarchical TM.py`.
- Return simple Python primitives/collections (`str`, `list[file]`) from helpers in `src/research_question_extractor.py`.
- Streamlit callback helpers mutate state and return `None` (`goto`, `cancel_upload_cb` in `src/DIPT research topics-hierarchical TM.py`).
## Module Design
- Explicit export surfaces are not used. Modules are script-style and execute logic on import/run (`src/research_question_extractor.py`, `src/DIPT research topics-hierarchical TM.py`).
- Not used in this repository.
<!-- GSD:conventions-end -->

<!-- GSD:architecture-start source:ARCHITECTURE.md -->
## Architecture

## Pattern Overview
- Top-level scripts execute end-to-end flows directly from module scope in `src/research_question_extractor.py` and `src/DIPT research topics-hierarchical TM.py`.
- File-based boundaries connect stages through CSV/PKL/XLSX/PDF artifacts under `data/` (for example `data/dipt_papers_2024/research_questions_0temp/results.csv`).
- External AI/ML tooling is integrated at the script layer without an internal service/repository abstraction (LangChain/OpenAI in `src/research_question_extractor.py`, BERTopic stack in `src/DIPT research topics-hierarchical TM.py`).
## Layers
- Purpose: Collect user inputs and step users through topic-model setup.
- Location: `src/DIPT research topics-hierarchical TM.py`
- Contains: Streamlit views, buttons, multiselects, upload workflow (`st.file_uploader`, `st.button`, `st.multiselect`).
- Depends on: Streamlit session state and pandas-loaded data.
- Used by: Human users running the Streamlit app.
- Purpose: Sequence data loading, model calls, and export.
- Location: `src/research_question_extractor.py`, `src/DIPT research topics-hierarchical TM.py`
- Contains: End-to-end control flow, loops over files, prompt/message assembly, export logic.
- Depends on: AI/ML adapters, local filesystem, prompt text embedded in script constants.
- Used by: CLI/script execution and Streamlit runtime.
- Purpose: Convert source material into structured model outputs.
- Location: `src/research_question_extractor.py` (LangChain + OpenAI), commented modeling pipeline in `src/DIPT research topics-hierarchical TM.py`.
- Contains: `ChatOpenAI(...).with_structured_output(...)`, `PyPDFLoader`, BERTopic component imports.
- Depends on: External model providers and Python ML libraries.
- Used by: Orchestration scripts.
- Purpose: Store inputs and outputs for downstream analysis.
- Location: `data/` (for example `data/dipt_papers_2024/pdfs/`, `data/dipt_papers_2024/research_questions_0temp/`, `data/dipt/*.csv`).
- Contains: PDFs, CSV exports, pickled extraction payloads, XLSX files, generated HTML.
- Depends on: Relative path conventions from script locations.
- Used by: Both scripts and notebook/manual analysis.
## Data Flow
- Streamlit flow state is kept in `st.session_state` keys (`step`, `uploaded`, `df_filtered`, `input`) in `src/DIPT research topics-hierarchical TM.py`.
- Batch extraction state is in in-memory lists/dicts (`results`, `extraction`) then serialized to files in `src/research_question_extractor.py`.
## Key Abstractions
- Purpose: Enforce normalized LLM output shape.
- Examples: `ResearchQuestion` and `ResearchQuestions` `TypedDict` declarations in `src/research_question_extractor.py`.
- Pattern: Type-annotated schema + LangChain structured output binding (`with_structured_output`).
- Purpose: Treat each paper as one processing unit with metadata.
- Examples: `Document(page_content=..., metadata={"paper_id": ...})` in `src/research_question_extractor.py`.
- Pattern: Convert files to unified document objects before model invocation.
- Purpose: Keep Streamlit app navigation deterministic.
- Examples: `goto(step: int)`, `cancel_upload_cb()`, and step checks in `src/DIPT research topics-hierarchical TM.py`.
- Pattern: Small callback functions mutate session state, then rerun.
## Entry Points
- Location: `src/research_question_extractor.py`
- Triggers: Run as a Python script from the project’s source context.
- Responsibilities: Load PDFs, query model with retries, write PKL/CSV outputs.
- Location: `src/DIPT research topics-hierarchical TM.py`
- Triggers: Run with Streamlit.
- Responsibilities: Upload/filter publication dataset and guide users through topic-model preparation.
- Location: `README.md`, `docs/loops.md`
- Triggers: Read by developers/operators.
- Responsibilities: Define conceptual pipeline loops and system stages that scripts implement operationally.
## Error Handling
- Retry with exponential backoff for model invocations via `@retry(...)` in `src/research_question_extractor.py`.
- Guarded UI progression through disabled Streamlit buttons and presence checks in `src/DIPT research topics-hierarchical TM.py`.
## Cross-Cutting Concerns
<!-- GSD:architecture-end -->

<!-- GSD:workflow-start source:GSD defaults -->
## GSD Workflow Enforcement

Before using Edit, Write, or other file-changing tools, start work through a GSD command so planning artifacts and execution context stay in sync.

Use these entry points:
- `/gsd:quick` for small fixes, doc updates, and ad-hoc tasks
- `/gsd:debug` for investigation and bug fixing
- `/gsd:execute-phase` for planned phase work

Do not make direct repo edits outside a GSD workflow unless the user explicitly asks to bypass it.
<!-- GSD:workflow-end -->



<!-- GSD:profile-start -->
## Developer Profile

> Profile not yet configured. Run `/gsd:profile-user` to generate your developer profile.
> This section is managed by `generate-claude-profile` -- do not edit manually.
<!-- GSD:profile-end -->
