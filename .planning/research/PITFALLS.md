# Pitfalls Research: Interactive Topic Modeling UI

**Domain:** Interactive topic modeling with BERTopic + Streamlit
**Researched:** 2026-04-29
**Confidence:** HIGH

## Critical Pitfalls

### Pitfall 1: Session State Rerun Race Conditions

**What goes wrong:**
Streamlit reruns the entire script from top to bottom on every interaction. When adding topic model results to session state during a long-running computation, the app may rerun before the computation completes, leading to incomplete or corrupted state. Users see partial results, missing visualizations, or exceptions when accessing expected state keys.

**Why it happens:**
Developers assume synchronous execution but Streamlit's rerun model is interruptive. Any widget interaction (button click, slider change) triggers an immediate rerun, even if a cached function is still computing. Session state mutations during computation can be overwritten by the rerun initialization.

**How to avoid:**
- Use status indicators (`st.spinner`, `st.status`) to show long-running operations
- Disable interactive widgets during computation using `disabled=True` parameter
- Store computation results in session state only after completion, not incrementally
- Use `st.cache_data` or `st.cache_resource` to prevent re-computation on rerun
- Guard all session state access with existence checks: `if 'key' not in st.session_state`

**Warning signs:**
- `KeyError` exceptions on session state access
- Widgets appear/disappear unexpectedly
- Results show from previous runs mixed with current run
- "Rerun requested while script was running" behaviors

**Phase to address:**
Phase 1 (Data Upload & Filtering) — Establish session state patterns early

---

### Pitfall 2: Memory Explosion from Uncached Embeddings

**What goes wrong:**
Generating sentence embeddings for thousands of documents on every rerun consumes 2-10 GB of memory and takes 30-120 seconds. Without caching, every parameter adjustment (UMAP n_neighbors, HDBSCAN min_cluster_size) regenerates embeddings from scratch. App becomes unusably slow and crashes with OOM errors on large datasets (>1000 documents).

**Why it happens:**
Sentence transformers (all-mpnet-base-v2, all-MiniLM-L6-v2) are computationally expensive. Developers focus on caching topic model fitting but forget embeddings are generated first. BERTopic's `embedding_model` parameter triggers embedding generation inside `fit_transform()`, which isn't cached automatically.

**How to avoid:**
- **Pre-compute and cache embeddings separately** before topic modeling:
  ```python
  @st.cache_resource
  def load_embedding_model():
      return SentenceTransformer('all-mpnet-base-v2')
  
  @st.cache_data
  def compute_embeddings(sentences, _model):  # underscore prefix = don't hash model
      return _model.encode(sentences, show_progress_bar=True)
  ```
- Pass pre-computed embeddings to BERTopic: `topic_model.fit_transform(docs, embeddings=cached_embeddings)`
- Set `BERTopic(embedding_model=None)` to prevent re-embedding
- Use `batch_size` parameter for large datasets: `model.encode(docs, batch_size=32)`
- Monitor memory with `st.sidebar.write(f"Memory: {psutil.Process().memory_info().rss / 1024**2:.0f} MB")`

**Warning signs:**
- App hangs for 30+ seconds on every parameter change
- Memory usage grows to 5-10 GB
- "ResourceExhausted" or "Killed" errors in logs
- Progress bars showing embedding generation repeatedly

**Phase to address:**
Phase 2 (Model Generation) — Cache embeddings before first model fit

---

### Pitfall 3: Outlier Removal Destroys Document-Topic Mapping

**What goes wrong:**
After removing outlier topics (topic ID = -1), papers that only appeared in outlier topics have no remaining topic assignments. Export CSVs contain papers with empty topic lists. Visualizations crash when filtering by topic. Quality checks show 10-30% of papers have "no relevant topics" but this isn't surfaced until post-export.

**Why it happens:**
Developers think of outlier removal as cleaning noise, but don't track which papers *only* exist in outlier topics. BERTopic assigns each sentence to exactly one topic. When you remove topic -1 and other noise topics, sentences from those topics don't get reassigned — they disappear from the topic model entirely.

