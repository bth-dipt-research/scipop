# Feature Research: Interactive Topic Modeling UI

**Domain:** Interactive topic modeling interfaces for research publication analysis  
**Researched:** 2026-04-29  
**Confidence:** MEDIUM-HIGH

## Context

This research focuses on the **v2.0 Interactive Topic Modeling UI** milestone — a standalone tool for iterative topic model refinement. This is NOT about integrating with the v1.0 static website. The v2.0 tool mirrors the notebook workflow (`experiments/BTH research topics.ipynb`) but adds side-by-side parameter comparisons at key decision points.

**Existing foundation:**
- Partial Streamlit prototype with upload + filtering (`src/DIPT research topics-hierarchical TM.py`)
- Complete notebook workflow demonstrating manual iterative refinement
- BERTopic + UMAP + HDBSCAN + KeyBERT representation pipeline

## Feature Landscape

### Table Stakes (Users Expect These)

Features users assume exist in topic modeling tools. Missing these = tool feels incomplete.

| Feature | Why Expected | Complexity | Dependencies |
|---------|--------------|------------|--------------|
| **Data upload with preview** | Standard first step in all data tools; users need to verify correct file loaded | LOW | File uploader widget, pandas dataframe display |
| **Publication type filtering** | Research datasets contain mixed document types (journals, conferences, books); users expect to filter by type | LOW | Multiselect widget, dataframe filtering |
| **Input column selection** | Users need control over which fields (Title, Abstract, Keywords) feed the model | LOW | Multiselect widget with smart defaults |
| **Progress indicator** | Long-running model training needs status feedback to prevent abandonment | LOW | Streamlit progress bar, spinner, or status widget |
| **Model parameter configuration** | Topic modeling inherently requires parameter tuning; users expect access to UMAP, HDBSCAN, vectorizer settings | MEDIUM | Form/expander with numeric inputs, sliders, text fields organized by sub-model |
| **Topic list view with labels** | Core output; users expect to browse all discovered topics with representative terms | LOW | Table/dataframe display of topic number, label, size, top terms |
| **Topic size distribution** | Users need to assess if topic granularity is reasonable (too many tiny topics vs too few giant ones) | LOW | Bar chart or histogram showing topic document counts |
| **Document-to-topic assignment view** | Users need to verify that documents are assigned to sensible topics | MEDIUM | Dataframe with document ID/title, assigned topic, and confidence/probability |
| **Model export** | Users need to save trained models for reuse or sharing | LOW | Download button for serialized model (pickle or safetensors) |
| **Results export (CSV/XLSX)** | Users expect to export topic assignments and metadata for downstream analysis | LOW | Download button for CSV/XLSX of documents with topic labels |

### Differentiators (v2.0-Specific Features)

Features that set this tool apart and align with the project's unique value proposition.

| Feature | Value Proposition | Complexity | Notes |
|---------|-------------------|------------|-------|
| **Side-by-side outlier reduction comparison** | BERTopic creates -1 outliers; comparing different UMAP/HDBSCAN parameter configurations (e.g., min_cluster_size, n_components) side-by-side helps users minimize outliers through informed parameter tuning without trial-and-error retraining | MEDIUM-HIGH | Train 2-3 models with different parameter sets (reusing cached embeddings), display outlier counts, total topics, avg topic size, and sample labels for comparison |
| **Side-by-side topic labeling comparison** | KeyBERT `nr_words` parameter affects topic interpretability; showing 3-5 word labels vs 7-10 word labels side-by-side lets users choose optimal verbosity | LOW-MEDIUM | Generate representations with different `nr_words` values, display in split columns with same topics |
| **Manual topic merge/remove with impact preview** | Users need to combine similar topics or remove noise topics; showing "before merge" vs "after merge" topic sizes and labels reduces uncertainty | MEDIUM | UI for selecting topics to merge/remove, instant preview of resulting topic structure without re-training |
| **Quality check: papers with no topics** | After manual curation (removing topics), some papers may end up orphaned; explicit QC step prevents accidentally leaving documents unclassified | LOW | Filter and display documents where assigned topic was removed, with option to reassign or flag |
| **Hierarchical topic tree visualization** | BERTopic's `.hierarchical_topics()` shows topic relationships; interactive tree helps users understand cluster structure and decide merge candidates | MEDIUM | BERTopic built-in visualization (`.visualize_hierarchy()`), embed in Streamlit with Plotly |
| **Comparison checkpoint system** | Allow users to "pin" a configuration at each decision point (outlier reduction, labeling, curation) and compare against alternatives before committing | HIGH | Session state management with multiple model snapshots, UI for switching between checkpoints |
| **Parameter presets by domain** | Research publication analysis has known "good starting points"; presets reduce initial configuration burden | LOW | Dropdown with preset configurations (e.g., "General Research", "Conference Papers", "Abstracts Only") |

