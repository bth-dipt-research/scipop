# Project Research Summary

**Project:** Static scipop - Interactive Topic Modeling UI (v2.0)
**Domain:** Interactive web application for ML-driven research publication analysis
**Researched:** 2026-04-29
**Confidence:** HIGH

## Executive Summary

This research focuses on building v2.0 of scipop: a **standalone Streamlit-based interactive topic modeling tool** that extends the existing partial prototype into a complete workflow mirroring the `experiments/BTH research topics.ipynb` notebook. The tool is NOT integrated with the v1.0 static site — it's a separate utility for iterative topic model refinement with side-by-side parameter comparison at key decision points.

The recommended approach is **incremental enhancement of validated stack components** rather than wholesale replacement. The existing BERTopic + Streamlit + UMAP + HDBSCAN foundation is proven; the research identifies specific version upgrades (Streamlit 1.57.0, BERTopic 0.17.4) and focused additions (Plotly 6.7.0 for visualization) needed to support comparison UI, interactive workflows, and export functionality. The key architectural pattern is a **multi-step wizard with session state** managing 8 workflow steps from upload through export, with aggressive caching of expensive ML operations (embeddings, model training) to prevent performance collapse.

The primary risks are **session state management complexity** and **memory/performance traps** from ML operations. These are mitigated through strict caching patterns (`@st.cache_resource` for models, `@st.cache_data` for embeddings), careful state isolation for comparison views, and upfront impact previews for destructive operations (topic removal). The research identifies 8 critical pitfalls with specific prevention strategies tied to implementation phases.

## Key Findings

### Recommended Stack

**Stack upgrades are targeted to v2.0 features, not wholesale changes.** The existing Python 3.12 + BERTopic + Streamlit + UMAP/HDBSCAN stack is validated and should be enhanced, not replaced.

**Core technology upgrades:**
- **Streamlit 1.57.0** (from 1.50.0) — Adds improved `st.columns()` layout control with gap parameter, better session state management, enhanced `st.dataframe()` with row selection events (`on_select`, `selection_mode`), and performance improvements for large datasets. Essential for side-by-side comparison UI.
- **BERTopic 0.17.4** (from 0.16.4) — Adds improved `reduce_outliers()` methods, enhanced `update_topics()` for iterative refinement, better `visualize_hierarchy()` output, and `merge_topics()` stability improvements. Critical for manual curation and comparison features.
- **Plotly 6.7.0** (add explicitly) — BERTopic's hierarchical visualization uses Plotly under the hood; explicit inclusion ensures compatibility and enables custom interactive visualizations. Already a transitive dependency but needs explicit version pinning.

**What NOT to add:**
- ❌ **streamlit-aggrid** — 40MB+ overhead, complex API, version conflicts with pandas/Streamlit. Built-in `st.dataframe()` now supports selection and column config.
- ❌ **Redis/SQLite for state** — v2.0 scope excludes session persistence. Built-in `st.session_state` is sufficient for single-user local tool.
- ❌ **Dash/Flask backend** — Streamlit already provides web server. Adding separate backend duplicates functionality and increases complexity.

### Expected Features

The v2.0 feature set extends the existing upload + filter prototype (steps 1-2) to a complete 8-step workflow. Features are categorized into **table stakes** (users expect in any topic modeling tool), **differentiators** (v2.0-specific value), and **anti-features** (explicitly out of scope).

**Must have (table stakes):**
- Data upload with preview (already implemented)
- Publication type filtering (already implemented)
- Input column selection (already implemented)
- Model parameter configuration (UMAP, HDBSCAN, vectorizer settings)
- Progress indicators for long-running operations
- Topic list view with labels and sizes
- Document-to-topic assignment view
- Model and results export (CSV/XLSX/pickle)

