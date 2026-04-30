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

- [x] **Phase 06: Data Upload & Filtering** - Establish data ingestion and session state foundation
- [ ] **Phase 07: Checkpoint Infrastructure** - Build persistent checkpoint save/load system with dataset fingerprinting
- [ ] **Phase 08: Model Configuration & Training** - Implement cached ML pipeline with parameter configuration and checkpoint integration
- [ ] **Phase 09: Basic Visualization** - Add hierarchical topic tree and results display
- [ ] **Phase 10: Outlier Reduction Comparison** - First decision point comparing current vs any saved checkpoint
- [ ] **Phase 11: Topic Labeling Comparison** - Second decision point comparing current vs any saved checkpoint
- [ ] **Phase 12: Manual Topic Curation** - Enable topic merge/remove with impact preview
- [ ] **Phase 13: Quality Check & Aggregation** - Validate paper-topic coverage and aggregation strategy
- [ ] **Phase 14: Export Generation** - Generate all output artifacts for downstream use

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
  5. System computes and stores dataset fingerprint (hash of filtered DataFrame) for checkpoint validation in later phases
**Plans**: 2 plans

Plans:
- [x] 06-01-PLAN.md — Enhanced upload with caching and fingerprinting
- [x] 06-02-PLAN.md — Enhanced filtering with real-time feedback and validation

**Pitfall Prevention**: Session state race conditions (guard all state access, disable widgets during load)

### Phase 07: Checkpoint Infrastructure
**Goal**: Establish persistent checkpoint save/load system that enables resuming work across sessions and reproducing analyses months/years later with exact parameter sets
**Depends on**: Phase 06
**Requirements**: TM-03
**Success Criteria** (what must be TRUE):
  1. System saves checkpoint to filesystem at data/checkpoints/{timestamp}_{dataset_name}/ with config.json, metadata.json, model.pkl, embeddings.npy, dataset_fingerprint.txt
  2. User can load existing checkpoint from sidebar dropdown on app startup showing checkpoint name, date, topic count, outlier percentage
  3. User can see list of all saved checkpoints with metadata in checkpoint management UI
  4. System validates checkpoint integrity on load (checks for missing files, corrupted pickle, file size anomalies)
  5. System blocks loading checkpoint if dataset fingerprint doesn't match current uploaded data and shows clear error message
  6. User can extract and clone parameters from any saved checkpoint to apply to current dataset
  7. User can delete old checkpoints via management UI to free disk space
  8. User can export checkpoint as zip file for backup or sharing
  9. System creates sidebar navigation showing all 9 workflow steps with checkmarks for completed steps and highlighting current step
**Plans**: 2 plans

Plans:
- [ ] 07-01-PLAN.md — Checkpoint manager module with save/load/validate/fingerprint
- [ ] 07-02-PLAN.md — Streamlit checkpoint management UI and 9-step navigation

**UI hint**: yes
**Pitfall Prevention**: Checkpoint corruption (validate pickle integrity, check file sizes), disk space exhaustion (show total checkpoint disk usage, provide bulk delete), dataset mismatch (fingerprint comparison with clear error messages)

### Phase 08: Model Configuration & Training
**Goal**: Users can configure topic model parameters, train models with cached embeddings, and create the first checkpoint, establishing both ML caching patterns and the checkpoint system that enable iterative refinement
**Depends on**: Phase 06
**Requirements**: TM-03
**Success Criteria** (what must be TRUE):
  1. User can navigate between workflow steps via sidebar showing all 8 steps with checkmarks for completed steps and highlighting current step
  2. User can configure UMAP parameters (n_neighbors, n_components, min_dist) with guidance explaining parameter relationships
  3. User can configure HDBSCAN parameters (min_cluster_size, min_samples) with preset options (Conservative/Balanced/Granular)
  4. User can configure vectorizer settings (n-gram range, min_df, max_df) for topic representation
  5. System generates and caches embeddings separately to prevent 30-120 sec regeneration on parameter changes
  6. User sees progress indicators for long-running operations (embedding generation, model training)
  7. User sees basic topic list view with topic IDs, labels, and document counts after successful training
  8. System creates first checkpoint (timestamp, config, model object, metadata) automatically when user proceeds to next step
  9. User is prompted to save checkpoint when navigating backward to earlier steps
**Plans**: TBD
**UI hint**: yes
**Pitfall Prevention**: Memory explosion from uncached embeddings (cache with @st.cache_data), UMAP/HDBSCAN parameter coupling confusion (add guidance and presets), checkpoint serialization size (use pickle protocol 5 for large models)

