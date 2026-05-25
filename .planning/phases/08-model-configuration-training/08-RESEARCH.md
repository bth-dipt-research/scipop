# Phase 08: Model Configuration & Training - Research

**Researched:** 2026-05-25
**Domain:** Topic modeling with BERTopic, UMAP, HDBSCAN, and Streamlit caching
**Confidence:** HIGH

## Summary

Phase 08 implements parameter configuration UI and cached model training for BERTopic topic modeling. The phase builds directly on Phase 07's checkpoint infrastructure (save/load/validate patterns already implemented) and Phase 06's session state patterns (DataFrame caching, navigation, fingerprinting). The core challenge is caching embeddings separately from model training to prevent 30-120 second regeneration on every parameter change, plus integrating checkpoint auto-save with the navigation guard system.

**Primary recommendation:** Use `@st.cache_data` with dataset fingerprint as cache key for embedding generation, disable all UI inputs during long operations via `st.session_state.training_in_progress` flag, and trigger checkpoint save only on "Proceed to Next Step" (not on every parameter change).

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions

**Parameter Configuration UI Layout:**
- D-01: Use single scrolling form with all parameters visible at once with section headings (no expand/collapse or tabs).
- D-02: Use default `st.slider()` behavior for all numeric parameters (sliders have built-in drag + type input box).
- D-03: Use `st.divider()` horizontal lines between sections (UMAP / HDBSCAN / Vectorizer) for clear visual breaks.
- D-04: Pre-fill parameter defaults from loaded checkpoint if available (from Phase 07 checkpoint config); otherwise use hard-coded sensible defaults.

**Parameter Guidance & Presets:**
- D-05: Provide single expandable Parameter Guide (▶ Need help? Click for parameter explanations) - available but not intrusive.
- D-06: Position Parameter Guide at bottom, after all parameters - doesn't interfere with parameter access.
- D-07: No preset buttons (Conservative/Balanced/Granular) - users adjust every parameter individually for full manual control. **NOTE:** This diverges from roadmap mention of preset options, but user preference for full manual control is clear.
- D-08: Parameter Guide content includes both parameter reference (definitions, typical ranges) and workflow-oriented tips (common tuning scenarios like "for more granular topics, decrease min_cluster_size and n_neighbors").

**Progress Indication:**
- D-09: Show spinner with elapsed time display for embedding generation (updates in real-time: "Elapsed: 45s") - runs 30-120 seconds but only once, then cached.
- D-10: Show spinner with elapsed time for model training - consistent feedback style with embedding generation (runs 10-60 seconds, repeats on parameter changes).
- D-11: Show brief success message for cache hit: `st.success('✓ Using cached embeddings')` when embeddings already cached.
- D-12: Disable all inputs during long operations (embedding generation, model training) - prevents state corruption from UI interactions during processing.

**Checkpoint Creation Timing:**
- D-13: Auto-save checkpoint on "Proceed to Next Step" button click - checkpoint created when user advances to visualization step.
- D-14: Block navigation and show error if checkpoint save fails - user must resolve checkpoint save issue (disk space, permissions, etc.) before continuing.
- D-15: Auto-save only on Proceed - no manual "Save Checkpoint Now" button (simpler UI).
- D-16: Use timestamp + dataset name for checkpoint naming: `{timestamp}_{dataset_name}` (e.g., `20260525_203045_publications_2024`) - matches Phase 07 pattern.

**Navigation Guard:**
- D-17: Always confirm backward navigation with "Are you sure? Parameter changes will be lost." even if no model trained yet - consistent confirmation pattern.
- D-18: Prompt to save checkpoint after training when navigating backward: show three options `[Save & Go Back] [Go Back Without Saving] [Cancel]` - matches roadmap language.
- D-19: Always prompt on backward navigation - no session memory of user choice (prioritizes safety over convenience).
- D-20: Show navigation guard prompt in sidebar near 9-step navigation where click originated - keeps context close to the action.