**How to avoid:**
- **Track paper-topic coverage BEFORE removal**:
  ```python
  papers_by_topic = output.groupby('paperid')['topic'].apply(set)
  papers_at_risk = papers_by_topic[papers_by_topic.apply(
      lambda topics: topics.issubset(topics_to_remove)
  )]
  ```
- Show quality check UI: "Removing these topics will leave N papers without any topic assignments"
- Provide remediation options:
  - Lower HDBSCAN min_cluster_size to reduce outliers
  - Adjust UMAP parameters to improve clustering
  - Review papers at risk and decide if they're truly irrelevant
- Store outlier removal impact in session state for undo capability
- Build "papers with no topics" view BEFORE export phase

**Warning signs:**
- Large gaps in paper counts between upload and export
- CSV exports with empty topic columns
- User complaints: "Where did my papers go?"
- High percentage (>15%) of outlier assignments in initial clustering

**Phase to address:**
Phase 4 (Outlier Reduction) — Before allowing topic removal, show impact preview

---

### Pitfall 4: Comparison State Leakage Between Parameter Variations

**What goes wrong:**
Side-by-side parameter comparison shows the same results in both columns. User adjusts parameters (outlier reduction strategy A vs B, or nr_words=3 vs nr_words=5 for labels), but left and right columns display identical outputs. Clicking "Select left" applies the wrong parameters. Session state mixes up which model belongs to which comparison slot.

**Why it happens:**
Session state keys for comparison results use simple names like `model_left` and `model_right` without scoping to the comparison context. When rebuilding models based on user selections, the code overwrites previous comparison state. BERTopic models contain mutable internal state (topics_, labels_, hierarchy), and session state doesn't create copies — both `model_left` and `model_right` may reference the same object.

**How to avoid:**
- Use **namespaced session state keys** for comparison contexts:
  ```python
  st.session_state[f'comparison_{comparison_id}_left'] = model_left
  st.session_state[f'comparison_{comparison_id}_right'] = model_right
  ```
- Create **deep copies** of models for comparison: `copy.deepcopy(topic_model)`
- Store parameters alongside results:
  ```python
  st.session_state['comparison_left'] = {
      'model': model_left,
      'params': {'strategy': 'probabilities', 'threshold': 0.5},
      'timestamp': time.time()
  }
  ```
- Display parameter summary above each comparison column for verification
- Use `st.cache_data` for comparison computations with parameter-specific keys
- Clear previous comparison state before new comparison: `st.session_state.pop('comparison_*', None)`

**Warning signs:**
- Identical results in supposedly different comparisons
- Parameter changes don't affect comparison outputs
- Selected option applies opposite set of parameters
- Changing left side also changes right side

**Phase to address:**
Phase 4 (Outlier Reduction Comparison) & Phase 5 (Label Configuration Comparison) — Isolate comparison state

---

### Pitfall 5: Plotly Visualization Memory Leak on Rerun

**What goes wrong:**
After 10-20 parameter adjustments and reruns, Streamlit session memory grows to 2-3 GB. Hierarchical topic visualizations (`visualize_hierarchy()`) are regenerated on every rerun but previous Plotly figure objects aren't garbage collected. Browser tab slows down, eventually crashes with "Page unresponsive" error.

**Why it happens:**
Plotly figures for hierarchical topics contain thousands of data points and SVG elements. Each `topic_model.visualize_hierarchy()` call creates a new 10-50 MB figure object. Streamlit's `st.plotly_chart()` keeps references to previous figures in session until explicit cleanup. Session state stores entire figure objects instead of serialized HTML, preventing garbage collection.

**How to avoid:**
- **Cache visualization generation** separately from model fitting:
  ```python
  @st.cache_data(ttl=3600, max_entries=10)
  def generate_hierarchy_viz(_topic_model, _hierarchical_topics):
      fig = _topic_model.visualize_hierarchy(
          hierarchical_topics=_hierarchical_topics,
          title='Topic Hierarchy'
      )
      return fig.to_html(include_plotlyjs='cdn')  # Return HTML, not figure object
  ```
- Use `st.empty()` containers and replace content instead of appending:
  ```python
  viz_container = st.empty()
  with viz_container:
      st.plotly_chart(fig, use_container_width=True)
  ```
