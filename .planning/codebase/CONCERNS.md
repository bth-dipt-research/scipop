# Codebase Concerns

**Analysis Date:** 2026-04-02

## Tech Debt

**Notebook-derived Streamlit script in production path:**
- Issue: `src/DIPT research topics-hierarchical TM.py` mixes active UI code with ~230 lines of commented notebook cells, making maintenance and review difficult.
- Files: `src/DIPT research topics-hierarchical TM.py`
- Impact: Changes are risky because active behavior is hard to separate from archival code; contributors can modify stale blocks by mistake.
- Fix approach: Split active Streamlit app into a clean module (for example `src/topic_model_app.py`) and move exploratory notebook logic to `experiments/*.ipynb` only.

**Hard-coded execution assumptions for paths and runtime context:**
- Issue: `src/research_question_extractor.py` defines `data_dir = Path("../data/dipt_papers_2024")` and imports `from keys import OPENAI_KEY`, both coupled to a specific working directory and local file layout.
- Files: `src/research_question_extractor.py`, `src/keys.py`
- Impact: Script behavior changes by launch directory; onboarding and CI reproducibility degrade.
- Fix approach: Resolve paths from `__file__` or project root and load secrets/config via environment variables.

## Known Bugs

**Extractor fails when run from repository root:**
- Symptoms: Input/output directories resolve incorrectly when launched outside `src/`, causing missing file errors.
- Files: `src/research_question_extractor.py`
- Trigger: Run `python src/research_question_extractor.py` from `/home/mun/development/scipop`.
- Workaround: Run from `/home/mun/development/scipop/src` so `../data/...` resolves as intended.

**CSV export can crash on non-parseable model responses:**
- Symptoms: The export loop assumes `result['response']['parsed']['research_questions']` always exists.
- Files: `src/research_question_extractor.py`
- Trigger: Any LLM response where `parsed` is `None` or schema parsing fails.
- Workaround: Manually inspect `response['raw']` and rerun extraction after removing failed entries.

## Security Considerations

**Plaintext API credential handling:**
- Risk: API key material is stored in a Python source file and imported directly by application code.
- Files: `src/keys.py`, `src/research_question_extractor.py`, `.gitignore`
- Current mitigation: `.gitignore` excludes `src/keys.py`.
- Recommendations: Use environment variables (for example `OPENAI_API_KEY`) and fail fast if unset; add a committed template like `.env.example` without secrets; add secret scanning in CI.

**Unsafe serialized output format for downstream consumers:**
- Risk: Writing extraction artifacts as pickle encourages future `pickle.load` usage, which is unsafe for untrusted files.
- Files: `src/research_question_extractor.py`
- Current mitigation: CSV output is also generated.
- Recommendations: Prefer JSON/JSONL for structured output and treat pickle artifacts as internal-only temporary files.

## Performance Bottlenecks

**Full-document prompt strategy scales poorly with corpus size:**
- Problem: Each PDF is loaded in full text and sent as a single LLM prompt.
- Files: `src/research_question_extractor.py`
- Cause: `pdf_to_text()` concatenates all pages; no chunking, summarization, or token budgeting is applied.
- Improvement path: Chunk documents by section/page, extract per chunk, then aggregate research questions.

**Sequential extraction creates long wall-clock runtime:**
- Problem: Processing is strictly serial with network-bound calls and long retry windows (`min=10`, `max=60`, `stop_after_attempt(5)`).
- Files: `src/research_question_extractor.py`
- Cause: For-loop invokes one request at a time and blocks on each retry cycle.
- Improvement path: Add bounded concurrency (worker pool) with rate-limit-aware scheduling and checkpointing.

## Fragile Areas

**Schema assumptions across LLM boundary:**
- Files: `src/research_question_extractor.py`
- Why fragile: Code depends on structured output shape without guarding for malformed/partial responses before CSV writing.
- Safe modification: Add explicit validation guard clauses around `response`, `parsed`, and `research_questions`; persist failed records separately.
- Test coverage: No automated tests detected for extractor behavior or parser edge cases.

**Stateful UI flow tied to Streamlit session keys:**
- Files: `src/DIPT research topics-hierarchical TM.py`
- Why fragile: Navigation relies on specific `st.session_state` keys (`step`, `uploaded`, `df_filtered`, `input`) initialized ad hoc in module scope.
- Safe modification: Centralize state initialization in one function and validate required keys before each step transition.
- Test coverage: No automated tests detected for multi-step UI transitions.

## Scaling Limits

**Repository growth from committed data and notebooks:**
- Current capacity: Repository includes tracked heavy assets (for example `experiments/BTH research topics.ipynb` ~17.3MB and `data/dipt_papers_2024/pdfs/1897893.pdf` ~7.6MB) and 84 tracked files under `data/**`.
- Limit: Clone/fetch time and PR review quality degrade as binary assets increase.
- Scaling path: Move large datasets/artifacts to object storage or DVC/LFS and keep only lightweight references in git.

**LLM extraction throughput limited by request model:**
- Current capacity: One paper processed per synchronous request cycle.
- Limit: Throughput drops sharply as `data/dipt_papers_2024/pdfs/**` grows.
- Scaling path: Add asynchronous batching, resumable checkpoints, and per-file progress persistence.

## Dependencies at Risk

**Unbounded platform dependency on local Poppler/system libs for PDF tooling:**
- Risk: `pdf2image` in `requirements.txt` depends on system-level binaries that are not pinned in project setup docs.
- Impact: Environment setup becomes non-reproducible across developer machines/CI runners.
- Migration plan: Document OS package prerequisites explicitly in `README.md` or replace usages with pure-Python alternatives where possible.

## Missing Critical Features

**No automated validation pipeline for extraction quality and regressions:**
- Problem: There is no automated way to detect schema regressions, parsing failures, or output drift.
- Blocks: Safe refactoring of `src/research_question_extractor.py` and reliable scaling of monthly/biannual processing loops described in `docs/loops.md`.

## Test Coverage Gaps

**Core extraction and export workflow is untested:**
- What's not tested: PDF loading, LLM response parsing, retry behavior, CSV serialization, and failure handling.
- Files: `src/research_question_extractor.py`
- Risk: Runtime failures and silent data-quality regressions reach production runs unnoticed.
- Priority: High

**Streamlit step flow and data filtering are untested:**
- What's not tested: Upload step, publication type filtering, input column selection, and step navigation.
- Files: `src/DIPT research topics-hierarchical TM.py`
- Risk: UI regressions can block topic model generation for end users.
- Priority: Medium

---

*Concerns audit: 2026-04-02*