**Should have (differentiators):**
- **Checkpoint-based comparison system** — Automatically save model state (config + trained model + metadata) at each step; compare current state against any saved checkpoint in 2-column view; navigate backward/forward with checkpoint save prompts
- **Outlier reduction via parameter comparison** — Adjust UMAP/HDBSCAN parameters and compare current results against any saved checkpoint to minimize outliers through informed parameter tuning
- **Topic labeling comparison** — Adjust verbosity and compare current labels against any saved checkpoint for optimal label length selection
- **Sidebar step navigation** — Jump to any workflow step with sidebar showing progress checkmarks and current step highlighting
- **Manual topic merge/remove with impact preview** — Show "before merge" vs "after merge" topic structure without re-training
- **Quality check: papers with no topics** — Explicit QC step after manual curation prevents orphaning documents
- **Hierarchical topic tree visualization** — Interactive Plotly dendrogram showing topic relationships

**Defer (v2+):**
- LLM-based topic naming (external API dependency, cost)
- Embedding model comparison (multiplies training time exponentially)
- Historical session replay (persistent storage complexity)
- Integration with v1.0 static site (explicitly deferred per PROJECT.md)

### Architecture Approach

The architecture is a **step-wizard pattern with session state** managing 8 sequential workflow steps, built as an extension of the existing `src/DIPT research topics-hierarchical TM.py` prototype. The system uses **aggressive caching** to prevent re-computation of expensive ML operations (embeddings take 30-120 sec, model training 2-5 min).

**Major components:**

1. **Sidebar Step Navigation** — Persistent sidebar showing all 8 workflow steps with checkmarks for completed steps and highlighting current step. Allows jumping to any step; prompts to save checkpoint when navigating backward.

2. **Checkpoint Storage System** — Stores model state snapshots {timestamp, config_dict, model_object, metadata} at key decision points. Auto-saves when proceeding forward; prompts when going backward. Enables comparison of current state against any saved checkpoint.

3. **Multi-Step Workflow Controller** — Orchestrates 8 workflow steps (Upload → Filter → Configure → Train → Visualize → Compare → Curate → Export) with validation gates and session state management. Uses existing `st.session_state.step` pattern, extended from 2 steps to 8.

4. **Cached ML Pipeline** — Wraps expensive operations in `@st.cache_resource` (sentence transformers, trained topic models) and `@st.cache_data` (embeddings, hierarchical topic computation). Critical for performance — prevents 30-120 sec waits on every parameter change. Embeddings cached globally and reused across all checkpoints.

5. **Checkpoint-Based Comparison Views** — Uses `st.columns(2)` to compare "Current" state vs "Selected Checkpoint" with dropdown to choose any saved checkpoint. Displays full config and metrics side-by-side for outlier reduction and topic labeling decisions.

6. **Manual Topic Curation Interface** — Checkboxes for topic removal, multiselect for merging, with impact preview before applying changes. Computes "papers that will lose all topics" count to prevent accidental orphaning.

7. **Hierarchical Visualization Engine** — Caches Plotly dendrogram generation (`topic_model.visualize_hierarchy()`) and stores serialized HTML rather than figure objects to prevent memory leaks (figures are 10-50 MB each).

8. **Export Generation** — Creates 5 artifact types: topic info CSV, papers-with-topics CSV, themed paper sets (grouped by manual topic themes), hierarchical visualization HTML, trained model pickle.

**Key architectural patterns:**
- **Sidebar Step Navigation** — Always-visible sidebar with all steps, checkmarks for completion, click to jump to any step
- **Checkpoint System with Auto-Save** — Store model snapshots (config + model + metadata) automatically on forward navigation; prompt on backward navigation
- **Checkpoint-Based Comparison** — 2-column view comparing Current vs Selected Checkpoint (dropdown to choose any saved checkpoint)
- **Step-Wizard with Session State** — Linear workflow with clear prerequisites and validation gates; state persists across reruns naturally
- **Cached ML Pipeline Components** — Expensive operations wrapped in `@st.cache_resource`/`@st.cache_data` with proper cache key strategies; embeddings cached globally and reused
- **Incremental Refinement with Preview** — Show impact of changes before committing (e.g., topic removal preview)