- Set `max_entries` on visualization caches to limit memory
- Store only serialized HTML in session state, not figure objects
- Use `fig.update_layout(autosize=True)` and limit data points for large hierarchies
- For very large topic models (>100 topics), generate static PNG instead of interactive Plotly

**Warning signs:**
- Memory usage grows continuously across reruns (monitor with `psutil`)
- Browser tab sluggish after multiple interactions
- "Out of memory" or tab crashes after 15-20 parameter changes
- Streamlit session size exceeds 1 GB (check `st.session_state` size)

**Phase to address:**
Phase 3 (Model Generation) & Phase 6 (Visualization) — Cache and limit visualization memory

---

### Pitfall 6: BERTopic Model Mutation Corrupts Cached State

**What goes wrong:**
After merging topics or updating labels, previous cached model states show the new labels. Comparison UI shows merged results in "before merge" column. Undo functionality fails because cached model was mutated in place. Users can't reproduce earlier results even with identical parameters.

**Why it happens:**
`st.cache_resource` returns the same object instance across all sessions without copying. BERTopic methods like `merge_topics()`, `set_topic_labels()`, and `update_topics()` mutate the model in place. When you modify a cached model, you're modifying the cached singleton. All references to that model now see the mutated state.

**How to avoid:**
- **Use `st.cache_data` for topic models** instead of `st.cache_resource`:
  ```python
  @st.cache_data  # Creates copy on return
  def fit_topic_model(sentences, embeddings, umap_params, hdbscan_params):
      topic_model = BERTopic(...)
      topics, probs = topic_model.fit_transform(sentences, embeddings)
      return topic_model, topics, probs
  ```
- If using `st.cache_resource` for memory efficiency, **deep copy before mutation**:
  ```python
  @st.cache_resource
  def get_base_model(...):
      return topic_model
  
  base_model = get_base_model(...)
  working_model = copy.deepcopy(base_model)  # Now safe to mutate
  working_model.merge_topics(...)
  ```
- Store mutation history in session state for undo:
  ```python
  st.session_state['model_history'] = [
      {'step': 'initial', 'model': copy.deepcopy(model)},
      {'step': 'merged_topics', 'model': copy.deepcopy(model), 'action': {...}}
  ]
  ```
- Document which BERTopic methods mutate vs. return new objects

**Warning signs:**
- "Before" and "after" comparisons show identical results
- Cannot reproduce earlier states with same parameters
- Undo button shows already-merged state
- Cached models change without cache invalidation

**Phase to address:**
Phase 5 (Label Configuration) & Phase 7 (Manual Curation) — Before any model mutation operations

---

### Pitfall 7: UMAP/HDBSCAN Parameter Coupling Creates Confusing Results

**What goes wrong:**
Users adjust UMAP `n_components` from 2 to 5 to "create more topics" but get *fewer* topics and more outliers. Changing HDBSCAN `min_cluster_size` from 25 to 15 creates 50 micro-clusters of 1-2 papers each. Parameter tooltips don't explain interdependencies. Users waste hours tweaking parameters randomly without understanding the combined effect.

**Why it happens:**
UMAP and HDBSCAN are tightly coupled: UMAP's output dimensionality and density structure directly affect HDBSCAN's ability to find clusters. Increasing `n_components` spreads points in higher-dimensional space, making HDBSCAN find fewer dense regions. Developers treat parameters as independent sliders without explaining the clustering pipeline: Embeddings → UMAP → HDBSCAN → Topics.

**How to avoid:**
- **Show parameter guidance in UI** with interdependency explanations:
  ```python
  st.info("""
  **Parameter relationships:**
  - Lower n_components (2-3) → Tighter clusters → More outliers
  - Higher n_components (5-10) → Spread points → Fewer large clusters
  - Lower min_cluster_size → More small clusters (risk: noise clusters)
  - Higher min_cluster_size → Fewer large clusters (risk: miss real topics)
  """)
  ```
- Provide **presets** for common scenarios:
  - "Conservative" (few large clusters): n_components=5, min_cluster_size=30
  - "Balanced" (default): n_components=3, min_cluster_size=20
  - "Granular" (many small clusters): n_components=2, min_cluster_size=10
