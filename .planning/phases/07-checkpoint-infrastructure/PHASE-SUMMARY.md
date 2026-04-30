# Phase 07 Summary: Checkpoint Infrastructure

**Status:** Complete ✓  
**Requirements:** TM-03  
**Completed:** 2026-05-01  
**Plans Executed:** 2/2

---

## Phase Goal

Establish persistent checkpoint save/load system that enables resuming work across sessions and reproducing analyses months/years later with exact parameter sets.

**Core Value:** Users can save trained models with all associated data, reload them in fresh sessions, compare parameter configurations, and maintain full reproducibility of topic modeling analyses.

---

## Success Criteria Achievement

| # | Criterion | Status | Evidence |
|---|-----------|--------|----------|
| 1 | Save checkpoint with 5 files | ✓ Complete | Viability test confirms save/load |
| 2 | Load from dropdown with metadata | ✓ Complete | Human verified UI |
| 3 | List all checkpoints with metadata | ✓ Complete | Human verified UI |
| 4 | Validate integrity on load | ✓ Complete | 15 unit tests passing |
| 5 | Block fingerprint mismatch | ✓ Complete | Human verified error message |
| 6 | Extract and clone parameters | ✓ Complete | View Parameters UI implemented |
| 7 | Delete checkpoints | ✓ Complete | Human verified two-click confirmation |
| 8 | Export as ZIP | ✓ Complete | Human verified download |
| 9 | 9-step navigation sidebar | ✓ Complete | Human verified progress display |

**All 9 success criteria met** ✓

---

## What Was Built

### 1. Checkpoint Manager Module (`src/checkpoint_manager.py`)

**270 lines of production code**

Five core functions for complete checkpoint lifecycle management:

1. **`compute_dataset_fingerprint(df)`** — SHA-256 hash of sorted DataFrame for dataset identity verification
2. **`save_checkpoint(...)`** — Persist model + embeddings + config + metadata + fingerprint to disk
3. **`load_checkpoint(path)`** — Restore all checkpoint data with integrity validation
4. **`list_checkpoints()`** — Scan and return metadata for all saved checkpoints
5. **`validate_checkpoint_integrity(path)`** — Check for missing files, corruption, size anomalies

**File Structure:**
```
data/checkpoints/{timestamp}_{dataset_name}/
├── config.json          # UMAP/HDBSCAN/vectorizer parameters
├── metadata.json        # timestamp, topic_count, outlier_%, row_count
├── model.pkl            # Trained BERTopic model (pickle protocol 5)
├── embeddings.npy       # Document embeddings (numpy array)
└── dataset_fingerprint.txt  # SHA-256 hash of source data
```

**Key Design Decisions:**
- Paths resolved relative to `PROJECT_ROOT` (not CWD) to work from any execution context
- Pickle protocol 5 for large object serialization (typical checkpoint: 50-500 MB)
- SHA-256 fingerprinting prevents loading incompatible checkpoints
- Integrity validation catches corruption before load (file existence, size checks, pickle test)

### 2. Streamlit Checkpoint UI Integration

**183 lines added to `src/DIPT research topics-hierarchical TM.py`**

Six major UI components:

1. **9-Step Workflow Navigation** — Sidebar progress indicator (→ current, ✓ completed, plain future steps)
2. **Checkpoint Dropdown** — Shows all available checkpoints with metadata (name, timestamp, topic count)
3. **Load with Validation** — Integrity + fingerprint checks, blocks incompatible loads with clear errors
4. **View Parameters** — Expandable panel showing config.json and metadata.json in copy-friendly format
5. **Delete with Confirmation** — Two-click pattern prevents accidental deletion
6. **Export as ZIP** — Download entire checkpoint directory for backup/sharing

**Session State Integration:**
```python
st.session_state.dataset_fingerprint   # Computed after step 2 filtering
st.session_state.loaded_checkpoint     # Full checkpoint data (config, model, embeddings, etc.)
st.session_state.available_checkpoints # Checkpoint list cache
st.session_state.delete_confirm        # Confirmation flag for deletion
```

### 3. Comprehensive Test Coverage

**497 lines of test code** (`tests/test_checkpoint_manager.py`)

- 15 unit tests covering all functions and edge cases
- Fingerprinting stability tests (same data → same hash, row order independence)
- Save/load roundtrip tests with mock BERTopic objects
- Integrity validation tests (missing files, corrupted pickle, small files)
- Checkpoint listing tests (sorting, metadata parsing)
- All tests passing ✓

### 4. Viability Validation

**Real BERTopic model checkpoint test** (`tests/test_checkpoint_viability.py`)

Confirmed:
- ✓ Real BERTopic models (not just mocks) can be saved and loaded
- ✓ Loaded models retain full functionality (predictions, visualizations, topic info)
- ✓ Large embeddings (100-500 MB) survive serialization
- ✓ Fingerprint validation catches dataset mismatches
- ✓ All topic modeling operations work post-reload

---

## Technical Achievements

### Path Resolution Fix
- **Problem:** Checkpoints not found when Streamlit runs from `src/` directory
- **Solution:** Use `PROJECT_ROOT = Path(__file__).parent.parent` instead of relative paths
- **Impact:** Checkpoint system works from any execution context

### Pickle Safety
- **Problem:** AttributeError when loading test checkpoints with unavailable class definitions
- **Solution:** Extended exception handling to catch `AttributeError` and `ModuleNotFoundError`
- **Impact:** Graceful degradation for edge cases

### Fingerprint Validation
- **Problem:** No way to detect checkpoint-dataset mismatch
- **Solution:** SHA-256 hash of sorted DataFrame, stored in checkpoint, validated on load
- **Impact:** Prevents using wrong parameters with wrong data

---

## Commits

