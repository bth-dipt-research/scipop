# Architecture Research: Interactive Topic Modeling UI

**Domain:** Interactive topic modeling workflow for ML-driven research synthesis
**Researched:** 2026-04-29
**Confidence:** HIGH

## Integration Context

**v2.0 is a STANDALONE tool**, not integrated with the v1.0 static site. The static site (Astro-based, GitHub Pages) remains separate. This milestone extends the existing Streamlit prototype into a complete interactive workflow that mirrors the notebook-based topic modeling process.

**Existing artifacts:**
- **Notebook workflow:** `experiments/BTH research topics.ipynb` — full iterative refinement process (UMAP/HDBSCAN tuning, outlier reduction, topic labeling, manual curation)
- **Partial Streamlit prototype:** `src/DIPT research topics-hierarchical TM.py` — upload + filtering only (steps 1-2 of ~8)
- **ML stack:** BERTopic 0.16.4, UMAP, HDBSCAN, KeyBERT, sentence-transformers
- **Static site:** `site/` directory (Astro 6 + GitHub Pages) — completely separate deployment

**Integration boundary:** NO integration with static site. New UI components extend Streamlit app only.

---

## System Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    UI Layer (Streamlit)                      │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐        │
│  │ Upload  │  │ Filter  │  │ Config  │  │Compare  │        │
│  │ (Step1) │  │ (Step2) │  │ (Step3) │  │ (Step4+)│        │
│  └────┬────┘  └────┬────┘  └────┬────┘  └────┬────┘        │
│       │            │            │            │              │
├───────┴────────────┴────────────┴────────────┴──────────────┤
│              State Management (st.session_state)             │
│   ┌────────────────────────────────────────────────────┐    │
│   │ workflow_step │ df │ df_filtered │ input_columns  │    │
│   │ topic_model_A │ topic_model_B │ selected_model   │    │
│   │ hierarchical_topics │ outlier_strategy │ curation │    │
│   └────────────────────────────────────────────────────┘    │
├─────────────────────────────────────────────────────────────┤
│              Caching Layer (st.cache_resource/data)          │
│   ┌─────────────────────┐  ┌──────────────────────────┐    │
│   │  Sentence Embeddings │  │  Trained Topic Models   │    │
│   │  (@cache_resource)   │  │  (@cache_resource)       │    │
│   └─────────────────────┘  └──────────────────────────┘    │
├─────────────────────────────────────────────────────────────┤
│                  ML Pipeline (BERTopic Stack)                │
│   ┌──────────┐  ┌──────────┐  ┌──────────┐                 │
│   │   UMAP   │  │ HDBSCAN  │  │ KeyBERT  │                 │
│   │ (dim red)│  │(cluster) │  │  (repr)  │                 │
│   └──────────┘  └──────────┘  └──────────┘                 │
├─────────────────────────────────────────────────────────────┤
│              Visualization Layer (Plotly)                    │
│   ┌──────────────────────┐  ┌──────────────────────────┐   │
│   │ Hierarchical Tree    │  │ Topic Info Tables        │   │
│   │ (st.plotly_chart)    │  │ (st.dataframe)           │   │
│   └──────────────────────┘  └──────────────────────────┘   │
├─────────────────────────────────────────────────────────────┤
│                Export Layer (Local Files)                    │
│   ┌──────────┐  ┌──────────┐  ┌──────────┐                 │
│   │ CSV      │  │   HTML   │  │  Pickle  │                 │
│   │ (papers) │  │ (viz)    │  │ (model)  │                 │
│   └──────────┘  └──────────┘  └──────────┘                 │
└─────────────────────────────────────────────────────────────┘
```

---

## New Components (v2.0)

### 1. Multi-Step Workflow Controller

**Purpose:** Orchestrate 7+ workflow steps with validation and navigation controls.

**Location:** Extended from existing `src/DIPT research topics-hierarchical TM.py`

**Responsibilities:**
- Maintain `st.session_state.step` (1=upload, 2=filter, 3=configure, 4=compare outliers, 5=compare labels, 6=curate, 7=quality check, 8=export)
- Validate prerequisites before allowing step progression
- Provide sidebar progress tracking with completion indicators
- Implement `goto(step)` navigation with state validation

**Implementation pattern:**
```python
# Step progression with validation
if st.session_state.step == 3:
    st.header('Configure Topic Model')
    # ... parameter UI ...
    
    if st.button('Train Model', disabled=not prerequisites_met()):
        # Train and advance
        st.session_state.step = 4
        st.rerun()