### Phase 08: Model Configuration & Training
**Goal**: Users can configure topic model parameters, train models with cached embeddings, and save checkpoints to persistent storage, establishing the ML caching patterns and checkpoint integration that enable iterative refinement
**Depends on**: Phase 07
**Requirements**: TM-04
**Success Criteria** (what must be TRUE):
  1. User can configure UMAP parameters (n_neighbors, n_components, min_dist) with guidance explaining parameter relationships
  2. User can configure HDBSCAN parameters (min_cluster_size, min_samples) with preset options (Conservative/Balanced/Granular)
  3. User can configure vectorizer settings (n-gram range, min_df, max_df) for topic representation
  4. System generates and caches embeddings separately to prevent 30-120 sec regeneration on parameter changes
  5. User sees progress indicators for long-running operations (embedding generation, model training)
  6. User sees basic topic list view with topic IDs, labels, and document counts after successful training
  7. System creates persistent checkpoint (config.json, model.pkl, embeddings.npy, metadata.json, dataset_fingerprint.txt) automatically when user proceeds to next step
  8. Checkpoint includes all trained model state and embeddings for fast reload across sessions
  9. User is prompted to save checkpoint when navigating backward to earlier steps
**Plans**: TBD
**UI hint**: yes
**Pitfall Prevention**: Memory explosion from uncached embeddings (cache with @st.cache_data), UMAP/HDBSCAN parameter coupling confusion (add guidance and presets), checkpoint serialization size (monitor pickle protocol 5 overhead, typical checkpoint 50-500 MB), embeddings storage (include in checkpoint for fast reload)

### Phase 09: Basic Visualization
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
**Goal**: Users can adjust UMAP/HDBSCAN parameters to minimize outliers and compare current results against any previously saved checkpoint, demonstrating v2.0's core value proposition of checkpoint-based iterative refinement
**Depends on**: Phase 08
**Requirements**: TM-04
**Success Criteria** (what must be TRUE):
  1. User can adjust UMAP/HDBSCAN parameters and retrain model (reusing cached embeddings)
  2. User can select any previous checkpoint from dropdown (showing timestamp, topic count, outlier %) for comparison
  3. User sees side-by-side comparison (2 columns) showing "Current" vs "Selected Checkpoint" with metrics: outlier count, total topics, average topic size, sample topic labels
  4. User sees full parameter configuration displayed for both Current and Selected Checkpoint
  5. System creates new checkpoint automatically when user proceeds to next step
  6. System prompts user to save checkpoint when navigating backward to earlier steps
**Plans**: TBD
**UI hint**: yes
**Pitfall Prevention**: Retraining overhead (reuse embeddings across parameter variations, show progress clearly), comparison state leakage (ensure checkpoint is deep copy of model), parameter coupling confusion (provide presets with rationale), checkpoint memory usage (monitor pickle size for large models)

### Phase 09: Basic Visualization
**Goal**: Users can visualize initial topic model results with hierarchical structure and topic-document assignments, providing validation feedback before refinement
**Depends on**: Phase 08
**Requirements**: TM-09
**Success Criteria** (what must be TRUE):
  1. User can view an interactive hierarchical topic dendrogram showing topic relationships and clustering structure
  2. User can see a topic info table displaying topic ID, representative terms, document count, and hierarchy level
  3. User can view document-topic assignments showing which papers are assigned to each topic
  4. System caches visualization generation to prevent memory leaks from 10-50 MB Plotly figures
**Plans**: TBD
**UI hint**: yes
**Pitfall Prevention**: Plotly visualization memory leak (cache HTML not figure objects, use st.empty() containers)

### Phase 10: Outlier Reduction Comparison
**Goal**: Users can adjust UMAP/HDBSCAN parameters to minimize outliers and compare current results against any previously saved checkpoint (from current session or disk), demonstrating v2.0's core value proposition of checkpoint-based iterative refinement
**Depends on**: Phase 09
**Requirements**: TM-05
**Success Criteria** (what must be TRUE):
  1. User can adjust UMAP/HDBSCAN parameters and retrain model (reusing cached embeddings)
  2. User can select any checkpoint from dropdown including both current session checkpoints and saved checkpoints loaded from disk
  3. System shows checkpoint metadata (timestamp, dataset name, topic count, outlier %) for each available checkpoint
  4. User sees side-by-side comparison (2 columns) showing "Current" vs "Selected Checkpoint" with metrics: outlier count, total topics, average topic size, sample topic labels
  5. User sees full parameter configuration displayed for both Current and Selected Checkpoint
  6. System creates new persistent checkpoint automatically when user proceeds to next step
  7. System prompts user to save checkpoint when navigating backward to earlier steps
**Plans**: TBD
**UI hint**: yes
**Pitfall Prevention**: Retraining overhead (reuse embeddings across parameter variations, show progress clearly), comparison state leakage (ensure checkpoint is deep copy of model), parameter coupling confusion (provide presets with rationale), checkpoint memory usage (monitor pickle size for large models), dataset mismatch (validate fingerprint before allowing comparison)

### Phase 11: Topic Labeling Comparison
**Goal**: Users can adjust topic labeling verbosity and compare current labels against any previously saved checkpoint (from current session or disk), reusing the checkpoint-based comparison patterns established in Phase 10
**Depends on**: Phase 10
**Requirements**: TM-06
**Success Criteria** (what must be TRUE):
  1. User can adjust nr_words settings (e.g., 5, 7, 10 words) and update topic representation
  2. User can select any checkpoint from dropdown including both current session checkpoints and saved checkpoints loaded from disk
  3. User sees side-by-side comparison (2 columns) showing "Current" vs "Selected Checkpoint" topic labels at different verbosity levels
  4. User sees full labeling configuration displayed for both Current and Selected Checkpoint
  5. System prevents model mutation from corrupting cached state during representation updates
  6. System creates new persistent checkpoint automatically when user proceeds to next step
  7. System prompts user to save checkpoint when navigating backward to earlier steps