### Anti-Features (Explicitly Out of Scope)

Features that seem valuable but conflict with v2.0 goals or add disproportionate complexity.

| Anti-Feature | Why Tempting | Why Avoid | Alternative |
|--------------|--------------|-----------|-------------|
| **Real-time collaborative editing** | Modern tools often support multi-user sessions | Adds server state, websockets, conflict resolution; v2.0 is single-user local tool | Users export/import models to share; defer to v3+ if validated |
| **Automated topic naming with LLMs** | GPT-4 can generate human-friendly topic names | External API dependency, cost, rate limits, non-determinism complicate iteration | Use KeyBERT/c-TF-IDF labels in v2.0; add LLM naming as optional v2.x feature |
| **Historical session replay** | Viewing past parameter choices and results | Persistent storage, database, replay engine add complexity before core workflow is validated | Export models at key checkpoints; user manages versions locally |
| **Embedding model comparison** | Comparing sentence-transformers, USE, Flair, etc. | Multiplies training time, UI complexity, and comparison dimensions exponentially | Fix one high-quality default (e.g., all-MiniLM-L6-v2); defer to v2.x if users request |
| **Dynamic parameter optimization** | Auto-tuning UMAP/HDBSCAN parameters via grid search | Long training times, unclear when "optimal" is reached, removes user control over tradeoffs | Provide presets + manual tuning; keep human-in-loop |
| **Topic evolution over time (dynamic modeling)** | Tracking how topics change over publication years | Requires timestamp data, adds temporal dimension to UI, different use case | Keep v2.0 focused on static corpus analysis; dynamic modeling is separate milestone |
| **Integration with v1.0 static site** | Publishing syntheses from topic models | Deferred per PROJECT.md; v2.0 validates topic modeling workflow before automation | Export CSVs for manual synthesis authoring; connect in v3+ |

## Feature Dependencies

```
[Data Upload] 
    └──requires──> [Preview Dataset]
    └──requires──> [Filter by Publication Type]
    └──requires──> [Select Input Columns]
                        └──requires──> [Configure Model Parameters]
                                            └──requires──> [Train Model]
                                                                └──requires──> [Topic List View]
                                                                └──optional──> [Outlier Reduction Comparison]
                                                                                    └──requires──> [Updated Topic Assignments]

[Train Model]
    └──produces──> [Base Topic Model]
                        └──enables──> [Topic Labeling Comparison]
                        └──enables──> [Hierarchical Visualization]
                        └──enables──> [Manual Curation]
                                            └──requires──> [Impact Preview]
                                            └──triggers──> [Quality Check (Orphaned Papers)]

[Manual Curation]
    └──modifies──> [Topic Assignments]
                        └──requires──> [Re-export Functionality]
                        └──optional──> [Comparison Checkpoint]

[All Steps]
    └──require──> [Progress Indicators]
    └──produce──> [Exportable Artifacts (model, CSVs)]
```

### Dependency Notes