```

**State dependencies:**
- Step 1 → 2: requires `uploaded_file is not None`
- Step 2 → 3: requires `len(df_filtered) > 0 and len(input_columns) > 0`
- Step 3 → 4: requires `topic_model_trained is True`
- Step 4 → 5: requires `outlier_strategy_selected is not None`

---

### 2. Model Configuration Panel

**Purpose:** Collect UMAP, HDBSCAN, vectorizer, and embedding parameters.

**New state keys:**
```python
st.session_state.umap_params = {
    'n_neighbors': 15,
    'n_components': 5,
    'min_dist': 0.0,
    'metric': 'cosine'
}
st.session_state.hdbscan_params = {
    'min_cluster_size': 25,
    'min_samples': 20,
    'metric': 'euclidean'
}
st.session_state.vectorizer_params = {
    'stop_words': 'english',
    'min_df': 2,
    'ngram_range': (1, 2)
}
st.session_state.embedding_model = 'all-mpnet-base-v2'  # or 'all-MiniLM-L6-v2'
```

**UI pattern:**
```python
with st.expander("UMAP Parameters"):
    st.slider('n_neighbors', 5, 50, 15, key='umap_n_neighbors')
    st.slider('n_components', 2, 10, 5, key='umap_n_components')
    st.slider('min_dist', 0.0, 1.0, 0.0, key='umap_min_dist')
    st.selectbox('metric', ['cosine', 'euclidean'], key='umap_metric')
```

**Training trigger:**
```python
if st.button('Train Topic Model'):
    with st.spinner('Training model... (this may take several minutes)'):
        trained_model = train_model_cached(
            df_filtered, 
            input_columns,
            st.session_state.umap_params,
            st.session_state.hdbscan_params,
            st.session_state.vectorizer_params,
            st.session_state.embedding_model
        )
        st.session_state.topic_model = trained_model
        st.session_state.step = 4
        st.rerun()
```

---

### 3. Side-by-Side Comparison Views

**Purpose:** Display before/after or A/B comparisons at decision points.

**Comparison contexts:**
1. **Outlier reduction strategies** (Step 4): Compare original vs c-TF-IDF vs distributions strategy
2. **Topic labeling settings** (Step 5): Compare different `nr_words` values (3 vs 5 vs 7)
3. **Manual curation preview** (Step 6): Show topic structure before/after merge or removal

**Implementation pattern using `st.columns`:**
```python
# Outlier reduction comparison
col_before, col_after = st.columns(2)

with col_before:
    st.subheader('Before Outlier Reduction')
    outlier_count_before = (topics == -1).sum()
    st.metric('Outlier Documents', outlier_count_before)
    st.dataframe(topic_info_before)

with col_after:
    st.subheader('After Outlier Reduction')
    outlier_count_after = (new_topics == -1).sum()
    st.metric('Outlier Documents', outlier_count_after, 
              delta=outlier_count_after - outlier_count_before,
              delta_color='inverse')
    st.dataframe(topic_info_after)

# Selection UI
strategy = st.radio('Select approach:', 
                    ['Keep original', 'Use c-TF-IDF', 'Use distributions'])
```

**Topic labeling comparison using `st.tabs`:**
```python
tab3, tab5, tab7 = st.tabs(['3 words', '5 words', '7 words'])

with tab3:
    labels_3 = generate_labels(topic_model, nr_words=3)
    st.dataframe(labels_3)

with tab5:
    labels_5 = generate_labels(topic_model, nr_words=5)
    st.dataframe(labels_5)
```

---

### 4. Cached ML Operations

**Purpose:** Prevent redundant expensive computations during UI iteration.

**Cache strategy:**

**Use `@st.cache_resource` for:**
- Sentence transformer models (shared across all users, not serializable)
- Trained topic models (large object, expensive to recreate)

```python
@st.cache_resource
def load_embedding_model(model_name: str):
    """Cache sentence transformer — expensive to load"""
    from sentence_transformers import SentenceTransformer
    return SentenceTransformer(model_name)