### Critical Pitfalls

Research identified 8 critical pitfalls with prevention strategies tied to specific implementation phases:

1. **Session State Rerun Race Conditions** — Streamlit reruns entire script on every interaction; incomplete state during long computations leads to KeyError exceptions and partial results. **Prevention:** Use `st.spinner` for long operations, disable widgets during computation (`disabled=True`), guard all session state access with existence checks, store results only after completion.

2. **Memory Explosion from Uncached Embeddings** — Generating embeddings for 1000+ documents takes 30-120 sec and consumes 2-10 GB RAM; without caching, every parameter adjustment regenerates from scratch. **Prevention:** Pre-compute and cache embeddings separately with `@st.cache_data`, pass pre-computed embeddings to BERTopic, use `batch_size` for large datasets.

3. **Outlier Removal Destroys Document-Topic Mapping** — Removing outlier topic -1 and noise topics leaves papers with no remaining assignments; 10-30% of papers silently vanish from exports. **Prevention:** Track paper-topic coverage before removal, show quality check UI ("N papers will have no topics"), provide remediation options (adjust HDBSCAN parameters, review at-risk papers).

4. **Comparison State Leakage Between Parameter Variations** — Side-by-side comparison shows identical results in both columns; session state keys (`model_left`, `model_right`) not scoped to comparison context; BERTopic models are mutable and both keys may reference same object. **Prevention:** Use namespaced session state keys (`comparison_{id}_left`), create deep copies of models, store parameters alongside results for verification.

5. **Plotly Visualization Memory Leak on Rerun** — After 10-20 parameter adjustments, session memory grows to 2-3 GB; hierarchical topic visualizations (10-50 MB Plotly figures) aren't garbage collected. **Prevention:** Cache visualization generation, return serialized HTML not figure objects, use `st.empty()` containers and replace content, set `max_entries` on visualization caches.

6. **BERTopic Model Mutation Corrupts Cached State** — `st.cache_resource` returns same object instance across sessions; BERTopic methods like `merge_topics()` mutate model in place, corrupting cached singleton. **Prevention:** Use `@st.cache_data` for topic models (creates copy on return), or deep copy before mutation if using `@st.cache_resource`.

7. **UMAP/HDBSCAN Parameter Coupling Creates Confusing Results** — Users adjust UMAP `n_components` expecting more topics but get fewer topics and more outliers; parameters are interdependent but UI presents as independent sliders. **Prevention:** Show parameter guidance explaining relationships, provide presets (Conservative/Balanced/Granular), show real-time preview metrics (topic count, outlier %), validate parameter combinations.

8. **Sentence-Level Topics Don't Aggregate to Paper-Level Semantics** — Topic model assigns each sentence independently; single paper split across 3+ topics; themed CSV exports contain duplicate papers. **Prevention:** Define primary aggregation strategy (most frequent topic, highest probability, or multi-label), show aggregation preview before export, provide filtering options for themed CSVs.

## Implications for Roadmap

Based on research, suggested phase structure follows the natural workflow progression from data ingestion through export, with careful attention to caching/performance in early phases to avoid rework.

### Phase 1: Data Upload & Filtering (Foundation)
**Rationale:** Extends existing prototype (steps 1-2 already implemented); establishes session state patterns and caching discipline that all later phases depend on. Must establish state management patterns correctly to avoid Pitfall #1 (session state race conditions).

**Delivers:** Complete data upload + preview + filtering + column selection workflow with proper session state initialization and DataFrame caching.

**Addresses:**
- Table stakes: Data upload with preview, publication type filtering, input column selection
- Architecture: Session state initialization (all keys for 8 steps), cached DataFrame loading

**Avoids:**
- Pitfall #1 (session state race conditions) — Establish session state guards and validation patterns
- Performance trap: Reading uploaded CSV/XLSX on every rerun — Cache DataFrame immediately after upload