- **Sequential core flow:** Upload → Filter → Configure → Train → Refine → Export is strictly ordered; users cannot skip steps
- **Comparison features are post-training:** Side-by-side comparisons (outlier reduction, labeling) require a trained base model
- **Manual curation affects downstream quality:** Topic merge/remove operations must trigger re-calculation of document assignments and quality checks
- **Checkpoints enable non-linear exploration:** Users may want to return to "after outlier reduction" state to try different labeling; checkpoint system prevents re-training

## MVP Definition (v2.0 Launch)

### Must-Have for Launch

Minimum features to replicate and improve upon the notebook workflow.

- [x] **Upload & Preview** — CSV/XLSX upload with dataframe preview (already in prototype)
- [x] **Filter Publications** — Multiselect by publication type (already in prototype)
- [x] **Select Input Columns** — Choose Title, Abstract, Keywords columns (already in prototype)
- [ ] **Configure Model Parameters** — Collapsible sections for UMAP (n_neighbors, n_components, min_dist), HDBSCAN (min_cluster_size, min_samples), Vectorizer (stop_words, ngram_range), Representation (nr_repr_docs)
- [ ] **Train Model** — Run BERTopic pipeline with progress indicator
- [ ] **Topic List View** — Display all topics with ID, label, size, top 10 terms
- [ ] **Side-by-Side Outlier Reduction** — Compare 2-3 strategies (c-TF-IDF, distributions, embeddings) with metrics (outlier count before/after, sample reassignments)
- [ ] **Side-by-Side Topic Labeling** — Compare 2-3 `nr_words` settings (e.g., 5, 7, 10) in split view
- [ ] **Manual Topic Curation** — Select topics to merge or remove with checkboxes/multiselect
- [ ] **Impact Preview** — Show resulting topic structure after merge/remove without committing
- [ ] **Quality Check** — Display papers orphaned by topic removal with option to review
- [ ] **Hierarchical Visualization** — Embed BERTopic's `.visualize_hierarchy()` plot
- [ ] **Export Model** — Download trained model (pickle or safetensors)
- [ ] **Export Results** — Download CSV with document IDs, topics, labels, probabilities

### Defer to v2.1 (Post-Launch Iteration)

Features that add value but aren't critical for initial validation.

- [ ] **Comparison checkpoint system** — Save/restore model states at decision points
- [ ] **Parameter presets** — Dropdown with domain-specific starting configurations
- [ ] **Document-level topic drill-down** — Click topic to see all assigned documents
- [ ] **Topic similarity heatmap** — BERTopic's `.visualize_heatmap()` for exploring topic relationships
- [ ] **2D topic scatter plot** — BERTopic's `.visualize_topics()` for spatial overview
- [ ] **Custom topic labels** — Allow users to rename topics from default c-TF-IDF labels
- [ ] **Advanced export options** — HTML reports, topic-document matrices, embeddings

### Future Consideration (v3+)

Features that depend on validated use cases or external dependencies.

- [ ] **LLM-based topic naming** — Optional GPT-4/Claude integration for human-friendly labels
- [ ] **Embedding model comparison** — Side-by-side training with different sentence transformers
- [ ] **Guided topic modeling** — Seed word injection for semi-supervised topic discovery
- [ ] **Integration with v1.0 site** — Export topic models as inputs to synthesis generation
- [ ] **Session history and replay** — Browse past configurations and results

## Workflow-Specific Patterns

### Comparison View Pattern

**What:** Display 2-4 parameter variations side-by-side for direct comparison.

**When to use:**
- Outlier reduction strategies (different algorithms)
- Topic labeling configurations (different nr_words values)
- Manual curation previews (before/after merge/remove)

**Design principles:**
- Equal visual weight for each variant (split columns)
- Consistent metrics across variants (outlier %, topic count, sample outputs)
- Clear labeling of which variant is which (strategy name, parameter values)
- Single "Select" button per variant to commit choice

**Implementation notes:**
- Use `st.columns()` for side-by-side layout
- Cache computations with `@st.cache_data` to avoid re-running on page rerun
- Store selected variant in `st.session_state` for downstream steps

### Impact Preview Pattern

