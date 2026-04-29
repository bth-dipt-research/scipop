# Roadmap: Static scipop

## Overview

This roadmap delivers scipop in two major milestones: v1.0 established the public static publication website (phases 01-05), and v2.0 builds an interactive topic modeling tool that transforms the iterative notebook workflow into a guided UI with side-by-side parameter comparisons at key decision points (phases 06-13).

## Milestones

- ✅ **v1.0 MVP Publication** - Phases 01-05 (shipped 2026-04-10)
- 🚧 **v2.0 Interactive Topic Modeling** - Phases 06-13 (in progress)

## Phases

**Phase Numbering:**
- Integer phases (1, 2, 3): Planned milestone work
- Decimal phases (2.1, 2.2): Urgent insertions (marked with INSERTED)

Decimal phases appear between their surrounding integers in numeric order.

<details>
<summary>✅ v1.0 MVP Publication (Phases 01-05) - SHIPPED 2026-04-10</summary>

### Phase 01: Core Publication
**Goal**: Establish the static site foundation with homepage and synthesis detail pages
**Requirements**: PUBL-01, PUBL-02, PUBL-03, PUBL-04
**Plans**: Complete

### Phase 02: Reading Quality
**Goal**: Ensure cross-device readability and synthesis disclaimers
**Requirements**: PUBL-05, PUBL-06
**Plans**: Complete

### Phase 03: Analytics Baseline
**Goal**: Add basic Google Analytics pageview tracking
**Requirements**: ANLT-01
**Plans**: Complete

### Phase 04: GDPR Compliance
**Goal**: Gate analytics behind explicit consent with persistent privacy controls
**Requirements**: PRIV-01, PRIV-02, PRIV-03
**Plans**: Complete

### Phase 05: UI Polish
**Goal**: Polish public site reading/navigation presentation while preserving accessibility, privacy, and analytics behavior
**Requirements**: UIP-01, UIP-02, UIP-03
**Plans**: 3 plans complete

</details>

### 🚧 v2.0 Interactive Topic Modeling (In Progress)

**Milestone Goal:** Build an interactive web UI that guides users through iterative topic model refinement with side-by-side parameter comparisons at key decision points, transforming the notebook workflow into a guided step-by-step tool.

- [ ] **Phase 06: Data Upload & Filtering** - Establish data ingestion and session state foundation
- [ ] **Phase 07: Model Configuration & Training** - Implement cached ML pipeline with parameter configuration
- [ ] **Phase 08: Basic Visualization** - Add hierarchical topic tree and results display
- [ ] **Phase 09: Outlier Reduction Comparison** - First decision point with side-by-side strategy comparison
- [ ] **Phase 10: Topic Labeling Comparison** - Second decision point for label verbosity selection
- [ ] **Phase 11: Manual Topic Curation** - Enable topic merge/remove with impact preview
- [ ] **Phase 12: Quality Check & Aggregation** - Validate paper-topic coverage and aggregation strategy
- [ ] **Phase 13: Export Generation** - Generate all output artifacts for downstream use

## Phase Details

### Phase 06: Data Upload & Filtering
**Goal**: Users can upload publication datasets and filter them for topic modeling input, establishing the session state patterns and caching discipline that all later phases depend on
**Depends on**: Phase 05 (v1.0 complete)
**Requirements**: TM-01, TM-02
**Success Criteria** (what must be TRUE):
  1. User can upload CSV or XLSX publication data and see an immediate preview of contents
  2. User can filter publications by type (article, conference paper, review, etc.) with real-time row count feedback
  3. User can select which columns to use for topic modeling (title, abstract, keywords) via checkboxes
  4. System caches the uploaded DataFrame to prevent re-reading on every interaction
**Plans**: TBD
**Pitfall Prevention**: Session state race conditions (guard all state access, disable widgets during load)