- Show **real-time preview metrics** as parameters change:
  - Number of topics found
  - % of papers in outliers (topic -1)
  - Average cluster size
  - Outlier rate by publication type
- Link to "Understanding Topic Model Parameters" documentation
- Validate parameter combinations: warn if n_components=10 + min_cluster_size=5 (likely too many tiny clusters)

**Warning signs:**
- User adjusts sliders repeatedly without improving results
- Extreme parameter values (n_components=20, min_cluster_size=3)
- Support questions: "How do I get more topics?"
- 50+ micro-clusters or >50% outlier rate

**Phase to address:**
Phase 2 (Model Generation) — Before exposing raw parameters, add guidance and presets

---

### Pitfall 8: Sentence-Level Topics Don't Aggregate to Paper-Level Semantics

**What goes wrong:**
Topic model assigns each sentence to a topic independently. A single paper with abstract containing sentences about "testing", "data", and "security" gets split across three topics. Paper export lists all three topics but user expects one primary topic per paper. Themed CSV exports contain duplicate papers (appears in testing.csv AND security.csv). Synthesis generation fails because papers aren't cohesively grouped.

**Why it happens:**
Existing notebook workflow tokenizes abstracts into sentences for finer-grained topic detection (see line 166-168 in `src/DIPT research topics-hierarchical TM.py` comments). This improves topic modeling quality but creates paper-level aggregation complexity. Developers forget to build paper-level topic aggregation logic after sentence-level classification.

**How to avoid:**
- **Decide on primary aggregation strategy** and document in UI:
  - **Most frequent topic**: Paper's primary topic = topic with most sentences
  - **Highest probability**: Paper's primary topic = topic with highest avg probability across sentences
  - **Multi-label**: Keep all topics, but show primary + secondary
- Show aggregation preview before export:
  ```python
  paper_topics = df.groupby('paperid')['topic'].apply(
      lambda x: x.mode()[0]  # Most frequent
  )
  st.write(f"Papers with 1 topic: {sum(counts == 1)}")
  st.write(f"Papers with 2+ topics: {sum(counts > 1)}")
  ```
- Provide **filtering options** for themed CSV exports:
  - "Include papers where topic appears in any sentence"
  - "Include only papers where topic is primary"
  - "Include papers where topic appears in >50% of sentences"
- Store both sentence-level AND paper-level topic assignments in session state
- Show paper-level topic distribution before manual curation (helps identify split papers)

**Warning signs:**
- Paper appears in 3+ themed CSV exports
- Single paper has 5+ different topics in sentence view
- User confusion: "Why is this testing paper in the security CSV?"
- Low topic coherence in exported paper groups

**Phase to address:**
Phase 8 (Export) — Define aggregation strategy before CSV generation

---

## Technical Debt Patterns

| Shortcut | Immediate Benefit | Long-term Cost | When Acceptable |
|----------|-------------------|----------------|-----------------|
| Skip embedding caching, regenerate on each parameter change | Simpler code (no cache management) | 30-120 sec waits per interaction, OOM crashes on large datasets | Never — caching is table stakes |
| Store full BERTopic models in session state instead of just parameters | Easy access to all model methods | 100-500 MB memory per model, session state bloat, can't reproduce from params | Never for production; OK for prototype with <1000 docs |
| Use `st.cache_resource` for topic models to save memory | 50% less memory than `st.cache_data` | Model mutations corrupt cache, comparison states leak, irreproducible results | Only if models are >500 MB AND you never mutate (rare) |
| Single global "compare these two" state instead of scoped comparison contexts | Simpler state management (2 keys not N keys) | Can only compare one thing at a time, state leaks between comparisons | Early prototypes (Phase 1-3); must fix by Phase 4 |
| Show raw parameter sliders without presets or guidance | Faster to implement | Users waste hours tuning parameters randomly, support burden | Never — at minimum provide tooltips with ranges |
| Export themed CSVs with all papers mentioning topic (sentence-level) | Matches BERTopic output directly | Duplicate papers across CSVs, confusing for synthesis generation | OK if users understand multi-label nature; must document |
| Generate Plotly visualizations on every rerun without caching | Always fresh, simpler code | Memory leak after 10-20 interactions, browser crashes | Never — visualization generation is expensive |
| Reload full dataset from uploaded file on every parameter change | Consistent with upload state | Slow reruns, file upload widget flickers, loses filtering state | Never — cache DataFrame after upload/filtering |