@st.cache_resource
def train_topic_model(_df, input_cols, umap_params, hdbscan_params, 
                      vectorizer_params, embedding_model_name):
    """Cache trained model — expensive to fit"""
    # Prefix _df to skip hashing large dataframe
    # Use parameters for cache key specificity
    
    embedding_model = load_embedding_model(embedding_model_name)
    
    # Concatenate input columns
    docs = _df[input_cols].apply(lambda x: '. '.join(x.dropna()), axis=1).tolist()
    
    # Generate embeddings
    embeddings = embedding_model.encode(docs, show_progress_bar=True)
    
    # Build and train BERTopic
    umap_model = UMAP(**umap_params, random_state=42)
    hdbscan_model = HDBSCAN(**hdbscan_params, prediction_data=True)
    vectorizer_model = CountVectorizer(**vectorizer_params)
    representation_model = KeyBERTInspired(nr_repr_docs=10, random_state=42)
    
    topic_model = BERTopic(
        umap_model=umap_model,
        hdbscan_model=hdbscan_model,
        vectorizer_model=vectorizer_model,
        representation_model=representation_model,
        embedding_model=embedding_model_name,
        calculate_probabilities=True
    )
    
    topics, probs = topic_model.fit_transform(docs, embeddings)
    
    return topic_model, topics, probs, embeddings
```

**Use `@st.cache_data` for:**
- DataFrame transformations
- Outlier reduction results
- Topic label generation

```python
@st.cache_data
def reduce_outliers_cached(_topic_model, docs, topics, strategy='c-tf-idf'):
    """Cache outlier reduction — moderately expensive"""
    return _topic_model.reduce_outliers(docs, topics, strategy=strategy)

@st.cache_data
def generate_hierarchical_topics(_topic_model, docs):
    """Cache hierarchical structure — expensive computation"""
    return _topic_model.hierarchical_topics(docs)
```

**Cache clearing:**
```python
# Manual cache clear button
if st.button('Reset Model Cache'):
    train_topic_model.clear()
    st.cache_resource.clear()
    st.success('Cache cleared. Next training will be from scratch.')
```

---

### 5. Manual Topic Curation Interface

**Purpose:** Allow merge/remove operations with impact preview.

**State structure:**
```python
st.session_state.topics_to_remove = set()  # {-1, 20, 23, 24, ...}
st.session_state.topics_to_merge = []      # [[5, 12], [7, 18, 33], ...]
st.session_state.custom_labels = {}        # {3: 'Testing & QA', 5: 'Data Engineering'}
```

**UI pattern:**
```python
st.subheader('Topic Curation')

# Display current topics with controls
topic_info = st.session_state.topic_model.get_topic_info()

for idx, row in topic_info.iterrows():
    topic_id = row['Topic']
    if topic_id == -1:
        continue  # Skip outlier topic
    
    col1, col2, col3, col4 = st.columns([1, 3, 2, 1])
    
    with col1:
        st.write(f"**Topic {topic_id}**")
    
    with col2:
        st.write(row['Representation'])
    
    with col3:
        st.text_input(f'Custom label', key=f'label_{topic_id}',
                     placeholder='Optional custom name')
    
    with col4:
        if st.checkbox('Remove', key=f'remove_{topic_id}'):
            st.session_state.topics_to_remove.add(topic_id)

# Merge interface
st.subheader('Merge Topics')
merge_from = st.multiselect('Select topics to merge', 
                            options=topic_info['Topic'].tolist())
if len(merge_from) > 1:
    if st.button('Preview Merge'):
        # Show what merge would produce
        merged_representation = preview_merge(merge_from)
        st.write(f'Merged representation: {merged_representation}')
```

**Impact preview:**
```python
# Show papers affected by removal
if st.session_state.topics_to_remove:
    st.subheader('Removal Impact Preview')
    
    # Count papers that would lose all topics
    papers_without_topics = count_papers_losing_all_topics(
        st.session_state.output_by_paper,
        st.session_state.topics_to_remove
    )
    
    st.metric('Papers losing all topics', papers_without_topics,
              help='These papers will have no topic after removal')
    
    # Show sample papers
    if papers_without_topics > 0:
        st.warning(f'⚠️ {papers_without_topics} papers will have no topics')
        show_affected_papers(limit=5)
```

---

### 6. Hierarchical Topic Visualization

**Purpose:** Render interactive Plotly dendrogram of topic hierarchy.

**Implementation:**
```python
@st.cache_data
def generate_hierarchy_viz(_topic_model, docs, title='Topic Hierarchy'):
    """Generate Plotly hierarchical visualization"""
    hierarchical_topics = _topic_model.hierarchical_topics(docs)
    fig = _topic_model.visualize_hierarchy(
        hierarchical_topics=hierarchical_topics,
        title=f'<b>{title}</b>',
        width=1200,
        height=800
    )
    return fig