### Phase 07: Model Configuration & Training
**Goal**: Users can configure topic model parameters and train models with cached embeddings and progress indicators, establishing the ML caching patterns that determine overall app performance
**Depends on**: Phase 06
**Requirements**: TM-03
**Success Criteria** (what must be TRUE):
  1. User can configure UMAP parameters (n_neighbors, n_components, min_dist) with guidance explaining parameter relationships
  2. User can configure HDBSCAN parameters (min_cluster_size, min_samples) with preset options (Conservative/Balanced/Granular)
  3. User can configure vectorizer settings (n-gram range, min_df, max_df) for topic representation
  4. System generates and caches embeddings separately to prevent 30-120 sec regeneration on parameter changes
  5. User sees progress indicators for long-running operations (embedding generation, model training)
  6. User sees basic topic list view with topic IDs, labels, and document counts after successful training
**Plans**: TBD
**UI hint**: yes
**Pitfall Prevention**: Memory explosion from uncached embeddings (cache with @st.cache_data), UMAP/HDBSCAN parameter coupling confusion (add guidance and presets)

### Phase 08: Basic Visualization
**Goal**: Users can visualize initial topic model results with hierarchical structure and topic-document assignments, providing validation feedback before refinement
**Depends on**: Phase 07
**Requirements**: TM-08
**Success Criteria** (what must be TRUE):
  1. User can view an interactive hierarchical topic dendrogram showing topic relationships and clustering structure
  2. User can see a topic info table displaying topic ID, representative terms, document count, and hierarchy level
  3. User can view document-topic assignments showing which papers are assigned to each topic
  4. System caches visualization generation to prevent memory leaks from 10-50 MB Plotly figures
**Plans**: TBD
**UI hint**: yes
**Pitfall Prevention**: Plotly visualization memory leak (cache HTML not figure objects, use st.empty() containers)

### Phase 09: Outlier Reduction Comparison
**Goal**: Users can compare 2-3 UMAP/HDBSCAN parameter configurations side-by-side to minimize outliers through retraining, demonstrating v2.0's core value proposition and establishing comparison patterns for later phases
**Depends on**: Phase 08
**Requirements**: TM-04
**Success Criteria** (what must be TRUE):
  1. User can configure 2-3 alternative parameter sets targeting different outlier/granularity tradeoffs (e.g., Conservative/Balanced/Granular presets or custom UMAP/HDBSCAN values)
  2. System trains models in parallel or sequentially with each parameter configuration, reusing cached embeddings to minimize overhead
  3. User sees side-by-side comparison showing outlier count, total topics, average topic size, and sample topic labels for each configuration
  4. User can select the preferred parameter configuration and replace the working model with the chosen variant
  5. System isolates comparison state to prevent model objects leaking between left/right/center columns
**Plans**: TBD
**UI hint**: yes
**Pitfall Prevention**: Retraining overhead (reuse embeddings across parameter variations, show progress clearly), comparison state leakage (use namespaced session keys, deep copy models), parameter coupling confusion (provide presets with rationale)

### Phase 10: Topic Labeling Comparison
**Goal**: Users can compare 2-3 topic labeling configurations side-by-side and select optimal label verbosity, reusing the comparison patterns established in Phase 09
**Depends on**: Phase 09
**Requirements**: TM-05
**Success Criteria** (what must be TRUE):
  1. User can trigger side-by-side comparison of nr_words settings (e.g., 5 words, 7 words, 10 words)
  2. User sees topic labels at different verbosity levels displayed in split columns for direct comparison
  3. User can select the preferred labeling configuration and apply it to update topic representation
  4. System prevents model mutation from corrupting cached state during representation updates
**Plans**: TBD
**UI hint**: yes
**Pitfall Prevention**: Model mutation corrupts cache (use @st.cache_data or deep copy before mutation), comparison state leakage (reuse Phase 09 patterns)