---

## Integration Gotchas

| Integration | Common Mistake | Correct Approach |
|-------------|----------------|------------------|
| BERTopic + Streamlit session state | Storing entire `BERTopic` object directly in `st.session_state['model']` → can't access from different session, mutation issues | Cache model creation with `@st.cache_data`, store only parameters + trained state (topics, labels, hierarchical_topics) in session state |
| SentenceTransformer + caching | Caching embedding function without excluding model parameter: `@st.cache_data def embed(docs, model)` → UnhashableParamError | Use `@st.cache_resource` for model loading, `@st.cache_data` for embedding with `_model` parameter: `def embed(docs, _model)` |
| Plotly + Streamlit columns | Generating two Plotly figures in side-by-side columns without keys → figures swap positions on rerun, wrong figure in wrong column | Use `st.plotly_chart(fig, key=f'fig_{side}_{param_hash}')` with unique keys per column and parameter set |
| HDBSCAN + BERTopic | Passing `prediction_data=True` to HDBSCAN without realizing it doubles memory usage → OOM on large datasets | Only enable `prediction_data` if you need `.probabilities_` for new documents; disable for initial model fitting |
| UMAP + reproducibility | Not setting `random_state=42` in UMAP → different embeddings on each run, can't reproduce topic model | Always set `random_state` in UMAP, HDBSCAN, and BERTopic for reproducible results |
| Pandas + BERTopic output | Using `df.merge(topic_info)` without handling outlier topic -1 → KeyError or missing rows | Filter outliers before merge: `topic_info = topic_info[topic_info['Topic'] != -1]` or left join with `how='left'` |
| Streamlit file uploader + caching | Caching function that uses `st.file_uploader` return value directly → cannot hash `UploadedFile` | Read file into bytes first: `file_bytes = uploaded_file.read()`, then cache function takes bytes |

---

## Performance Traps

| Trap | Symptoms | Prevention | When It Breaks |
|------|----------|------------|----------------|
| Generating sentence embeddings on every parameter change | 30-120 sec waits, 100% CPU for 2 min, memory grows to 5+ GB | Cache embeddings separately with `@st.cache_data`, pass pre-computed embeddings to BERTopic | >500 documents with sentence-level tokenization |
| Regenerating hierarchical visualizations on every rerun | Slow reruns (5-10 sec), memory growth, browser lag | Cache visualization HTML with `@st.cache_data(ttl=3600)`, store HTML string not figure object | >50 topics in hierarchy |
| Storing full topic models in session state without garbage collection | Memory grows from 200 MB to 2 GB over 20 interactions, eventual crash | Use `st.cache_data` for models (auto-managed), or manually clear old models: `st.session_state.pop('old_model', None)` | >5 model variations stored in session |
| Reading uploaded CSV/XLSX on every rerun | 2-5 sec lag on every interaction, file uploader flickers | Cache DataFrame immediately after upload: `@st.cache_data def load_data(file_bytes, filename)` | Files >10 MB or >10,000 rows |
| Computing sentence tokenization on every rerun | 1-3 sec lag, blocks UI updates | Cache tokenized sentences: `@st.cache_data def tokenize(abstracts)` using NLTK sent_tokenize | >1000 documents |
| Filtering DataFrame in multiple places without caching | Repeated computation (10-50ms each), adds up across UI | Cache filtered DataFrame in session state after filtering step: `st.session_state['df_filtered']` | >5000 rows with complex filtering |
| Rendering 1000-row DataFrames with `st.dataframe` without pagination | Slow initial render, laggy scrolling, high memory | Use `st.dataframe(height=400)` + pagination: only show top N rows, provide download CSV button for full data | >1000 rows |
| Side-by-side comparison generating full topic models twice | 2-3 min wait for comparisons, 2x memory usage | Cache both model variations with parameter-specific keys, compute both in parallel with threading (if possible) | Parameter variations require full retraining |