**Research flags:** Low complexity; standard Streamlit patterns with existing prototype as foundation. No additional research needed.

### Phase 2: Model Configuration & Training (Core ML Pipeline)
**Rationale:** Most complex phase technically; establishes caching patterns for embeddings and model training that determine app performance. Must get caching right to avoid Pitfall #2 (memory explosion) and performance collapse.

**Delivers:** Parameter configuration UI (UMAP, HDBSCAN, vectorizer), cached embedding generation, cached model training, progress indicators, basic topic list view.

**Uses:**
- Streamlit 1.57.0 (parameter forms, progress indicators)
- BERTopic 0.17.4 (model training pipeline)
- sentence-transformers (embedding generation with caching)

**Implements:**
- Architecture: Cached ML Pipeline (embeddings + model training)
- Architecture: Model Configuration Panel with parameter collection

**Avoids:**
- Pitfall #2 (memory explosion from uncached embeddings) — Cache embeddings separately with `@st.cache_data`
- Pitfall #7 (UMAP/HDBSCAN parameter coupling) — Add parameter guidance, presets, validation
- Performance trap: Generating embeddings on every parameter change — Pre-compute and pass to BERTopic

**Research flags:** Medium complexity; well-documented BERTopic and Streamlit caching patterns, but caching strategy is critical to get right. No additional research needed if following established patterns from STACK.md and ARCHITECTURE.md.

### Phase 3: Basic Visualization (Validation Feedback)
**Rationale:** Users need to see initial topic model results before refinement; hierarchical visualization helps understand cluster structure and identify merge candidates. Must address Pitfall #5 (Plotly memory leak) early to avoid 20+ reruns consuming 2-3 GB.

**Delivers:** Hierarchical topic tree visualization (Plotly dendrogram), topic info table with size and terms, document-topic assignment view.