# In UI
if st.session_state.topic_model is not None:
    st.subheader('Topic Hierarchy')
    
    docs = st.session_state.df_filtered[st.session_state.input_columns]\
           .apply(lambda x: '. '.join(x.dropna()), axis=1).tolist()
    
    fig = generate_hierarchy_viz(
        st.session_state.topic_model,
        docs,
        title='Topics in Research Publications'
    )
    
    st.plotly_chart(fig, use_container_width=True, key='hierarchy_chart')
```

**Plotly configuration:**
```python
# Enable full interactivity
config = {
    'displayModeBar': True,
    'displaylogo': False,
    'toImageButtonOptions': {
        'format': 'png',
        'filename': 'topic_hierarchy',
        'height': 1200,
        'width': 1600,
        'scale': 2
    }
}
st.plotly_chart(fig, use_container_width=True, config=config)
```

---

### 7. Export Generation

**Purpose:** Generate CSV, HTML, and model artifacts for downstream use.

**Export outputs:**
1. **Topic info table** (CSV) — topic IDs, counts, representations
2. **Papers by topic** (CSV) — paper metadata + assigned topics
3. **Themed paper sets** (multiple CSVs) — papers grouped by manual topic themes
4. **Hierarchical visualization** (HTML) — standalone interactive viz
5. **Trained model** (pickle) — BERTopic model object for reuse

**Implementation:**
```python
def generate_exports():
    """Create all export artifacts"""
    base_path = Path('../data/exports') / datetime.now().strftime('%Y%m%d_%H%M%S')
    base_path.mkdir(parents=True, exist_ok=True)
    
    # 1. Topic info
    topic_info = st.session_state.topic_model.get_topic_info()
    topic_info.to_csv(base_path / 'topic_info.csv', index=False)
    
    # 2. Papers with topics
    output = st.session_state.df_filtered.copy()
    output['topics'] = st.session_state.topics
    output['topic_probs'] = [p.max() if p is not None else None 
                             for p in st.session_state.probs]
    output.to_csv(base_path / 'papers_with_topics.csv', index=False)
    
    # 3. Themed paper sets
    if st.session_state.topic_themes:
        for theme_name, topic_ids in st.session_state.topic_themes.items():
            themed_papers = filter_papers_by_topics(output, topic_ids)
            themed_papers.to_csv(base_path / f'{theme_name}.csv', index=False)
    
    # 4. HTML visualization
    fig = generate_hierarchy_viz(st.session_state.topic_model, docs)
    fig.write_html(base_path / 'topic_hierarchy.html')
    
    # 5. Model pickle
    with open(base_path / 'topic_model.pkl', 'wb') as f:
        pickle.dump(st.session_state.topic_model, f)
    
    return base_path

# In UI
st.subheader('Export Results')

if st.button('Generate Exports', type='primary'):
    with st.spinner('Generating export files...'):
        export_path = generate_exports()
    st.success(f'✅ Exports saved to: {export_path}')
    st.info('Files: topic_info.csv, papers_with_topics.csv, '
            'topic_hierarchy.html, topic_model.pkl')
```

**Download buttons for individual files:**
```python
# Provide in-browser download
topic_info_csv = st.session_state.topic_model.get_topic_info().to_csv(index=False)
st.download_button(
    label='Download Topic Info (CSV)',
    data=topic_info_csv,
    file_name='topic_info.csv',
    mime='text/csv'
)

# HTML viz download
fig = generate_hierarchy_viz(st.session_state.topic_model, docs)
html_str = fig.to_html()
st.download_button(
    label='Download Hierarchy Visualization (HTML)',
    data=html_str,
    file_name='topic_hierarchy.html',
    mime='text/html'
)
```

---

## Modified Components (Existing → Extended)

### 1. Upload and Filtering (Steps 1-2)

**Current state:** Already implemented in prototype
**Modifications needed:** Minimal — just ensure state keys align with new workflow

**Existing code to preserve:**
```python
# Step 1: Upload
if st.session_state.step == 1:
    file = st.file_uploader('Choose a file', type=['csv', 'xlsx'])
    if file is not None:
        st.session_state.uploaded = file
        if file.name.endswith('.csv'):
            df = pd.read_csv(file)
        else:
            df = pd.read_excel(file)
        st.session_state.df = df

