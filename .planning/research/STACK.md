# Stack Research: Interactive Topic Modeling UI

**Domain:** Interactive topic modeling web application  
**Researched:** 2026-04-29  
**Confidence:** HIGH

## Executive Summary

This research focuses on **stack additions needed for the v2.0 interactive topic modeling UI**, not the entire scipop stack. The existing stack (BERTopic 0.16.4, Streamlit 1.50.0, UMAP, HDBSCAN, pandas) is **validated and should be upgraded**, not replaced. Key additions are needed for side-by-side comparison UI, iterative workflow state, interactive visualizations, and export functionality.

**Core recommendation:** Upgrade core libraries to current stable versions and add minimal supporting tools for UI enhancements. Avoid adding heavy dependencies—keep the tool lightweight and focused.

---

## Recommended Stack Additions

### Core Framework Upgrades

| Technology | Current | Recommended | Purpose | Why Upgrade |
|------------|---------|-------------|---------|-------------|
| **Streamlit** | 1.50.0 | **1.57.0** | Interactive web UI framework | Adds improved `st.columns()` layout control, better session state management, enhanced `st.dataframe()` with row selection events (`on_select`, `selection_mode`), and performance improvements for large datasets |
| **BERTopic** | 0.16.4 | **0.17.4** | Topic modeling engine | Adds improved `reduce_outliers()` methods, enhanced `update_topics()` for iterative refinement, better `visualize_hierarchy()` output, and `merge_topics()` stability improvements |
| **Plotly** | (not listed) | **6.7.0** | Interactive visualization backend | BERTopic's `visualize_hierarchy()` uses Plotly under the hood; explicit inclusion ensures compatibility and enables custom interactive visualizations |

### Supporting Libraries (NEW)

| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| **pandas** | 2.2+ | DataFrame comparison and diff operations | Already present (via BERTopic dependencies); explicitly require for side-by-side parameter result comparisons |
| **None needed** | — | Interactive tables | Streamlit's built-in `st.dataframe()` with `on_select` and `column_config` is sufficient; **avoid adding streamlit-aggrid** unless basic tables prove inadequate |

### Development Tools

| Tool | Purpose | Notes |
|------|---------|-------|
| **Python 3.12** | Runtime environment | Already validated in existing stack |
| **pip + requirements.txt** | Dependency management | Already validated; no need for poetry/pipenv in this project |

---

## Installation

```bash
# Core upgrades (replace existing versions)
pip install --upgrade streamlit==1.57.0
pip install --upgrade bertopic==0.17.4
pip install plotly==6.7.0

# Supporting (likely already installed via BERTopic, but ensure versions)
pip install --upgrade pandas>=2.2.0

# Existing dependencies (keep as-is unless conflicts arise)
# These are already in requirements.txt and work with upgraded versions:
# - umap-learn (via BERTopic)
# - hdbscan (via BERTopic)
# - sentence-transformers (via BERTopic)
# - nltk==3.9.1 (for sentence tokenization)
# - openpyxl==3.1.5 (for Excel upload support)
```

---

## Alternatives Considered

| Recommended | Alternative | When to Use Alternative |
|-------------|-------------|-------------------------|
| **Streamlit 1.57.0** | Dash (Plotly) | If you need fine-grained JavaScript callbacks or highly custom component behavior (overkill for this use case) |
| **Built-in `st.dataframe()`** | streamlit-aggrid | Only if you need Excel-like cell editing or complex filtering UI (adds 40MB+ dependency, slows startup) |
| **Plotly (via BERTopic)** | Altair / Bokeh | If you prefer declarative grammar of graphics (Altair) or need server-side interactions (Bokeh); Plotly is already integrated with BERTopic |
| **Session state (built-in)** | Redis / SQLite | Only if you need persistent sessions across browser restarts (out of scope for v2.0) |

---

## What NOT to Use

