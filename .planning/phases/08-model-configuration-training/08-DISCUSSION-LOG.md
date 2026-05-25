# Phase 08: Model Configuration & Training - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-05-25
**Phase:** 08-model-configuration-training
**Areas discussed:** Parameter Configuration UI Layout, Parameter Guidance & Presets, Progress Indication, Checkpoint Creation Timing, Navigation Guard

---

## Parameter Configuration UI Layout

### Question 1: How should parameter groups be organized?

| Option | Description | Selected |
|--------|-------------|----------|
| Grouped Expandable Sections | UMAP/HDBSCAN/Vectorizer sections with collapse/expand (▼/▶) | |
| Single Scrolling Form | All parameters visible at once with section headings but no collapse | ✓ |
| Tabbed Panels | Three tabs: "UMAP" \| "HDBSCAN" \| "Vectorizer" | |

**User's choice:** Single Scrolling Form
**Notes:** User wants to see everything at a glance for understanding parameter relationships during iteration.

### Question 2: Should parameter inputs use specific widget types?

| Option | Description | Selected |
|--------|-------------|----------|
| Sliders for numeric ranges | st.slider() for all bounded numeric params | |
| Number inputs for all numeric | st.number_input() for easier precise entry | |
| Mixed approach | Sliders for commonly adjusted, number inputs for rest | |
| Default slider behavior | st.slider() has built-in drag + type (both features) | ✓ |

**User's choice:** Default slider behavior
**Notes:** User asked "Isn't it possible to have both?" — confirmed that Streamlit sliders already include both drag and type input functionality.

### Question 3: Should sections have visual separators?