# Step 2: Filter
elif st.session_state.step == 2:
    df = st.session_state.df
    # Publication type filtering
    if 'PublicationType' in df.keys():
        selected_pbtypes = st.multiselect(
            label='Select publication types',
            options=set(df['PublicationType'])
        )
        df = df[df['PublicationType'].isin(selected_pbtypes)]
    
    # Input column selection
    input_columns = st.multiselect(
        label='Select input columns for topic model',
        options=df.keys(),
        default=[c for c in ['Title', 'Abstract'] if c in df.keys()]
    )
    
    st.session_state.df_filtered = df
    st.session_state.input_columns = input_columns
```

**No breaking changes needed** — just extend with new steps.

### 2. Session State Initialization

**Current initialization:**
```python
if 'step' not in st.session_state:
    st.session_state.step = 1
if 'uploaded' not in st.session_state:
    st.session_state.uploaded = None
if 'df_filtered' not in st.session_state:
    st.session_state.df_filtered = None
if 'input' not in st.session_state:
    st.session_state.input = None
```

**Extended initialization:**
```python
# Existing keys
if 'step' not in st.session_state:
    st.session_state.step = 1
if 'uploaded' not in st.session_state:
    st.session_state.uploaded = None
if 'df_filtered' not in st.session_state:
    st.session_state.df_filtered = None
if 'input_columns' not in st.session_state:
    st.session_state.input_columns = None

# New keys for v2.0
if 'topic_model' not in st.session_state:
    st.session_state.topic_model = None
if 'topics' not in st.session_state:
    st.session_state.topics = None
if 'probs' not in st.session_state:
    st.session_state.probs = None
if 'embeddings' not in st.session_state:
    st.session_state.embeddings = None
if 'hierarchical_topics' not in st.session_state:
    st.session_state.hierarchical_topics = None
if 'outlier_strategy' not in st.session_state:
    st.session_state.outlier_strategy = None
if 'topics_to_remove' not in st.session_state:
    st.session_state.topics_to_remove = set()
if 'topics_to_merge' not in st.session_state:
    st.session_state.topics_to_merge = []
if 'custom_labels' not in st.session_state:
    st.session_state.custom_labels = {}
if 'topic_themes' not in st.session_state:
    st.session_state.topic_themes = {}
```

### 3. Progress Sidebar

**Current progress tracking:**
```python
with st.sidebar:
    st.markdown("### Progress")
    steps = [
        ('Upload data', st.session_state.step > 1),
        ('Select data', st.session_state.step > 2),
    ]
    for label, done in steps:
        icon = ':material/check:' if done else ':material/hourglass:'
        color = 'green' if done else 'orange'
        st.badge(label, icon=icon, color=color)
```

**Extended progress tracking:**
```python
with st.sidebar:
    st.markdown("### Progress")
    steps = [
        ('1. Upload data', st.session_state.step > 1),
        ('2. Filter data', st.session_state.step > 2),
        ('3. Configure model', st.session_state.step > 3),
        ('4. Compare outlier strategies', st.session_state.step > 4),
        ('5. Compare topic labels', st.session_state.step > 5),
        ('6. Curate topics', st.session_state.step > 6),
        ('7. Quality check', st.session_state.step > 7),
        ('8. Export results', st.session_state.step > 8),
    ]
    for label, done in steps:
        icon = ':material/check:' if done else ':material/hourglass:'
        color = 'green' if done else 'orange'
        st.badge(label, icon=icon, color=color)
```

---

## Data Flow (Complete Workflow)

### Full Pipeline Flow

```
[User uploads CSV/XLSX]
    ↓
[Step 1: Upload] → st.session_state.df
    ↓
[Step 2: Filter] → st.session_state.df_filtered, input_columns
    ↓
[Step 3: Configure] → umap_params, hdbscan_params, vectorizer_params, embedding_model
    ↓
[Cache: Load Embeddings] → @st.cache_resource(load_embedding_model)
    ↓
[Cache: Train Model] → @st.cache_resource(train_topic_model)
    ↓ (stores in session_state)
topic_model, topics, probs, embeddings
    ↓
[Step 4: Compare Outliers] → Side-by-side display of strategies
    ↓ (user selects)
outlier_strategy → new_topics
    ↓
[Step 5: Compare Labels] → Tabs showing nr_words=3,5,7
    ↓ (user selects)
topic_labels (applied to model)
    ↓
[Step 6: Curate Topics] → topics_to_remove, topics_to_merge, custom_labels
    ↓ (show impact preview)
papers_without_topics (quality check)
    ↓
[Step 7: Quality Check] → Display affected papers, warnings
    ↓ (user confirms)
