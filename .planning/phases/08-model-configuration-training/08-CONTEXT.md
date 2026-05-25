# Phase 08: Model Configuration & Training - Context

**Gathered:** 2026-05-25
**Status:** Ready for planning

<domain>
## Phase Boundary

Users can configure topic model parameters (UMAP, HDBSCAN, vectorizer), train models with cached embeddings, and save checkpoints to persistent storage. This establishes the ML caching patterns and checkpoint integration that enable iterative refinement in later phases (Phase 10-11 comparisons).

</domain>

<decisions>
## Implementation Decisions

### Parameter Configuration UI Layout
- **D-01:** Use single scrolling form with all parameters visible at once with section headings (no expand/collapse or tabs).
- **D-02:** Use default `st.slider()` behavior for all numeric parameters (sliders have built-in drag + type input box).
- **D-03:** Use `st.divider()` horizontal lines between sections (UMAP / HDBSCAN / Vectorizer) for clear visual breaks.
- **D-04:** Pre-fill parameter defaults from loaded checkpoint if available (from Phase 07 checkpoint config); otherwise use hard-coded sensible defaults.

### Parameter Guidance & Presets
- **D-05:** Provide single expandable Parameter Guide (▶ Need help? Click for parameter explanations) - available but not intrusive.
- **D-06:** Position Parameter Guide at bottom, after all parameters - doesn't interfere with parameter access.
- **D-07:** No preset buttons (Conservative/Balanced/Granular) - users adjust every parameter individually for full manual control. **NOTE:** This diverges from roadmap mention of preset options, but user preference for full manual control is clear.
- **D-08:** Parameter Guide content includes both parameter reference (definitions, typical ranges) and workflow-oriented tips (common tuning scenarios like "for more granular topics, decrease min_cluster_size and n_neighbors").

### Progress Indication
- **D-09:** Show spinner with elapsed time display for embedding generation (updates in real-time: "Elapsed: 45s") - runs 30-120 seconds but only once, then cached.
- **D-10:** Show spinner with elapsed time for model training - consistent feedback style with embedding generation (runs 10-60 seconds, repeats on parameter changes).
- **D-11:** Show brief success message for cache hit: `st.success('✓ Using cached embeddings')` when embeddings already cached.
- **D-12:** Disable all inputs during long operations (embedding generation, model training) - prevents state corruption from UI interactions during processing.

### Checkpoint Creation Timing
- **D-13:** Auto-save checkpoint on "Proceed to Next Step" button click - checkpoint created when user advances to visualization step.
- **D-14:** Block navigation and show error if checkpoint save fails - user must resolve checkpoint save issue (disk space, permissions, etc.) before continuing.
- **D-15:** Auto-save only on Proceed - no manual "Save Checkpoint Now" button (simpler UI).
- **D-16:** Use timestamp + dataset name for checkpoint naming: `{timestamp}_{dataset_name}` (e.g., `20260525_203045_publications_2024`) - matches Phase 07 pattern.

### Navigation Guard
- **D-17:** Always confirm backward navigation with "Are you sure? Parameter changes will be lost." even if no model trained yet - consistent confirmation pattern.
- **D-18:** Prompt to save checkpoint after training when navigating backward: show three options `[Save & Go Back] [Go Back Without Saving] [Cancel]` - matches roadmap language.
- **D-19:** Always prompt on backward navigation - no session memory of user choice (prioritizes safety over convenience).
- **D-20:** Show navigation guard prompt in sidebar near 9-step navigation where click originated - keeps context close to the action.

### the agent's Discretion
- Exact hard-coded default values for UMAP/HDBSCAN/vectorizer parameters (as long as they reflect typical ranges from notebook workflow).
- Exact wording of parameter explanations in the Parameter Guide (as long as they cover parameter definitions and workflow tips).
- Exact implementation of elapsed time display (as long as it updates in real-time during operations).
- Exact UI state management for disabling inputs during operations (as long as all inputs are disabled during embedding/training).
- Exact error messages for checkpoint save failures (as long as they're clear and actionable).

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Phase scope and continuity
- `.planning/PROJECT.md` — v2.0 milestone scope, ML stack constraints (BERTopic + UMAP + HDBSCAN), workflow fidelity requirements.
- `.planning/ROADMAP.md` — Phase 08 success criteria (9 criteria defining what must be TRUE), pitfall prevention notes (memory explosion from uncached embeddings, parameter coupling confusion).
- `.planning/REQUIREMENTS.md` — TM-04 requirement mapping.
- `.planning/phases/06-data-upload-filtering/06-VERIFICATION.md` — Dataset fingerprinting established in Phase 06 (used for checkpoint validation).
- `.planning/phases/07-checkpoint-infrastructure/PHASE-SUMMARY.md` — Checkpoint save/load patterns, checkpoint structure (5-file layout), `PROJECT_ROOT` path resolution, integrity validation patterns.

### Notebook workflow reference
- `experiments/BTH research topics.ipynb` — Original iterative parameter tuning workflow that this phase formalizes (shows UMAP/HDBSCAN/vectorizer parameter relationships and typical value ranges).

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `src/checkpoint_manager.py`: Five core functions for checkpoint lifecycle (save_checkpoint, load_checkpoint, compute_dataset_fingerprint, list_checkpoints, validate_checkpoint_integrity) — all available for Phase 08 to call.
- `src/DIPT research topics-hierarchical TM.py`: Streamlit app with established session state patterns (`st.session_state.df`, `st.session_state.df_filtered`, `st.session_state.dataset_fingerprint`), `goto(step)` navigation, and 9-step sidebar navigation from Phase 07.
- BERTopic stack already imported: `from bertopic import BERTopic` and related imports for UMAP, HDBSCAN, vectorizer components.

### Established Patterns
- **Session state for UI flow**: All data stored in `st.session_state` keys; navigation via `goto(step: int)` callback pattern.
- **Caching with `@st.cache_data`**: Phase 06 established DataFrame caching pattern; Phase 08 must use same pattern for embedding caching to prevent 30-120 sec regeneration.
- **Progress feedback**: Phase 06/07 use `st.spinner()` and `st.success()` for operation feedback — extend with elapsed time display.
- **Path resolution**: Phase 07 established `PROJECT_ROOT = Path(__file__).parent.parent` pattern for resolving checkpoint paths relative to project root (not CWD).
- **9-step sidebar navigation**: Phase 07 implemented step progress indicator (→ current, ✓ completed, plain future) — Phase 08 is Step 3.

### Integration Points
- **Phase 06 handoff**: `st.session_state.dataset_fingerprint` computed after filtering — used for checkpoint validation.
- **Phase 07 handoff**: `st.session_state.loaded_checkpoint` contains checkpoint data if user loaded one; use `config` from loaded checkpoint to pre-fill parameters.
- **Phase 09 handoff**: Phase 08 creates first real checkpoints (config + model + embeddings + metadata + fingerprint); Phase 09 will consume trained model for visualization.
- **Phases 10-11 handoff**: Checkpoints saved in Phase 08 become comparison targets in later phases (side-by-side parameter comparisons at decision points).

</code_context>

<specifics>
## Specific Ideas

- Sliders with built-in input boxes (Streamlit default) provide both visual range feedback and precise value entry — user specifically asked "Isn't it possible to have both?"
- No preset buttons despite roadmap mention — user preference for full manual control is explicit.
- Consistent elapsed time feedback for both embedding generation and model training — helps users understand operation duration patterns.
- Navigation guards always prompt regardless of state — prioritizes data safety over convenience.

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope.

</deferred>

---

*Phase: 08-model-configuration-training*
*Context gathered: 2026-05-25*