**What:** Show consequences of an action before committing (e.g., merging topics, removing topics).

**When to use:**
- Manual topic merge (show resulting topic size, new label)
- Manual topic removal (show orphaned document count)
- Outlier reduction strategy selection (show topic assignment changes)

**Design principles:**
- Visual diff: "Current State" vs "After Action"
- Quantitative metrics (e.g., "23 documents will be reassigned")
- Qualitative samples (e.g., show 5 example documents affected)
- Clear "Commit" vs "Cancel" actions

**Implementation notes:**
- Use expander or tabs for before/after views
- Compute preview without mutating model state
- Only update model and assignments on explicit user confirmation

### Progressive Disclosure Pattern

**What:** Hide advanced configuration behind collapsible sections; show essentials by default.

**When to use:**
- Model parameter configuration (UMAP, HDBSCAN, Vectorizer)
- Advanced export options
- Quality check details (orphaned papers list)

**Design principles:**
- Sensible defaults for collapsed sections
- Clear labels for what's hidden ("Advanced UMAP Settings")
- No required actions inside collapsed sections (users can proceed with defaults)

**Implementation notes:**
- Use `st.expander()` for collapsible sections
- Use `st.sidebar` for global settings (e.g., random seed, verbose logging)
- Set `expanded=False` for advanced options, `expanded=True` for critical choices

## Interactive Behaviors Expected by Users

Based on BERTopic documentation and standard data science tool patterns:

1. **Immediate feedback on data filtering** — When user selects publication types, dataset preview and count update instantly
2. **Parameter validation before training** — Disable "Train Model" button if required fields are empty or invalid (e.g., min_cluster_size < 2)
3. **Non-blocking progress updates** — During long operations (training, outlier reduction), show spinner + estimated time or step-by-step progress
4. **Undo/reset at each stage** — Users should be able to return to previous step without losing uploaded data (session state preservation)
5. **Hover tooltips on parameters** — UMAP/HDBSCAN parameters are technical; brief explanations on hover reduce friction
6. **Export availability at any point** — After training, users should be able to export model and results without completing all refinement steps
7. **Visual confirmation of selections** — Checkboxes/multiselect for topic curation show currently selected topics clearly
8. **Responsive to accidental actions** — Confirmation dialog for destructive actions (e.g., "Remove 5 topics? This will orphan 47 documents.")

## Complexity Assessment

| Feature | Implementation Complexity | User Complexity | Priority |
|---------|---------------------------|-----------------|----------|
| Data upload & preview | LOW | LOW | P0 (MVP) |
| Publication type filtering | LOW | LOW | P0 (MVP) |
| Input column selection | LOW | LOW | P0 (MVP) |
| Model parameter configuration | MEDIUM (UI organization) | MEDIUM (parameter understanding) | P0 (MVP) |
| Train model with progress | MEDIUM (async handling) | LOW | P0 (MVP) |
| Topic list view | LOW | LOW | P0 (MVP) |
| Side-by-side outlier reduction | MEDIUM (parallel computation + UI) | MEDIUM (strategy understanding) | P0 (MVP) |
| Side-by-side topic labeling | LOW (same model, different repr) | LOW | P0 (MVP) |
| Manual topic curation | MEDIUM (selection + merge logic) | MEDIUM (understanding impact) | P0 (MVP) |
| Impact preview | MEDIUM (preview computation) | LOW | P0 (MVP) |
| Quality check (orphaned papers) | LOW (filter + display) | LOW | P0 (MVP) |
| Hierarchical visualization | LOW (use BERTopic built-in) | MEDIUM (interpreting dendrogram) | P0 (MVP) |
| Export model & results | LOW | LOW | P0 (MVP) |
| Comparison checkpoints | HIGH (state management) | MEDIUM | P1 (v2.1) |
| Parameter presets | LOW | LOW | P1 (v2.1) |
| Document drill-down | MEDIUM (interactive table + filtering) | LOW | P1 (v2.1) |
| Topic similarity heatmap | LOW (use BERTopic built-in) | MEDIUM | P1 (v2.1) |
| 2D topic scatter plot | LOW (use BERTopic built-in) | MEDIUM | P1 (v2.1) |
| Custom topic labels | LOW (text input + mapping) | LOW | P1 (v2.1) |
| LLM topic naming | HIGH (API integration + cost) | LOW | P2 (v3+) |
| Embedding model comparison | HIGH (training time + UI) | HIGH | P2 (v3+) |