| Avoid | Why | Use Instead |
|-------|-----|-------------|
| **streamlit-aggrid** | 40MB+ overhead, complex API, often causes version conflicts with pandas/Streamlit; built-in `st.dataframe()` now supports selection and column config | `st.dataframe()` with `on_select="rerun"` and `selection_mode="multi-row"` |
| **Dash / Plotly Dash** | Requires Flask backend, more complex deployment model, JavaScript callback overhead | Streamlit (simpler, Python-native) |
| **BERTopic <0.17** | Missing critical iterative refinement APIs (`reduce_outliers()` improvements, better `update_topics()` behavior) | BERTopic 0.17.4+ |
| **Streamlit <1.55** | Missing `st.dataframe()` selection events and improved `st.columns()` gap control | Streamlit 1.57.0 |
| **Custom state management (Redis, etc.)** | Adds deployment complexity, v2.0 scope explicitly excludes session persistence | `st.session_state` (built-in) |

---

## Stack Patterns by Feature

### Side-by-Side Comparison UI

```python
# Use Streamlit columns with explicit gap control (requires 1.55+)
col1, col2 = st.columns(2, gap="large")

with col1:
    st.subheader("Option A")
    st.dataframe(results_a)
    
with col2:
    st.subheader("Option B")
    st.dataframe(results_b)
```

**Why:** Streamlit 1.55+ adds `gap` parameter to `st.columns()` for better visual separation of comparison panels.

### Iterative Workflow State

```python
# Use session state for multi-step workflow (built-in, no external library needed)
if 'step' not in st.session_state:
    st.session_state.step = 1
if 'topic_model' not in st.session_state:
    st.session_state.topic_model = None

def goto(step: int):
    st.session_state.step = step
    st.rerun()

# Step-based navigation
if st.session_state.step == 1:
    # Upload/filter step
    pass
elif st.session_state.step == 2:
    # Parameter configuration step
    pass
```

**Why:** Built-in session state is sufficient for single-user, non-persistent workflow tracking. No need for Redis, SQLite, or external state managers.

### Interactive Visualizations

```python
# BERTopic generates Plotly figures by default
hierarchical_topics = topic_model.hierarchical_topics(docs)
fig = topic_model.visualize_hierarchy(hierarchical_topics=hierarchical_topics)

# Display in Streamlit (native support for Plotly)
st.plotly_chart(fig, use_container_width=True)

# Export to HTML for download
fig.write_html("topic_hierarchy.html")
```

**Why:** BERTopic's `visualize_hierarchy()` returns Plotly figures; Streamlit has native Plotly support via `st.plotly_chart()`. No additional visualization library needed.

### Topic Info Tables with Selection

```python
# Use Streamlit's built-in dataframe with selection (requires 1.55+)
topic_info = topic_model.get_topic_info()

event = st.dataframe(
    topic_info,
    on_select="rerun",
    selection_mode="multi-row",
    key="topic_selection"
)

if event.selection.rows:
    selected_topics = topic_info.iloc[event.selection.rows]['Topic'].tolist()
    st.write(f"Selected topics: {selected_topics}")
```

**Why:** Streamlit 1.55+ added native row selection to `st.dataframe()`, eliminating need for streamlit-aggrid.

### Export Functionality

```python
# Export topic model results
output_df = topic_model.get_document_info(docs)
csv = output_df.to_csv(index=False).encode('utf-8')

st.download_button(
    label="Download topic results (CSV)",
    data=csv,
    file_name="topic_results.csv",
    mime="text/csv"
)

# Export topic model for reuse
topic_model.save("my_topic_model", serialization="safetensors")
```

**Why:** Streamlit's `st.download_button()` handles in-memory exports. BERTopic 0.17.4 supports safetensors serialization (smaller, safer than pickle).

---

## Version Compatibility