**Plans**: TBD
**UI hint**: yes
**Pitfall Prevention**: Model mutation corrupts cache (deep copy before representation update), comparison state leakage (reuse Phase 10 checkpoint patterns), checkpoint versioning (ensure representation changes are captured in checkpoint metadata), dataset mismatch (validate fingerprint before allowing comparison)

### Phase 12: Manual Topic Curation
**Goal**: Users can manually merge similar topics and remove noise topics with impact preview, completing the iterative refinement workflow before quality validation
**Depends on**: Phase 11
**Requirements**: TM-07
**Success Criteria** (what must be TRUE):
  1. User can select topics for removal via checkboxes with real-time count of affected documents
  2. User can select multiple topics for merging via multiselect with before/after topic structure preview
  3. User sees impact preview showing which papers will lose all topics before confirming removal
  4. System applies merge/remove operations only after user confirmation, preserving pre-curation state for comparison
  5. System creates new persistent checkpoint automatically after manual curation operations are applied
  6. System prompts user to save checkpoint when navigating backward to earlier steps
**Plans**: TBD
**UI hint**: yes
**Pitfall Prevention**: Outlier removal destroys document-topic mapping (compute and show at-risk papers), model mutation corrupts cache (deep copy before merge_topics/reduce_topics), checkpoint captures curation state (store merged/removed topic IDs in metadata)

### Phase 13: Quality Check & Aggregation
**Goal**: Users can validate paper-topic coverage after curation and select aggregation strategy for paper-level topic assignment, preventing orphaned documents and sentence-level aggregation issues
**Depends on**: Phase 12
**Requirements**: TM-08
**Success Criteria** (what must be TRUE):
  1. User sees quality check view listing papers with no remaining topics after curation
  2. User can select paper-level aggregation strategy (most frequent topic, highest probability, or multi-label)
  3. User sees aggregation preview showing distribution of papers across topics with selected strategy
  4. System provides remediation options for orphaned papers (adjust HDBSCAN parameters, review at-risk papers)
**Plans**: TBD
**UI hint**: yes
**Pitfall Prevention**: Outlier removal destroys document-topic mapping (explicit QC step with remediation), sentence-level topics don't aggregate to paper-level (define and preview aggregation strategy)

### Phase 14: Export Generation
**Goal**: Users can export all topic model results and artifacts for downstream synthesis workflows, producing the deliverables for handoff
**Depends on**: Phase 13
**Requirements**: TM-10
**Success Criteria** (what must be TRUE):
  1. User can export topic info as CSV (topic ID, labels, sizes, hierarchy levels)
  2. User can export papers-with-topics as CSV with selected aggregation strategy applied
  3. User can export themed paper sets grouped by manually-assigned topic themes
  4. User can export hierarchical visualization as standalone HTML file
  5. User can export trained topic model as pickle file for programmatic reuse
  6. User sees download buttons for each artifact type and export success feedback with file listing
**Plans**: TBD
**Pitfall Prevention**: Sentence-level topics don't aggregate (apply Phase 13 aggregation strategy to themed CSVs), rendering 1000-row DataFrames (provide download buttons, not inline display)

## Progress

| Phase | Milestone | Plans Complete | Status | Completed |
|-------|-----------|----------------|--------|-----------|
| 01. Core Publication | v1.0 | Complete | Complete | 2026-04-03 |
| 02. Reading Quality | v1.0 | Complete | Complete | 2026-04-04 |
| 03. Analytics Baseline | v1.0 | Complete | Complete | 2026-04-05 |
| 04. GDPR Compliance | v1.0 | Complete | Complete | 2026-04-08 |
| 05. UI Polish | v1.0 | 3/3 | Complete | 2026-04-10 |
| 06. Data Upload & Filtering | v2.0 | 2/2 | Complete | 2026-05-01 |
| 07. Checkpoint Infrastructure | v2.0 | 0/2 | Planned | - |
| 08. Model Configuration & Training | v2.0 | 0/TBD | Not started | - |
| 09. Basic Visualization | v2.0 | 0/TBD | Not started | - |
| 10. Outlier Reduction Comparison | v2.0 | 0/TBD | Not started | - |
| 11. Topic Labeling Comparison | v2.0 | 0/TBD | Not started | - |
| 12. Manual Topic Curation | v2.0 | 0/TBD | Not started | - |
| 13. Quality Check & Aggregation | v2.0 | 0/TBD | Not started | - |
| 14. Export Generation | v2.0 | 0/TBD | Not started | - |

---
*Roadmap created: 2026-04-03*
*v2.0 milestone added: 2026-04-29*