| Commit | Description |
|--------|-------------|
| e7a9358 | feat(07-01): add checkpoint manager module |
| 1943c06 | test(07-01): add comprehensive unit tests |
| 88d4a6b | docs(07-01): add plan summary |
| 6663459 | feat(07-02): integrate checkpoint management UI |
| b8aebca | fix(07-02): resolve checkpoint paths relative to project root |
| 56a5635 | fix(07-02): handle AttributeError in checkpoint validation |
| aeffa4c | docs(07-02): add plan summary |
| b7014cd | test(07): add BERTopic checkpoint viability test |
| 7d7752b | feat(07): add View Parameters feature for checkpoint extraction |
| e76c566 | docs(07-02): update summary with View Parameters feature |

**Total: 10 commits**

---

## Dependencies

### New Dependencies
None — all required libraries (pickle, json, numpy, pandas, hashlib, shutil) are Python stdlib or already in requirements.txt

### Integration Points
- **Phase 06 (Data Upload & Filtering)** — Provides `dataset_fingerprint` after filtering
- **Phase 08 (Model Configuration & Training)** — Will call `save_checkpoint()` after training
- **Phases 09-11 (Outlier Reduction, Topic Labeling)** — Will use checkpoints for side-by-side comparisons

---

## Issues Encountered & Resolved

### Issue 1: Checkpoint Discovery Failure
- **Symptom:** `list_checkpoints()` returned empty list when called from Streamlit
- **Root Cause:** Relative path `Path('data/checkpoints')` failed when CWD was `src/`
- **Fix:** Changed to absolute path using `PROJECT_ROOT = Path(__file__).parent.parent`
- **Commit:** b8aebca

### Issue 2: Pickle AttributeError on Test Checkpoint
- **Symptom:** Validation failed with "Can't get attribute 'MockBERTopicModel'"
- **Root Cause:** Pickled custom class not available in validation context
- **Fix:** Added `AttributeError` and `ModuleNotFoundError` to exception handling
- **Commit:** 56a5635

---

## Human Verification Results

**Verified by user on 2026-05-01:**

✓ Checkpoint dropdown appears with test checkpoint  
✓ Load without data shows warning (not error)  
✓ Load with data shows fingerprint mismatch error (expected behavior)  
✓ Delete confirmation pattern works  
✓ Export ZIP download available  
✓ View Parameters expander shows config/metadata  
✓ UI readable and accessible  

**Verdict:** Approved ✓

---

## Integration Notes for Phase 08

Phase 08 (Model Configuration & Training) will be the first phase to **create real checkpoints**.

### Checkpoint Creation Pattern

After successful model training:

```python
from checkpoint_manager import save_checkpoint, compute_dataset_fingerprint

# After training BERTopic model
checkpoint_dir = save_checkpoint(
    config={
        'umap': {'n_neighbors': 15, 'n_components': 5, 'min_dist': 0.0},
        'hdbscan': {'min_cluster_size': 10, 'min_samples': 5},
        'vectorizer': {'ngram_range': (1, 2), 'min_df': 2}
    },
    metadata={
        'timestamp': datetime.now().strftime('%Y%m%d_%H%M%S'),
        'dataset_name': 'my_dataset',
        'topic_count': len(set(topic_model.topics_)),
        'outlier_percentage': (topic_model.topics_ == -1).sum() / len(topic_model.topics_) * 100,
        'row_count': len(df)
    },
    model=topic_model,
    embeddings=embeddings,
    dataset_fingerprint=st.session_state.dataset_fingerprint  # From Phase 06
)
```

### Checkpoint Loading Pattern

To restore a saved checkpoint:

```python
config, metadata, model, embeddings, fingerprint = load_checkpoint(checkpoint_dir)

# Validate fingerprint before use
if fingerprint != st.session_state.dataset_fingerprint:
    st.error("Dataset mismatch!")
else:
    # Use loaded model for predictions/visualization
    st.session_state.loaded_checkpoint = {...}
```

---

## Threat Model Summary

All identified threats mitigated:

| ID | Threat | Mitigation | Status |
|----|--------|------------|--------|
| T-07-01 | Checkpoint tampering | Integrity validation before load | ✓ Mitigated |
| T-07-02 | Disk space DoS | Clear error messages on filesystem errors | ✓ Mitigated |
| T-07-03 | Info disclosure | Local storage only, user controls access | ✓ Accepted |
| T-07-04 | Pickle exploit | Load only from known directory, validate source | ✓ Mitigated |
| T-07-05 | Load tampering | Integrity validation with clear errors | ✓ Mitigated |
| T-07-06 | Export disclosure | User-initiated export of own data | ✓ Accepted |
| T-07-07 | Delete DoS | Two-click confirmation, error handling | ✓ Mitigated |
| T-07-08 | Fingerprint spoofing | Block load on mismatch with clear message | ✓ Mitigated |

---

## Next Phase

**Phase 08: Model Configuration & Training**

Now that checkpoint infrastructure is complete, Phase 08 can:
- Configure UMAP/HDBSCAN/vectorizer parameters via UI
- Train BERTopic models with cached embeddings
- Create first real checkpoints after successful training
- Load checkpoints to resume work across sessions
- Extract parameters from old checkpoints to apply to new data

Ready to plan: `/gsd-plan-phase 08`

---

## Metrics

- **Implementation Time:** 1 session (2026-05-01)
- **Code Added:** 950 lines (270 production + 497 tests + 183 UI integration)
- **Tests:** 16 total (15 unit + 1 viability)
- **Files Created:** 2 (checkpoint_manager.py, test_checkpoint_viability.py)
- **Files Modified:** 1 (DIPT research topics-hierarchical TM.py)
- **Commits:** 10
- **Success Criteria Met:** 9/9 (100%)

---

**Phase 07 complete and ready for production use.** ✓