### Phase 11: Manual Topic Curation
**Goal**: Users can manually merge similar topics and remove noise topics with impact preview, completing the iterative refinement workflow before quality validation
**Depends on**: Phase 10
**Requirements**: TM-06
**Success Criteria** (what must be TRUE):
  1. User can select topics for removal via checkboxes with real-time count of affected documents
  2. User can select multiple topics for merging via multiselect with before/after topic structure preview
  3. User sees impact preview showing which papers will lose all topics before confirming removal
  4. System applies merge/remove operations only after user confirmation, preserving pre-curation state for comparison
**Plans**: TBD
**UI hint**: yes
**Pitfall Prevention**: Outlier removal destroys document-topic mapping (compute and show at-risk papers), model mutation corrupts cache (deep copy before merge_topics/reduce_topics)

### Phase 12: Quality Check & Aggregation
**Goal**: Users can validate paper-topic coverage after curation and select aggregation strategy for paper-level topic assignment, preventing orphaned documents and sentence-level aggregation issues
**Depends on**: Phase 11
**Requirements**: TM-07
**Success Criteria** (what must be TRUE):
  1. User sees quality check view listing papers with no remaining topics after curation
  2. User can select paper-level aggregation strategy (most frequent topic, highest probability, or multi-label)
  3. User sees aggregation preview showing distribution of papers across topics with selected strategy
  4. System provides remediation options for orphaned papers (adjust HDBSCAN parameters, review at-risk papers)
**Plans**: TBD
**UI hint**: yes
**Pitfall Prevention**: Outlier removal destroys document-topic mapping (explicit QC step with remediation), sentence-level topics don't aggregate to paper-level (define and preview aggregation strategy)

### Phase 13: Export Generation
**Goal**: Users can export all topic model results and artifacts for downstream synthesis workflows, producing the deliverables for handoff
**Depends on**: Phase 12
**Requirements**: TM-09
**Success Criteria** (what must be TRUE):
  1. User can export topic info as CSV (topic ID, labels, sizes, hierarchy levels)
  2. User can export papers-with-topics as CSV with selected aggregation strategy applied
  3. User can export themed paper sets grouped by manually-assigned topic themes
  4. User can export hierarchical visualization as standalone HTML file
  5. User can export trained topic model as pickle file for programmatic reuse
  6. User sees download buttons for each artifact type and export success feedback with file listing
**Plans**: TBD
**Pitfall Prevention**: Sentence-level topics don't aggregate (apply Phase 12 aggregation strategy to themed CSVs), rendering 1000-row DataFrames (provide download buttons, not inline display)

## Progress

| Phase | Milestone | Plans Complete | Status | Completed |
|-------|-----------|----------------|--------|-----------|
| 01. Core Publication | v1.0 | Complete | Complete | 2026-04-03 |
| 02. Reading Quality | v1.0 | Complete | Complete | 2026-04-04 |
| 03. Analytics Baseline | v1.0 | Complete | Complete | 2026-04-05 |
| 04. GDPR Compliance | v1.0 | Complete | Complete | 2026-04-08 |
| 05. UI Polish | v1.0 | 3/3 | Complete | 2026-04-10 |
| 06. Data Upload & Filtering | v2.0 | 0/TBD | Not started | - |
| 07. Model Configuration & Training | v2.0 | 0/TBD | Not started | - |
| 08. Basic Visualization | v2.0 | 0/TBD | Not started | - |
| 09. Outlier Reduction Comparison | v2.0 | 0/TBD | Not started | - |
| 10. Topic Labeling Comparison | v2.0 | 0/TBD | Not started | - |
| 11. Manual Topic Curation | v2.0 | 0/TBD | Not started | - |
| 12. Quality Check & Aggregation | v2.0 | 0/TBD | Not started | - |
| 13. Export Generation | v2.0 | 0/TBD | Not started | - |

---
*Roadmap created: 2026-04-03*
*v2.0 milestone added: 2026-04-29*