**Uses:**
- Plotly 6.7.0 (interactive dendrogram via BERTopic's `visualize_hierarchy()`)
- Streamlit 1.57.0 (`st.plotly_chart`, `st.dataframe` with enhanced features)

**Implements:**
- Architecture: Hierarchical Visualization Engine with caching

**Avoids:**
- Pitfall #5 (Plotly visualization memory leak) — Cache visualization HTML, use `st.empty()` containers
- Performance trap: Regenerating hierarchical visualizations on every rerun — Cache with `@st.cache_data(ttl=3600)`

**Research flags:** Low complexity; BERTopic's `visualize_hierarchy()` is built-in, just needs proper caching. No additional research needed.

### Phase 4: Outlier Reduction Comparison (First Decision Point)
**Rationale:** BERTopic creates -1 outliers by default; minimizing outliers through parameter tuning is first major refinement decision. Side-by-side comparison of 2-3 UMAP/HDBSCAN parameter configurations demonstrates v2.0's core value proposition. Must establish comparison state isolation patterns for Phases 5 and 7.

**Delivers:** Side-by-side comparison view for 2-3 parameter configurations (e.g., Conservative/Balanced/Granular presets or custom UMAP/HDBSCAN values) with metrics (outlier count, total topics, avg topic size, sample labels), configuration selection UI.

**Addresses:**
- Differentiator: Side-by-side outlier reduction comparison via parameter tuning
- Table stakes: Outlier minimization workflow

**Implements:**
- Architecture: Side-by-Side Comparison Views (using `st.columns(2)` or `st.columns(3)`)

**Avoids:**
- Pitfall #2 (memory explosion from uncached embeddings) — Reuse cached embeddings across parameter variations to minimize retraining overhead
- Pitfall #4 (comparison state leakage) — Use namespaced session state keys, deep copy models
- Pitfall #7 (UMAP/HDBSCAN parameter coupling) — Provide presets with rationale, explain parameter relationships

**Research flags:** Medium-HIGH complexity; requires retraining models with different parameters (more expensive than post-training outlier reduction), comparison state isolation requires careful session state management, embeddings must be cached and reused. Pattern established here reused in Phases 5 and 7.

### Phase 5: Topic Labeling Comparison (Second Decision Point)
**Rationale:** KeyBERT `nr_words` parameter affects topic interpretability; side-by-side comparison of 3-5-7 word labels lets users choose optimal verbosity. Simpler than Phase 4 (same model, different representation) but reuses comparison patterns.

**Delivers:** Side-by-side comparison view for 2-3 `nr_words` settings (e.g., 5, 7, 10 words), label preview in split columns, selection UI.

**Addresses:**
- Differentiator: Side-by-side topic labeling comparison
- Table stakes: Topic label configuration

**Implements:**
- Architecture: Side-by-Side Comparison Views (reuses Phase 4 patterns)

**Avoids:**
- Pitfall #4 (comparison state leakage) — Reuse namespaced session state patterns from Phase 4
- Pitfall #6 (model mutation corrupts cache) — Representation changes mutate model; use `@st.cache_data` or deep copy

**Research flags:** Low complexity; simpler than Phase 4, reuses comparison patterns. No additional research needed.

### Phase 6: Manual Topic Curation (User Control)
**Rationale:** Users need ability to merge similar topics and remove noise topics; manual curation completes the iterative refinement workflow before quality check. Must provide impact preview to avoid Pitfall #3.

**Delivers:** Topic curation UI (checkboxes for removal, multiselect for merging), impact preview ("before merge" vs "after merge" topic structure), removal impact calculation (papers that will lose all topics).

**Addresses:**
- Differentiator: Manual topic merge/remove with impact preview
- Table stakes: Manual curation workflow

**Implements:**
- Architecture: Manual Topic Curation Interface
- Architecture: Incremental Refinement with Preview pattern

**Avoids:**
- Pitfall #3 (outlier removal destroys document-topic mapping) — Compute and show papers at risk before allowing removal
- Pitfall #6 (model mutation corrupts cache) — `merge_topics()` and topic removal mutate model; deep copy before mutation

**Research flags:** Medium complexity; BERTopic's `merge_topics()` and `reduce_topics()` are documented, but impact preview calculation requires custom logic for paper-topic coverage analysis.

### Phase 7: Quality Check & Aggregation (Data Integrity)
**Rationale:** After manual curation, some papers may be orphaned (assigned topic was removed); explicit QC step prevents accidentally leaving documents unclassified. Also addresses Pitfall #8 (sentence-level topics don't aggregate to paper-level).

**Delivers:** Quality check view showing papers with no remaining topics, paper-level topic aggregation strategy (most frequent topic, highest probability, or multi-label), aggregation preview with paper-topic distribution.

**Addresses:**
- Differentiator: Quality check for papers with no topics
- Feature requirement: Paper-level topic aggregation for themed exports

**Implements:**
- Architecture: Quality check display with warnings

**Avoids:**
- Pitfall #3 (outlier removal destroys document-topic mapping) — Show affected papers, provide remediation options
- Pitfall #8 (sentence-level topics don't aggregate) — Define and apply primary aggregation strategy before export

**Research flags:** Low complexity; quality check is straightforward filtering, aggregation strategy is pandas groupby logic. No additional research needed.

### Phase 8: Export Generation (Deliverables)
**Rationale:** Users need to export results for downstream analysis (synthesis generation, publication); multiple export formats support different workflows. Final phase produces all artifacts for handoff.

**Delivers:** Export generation (topic info CSV, papers-with-topics CSV, themed paper sets, hierarchical visualization HTML, trained model pickle), download buttons for individual files, export success feedback with file listing.

**Addresses:**
- Table stakes: Model export, results export (CSV/XLSX)
- Feature requirement: Themed paper sets for synthesis generation

**Implements:**
- Architecture: Export Generation component

**Avoids:**
- Pitfall #8 (sentence-level topics don't aggregate) — Apply aggregation strategy from Phase 7 to themed CSV exports
- Performance trap: Rendering 1000-row DataFrames — Provide download buttons instead of inline display

**Research flags:** Low complexity; pandas CSV export and pickle serialization are standard. BERTopic's `save()` method handles model serialization. No additional research needed.

### Phase Ordering Rationale

- **Early caching establishment (Phase 1-2):** Session state and ML caching patterns must be correct from the start; rework after Phase 3+ is expensive due to state dependencies
- **Validation feedback before refinement (Phase 3 before 4-6):** Users need to see initial topic model results (visualization, topic list) before making refinement decisions
- **Comparison patterns reused (Phase 4 → Phase 5):** Outlier reduction comparison (Phase 4) establishes state isolation and UI patterns reused in labeling comparison (Phase 5) and curation (Phase 6)
- **Quality check before export (Phase 7 before 8):** Paper-level aggregation and orphan detection must happen before CSV generation to prevent data integrity issues in exports
- **Pitfall prevention sequenced with phases:** Each phase addresses specific pitfalls discovered in research (e.g., Phase 2 addresses caching, Phase 4 addresses comparison state, Phase 7 addresses aggregation)

### Research Flags

**Phases likely needing deeper research during planning:**
- **Phase 2 (Model Configuration & Training):** Caching strategy is critical and nuanced; review BERTopic + Streamlit caching best practices, test with 1000+ document dataset to validate performance assumptions. Guidance provided in STACK.md and PITFALLS.md should be sufficient, but validate caching approach early.
- **Phase 6 (Manual Topic Curation):** Impact preview calculation requires custom logic for paper-topic coverage analysis; BERTopic doesn't provide this directly. May need research on efficient graph/set operations for large datasets.

**Phases with standard patterns (skip research-phase):**
- **Phase 1 (Data Upload & Filtering):** Existing prototype provides foundation; standard Streamlit file upload and DataFrame filtering patterns
- **Phase 3 (Basic Visualization):** BERTopic's `visualize_hierarchy()` is built-in; Streamlit's Plotly integration is well-documented
- **Phase 5 (Topic Labeling Comparison):** Reuses comparison patterns from Phase 4; BERTopic's representation configuration is straightforward
- **Phase 7 (Quality Check):** Standard pandas filtering and groupby operations
- **Phase 8 (Export Generation):** Standard CSV export and pickle serialization

## Confidence Assessment

| Area | Confidence | Notes |
|------|------------|-------|
| Stack | HIGH | Recommended versions verified on PyPI (Streamlit 1.57.0 released 2026-04-28, BERTopic 0.17.4 released 2025-12-03, Plotly 6.7.0 released 2026-04-09). All compatible with Python 3.12. Existing stack (BERTopic + Streamlit + UMAP/HDBSCAN) already validated in codebase. |
| Features | MEDIUM-HIGH | Core features (upload, train, export) and comparison features (outlier reduction, labeling) well-documented in BERTopic and Streamlit. Side-by-side UI pattern is project-specific interpretation (not explicitly documented in tools). Manual curation and impact preview are custom implementations. |
| Architecture | HIGH | Step-wizard pattern with session state is established Streamlit best practice. Caching patterns (`@st.cache_resource` vs `@st.cache_data`) documented in official Streamlit docs. BERTopic integration patterns verified in existing notebook (`experiments/BTH research topics.ipynb`). |
| Pitfalls | HIGH | Based on official Streamlit session state and caching documentation, BERTopic GitHub repository guidance, HDBSCAN and UMAP parameter selection guides, and analysis of existing codebase patterns (`src/DIPT research topics-hierarchical TM.py`). Real-world session state race conditions and memory leak patterns well-documented in Streamlit community. |

**Overall confidence:** HIGH

### Gaps to Address

**Caching performance validation:** Research provides specific caching strategies (`@st.cache_resource` for models, `@st.cache_data` for embeddings) but these should be validated with real datasets (1000+ documents) early in Phase 2. Memory usage monitoring recommended during development to catch performance traps before they become architectural rework.

**Paper-level aggregation strategy:** Research identifies the problem (sentence-level topics don't aggregate cleanly to paper-level) and suggests strategies (most frequent topic, highest probability, multi-label), but optimal approach may depend on downstream synthesis workflow. Consider deferring final decision to Phase 7 after seeing real topic model results; implement all three strategies and let users choose.

**Comparison checkpoint system (deferred to v2.1):** Research identifies value (save/restore model states at decision points) but notes HIGH implementation complexity due to state management. If users request during v2.0 validation, this will need deeper research into state serialization and UI for checkpoint navigation.

**Embedding model selection (deferred to v3+):** Research explicitly defers embedding model comparison (multiplies training time, UI complexity) but uses default (all-MiniLM-L6-v2 or all-mpnet-base-v2). If domain-specific embeddings become necessary (e.g., biomedical research papers), this will need research into sentence-transformer alternatives and performance tradeoffs.

## Sources

### Primary (HIGH confidence)
- **Streamlit 1.57.0** — PyPI (https://pypi.org/project/streamlit/1.57.0/) — Released 2026-04-28 (VERIFIED)
- **BERTopic 0.17.4** — PyPI (https://pypi.org/project/bertopic/0.17.4/) — Released 2025-12-03 (VERIFIED)
- **Plotly 6.7.0** — PyPI (https://pypi.org/project/plotly/6.7.0/) — Released 2026-04-09 (VERIFIED)
- **Streamlit Documentation** — Context7 (/streamlit/streamlit) — Session state management, caching patterns, layout components, Plotly integration
- **BERTopic Documentation** — Context7 (/maartengr/bertopic) — Hierarchical topics, outlier reduction strategies, topic representation configuration, visualization methods
- **BERTopic Official Docs** — https://maartengr.github.io/BERTopic/ — Comprehensive API and visualization patterns
- **BERTopic Outlier Reduction** — https://maartengr.github.io/BERTopic/getting_started/outlier_reduction/outlier_reduction.html — c-TF-IDF, distributions, embeddings, probabilities strategies
- **BERTopic Topic Reduction** — https://maartengr.github.io/BERTopic/getting_started/topicreduction/topicreduction.html — Manual merge, automatic reduction, post-training reduction
- **Streamlit Session State Docs** — https://docs.streamlit.io/develop/concepts/architecture/session-state — Official guidance on persistence and limitations
- **Streamlit Caching Docs** — https://docs.streamlit.io/develop/concepts/architecture/caching — `st.cache_data` vs `st.cache_resource`, mutation issues, memory management

### Secondary (MEDIUM confidence)
- **Project context** — `.planning/PROJECT.md` — v2.0 milestone goals, constraints, explicitly deferred features (integration with v1.0 static site)
- **Existing codebase** — `src/DIPT research topics-hierarchical TM.py` — Current implementation (steps 1-2), session state patterns, state key naming
- **Reference notebook** — `experiments/BTH research topics.ipynb` — Complete iterative refinement process demonstrating target workflow
- **HDBSCAN Parameter Guide** — https://github.com/scikit-learn-contrib/hdbscan/blob/master/docs/parameter_selection.rst — min_cluster_size and min_samples tuning
- **UMAP Parameter Guide** — https://umap-learn.readthedocs.io — n_neighbors, min_dist, n_components interdependencies

### Domain expertise (inferred patterns)
- Interactive ML app patterns — Caching expensive operations, state management, comparison UI isolation
- Streamlit rerun model implications — Race conditions, widget state management, memory leaks
- Topic modeling workflow — Sentence vs document granularity, outlier handling, parameter interdependencies

---

*Research completed: 2026-04-29*  
*Ready for roadmap: yes*