[Step 8: Export] → CSV, HTML, Pickle files
    ↓
[Local filesystem: data/exports/YYYYMMDD_HHMMSS/]
```

### State Dependencies

| Step | Prerequisites | Produces | Validates |
|------|--------------|----------|-----------|
| 1. Upload | None | `df` | File format, data preview |
| 2. Filter | `df` exists | `df_filtered`, `input_columns` | Row count > 0, columns exist |
| 3. Configure | `df_filtered`, `input_columns` | `topic_model`, `topics`, `probs` | Parameters reasonable, training succeeds |
| 4. Outlier Compare | `topic_model`, `topics` | `outlier_strategy`, `new_topics` | Strategy applied successfully |
| 5. Label Compare | `topic_model` | `selected_nr_words`, `custom_labels` | Labels generated |
| 6. Curate | `topic_model`, `topics` | `topics_to_remove`, `topics_to_merge` | User selections recorded |
| 7. Quality Check | `topics_to_remove` | `papers_without_topics` | Impact calculated, warnings shown |
| 8. Export | `topic_model`, final state | CSV/HTML/PKL files | Files written successfully |

---

## Architectural Patterns

### Pattern 1: Step-Wizard with Session State

**What:** Multi-step workflow where each step is a conditional block driven by `st.session_state.step`

**When to use:** Linear workflows with clear prerequisites and validation gates

**Trade-offs:**
- ✅ **Pro:** Simple mental model, easy debugging, clear progression logic
- ✅ **Pro:** State persists across reruns naturally
- ❌ **Con:** All steps in one file can grow large (mitigate with helper functions)
- ❌ **Con:** No built-in step history/undo (must implement manually)

**Example:**
```python
if st.session_state.step == 1:
    # Upload UI
    if upload_valid():
        st.button('Next', on_click=lambda: goto(2))

elif st.session_state.step == 2:
    # Filter UI
    if filter_valid():
        st.button('Next', on_click=lambda: goto(3))
```

### Pattern 2: Cached ML Pipeline Components

**What:** Expensive operations (embeddings, model training) wrapped in `@st.cache_resource` to avoid recomputation

**When to use:** Operations that are deterministic given inputs and take >2 seconds

**Trade-offs:**
- ✅ **Pro:** Massive performance improvement (10+ seconds → instant on reruns)
- ✅ **Pro:** Enables responsive UI during parameter exploration
- ❌ **Con:** Cache invalidation complexity if parameters change subtly
- ❌ **Con:** Memory usage grows with cached objects (clear periodically)

**Cache key strategy:**
```python
@st.cache_resource
def train_model(_df, params_dict):
    # _df prefix skips hashing (large dataframe)
    # params_dict hashed for cache key
    ...
```

### Pattern 3: Side-by-Side Comparison with Columns

**What:** Use `st.columns([1,1])` to display before/after or A/B views with selection UI below

**When to use:** Decision points where users need visual comparison to choose

**Trade-offs:**
- ✅ **Pro:** Clear visual comparison, intuitive for users
- ✅ **Pro:** Works well on desktop (most ML users)
- ❌ **Con:** Degrades on mobile (columns stack vertically)
- ❌ **Con:** Limited to 2-3 options before cluttered (use tabs for 4+)

**Example:**
```python
col_a, col_b = st.columns(2)
with col_a:
    st.subheader('Option A')
    st.metric('Outliers', outliers_a)
with col_b:
    st.subheader('Option B')
    st.metric('Outliers', outliers_b)

choice = st.radio('Select:', ['A', 'B'])
```

### Pattern 4: Incremental Refinement with Preview

**What:** Show impact of changes before committing (e.g., topic removal preview)

**When to use:** Destructive or complex operations where users need confidence before applying

**Trade-offs:**
- ✅ **Pro:** Reduces mistakes, builds user trust
- ✅ **Pro:** Allows exploration without fear of breaking state
- ❌ **Con:** Requires computing preview (can be slow)
- ❌ **Con:** More complex state management (preview vs applied)

**Example:**
```python
if st.button('Preview Removal'):
    st.session_state.removal_preview = compute_impact(
        st.session_state.topics_to_remove
    )
    
if st.session_state.removal_preview:
    st.warning(f'{preview.papers_affected} papers will lose topics')
    if st.button('Confirm Removal'):
        apply_removal(st.session_state.topics_to_remove)
