# Technology Stack

**Analysis Date:** 2026-04-02

## Languages

**Primary:**
- Python 3.12 - Main application and data-processing code in `src/research_question_extractor.py` and `src/DIPT research topics-hierarchical TM.py`.

**Secondary:**
- Markdown - Project documentation in `README.md`.
- Plain text prompts - LLM prompt assets in `prompts/research-to-practice.txt` and `prompts/vision-builder.txt`.

## Runtime

**Environment:**
- CPython 3.12 (explicitly documented via conda setup in `README.md` line 27).

**Package Manager:**
- pip (usage documented in `README.md` line 32; pinned as dependency `pip==24.2` in `requirements.txt` line 10).
- Lockfile: missing (dependency pinning is done only in `requirements.txt`).

## Frameworks

**Core:**
- Streamlit 1.50.0 - Interactive UI for topic modeling workflow in `src/DIPT research topics-hierarchical TM.py`.
- LangChain Community 0.3.14 + LangChain OpenAI 0.3.0 - PDF loading and LLM orchestration in `src/research_question_extractor.py` (`PyPDFLoader`, `ChatOpenAI`).
- BERTopic 0.16.4 - Topic modeling pipeline in `src/DIPT research topics-hierarchical TM.py`.

**Testing:**
- Not detected (no `tests/` directory, no `pytest`/`unittest` test files, and no dedicated test config files found).

**Build/Dev:**
- Conda environment workflow documented in `README.md` (`conda create --name scipop python=3.12 pip`).
- Jupyter notebook experimentation present in `experiments/DIPT research topics.ipynb` and `experiments/BTH research topics.ipynb`.

## Key Dependencies

**Critical:**
- `langchain-openai==0.3.0` (`requirements.txt`) - Connects extraction flow to GPT models via `ChatOpenAI` in `src/research_question_extractor.py`.
- `langchain-community==0.3.14` (`requirements.txt`) - Provides `PyPDFLoader` for ingesting local PDF papers in `src/research_question_extractor.py`.
- `bertopic==0.16.4` (`requirements.txt`) - Core topic discovery engine used in `src/DIPT research topics-hierarchical TM.py`.
- `streamlit==1.50.0` (`requirements.txt`) - Front-end runtime for upload/filter/topic-model UI in `src/DIPT research topics-hierarchical TM.py`.

**Infrastructure:**
- `openpyxl==3.1.5` and `xlrd==2.0.1` (`requirements.txt`) - Excel ingestion/export support used by pandas workflows in `src/DIPT research topics-hierarchical TM.py`.
- `PyMuPDF==1.25.1` and `pypdf==5.1.0` (`requirements.txt`) - PDF processing dependencies supporting paper ingestion flows centered in `src/research_question_extractor.py`.
- `nltk==3.9.1` (`requirements.txt`) - Sentence tokenization via `sent_tokenize` in `src/DIPT research topics-hierarchical TM.py`.

## Configuration

**Environment:**
- Runtime parameters are configured in code, not via environment files (for example `model = "gpt-4o-mini"` and `temperature = 0` in `src/research_question_extractor.py`).
- API credential is imported from `src/keys.py` (`from keys import OPENAI_KEY` in `src/research_question_extractor.py`).
- `.gitignore` excludes `src/keys.py` (line 2), indicating local-only secret handling.

**Build:**
- Dependency configuration: `requirements.txt`.
- Developer setup instructions: `README.md`.
- No CI build config (`.github/workflows/*` not detected) and no container build files (`Dockerfile*` not detected).

## Platform Requirements

**Development:**
- Conda + Python 3.12 + pip workflow as documented in `README.md`.
- Local data files expected under `data/` and consumed by scripts in `src/` (for example `../data/dipt_papers_2024` in `src/research_question_extractor.py`).

**Production:**
- Not detected as a packaged/deployed service.
- Current execution targets are local script runs (`src/research_question_extractor.py`) and local Streamlit app sessions (`src/DIPT research topics-hierarchical TM.py`).

---

*Stack analysis: 2026-04-02*