---

## UX Pitfalls

| Pitfall | User Impact | Better Approach |
|---------|-------------|-----------------|
| No progress indication during 60-120 sec embedding generation | User thinks app is frozen, refreshes page, loses work | Use `st.status` with step-by-step updates: "Loading model (10s)... Generating embeddings (90s)... Clustering (20s)..." |
| Parameter sliders with no guidance on what values are reasonable | Random tweaking, frustration, poor results | Show recommended ranges in help tooltips, provide 3 presets (Conservative/Balanced/Granular), show live preview metrics |
| Comparison UI shows identical results but doesn't explain why | User thinks app is broken, loses trust | Add parameter diff summary at top: "Comparing: min_cluster_size 20 vs 30" with differences highlighted |
| Removing outlier topics without showing impact preview | User removes topics, 30% of papers vanish from export, confusion and frustration | Show "Impact Preview" before confirmation: "Removing these topics will leave 45 papers (12%) without any topic assignments. Continue?" |
| Export generates 8 CSV files with no explanation of what's in each | User opens 8 files trying to find their data, doesn't understand multi-label output | Provide export summary: "security.csv: 87 papers (primary topic: security)" + README.txt explaining aggregation logic |
| Side-by-side comparison but "Select left" button applies right parameters | User makes wrong choice, has to redo comparison, frustration | Show confirmation dialog: "Apply these parameters? - min_cluster_size: 20, min_samples: 15" with parameter summary |
| No way to undo topic merge or label change | User makes mistake, has to restart entire workflow (15+ min), high frustration | Store model history in session state, provide "Undo last action" button with stack of previous states |
| Upload 10,000-row CSV, app hangs for 5 minutes with no feedback | User thinks app crashed, closes tab and reports bug | Show upload progress: "Uploaded 10,000 rows... Validating columns... Filtering..." + estimated time remaining |

---

## "Looks Done But Isn't" Checklist

- [ ] **Embedding caching:** Verify embeddings are cached separately from model fitting — check cache hit logs, confirm no re-encoding on parameter changes
- [ ] **Session state initialization:** Every session state key has initialization guard (`if 'key' not in st.session_state`) — test by refreshing page mid-workflow
- [ ] **Outlier impact preview:** Before topic removal, app shows count of papers that will have no remaining topics — test with dataset where 50% of papers are in topic -1
- [ ] **Comparison state isolation:** Side-by-side comparisons use namespaced keys, verify left/right don't share references — test by making 3 comparisons in sequence
- [ ] **Visualization memory management:** Plotly figures are cached and old figures are cleared — monitor memory usage over 20 parameter changes
- [ ] **Paper-level aggregation logic:** Sentence-level topics are aggregated to paper level with documented strategy — verify paper doesn't appear in 5+ themed CSVs
- [ ] **Widget state during computation:** Interactive widgets are disabled during long operations — try clicking buttons during 60-sec embedding generation
- [ ] **Model mutation protection:** BERTopic models are deep copied before mutation or cached with `@st.cache_data` — test undo functionality and comparison consistency
- [ ] **Parameter validation:** UMAP/HDBSCAN parameter combinations are validated (e.g., reject n_components=20 + min_cluster_size=3) — test with extreme values
- [ ] **Upload state persistence:** Uploaded DataFrame is cached and doesn't reload on every parameter change — verify file uploader doesn't flicker on slider adjustment

---

## Recovery Strategies