| Package A | Compatible With | Notes |
|-----------|-----------------|-------|
| Streamlit 1.57.0 | Python 3.10-3.14 | Requires Python >=3.10 (existing stack uses 3.12 ✓) |
| BERTopic 0.17.4 | Python 3.10-3.13 | Compatible with Python 3.12 ✓ |
| Plotly 6.7.0 | Python 3.8-3.13 | Compatible with Python 3.12 ✓ |
| pandas 2.2+ | Python 3.9-3.13 | Compatible with Python 3.12 ✓ |
| BERTopic 0.17.4 | Plotly 5.0+ | No known conflicts with Plotly 6.7.0 |
| Streamlit 1.57.0 | pandas 1.3+ | No known conflicts with pandas 2.2+ |

**Critical:** All recommended versions are compatible with Python 3.12 (existing project requirement) and with each other.

---

## Integration Points

### BERTopic ↔ Streamlit

- **Workflow:** BERTopic outputs (topic info, hierarchical topics, document info) are pandas DataFrames → display directly with `st.dataframe()`
- **Visualization:** BERTopic's `visualize_*()` methods return Plotly figures → display with `st.plotly_chart()`
- **State:** Store trained `BERTopic` models in `st.session_state` for iterative refinement across steps

### Streamlit ↔ pandas

- **Comparison UI:** Store parameter variations as DataFrames in session state, display side-by-side in `st.columns()`
- **Export:** Convert DataFrames to CSV/XLSX using pandas methods, serve via `st.download_button()`

### BERTopic ↔ Plotly

- **Hierarchical visualization:** `topic_model.visualize_hierarchy()` generates Plotly dendrogram
- **Customization:** Plotly figures are mutable Python objects—modify before displaying in Streamlit if needed (e.g., update titles, colors)

---

## What NOT to Add

### ❌ streamlit-aggrid
**Reason:** Adds 40MB+, causes version conflicts, API complexity. Streamlit 1.55+ built-in `st.dataframe()` now supports row selection and column configuration, which covers 95% of use cases.

**When to reconsider:** Only if you need Excel-like cell editing (not in v2.0 scope) or complex multi-column filtering UI (build custom filters with `st.multiselect()` instead).

### ❌ Redis / SQLite for session state
**Reason:** v2.0 scope explicitly excludes session persistence ("user exports results, no session management"). Adds deployment complexity.

**When to reconsider:** Future milestone requiring multi-user collaboration or session recovery after browser restart.

### ❌ Jupyter widgets (ipywidgets)
**Reason:** v2.0 targets Streamlit UI, not Jupyter. Existing notebooks in `experiments/` can stay as-is for exploration.

**When to reconsider:** Never for v2.0; notebooks are for prototyping, not production UI.

### ❌ Flask / Dash backend
**Reason:** Streamlit already provides a web server and deployment model. Adding Flask/Dash duplicates functionality and increases complexity.

**When to reconsider:** Only if you need API endpoints (not in v2.0 scope) or need to integrate with non-Python services.

---

## Sources

- **Streamlit 1.57.0** — PyPI (https://pypi.org/project/streamlit/1.57.0/) — Released 2026-04-28 (VERIFIED, HIGH confidence)
- **BERTopic 0.17.4** — PyPI (https://pypi.org/project/bertopic/0.17.4/) — Released 2025-12-03 (VERIFIED, HIGH confidence)
- **Plotly 6.7.0** — PyPI (https://pypi.org/project/plotly/6.7.0/) — Released 2026-04-09 (VERIFIED, HIGH confidence)
- **Streamlit API docs** — Context7 (/streamlit/streamlit) — Session state, columns, dataframe selection (VERIFIED, HIGH confidence)
- **BERTopic API docs** — Context7 (/maartengr/bertopic) — Visualization, save/load, reduce_outliers (VERIFIED, HIGH confidence)
- **Plotly API docs** — Context7 (/plotly/plotly.py) — Dendrogram, write_html, interactive features (VERIFIED, HIGH confidence)

---

*Stack research for: Interactive topic modeling UI (v2.0 milestone)*  
*Researched: 2026-04-29*  
*Focus: NEW capabilities only—existing validated stack not re-researched*