**Priority key:**
- P0 (MVP): Must-have for v2.0 launch
- P1 (v2.1): High-value enhancements for post-launch iteration
- P2 (v3+): Future consideration pending validation

## Sources

### Official Documentation (HIGH Confidence)

- BERTopic documentation — https://maartengr.github.io/BERTopic/ (comprehensive API and visualization patterns)
- BERTopic outlier reduction strategies — https://maartengr.github.io/BERTopic/getting_started/outlier_reduction/outlier_reduction.html (c-TF-IDF, distributions, embeddings, probabilities)
- BERTopic topic reduction — https://maartengr.github.io/BERTopic/getting_started/topicreduction/topicreduction.html (manual merge, automatic reduction, post-training reduction)
- BERTopic visualizations — https://maartengr.github.io/BERTopic/getting_started/visualization/visualize_topics.html (hierarchy, heatmap, topics, documents)
- Streamlit widgets documentation — https://docs.streamlit.io/develop/api-reference/widgets (file uploader, multiselect, sliders, buttons, expanders)

### Codebase Context (HIGH Confidence)

- Existing Streamlit prototype — `src/DIPT research topics-hierarchical TM.py` (upload, filter, column selection implemented)
- Reference notebook workflow — `experiments/BTH research topics.ipynb` (demonstrates iterative refinement process)
- Project requirements — `.planning/PROJECT.md` (v2.0 milestone goals and constraints)

### Domain Knowledge (MEDIUM Confidence)

- Interactive topic modeling patterns inferred from BERTopic's API design (side-by-side comparisons not explicitly documented but implied by multiple strategy support)
- Research publication dataset conventions (Web of Science/Scopus format with publication types, titles, abstracts)
- Standard data science tool UX patterns (progress indicators, parameter validation, export functionality)

## Confidence Assessment

| Area | Confidence | Reason |
|------|------------|--------|
| Core features (upload, train, export) | HIGH | Well-documented in BERTopic and Streamlit; already partially implemented |
| Comparison features (outlier reduction, labeling) | MEDIUM-HIGH | BERTopic supports strategies but side-by-side UI pattern is project-specific interpretation |
| Manual curation (merge/remove) | HIGH | BERTopic `.merge_topics()` and `.reduce_topics()` explicitly documented |
| Hierarchical visualization | HIGH | BERTopic `.visualize_hierarchy()` is built-in |
| Impact preview pattern | MEDIUM | Not explicitly documented in tools; inferred from iterative workflow needs |
| Comparison checkpoints | MEDIUM | Complex state management; pattern adapted from Streamlit session state best practices |

## Open Questions

1. **Outlier reduction strategy defaults:** Should the tool pre-select a "recommended" strategy (e.g., c-TF-IDF first, then distributions for remainder) or force users to choose?
2. **Topic labeling word counts:** What nr_words values should be compared? Notebook uses 10; could compare 5, 7, 10 or 3, 5, 7 depending on user preference.
3. **Manual curation scope:** Should users be able to split topics (assign subset of documents to new topic) or only merge/remove?
4. **Quality check action:** When papers are orphaned, should tool auto-reassign to nearest topic, flag for manual review, or offer both options?
5. **Hierarchical viz interactivity:** BERTopic's `.visualize_hierarchy()` is Plotly-based; should we add custom controls (e.g., expand/collapse subtrees) or use as-is?

---

*Feature research for: Interactive topic modeling UI (v2.0 scipop milestone)*  
*Researched: 2026-04-29*  
*Downstream consumer: Phase planning (roadmap generation)*
