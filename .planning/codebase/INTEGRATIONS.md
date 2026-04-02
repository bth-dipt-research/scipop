# External Integrations

**Analysis Date:** 2026-04-02

## APIs & External Services

**LLM API:**
- OpenAI Chat Completions (through LangChain) - Used to extract structured research questions from full-paper text in `src/research_question_extractor.py`.
  - SDK/Client: `langchain-openai` (`ChatOpenAI` imported in `src/research_question_extractor.py` line 5).
  - Auth: `OPENAI_KEY` loaded from `src/keys.py` and passed to `ChatOpenAI(api_key=OPENAI_KEY)` in `src/research_question_extractor.py` line 57.

**Content Ingestion:**
- Local PDF corpus - Ingested via `PyPDFLoader` from `langchain_community.document_loaders` in `src/research_question_extractor.py` lines 4 and 28-31.
  - SDK/Client: `langchain-community`.
  - Auth: Not applicable (local filesystem reads).

## Data Storage

**Databases:**
- Not detected.
  - Connection: Not applicable.
  - Client: Not applicable.

**File Storage:**
- Local filesystem only.
  - Input PDFs from `data/dipt_papers_2024/pdfs/` (referenced as `../data/dipt_papers_2024/pdfs/missed` in `src/research_question_extractor.py` line 46).
  - Outputs written as pickle/CSV to `data/dipt_papers_2024/research_questions_0temp/` in `src/research_question_extractor.py` lines 48 and 107-121.
  - Streamlit app ingests user-uploaded CSV/XLSX files in memory via `st.file_uploader` and pandas in `src/DIPT research topics-hierarchical TM.py` lines 57-68.

**Caching:**
- None detected.

## Authentication & Identity

**Auth Provider:**
- External provider: OpenAI API key authentication only.
  - Implementation: Direct key import from `src/keys.py` and direct parameter injection into `ChatOpenAI` in `src/research_question_extractor.py`.
- End-user authentication for the Streamlit app is not detected in `src/DIPT research topics-hierarchical TM.py`.

## Monitoring & Observability

**Error Tracking:**
- None detected (no Sentry/Bugsnag/Datadog SDK imports in `src/*.py`).

**Logs:**
- Basic console output with `print(...)` (for example `print(f'Analyzing {paper_id}')` in `src/research_question_extractor.py` line 77).

## CI/CD & Deployment

**Hosting:**
- Not detected (no deployment manifests or infra configuration files found).

**CI Pipeline:**
- None detected (`.github/workflows/` not found).

## Environment Configuration

**Required env vars:**
- Not detected as environment variables in current implementation.
- The effective required secret is an OpenAI API key stored as Python constant `OPENAI_KEY` in `src/keys.py`.

**Secrets location:**
- `src/keys.py` (excluded by `.gitignore` line 2).
- No `.env` files detected in repository root or subdirectories.

## Webhooks & Callbacks

**Incoming:**
- None detected.

**Outgoing:**
- HTTPS API call flow to OpenAI via `ChatOpenAI` in `src/research_question_extractor.py`.

---

*Integration audit: 2026-04-02*