```

---

## Scaling Considerations

| Scale | Approach | Notes |
|-------|----------|-------|
| **100-1,000 papers** | Single-user Streamlit, local execution | Current scope; fast enough on laptop |
| **1,000-10,000 papers** | Add progress bars, consider sentence-level batching for embeddings | May hit memory limits; chunk embedding generation |
| **10,000+ papers** | Move to notebook/script for training, load pre-trained model in Streamlit | UI becomes too slow for full pipeline; separate train/explore |

**Current architecture supports 100-1,000 papers well.** Beyond this, consider:
1. **Pre-compute embeddings** in batch script, load in UI
2. **Limit comparison views** to summary statistics rather than full dataframes
3. **Add progress indicators** for long operations (embedding, training)

**DO NOT prematurely optimize for 10K+ papers** — v2.0 scope is iterative refinement on typical research corpus (hundreds of papers).

---

## Anti-Patterns

### Anti-Pattern 1: Training Models on Every Rerun

**What people do:** Call `topic_model.fit_transform()` at module level or without caching

**Why it's wrong:** Streamlit reruns on every interaction; training takes minutes and will block all UI updates

**Do this instead:**
```python
# ❌ Bad
topic_model.fit_transform(docs)  # Runs every rerun!

# ✅ Good
@st.cache_resource
def train_model(_docs, params):
    return topic_model.fit_transform(_docs)

model = train_model(docs, params)
```

### Anti-Pattern 2: Storing Large DataFrames in Session State

**What people do:** Store full dataframe copies in `st.session_state` for every intermediate step

**Why it's wrong:** Memory usage grows, serialization overhead on state updates

**Do this instead:**
```python
# ❌ Bad
st.session_state.df_step3 = df.copy()
st.session_state.df_step4 = df.copy()

# ✅ Good
# Store only minimal state (indices, filters)
st.session_state.df_filtered_indices = df.index.tolist()

# Recompute when needed
df_filtered = st.session_state.df.loc[st.session_state.df_filtered_indices]
```

### Anti-Pattern 3: No Validation Between Steps

**What people do:** Allow progression to next step without checking prerequisites

**Why it's wrong:** Leads to cryptic errors, poor UX, broken workflows

**Do this instead:**
```python
# ❌ Bad
st.button('Next', on_click=lambda: goto(3))

# ✅ Good
next_enabled = (
    st.session_state.df_filtered is not None and
    len(st.session_state.df_filtered) > 0 and
    len(st.session_state.input_columns) > 0
)
st.button('Next', on_click=lambda: goto(3), disabled=not next_enabled)

if not next_enabled:
    st.info('Select at least one input column to continue')
```

### Anti-Pattern 4: Inline Complex Logic in UI Code

**What people do:** Write 100+ line functions directly in step blocks

**Why it's wrong:** Hard to test, debug, or reuse; mixing UI and business logic

**Do this instead:**
```python
# ❌ Bad
if st.session_state.step == 6:
    # 200 lines of curation logic inline...

# ✅ Good
# Extract to helper functions
def compute_removal_impact(topics_to_remove, output_by_paper):
    """Returns count and list of affected papers"""
    ...

# Keep UI code clean
if st.session_state.step == 6:
    impact = compute_removal_impact(
        st.session_state.topics_to_remove,
        st.session_state.output_by_paper
    )
    st.metric('Affected Papers', impact['count'])