| Pitfall | Recovery Cost | Recovery Steps |
|---------|---------------|----------------|
| Session state race condition corrupted state | LOW | Add initialization guards to all session state access, implement state validation on rerun, use `st.rerun()` to reset clean state |
| Memory explosion from uncached embeddings | LOW | Add `@st.cache_data` to embedding generation, pass `_model` parameter, test with small dataset first, add memory monitoring to sidebar |
| Outlier removal left papers without topics | MEDIUM | Add undo stack to session state, store model history before destructive operations, rebuild model from cached embeddings (2-5 min), implement impact preview UI |
| Comparison state leaked between variations | LOW | Refactor to namespaced keys (`comparison_{id}_left/right`), clear previous comparison state on new comparison, add parameter summary display |
| Plotly memory leak after 20 interactions | LOW | Cache visualization generation, convert to HTML string before storage, use `st.empty()` containers, add manual "Clear visualizations" button |
| BERTopic model mutation corrupted cache | HIGH | Switch to `@st.cache_data` (forces copy), add deep copy before all mutations, rebuild cache (30-60 min), document which methods mutate |
| UMAP/HDBSCAN parameters created 100 micro-clusters | LOW | Provide "Reset to defaults" button, show parameter presets, add validation warnings, explain parameter relationships in UI |
| Sentence-level topics don't aggregate correctly | MEDIUM | Implement paper-level aggregation function, add aggregation strategy selector to UI, regenerate themed CSVs with new logic, update export documentation |

---

## Pitfall-to-Phase Mapping

| Pitfall | Prevention Phase | Verification |
|---------|------------------|--------------|
| Session state rerun race conditions | Phase 1: Data Upload & Filtering | Run upload → filter → navigate back → verify state intact; monitor logs for KeyError exceptions |
| Memory explosion from uncached embeddings | Phase 2: Model Generation | Generate model with 1000 docs → adjust parameters → verify embeddings not regenerated (check timing and memory logs) |
| Outlier removal destroys document-topic mapping | Phase 4: Outlier Reduction | Remove outlier topics → verify "papers with no topics" count shown; test with dataset where 40% are in topic -1 |
| Comparison state leakage | Phase 4: Outlier Reduction Comparison | Create comparison → adjust parameters → verify left ≠ right; create 2nd comparison → verify doesn't affect 1st |
| Plotly visualization memory leak | Phase 3: Model Generation, Phase 6: Visualization | Generate model → adjust parameters 20 times → monitor memory (should stay <500 MB), check browser memory usage |
| BERTopic model mutation corrupts cache | Phase 5: Label Configuration, Phase 7: Manual Curation | Generate labels → merge topics → undo → verify returns to pre-merge state; compare "before" vs "after" columns |
| UMAP/HDBSCAN parameter coupling | Phase 2: Model Generation | Test with extreme parameters → verify validation warnings; provide presets → verify reasonable topic counts |
| Sentence-level topics don't aggregate | Phase 8: Export | Export themed CSVs → verify paper appears in ≤2 files; check aggregation strategy is documented in UI and README |

---

## Sources

**HIGH confidence sources:**
- [Streamlit Session State Documentation](https://docs.streamlit.io/develop/concepts/architecture/session-state) — Official guidance on session state persistence and limitations
- [Streamlit Caching Documentation](https://docs.streamlit.io/develop/concepts/architecture/caching) — Official guidance on `st.cache_data` vs `st.cache_resource`, mutation issues, memory management
- [BERTopic GitHub Repository](https://github.com/maartengr/bertopic) — Official documentation on caching, memory optimization, visualization performance
- [HDBSCAN Parameter Selection Guide](https://github.com/scikit-learn-contrib/hdbscan/blob/master/docs/parameter_selection.rst) — Official guidance on min_cluster_size and min_samples tuning
- [UMAP Parameter Guide](https://umap-learn.readthedocs.io) — Official documentation on n_neighbors, min_dist, n_components interdependencies

**MEDIUM confidence sources:**
- Context7 documentation queries for Streamlit, BERTopic, HDBSCAN, UMAP — Aggregated best practices and common patterns
- Existing scipop codebase analysis (`src/DIPT research topics-hierarchical TM.py`, `experiments/BTH research topics.ipynb`) — Real-world patterns and commenting showing known issues

**Domain expertise:**
- Interactive ML app patterns — Caching expensive operations, state management, comparison UI isolation
- Streamlit rerun model implications — Race conditions, widget state management, memory leaks
- Topic modeling workflow — Sentence vs document granularity, outlier handling, parameter interdependencies

---

*Pitfalls research for: Interactive Topic Modeling UI (scipop v2.0)*  
*Researched: 2026-04-29*  
*Confidence: HIGH — based on official documentation, real codebase patterns, and domain expertise*