| Option | Description | Selected |
|--------|-------------|----------|
| Text headings only | Simple markdown headings (## UMAP Parameters) | |
| Visual separators | st.divider() horizontal lines between sections | ✓ |
| Colored/bordered containers | st.container() with backgrounds or borders | |

**User's choice:** Visual separators (dividers)
**Notes:** Clean visual breaks without heavy styling.

### Question 4: Should defaults come from checkpoint or be hard-coded?

| Option | Description | Selected |
|--------|-------------|----------|
| Hard-coded sensible defaults | Same defaults every time from notebook patterns | |
| Load from checkpoint if available | Pre-fill from Phase 07 loaded checkpoint config | ✓ |
| Remember last-used in session | st.session_state persistence within session only | |

**User's choice:** Load from checkpoint if available
**Notes:** Fallback to hard-coded defaults if no checkpoint loaded.

---

## Parameter Guidance & Presets

### Question 1: How much inline guidance?

| Option | Description | Selected |
|--------|-------------|----------|
| Tooltips only | Use help parameter on widgets (hover to see) | |
| Inline help text | st.caption() below each parameter | |
| Single expandable guide | ▶ Need help? Click for parameter explanations | ✓ |

**User's choice:** Single expandable Parameter Guide
**Notes:** Available but not intrusive — keeps form clean.

### Question 2: Where should Parameter Guide be positioned?

| Option | Description | Selected |
|--------|-------------|----------|
| At top before parameters | Users see it first but pushes parameters down | |
| At bottom after parameters | Doesn't interfere with parameter access | ✓ |
| In sidebar | Separate from main parameter form | |

**User's choice:** Bottom, after parameters
**Notes:** Parameters stay accessible, help available when needed.

### Question 3: Should preset buttons offer quick configurations?

| Option | Description | Selected |
|--------|-------------|----------|
| No presets | Manual configuration only | ✓ |
| HDBSCAN presets only | Conservative/Balanced/Granular for HDBSCAN params | |
| Full configuration presets | All UMAP+HDBSCAN+vectorizer coordinated presets | |

**User's choice:** No presets - manual only
**Notes:** User wants full manual control. Diverges from roadmap mention of "preset options (Conservative/Balanced/Granular)" but user preference is clear.

### Question 4: What should Parameter Guide contain?

| Option | Description | Selected |
|--------|-------------|----------|
| Parameter-by-parameter reference | Definitions and typical ranges for each param | |
| Workflow-oriented guidance | Common tuning scenarios (e.g., "for granular topics...") | |
| Both reference + workflow tips | Parameter definitions + tuning scenarios | ✓ |

**User's choice:** Both reference + workflow tips
**Notes:** Combines definitions with practical guidance for manual tuning.

---

## Progress Indication

### Question 1: Progress detail for embedding generation?

| Option | Description | Selected |
|--------|-------------|----------|
| Simple spinner | st.spinner() with static message | |
| Progress bar with percentage | Instrumented progress tracking | |
| Spinner with elapsed time | Real-time elapsed time counter | ✓ |

**User's choice:** Spinner with elapsed time display
**Notes:** Shows elapsed time updating in real-time (e.g., "Elapsed: 45s") for 30-120 sec operation.

### Question 2: Progress indication for model training?

| Option | Description | Selected |
|--------|-------------|----------|
| Simple spinner only | st.spinner() with static message | |
| Spinner with elapsed time | Same as embedding generation | ✓ |
| Spinner with stage messages | "Running UMAP...", "Running HDBSCAN...", etc. | |

**User's choice:** Spinner with elapsed time
**Notes:** Consistent feedback style with embedding generation for 10-60 sec operation.

### Question 3: Visual distinction for cached operations?

| Option | Description | Selected |
|--------|-------------|----------|
| Silent cache hit | No message if cached | |
| Brief success message | st.success("✓ Using cached embeddings") | ✓ |
| Info message explaining cache | Longer explanation of cache behavior | |

**User's choice:** Brief success message for cache hit
**Notes:** Brief acknowledgment when cached embeddings loaded (<1 sec).

### Question 4: Should UI be disabled during operations?

| Option | Description | Selected |
|--------|-------------|----------|
| Disable all inputs | st.session_state flag disables widgets | ✓ |
| Allow navigation only | Block parameter changes but allow step navigation | |
| No restrictions | Trust Streamlit rerun behavior | |

**User's choice:** Disable all inputs
**Notes:** Prevents state corruption during long operations.

---

## Checkpoint Creation Timing

### Question 1: When should checkpoint be auto-created?

| Option | Description | Selected |
|--------|-------------|----------|
| Immediately after training | Auto-save right away after model.fit() | |
| On "Proceed" button click | When user clicks "Proceed to Visualization" | ✓ |
| Manual save button only | User controls when to save | |

**User's choice:** On Proceed button click
**Notes:** Explicit progression triggers checkpoint creation — matches roadmap language.

### Question 2: What if checkpoint save fails?

| Option | Description | Selected |
|--------|-------------|----------|
| Block navigation and show error | User must resolve before continuing | ✓ |
| Warn but allow navigation | Proceed without save with warning | |
| Retry with fallback | Give user retry/proceed options | |

**User's choice:** Block navigation and show error
**Notes:** Ensures checkpoint integrity — user must resolve disk space/permission issues.

### Question 3: Manual save button in addition to auto-save?

| Option | Description | Selected |
|--------|-------------|----------|
| Auto-save only | No manual button, simpler UI | ✓ |
| Manual + auto-save | Flexibility to save without navigating | |
| Manual disables auto-save | Skip auto-save if manually saved | |

**User's choice:** Auto-save only on Proceed
**Notes:** No manual save button — simpler UI.

### Question 4: Checkpoint naming for auto-saved checkpoints?

| Option | Description | Selected |
|--------|-------------|----------|
| Timestamp only | Simple, always unique | |
| Timestamp + dataset name | Matches Phase 07 pattern | ✓ |
| Timestamp + dataset + params | Verbose but descriptive | |

**User's choice:** Timestamp + dataset name
**Notes:** Format: `{timestamp}_{dataset_name}` (e.g., `20260525_203045_publications_2024`).

---

## Navigation Guard

### Question 1: What happens on backward navigation before training?

| Option | Description | Selected |
|--------|-------------|----------|
| Allow silently | No warning if no model trained | |
| Confirm anyway | "Parameter changes will be lost" even if no model | ✓ |
| Check for unsaved work | Only prompt if parameters changed | |

**User's choice:** Confirm navigation anyway
**Notes:** Consistent confirmation pattern regardless of whether model was trained.

### Question 2: What happens after training but before proceeding?

| Option | Description | Selected |
|--------|-------------|----------|
| Prompt to save checkpoint | [Save & Go Back] [Go Back Without Saving] [Cancel] | ✓ |
| Auto-save then navigate | No user decision needed | |
| Block navigation | Force forward progression only | |

**User's choice:** Prompt to save checkpoint
**Notes:** Three options give user control — matches roadmap language "prompted to save checkpoint when navigating backward".

### Question 3: Should prompt remember user's choice?

| Option | Description | Selected |
|--------|-------------|----------|
| Always prompt | Every backward navigation shows prompt | ✓ |
| Remember "don't save" | Session memory with "Don't ask again" checkbox | |
| No memory | Same as "Always prompt" | |

**User's choice:** Always prompt
**Notes:** Safety over convenience — every backward navigation prompts.

### Question 4: How should navigation prompt be displayed?

| Option | Description | Selected |
|--------|-------------|----------|
| st.dialog modal | Modal overlay with clear focus | |
| Inline warning with buttons | Warning in main content flow | |
| Sidebar warning | Near 9-step navigation where click originated | ✓ |

**User's choice:** Sidebar warning near navigation
**Notes:** Keeps context close to where user clicked in navigation.

---

## the agent's Discretion

- Exact hard-coded default parameter values (as long as they reflect notebook workflow patterns)
- Exact wording of parameter explanations in Parameter Guide
- Exact elapsed time display implementation
- Exact UI state management for input disabling
- Exact error message wording for checkpoint save failures

## Deferred Ideas

None — all discussion stayed within Phase 08 scope.