```

---

## Integration Points

### Internal Boundaries

| Boundary | Communication | Notes |
|----------|---------------|-------|
| **UI ↔ State** | `st.session_state` dict | All workflow state stored here; UI reads/writes directly |
| **State ↔ ML Pipeline** | Function parameters | Pass params from state to cached functions |
| **ML Pipeline ↔ Cache** | `@st.cache_resource` decorator | Cache wraps expensive operations |
| **Export ↔ Filesystem** | Direct file writes to `data/exports/` | No integration with static site; local-only |

### External Services

| Service | Integration Pattern | Notes |
|---------|---------------------|-------|
| **Sentence Transformers** | Load via `SentenceTransformer(model_name)` | Hugging Face model download on first use |
| **BERTopic** | Direct API (`BERTopic().fit_transform()`) | Pure Python, no external service |
| **Plotly** | `st.plotly_chart(fig)` | Client-side rendering in browser |

**No external API calls** — entire pipeline runs locally.

---

## Deployment Considerations

### v2.0 Deployment: Standalone Streamlit App

**NOT deployed to GitHub Pages** (Pages is for static site only).

**Options for v2.0:**
1. **Local execution only** (MVP scope) — `streamlit run src/DIPT\ research\ topics-hierarchical\ TM.py`
2. **Streamlit Community Cloud** (if sharing needed) — free hosting for public repos
3. **Docker + self-hosted** (if data privacy required) — run on research group's infrastructure

**Recommended for v2.0 MVP:** Local execution only. No deployment complexity.

**If future sharing needed:**
```bash
# Streamlit Community Cloud deployment
# 1. Push code to GitHub
# 2. Connect repo at share.streamlit.io
# 3. Select entry file: src/DIPT research topics-hierarchical TM.py
# 4. Deploy (auto-installs from requirements.txt)
```

**Requirements:**
```txt
streamlit==1.50.0
bertopic==0.16.4
pandas>=2.0.0
plotly>=5.0.0
sentence-transformers>=2.0.0
umap-learn>=0.5.0
hdbscan>=0.8.0
scikit-learn>=1.3.0
nltk>=3.9.0
```

---

## Build Order (Suggested)

### Phase 1: Core Workflow Extension (Steps 3-5)

**Build order:**
1. **Session state initialization** — Add new keys for topic model, params, results
2. **Step 3: Model configuration UI** — Parameter collection for UMAP/HDBSCAN/vectorizer
3. **Cached training function** — `@st.cache_resource` wrapper for model training
4. **Step 4: Outlier comparison** — Side-by-side original vs c-TF-IDF vs distributions
5. **Step 5: Label comparison** — Tabs for nr_words=3,5,7

**Validation:** Can train model and compare outlier strategies

### Phase 2: Curation and Quality (Steps 6-7)

**Build order:**
1. **Step 6: Topic curation UI** — Checkboxes for removal, multiselect for merging
2. **Removal impact calculation** — Helper function to compute affected papers
3. **Step 7: Quality check display** — Show papers losing all topics with warnings
4. **Preview functionality** — Before/after comparison for merge operations

**Validation:** Can curate topics and see impact before applying

### Phase 3: Visualization and Export (Step 8)

**Build order:**
1. **Hierarchical visualization** — Plotly chart integration with caching
2. **Export generation** — CSV, HTML, pickle file creation
3. **Download buttons** — In-browser download for individual files
4. **Export success feedback** — Path display and file listing

**Validation:** Can generate complete export package

### Phase 4: Polish and Error Handling

**Build order:**
1. **Progress sidebar** — Update with all 8 steps
2. **Validation gates** — Disable buttons when prerequisites not met
3. **Error handling** — Try/except around training, clear error messages
4. **Help text** — Expanders with parameter explanations
5. **Cache management** — Manual cache clear button

**Validation:** Complete workflow runs smoothly with good UX

---

## File Structure Changes

**Before (v1.5):**
```
src/
└── DIPT research topics-hierarchical TM.py  # Steps 1-2 only
```

**After (v2.0):**
```
src/
├── DIPT research topics-hierarchical TM.py  # Extended to Steps 1-8
└── topic_model_utils.py                     # NEW: Helper functions
    ├── train_model_cached()
    ├── reduce_outliers_cached()
    ├── generate_hierarchical_viz()
    ├── compute_removal_impact()
    ├── generate_exports()
    └── count_papers_losing_all_topics()
```

**Recommendation:** Keep main file for UI, extract reusable logic to `topic_model_utils.py` to prevent 1000+ line monolith.

---

## Sources

### High Confidence
- Streamlit official docs (`/streamlit/streamlit` via Context7): Session state management, caching patterns (`@st.cache_resource`, `@st.cache_data`), layout components (`st.columns`, `st.tabs`), Plotly integration (`st.plotly_chart`)
- BERTopic official docs (`/maartengr/bertopic` via Context7): Hierarchical topics (`visualize_hierarchy`), outlier reduction strategies (`reduce_outliers`, c-TF-IDF, distributions), topic representation configuration
- Existing codebase: `src/DIPT research topics-hierarchical TM.py` (current implementation), `experiments/BTH research topics.ipynb` (target workflow), `.planning/codebase/ARCHITECTURE.md` (existing patterns)

### Medium Confidence
- Project context: `.planning/PROJECT.md` (milestone scope and out-of-scope items), `.planning/research/STACK.md` (v1.0 static site stack, deployment boundaries)

---

*Architecture research for: v2.0 Interactive Topic Modeling UI integration*
*Researched: 2026-04-29*
*Ready for roadmap: yes*