### the agent's Discretion
- Exact hard-coded default values for UMAP/HDBSCAN/vectorizer parameters (as long as they reflect typical ranges from notebook workflow).
- Exact wording of parameter explanations in the Parameter Guide (as long as they cover parameter definitions and workflow tips).
- Exact implementation of elapsed time display (as long as it updates in real-time during operations).
- Exact UI state management for disabling inputs during operations (as long as all inputs are disabled during embedding/training).
- Exact error messages for checkpoint save failures (as long as they're clear and actionable).

### Deferred Ideas (OUT OF SCOPE)
None — discussion stayed within phase scope.
</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| TM-04 | User can configure and run topic model with adjustable parameters (UMAP, HDBSCAN, vectorizer, embedding) with cached embeddings and checkpoint integration | Standard Stack (BERTopic, UMAP, HDBSCAN), Architecture Patterns (cached embedding generation, checkpoint save integration), Code Examples (parameter initialization from checkpoint config) |
</phase_requirements>

## Architectural Responsibility Map

| Capability | Primary Tier | Secondary Tier | Rationale |
|------------|-------------|----------------|-----------|
| Parameter UI configuration | Browser / Client | — | Streamlit widgets render in browser; user interaction is client-side |
| Embedding generation | Frontend Server (SSR) | — | CPU/GPU-bound operation runs in Streamlit server process, not client browser |
| Model training | Frontend Server (SSR) | — | BERTopic fit_transform executes in Streamlit server process with 10-60 sec runtime |
| Checkpoint save/load | Frontend Server (SSR) | Database / Storage | Streamlit orchestrates save/load; filesystem/pickle handles persistence |
| Navigation guard logic | Frontend Server (SSR) | Browser / Client | Guard decision logic in Streamlit; prompt rendering happens client-side |

## Standard Stack

### Core
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| BERTopic | 0.16.4 | Topic modeling orchestration | Industry standard for transformer-based topic modeling, bundles UMAP/HDBSCAN/vectorizer configuration [VERIFIED: requirements.txt line 3] |
| umap-learn | 0.5.7 | Dimensionality reduction | Standard UMAP implementation, used by BERTopic for embedding projection [VERIFIED: requirements.txt line 9] |
| hdbscan | 0.8.40 | Clustering | Standard hierarchical density-based clustering, used by BERTopic for topic assignment [VERIFIED: requirements.txt line 8] |
| scikit-learn | 1.6.1 | CountVectorizer for term extraction | Standard ML library, provides TF-IDF and count vectorization [VERIFIED: requirements.txt line 11] |
| sentence-transformers | 3.3.1 | Embedding generation | Standard library for semantic embeddings, uses "all-MiniLM-L6-v2" model [VERIFIED: requirements.txt line 12] |
| Streamlit | 1.50.0 | Web UI framework | Already established in Phase 06-07 [VERIFIED: requirements.txt line 1] |
| NumPy | 2.2.2 | Array operations for embeddings | Standard numerical computing, used for embedding persistence [VERIFIED: requirements.txt line 6] |

**Installation:**
All dependencies already installed via `requirements.txt`.

**Version verification:** All versions verified against current requirements.txt file in repository (2026-05-25).

## Architecture Patterns

### System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                        Streamlit UI                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │ UMAP Params  │  │ HDBSCAN      │  │ Vectorizer   │          │
│  │ (sliders)    │  │ Params       │  │ Params       │          │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘          │
│         │                 │                 │                   │
│         └─────────────────┼─────────────────┘                   │
│                           ▼                                     │
│                 ┌────────────────────┐                          │
│                 │  Train Model BTN   │                          │
│                 └─────────┬──────────┘                          │
└───────────────────────────┼─────────────────────────────────────┘
                            ▼
                ┌──────────────────────┐
                │ Cached Embedding Gen │
                │  (30-120 sec, once)  │
                └──────────┬───────────┘
                           ▼
                ┌──────────────────────┐
                │  BERTopic Training   │
                │   (10-60 sec, per    │
                │   parameter change)  │
                └──────────┬───────────┘
                           ▼
                ┌──────────────────────┐
                │  Display Results     │
                │  (topic list view)   │
                └──────────┬───────────┘
                           ▼
                ┌──────────────────────┐
                │ "Proceed" BTN Click  │
                └──────────┬───────────┘
                           ▼
                ┌──────────────────────┐
                │  Checkpoint Save     │
                │  (config, model,     │
                │   embeddings, meta)  │
                └──────────────────────┘
```

### Recommended Project Structure
```
src/
├── checkpoint_manager.py    # Already exists (Phase 07)
├── DIPT research topics-hierarchical TM.py    # Main Streamlit app
```

### Pattern 1: Cached Embedding Generation

**What:** Generate embeddings once per dataset fingerprint, cache with `@st.cache_data` to prevent 30-120 sec regeneration on parameter changes.

**When to use:** Embedding generation is expensive (sentence-transformers encode) but dataset-dependent only — parameter changes don't require regeneration.

**Example:**
```python
# Source: Phase 06 patterns + Streamlit caching docs
@st.cache_data
def generate_embeddings(input_texts: list, dataset_fingerprint: str):
    """
    Generate embeddings with caching by dataset fingerprint.
    
    Args:
        input_texts: List of text strings to embed
        dataset_fingerprint: SHA-256 fingerprint from Phase 06
        
    Returns:
        np.ndarray of embeddings
    """
    sentence_model = SentenceTransformer("all-MiniLM-L6-v2")
    embeddings = sentence_model.encode(input_texts, show_progress_bar=False)
    return embeddings

# Usage in training flow:
embeddings = generate_embeddings(
    st.session_state.df_filtered['input'].tolist(),
    st.session_state.dataset_fingerprint
)
```

**Why fingerprint in cache key:** Dataset changes (filter adjustments, different upload) must invalidate cache. Fingerprint ensures cache miss when dataset changes.

### Pattern 2: UI State Management During Long Operations

**What:** Disable all interactive widgets during embedding generation and model training to prevent state corruption from user interactions mid-operation.

**When to use:** Any operation taking >5 seconds that modifies `st.session_state` (embedding generation, model training, checkpoint save).

**Example:**
```python
# Set flag before operation
if 'training_in_progress' not in st.session_state:
    st.session_state.training_in_progress = False

# Disable all inputs during operation
n_neighbors = st.slider(
    "n_neighbors", 
    min_value=5, 
    max_value=50, 
    value=15,
    disabled=st.session_state.training_in_progress
)

# Run operation with flag set
if st.button("Train Model", disabled=st.session_state.training_in_progress):
    st.session_state.training_in_progress = True
    st.rerun()  # Rerun to apply disabled state

if st.session_state.training_in_progress:
    with st.spinner("Training model..."):
        # Long operation
        trained_model = fit_model(...)
        st.session_state.trained_model = trained_model
        st.session_state.training_in_progress = False
        st.rerun()
```

### Pattern 3: Elapsed Time Display for Long Operations

**What:** Show real-time elapsed time during embedding generation and model training using `st.empty()` container and time tracking.

**When to use:** Operations taking >10 seconds where user needs feedback on progress.

**Example:**
```python
import time

status_container = st.empty()
start_time = time.time()

while operation_in_progress:
    elapsed = int(time.time() - start_time)
    status_container.text(f"Training model... Elapsed: {elapsed}s")
    time.sleep(1)  # Update every second
```

**Note:** Streamlit reruns don't support true async updates — use spinner for simple cases, implement progress bar for <30 sec operations where time updates matter.

### Pattern 4: Checkpoint Auto-Save on Navigation

**What:** Trigger checkpoint save when user clicks "Proceed to Next Step", blocking navigation until save completes or fails.

**When to use:** After model training completes and user wants to advance workflow.

**Example:**
```python
# In Step 3 (Model Configuration & Training)
if st.button("Proceed to Next Step"):
    if st.session_state.trained_model is None:
        st.error("Train a model before proceeding")
    else:
        try:
            checkpoint_dir = save_checkpoint(
                config=st.session_state.model_config,
                metadata={
                    'timestamp': datetime.now().isoformat(),
                    'dataset_name': st.session_state.dataset_name,
                    'topic_count': len(st.session_state.trained_model.get_topics()),
                },
                model=st.session_state.trained_model,
                embeddings=st.session_state.embeddings,
                dataset_fingerprint=st.session_state.dataset_fingerprint
            )
            st.success(f"Checkpoint saved: {checkpoint_dir.name}")
            goto(4)  # Advance to visualization
        except Exception as e:
            st.error(f"Checkpoint save failed: {e}")
            # Block navigation — user must fix issue
```

### Pattern 5: Parameter Pre-fill from Loaded Checkpoint

**What:** If user loaded a checkpoint in Phase 07, pre-fill parameter defaults from checkpoint config; otherwise use hard-coded defaults.

**When to use:** Step 3 initialization when rendering parameter widgets.

**Example:**
```python
# At top of Step 3
if st.session_state.loaded_checkpoint is not None:
    checkpoint_config = st.session_state.loaded_checkpoint['config']
    default_n_neighbors = checkpoint_config.get('umap', {}).get('n_neighbors', 15)
    default_n_components = checkpoint_config.get('umap', {}).get('n_components', 5)
    # ...etc for all parameters
else:
    # Hard-coded defaults from notebook workflow
    default_n_neighbors = 15
    default_n_components = 5
    default_min_dist = 0.0
    # ...etc

# Render widgets with dynamic defaults
n_neighbors = st.slider("n_neighbors", 5, 50, default_n_neighbors)
```

### Anti-Patterns to Avoid

- **Caching model training:** Training is parameter-dependent (every change requires retrain). Only cache embeddings (dataset-dependent only).
- **Manual checkpoint save button:** Per D-15, no manual save button — auto-save on "Proceed" only. Reduces UI clutter and decision fatigue.
- **Enabling widgets during training:** Streamlit reruns can corrupt state if user interacts mid-operation. Always disable inputs during long operations.
- **Storing trained model in widget key:** BERTopic models are >10 MB. Store in `st.session_state.trained_model`, not as widget default_value (causes performance issues).

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Elapsed time display during operations | Custom async time tracker with threads | `st.spinner()` with periodic reruns or `st.progress()` for determinate operations | Streamlit's rerun model doesn't support true async updates; custom threading adds complexity with marginal benefit for 30-120 sec operations |
| Parameter validation | Custom min/max checking with error messages | `st.slider()` min_value/max_value constraints | Streamlit sliders enforce bounds automatically; validation is built-in |
| Embedding model selection | Custom model picker UI | Hard-code "all-MiniLM-L6-v2" (established in notebook workflow) | User constraints say "no presets", but embeddings are outside parameter scope — changing embedding model invalidates all checkpoints, so hard-code for consistency |
| Checkpoint directory cleanup | Custom disk space monitoring | Manual delete via Phase 07 checkpoint management UI | Phase 07 already provides checkpoint list and delete functionality; don't duplicate |

**Key insight:** Streamlit's rerun model and widget ecosystem handle most UI complexity automatically. Hand-rolling custom solutions adds bugs without UX benefit.

## Common Pitfalls

### Pitfall 1: Embedding Cache Miss on Dataset Change
**What goes wrong:** User adjusts filters in Step 2 (Phase 06), returns to Step 3, embeddings regenerate unnecessarily because cache key didn't include fingerprint.

**Why it happens:** Naive caching uses only `input_texts` as key. Two different datasets with identical text content (rare but possible) would share cache incorrectly.

**How to avoid:** Include `dataset_fingerprint` from Phase 06 in cache key: `generate_embeddings(texts, fingerprint)`.

**Warning signs:** User reports "embeddings regenerating even though I didn't change the data" — missing fingerprint in cache key.

### Pitfall 2: UI Corruption from Mid-Operation Interaction
**What goes wrong:** User clicks "Train Model", then immediately adjusts slider while training is in progress. Streamlit reruns mid-operation, `st.session_state` gets corrupted, training fails or produces incorrect results.

**Why it happens:** Streamlit's rerun model allows interactions during long operations unless explicitly disabled.

**How to avoid:** Set `disabled=st.session_state.training_in_progress` on all widgets during operations.

**Warning signs:** Intermittent training failures, error messages mentioning "model object has no attribute X" (partial state overwrite).

### Pitfall 3: Checkpoint Save Failure Silently Ignored
**What goes wrong:** User clicks "Proceed", checkpoint save fails (disk full, permission denied), but navigation proceeds anyway. Later phases fail because checkpoint is missing.

**Why it happens:** Exception handling wrapped with `try/except pass` or error not surfaced to UI.

**How to avoid:** Per D-14, block navigation on checkpoint save failure with explicit error message. User must resolve issue before advancing.

**Warning signs:** Phase 09/10 reports "checkpoint not found" even though user trained model in Phase 08.

### Pitfall 4: Memory Explosion from Large Model Storage
**What goes wrong:** App crashes with "MemoryError" or becomes unresponsive after training large models (>1000 documents, >100 topics).

**Why it happens:** BERTopic models are >10 MB in memory. Storing in widget `value` or `default_value` causes duplication on every rerun.

**How to avoid:** Store trained model in `st.session_state.trained_model` only. Never pass large objects through widget parameters.

**Warning signs:** App slowdown after training, increasing memory usage visible in task manager.

### Pitfall 5: Navigation Guard Not Showing Near Sidebar Click
**What goes wrong:** User clicks Step 2 in sidebar, navigation guard prompt appears at bottom of page (below viewport), user doesn't see it and thinks app is frozen.

**Why it happens:** Guard logic uses `st.warning()` or `st.error()` in main content area, not near sidebar where click originated.

**How to avoid:** Per D-20, render navigation guard in sidebar near 9-step navigation using `with st.sidebar:` context.

**Warning signs:** User reports "app freezes when I click previous steps" — guard is rendering but out of viewport.

## Code Examples

Verified patterns from existing codebase:

### Existing Checkpoint Save (from checkpoint_manager.py)
```python
# Source: src/checkpoint_manager.py lines 47-98
def save_checkpoint(
    config: dict,
    metadata: dict,
    model: BERTopic,
    embeddings: np.ndarray,
    dataset_fingerprint: str
) -> Path:
    """
    Save complete checkpoint to filesystem.
    
    Creates directory structure: data/checkpoints/{timestamp}_{dataset_name}/
    containing all required checkpoint files.
    """
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    dataset_name = metadata.get('dataset_name', 'unknown').replace(' ', '_')
    checkpoint_name = f"{timestamp}_{dataset_name}"
    
    checkpoint_dir = CHECKPOINTS_DIR / checkpoint_name
    checkpoint_dir.mkdir(parents=True, exist_ok=True)
    
    # Save 5 files: config.json, metadata.json, model.pkl, embeddings.npy, dataset_fingerprint.txt
    with open(checkpoint_dir / 'config.json', 'w') as f:
        json.dump(config, f, indent=2)
    
    with open(checkpoint_dir / 'metadata.json', 'w') as f:
        json.dump(metadata, f, indent=2)
    
    with open(checkpoint_dir / 'model.pkl', 'wb') as f:
        pickle.dump(model, f, protocol=5)
    
    np.save(checkpoint_dir / 'embeddings.npy', embeddings)
    
    with open(checkpoint_dir / 'dataset_fingerprint.txt', 'w') as f:
        f.write(dataset_fingerprint)
    
    return checkpoint_dir
```

### Existing Navigation Pattern (from Streamlit app)
```python
# Source: src/DIPT research topics-hierarchical TM.py lines 50-51
def goto(step: int):
    st.session_state.step = step
    st.rerun()
```

### Existing Session State Initialization (from Streamlit app)
```python
# Source: src/DIPT research topics-hierarchical TM.py lines 61-72
if 'step' not in st.session_state:
    st.session_state.step = 1
if 'uploaded' not in st.session_state:
    st.session_state.uploaded = None
if 'df_filtered' not in st.session_state:
    st.session_state.df_filtered = None
if 'dataset_fingerprint' not in st.session_state:
    st.session_state.dataset_fingerprint = None
if 'loaded_checkpoint' not in st.session_state:
    st.session_state.loaded_checkpoint = None
```

### BERTopic Training Pattern (from notebook)
```python
# Source: experiments/BTH research topics.ipynb
umap_model = UMAP(n_neighbors=15, n_components=5, min_dist=0.0, metric='cosine', random_state=42)
hdbscan_model = HDBSCAN(metric='euclidean', cluster_selection_method='eom', prediction_data=True)
vectorizer_model = CountVectorizer(stop_words="english", min_df=2, ngram_range=(1, 2))

sentence_model = SentenceTransformer("all-MiniLM-L6-v2")
embeddings = sentence_model.encode(df_filtered['input'], show_progress_bar=False)

topic_model = BERTopic(
    umap_model=umap_model,
    hdbscan_model=hdbscan_model,
    vectorizer_model=vectorizer_model,
    verbose=True
)

topics, probs = topic_model.fit_transform(df_filtered['input'], embeddings)
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| Generate embeddings on every parameter change | Cache embeddings by dataset fingerprint using `@st.cache_data` | Phase 08 (this phase) | 30-120 sec saved on every parameter adjustment (20-30x speedup for iterative tuning) |
| Save checkpoints manually via button click | Auto-save on "Proceed to Next Step" | Phase 08 (per D-13) | Reduces decision fatigue, prevents forgetting to save |
| Show spinner without time indication | Show elapsed time in spinner | Phase 08 (per D-09/D-10) | Better user feedback for operations with variable duration |

**Deprecated/outdated:**
- HDBSCAN `min_cluster_size` parameter commented out in notebook (line showing commented version) — indicates parameter tuning is experimental, planner should expose this parameter in UI per roadmap.

## Open Questions

1. **What's the "basic topic list view" format mentioned in success criteria 7?**
   - What we know: Roadmap says "User sees basic topic list view with topic IDs, labels, and document counts after successful training"
   - What's unclear: Display as st.dataframe(), st.table(), or custom HTML? How many topics to show (all vs top N)?
   - Recommendation: Use `st.dataframe()` showing all topics (ID, label, doc count columns) — matches Streamlit conventions and supports sorting/search out of box.

2. **Should HDBSCAN min_cluster_size be exposed in UI given it's commented out in notebook?**
   - What we know: Notebook has `min_cluster_size=50` commented out, suggesting experimentation. Roadmap success criteria 3 says "configure HDBSCAN parameters (min_cluster_size, min_samples)".
   - What's unclear: Is commented-out value a signal to exclude from UI, or is it experimental tuning that should be exposed?
   - Recommendation: Expose in UI per roadmap — comment in notebook likely indicates "optional tuning", not "never expose". Include in Parameter Guide with explanation.

## Environment Availability

| Dependency | Required By | Available | Version | Fallback |
|------------|------------|-----------|---------|----------|
| Python 3.12 | All Python code | ✓ | 3.12 | — |
| BERTopic | Model training | ✓ | 0.16.4 | — |
| Streamlit | Web UI | ✓ | 1.50.0 | — |
| sentence-transformers | Embedding generation | ✓ | 3.3.1 | — |
| NumPy | Array operations | ✓ | 2.2.2 | — |

**Missing dependencies with no fallback:**
None — all dependencies already installed.

**Missing dependencies with fallback:**
None.

## Validation Architecture

> Workflow.nyquist_validation is enabled (checked .planning/config.json line 19: `"nyquist_validation": true`).

### Test Framework
| Property | Value |
|----------|-------|
| Framework | Not detected — no pytest.ini, jest.config, vitest.config found in repository |
| Config file | None — see Wave 0 |
| Quick run command | `pytest tests/ -x` (if pytest installed) |
| Full suite command | `pytest tests/` (if pytest installed) |

### Phase Requirements → Test Map
| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| TM-04 | User can configure UMAP parameters (n_neighbors, n_components, min_dist) | manual | Visual verification — sliders render with correct ranges | ❌ (manual verification step) |
| TM-04 | User can configure HDBSCAN parameters (min_cluster_size, min_samples) | manual | Visual verification — sliders render with correct ranges | ❌ (manual verification step) |
| TM-04 | User can configure vectorizer settings (n-gram range, min_df, max_df) | manual | Visual verification — widgets render with correct options | ❌ (manual verification step) |
| TM-04 | System generates and caches embeddings separately | unit | `pytest tests/test_embedding_cache.py::test_cache_hit_on_same_fingerprint -x` | ❌ Wave 0 |
| TM-04 | System generates and caches embeddings separately | unit | `pytest tests/test_embedding_cache.py::test_cache_miss_on_different_fingerprint -x` | ❌ Wave 0 |
| TM-04 | User sees progress indicators for long-running operations | manual | Visual verification — spinner + elapsed time display during training | ❌ (manual verification step) |
| TM-04 | User sees basic topic list view after successful training | manual | Visual verification — dataframe displays topics with ID/label/count | ❌ (manual verification step) |
| TM-04 | System creates persistent checkpoint automatically when user proceeds | integration | `pytest tests/test_checkpoint_autosave.py::test_checkpoint_created_on_proceed -x` | ❌ Wave 0 |
| TM-04 | Checkpoint includes all trained model state and embeddings | integration | `pytest tests/test_checkpoint_integrity.py::test_checkpoint_contains_all_files -x` | ❌ Wave 0 |
| TM-04 | User is prompted to save checkpoint when navigating backward | manual | Visual verification — navigation guard appears with 3-option prompt | ❌ (manual verification step) |

### Sampling Rate
- **Per task commit:** `pytest tests/ -x` (quick run, stops on first failure)
- **Per wave merge:** `pytest tests/` (full suite)
- **Phase gate:** Full suite green before `/gsd-verify-work`

### Wave 0 Gaps
- [ ] `tests/test_embedding_cache.py` — covers cache hit/miss behavior for embedding generation (TM-04)
- [ ] `tests/test_checkpoint_autosave.py` — covers checkpoint creation on "Proceed" click (TM-04)
- [ ] `tests/test_checkpoint_integrity.py` — covers checkpoint file completeness (TM-04)
- [ ] `tests/conftest.py` — shared fixtures for mock Streamlit session state
- [ ] Framework install: `pip install pytest pytest-mock` — if pytest not detected

**Note:** 6 out of 10 success criteria require manual visual verification (UI layout, widget rendering, progress indicators, topic display, navigation guard). These are inherently manual for Streamlit apps — automated testing would require selenium/playwright, which is out of scope for this phase.

## Security Domain

> Security enforcement is enabled (checked .planning/config.json — `workflow.security_enforcement` not present, absent = enabled).

### Applicable ASVS Categories

| ASVS Category | Applies | Standard Control |
|---------------|---------|-----------------|
| V2 Authentication | no | Not applicable — no user accounts, authentication, or session tokens in this phase |
| V3 Session Management | no | Not applicable — Streamlit session state is server-side only, no cookies/tokens sent to client |
| V4 Access Control | no | Not applicable — no authorization logic, no protected resources |
| V5 Input Validation | yes | Validate numeric parameter ranges via `st.slider()` min_value/max_value; validate dataset fingerprint format (64-char hex) before cache lookup |
| V6 Cryptography | no | Not applicable — no encryption, hashing (fingerprint is integrity check, not security boundary), or key management in this phase |

### Known Threat Patterns for Streamlit + Python ML Stack

| Pattern | STRIDE | Standard Mitigation |
|---------|--------|---------------------|
| Pickle deserialization attack (malicious checkpoint loading) | Tampering | Phase 07 already implements integrity validation (file size checks, pickle load in try/except); Phase 08 inherits this mitigation |
| Path traversal in checkpoint naming | Tampering | Use `dataset_name.replace(' ', '_')` only — no user-controlled slashes in checkpoint paths; Phase 07 already implements this |
| Denial of service via large embedding generation | Denial of Service | No mitigation in scope — dataset size is controlled by user upload in Phase 06; typical workload is <10k documents (manageable) |

**Note:** This phase has minimal attack surface — it's a single-user local Streamlit app with no network exposure, no authentication, and no external API calls. The primary threat is malicious checkpoint files (already mitigated in Phase 07 via integrity validation).

## Sources

### Primary (HIGH confidence)
- `requirements.txt` — verified all library versions (BERTopic 0.16.4, UMAP 0.5.7, HDBSCAN 0.8.40, etc.)
- `src/checkpoint_manager.py` — verified checkpoint save/load patterns, file structure, fingerprint handling
- `experiments/BTH research topics.ipynb` — verified UMAP/HDBSCAN/vectorizer parameter values used in notebook workflow
- `src/DIPT research topics-hierarchical TM.py` — verified session state patterns, navigation, caching setup
- `.planning/phases/08-model-configuration-training/08-CONTEXT.md` — verified user decisions (D-01 through D-20)
- `.planning/ROADMAP.md` — verified Phase 08 success criteria (9 criteria) and pitfall prevention notes

### Secondary (MEDIUM confidence)
- BERTopic documentation (via training data knowledge) — typical parameter ranges, model training patterns

### Tertiary (LOW confidence)
None — all claims verified against repository artifacts or requirements file.

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH - all versions verified in requirements.txt
- Architecture: HIGH - patterns verified in existing Phase 06/07 code
- Pitfalls: HIGH - derived from Streamlit documentation and codebase analysis

**Research date:** 2026-05-25
**Valid until:** 2026-06-25 (30 days — stable stack, no fast-moving dependencies)
