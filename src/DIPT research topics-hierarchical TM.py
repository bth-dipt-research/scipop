#!/usr/bin/env python
# coding: utf-8

# In[1]:

from pathlib import Path
import io
import json
import hashlib
import sys
import shutil
import tempfile
import streamlit as st
import pandas as pd
from bertopic import BERTopic
from umap import UMAP
from hdbscan import HDBSCAN
from bertopic.vectorizers import ClassTfidfTransformer
from bertopic.representation import KeyBERTInspired
from sklearn.feature_extraction.text import CountVectorizer
from sentence_transformers import SentenceTransformer
from nltk.tokenize import sent_tokenize

# Import checkpoint manager
sys.path.insert(0, str(Path(__file__).parent))
from checkpoint_manager import (
    compute_dataset_fingerprint as cm_compute_fingerprint,
    save_checkpoint,
    load_checkpoint,
    list_checkpoints,
    validate_checkpoint_integrity
)


@st.cache_data
def load_dataframe(file_bytes: bytes, filename: str) -> pd.DataFrame:
    """Load DataFrame from uploaded file bytes. Cached to prevent re-reading on rerun."""
    if filename.endswith('.csv'):
        return pd.read_csv(io.BytesIO(file_bytes))
    elif filename.endswith('.xlsx'):
        return pd.read_excel(io.BytesIO(file_bytes))
    else:
        raise ValueError(f"Unsupported file type: {filename}")


# Note: Using checkpoint_manager.compute_dataset_fingerprint for all fingerprinting
# to ensure consistency with checkpoint validation


def goto(step: int):
    st.session_state.step = step
    st.rerun()


def cancel_upload_cb():
    st.session_state.step = 1
    st.session_state.uploaded = None
    st.session_state.pop('uploader', None)


if 'step' not in st.session_state:
    st.session_state.step = 1
if 'uploaded' not in st.session_state:
    st.session_state.uploaded = None
if 'df_filtered' not in st.session_state:
    st.session_state.df_filtered = None
if 'input' not in st.session_state:
    st.session_state.input = None
if 'dataset_fingerprint' not in st.session_state:
    st.session_state.dataset_fingerprint = None
if 'loaded_checkpoint' not in st.session_state:
    st.session_state.loaded_checkpoint = None
if 'available_checkpoints' not in st.session_state:
    st.session_state.available_checkpoints = []
if 'delete_confirm' not in st.session_state:
    st.session_state.delete_confirm = False

with st.sidebar:
    st.markdown("### Workflow Steps")
    
    # Define all 9 steps for v2.0 workflow
    workflow_steps = [
        ('1. Upload Data', 1),
        ('2. Filter Data', 2),
        ('3. Configure Model', 3),
        ('4. Train Model', 4),
        ('5. Visualize Results', 5),
        ('6. Reduce Outliers', 6),
        ('7. Refine Labels', 7),
        ('8. Curate Topics', 8),
        ('9. Export Results', 9),
    ]
    
    for label, step_num in workflow_steps:
        if st.session_state.step == step_num:
            # Current step: highlighted
            st.markdown(f"**→ {label}**")
        elif st.session_state.step > step_num:
            # Completed step: checkmark
            st.markdown(f"✓ {label}")
        else:
            # Future step: plain text
            st.markdown(f"  {label}")
    
    st.markdown("---")
    st.markdown("### Checkpoint Management")
    
    # Refresh available checkpoints
    st.session_state.available_checkpoints = list_checkpoints()
    
    if len(st.session_state.available_checkpoints) > 0:
        checkpoint_options = [
            f"{cp['dataset_name']} ({cp['timestamp']}) - {cp['topic_count']} topics"
            for cp in st.session_state.available_checkpoints
        ]
        
        selected_idx = st.selectbox(
            "Load checkpoint",
            range(len(checkpoint_options)),
            format_func=lambda i: checkpoint_options[i],
            key='checkpoint_selector'
        )
        
        if st.button("Load Selected", use_container_width=True):
            selected_checkpoint = st.session_state.available_checkpoints[selected_idx]
            checkpoint_path = Path(selected_checkpoint['path'])
            
            # Validate integrity first
            is_valid, errors = validate_checkpoint_integrity(checkpoint_path)
            if not is_valid:
                st.error(f"Checkpoint validation failed: {', '.join(errors)}")
            else:
                try:
                    config, metadata, model, embeddings, fingerprint = load_checkpoint(checkpoint_path)
                    
                    # Check dataset fingerprint match if data is loaded
                    if st.session_state.df_filtered is not None:
                        current_fingerprint = cm_compute_fingerprint(st.session_state.df_filtered)
                        if current_fingerprint != fingerprint:
                            st.error("❌ Dataset fingerprint mismatch! This checkpoint was created with different data. Please upload the original dataset or use a different checkpoint.")
                        else:
                            st.session_state.loaded_checkpoint = {
                                'config': config,
                                'metadata': metadata,
                                'model': model,
                                'embeddings': embeddings,
                                'fingerprint': fingerprint,
                                'path': checkpoint_path
                            }
                            st.success(f"✓ Loaded checkpoint: {metadata['dataset_name']}")
                            st.rerun()
                    else:
                        st.warning("⚠ Please upload and filter data first to validate checkpoint compatibility")
                except Exception as e:
                    st.error(f"Error loading checkpoint: {str(e)}")
        
        if st.button("Delete Selected", use_container_width=True, type="secondary"):
            selected_checkpoint = st.session_state.available_checkpoints[selected_idx]
            checkpoint_path = Path(selected_checkpoint['path'])
            
            if not st.session_state.delete_confirm:
                st.session_state.delete_confirm = True
                st.warning("⚠ Click Delete again to confirm permanent removal")
                st.rerun()
            else:
                try:
                    shutil.rmtree(checkpoint_path)
                    st.success(f"Deleted checkpoint: {selected_checkpoint['dataset_name']}")
                    st.session_state.delete_confirm = False
                    st.rerun()
                except Exception as e:
                    st.error(f"Error deleting checkpoint: {str(e)}")
                    st.session_state.delete_confirm = False
        
        if st.button("Export as ZIP", use_container_width=True, type="secondary"):
            selected_checkpoint = st.session_state.available_checkpoints[selected_idx]
            checkpoint_path = Path(selected_checkpoint['path'])
            
            try:
                # Create zip file in temp directory
                with tempfile.NamedTemporaryFile(delete=False, suffix='.zip') as tmp:
                    zip_path = tmp.name
                
                shutil.make_archive(zip_path.replace('.zip', ''), 'zip', checkpoint_path)
                
                with open(zip_path, 'rb') as f:
                    st.download_button(
                        label="Download ZIP",
                        data=f.read(),
                        file_name=f"{selected_checkpoint['dataset_name']}_{selected_checkpoint['timestamp']}.zip",
                        mime="application/zip",
                        use_container_width=True
                    )
            except Exception as e:
                st.error(f"Error creating ZIP: {str(e)}")
        
        # View Parameters - allow extracting config from checkpoint
        with st.expander("📋 View Parameters", expanded=False):
            selected_checkpoint = st.session_state.available_checkpoints[selected_idx]
            checkpoint_path = Path(selected_checkpoint['path'])
            
            try:
                config_file = checkpoint_path / 'config.json'
                metadata_file = checkpoint_path / 'metadata.json'
                
                if config_file.exists():
                    with open(config_file, 'r') as f:
                        config = json.load(f)
                    
                    st.markdown("**Model Configuration:**")
                    st.json(config)
                    
                    # Copy-friendly format
                    config_str = json.dumps(config, indent=2)
                    st.code(config_str, language='json')
                    
                    st.caption("💡 Copy these parameters to apply to a new dataset in Phase 08")
                else:
                    st.warning("Config file not found in checkpoint")
                
                if metadata_file.exists():
                    with open(metadata_file, 'r') as f:
                        metadata = json.load(f)
                    
                    st.markdown("**Metadata:**")
                    st.json(metadata)
                else:
                    st.warning("Metadata file not found in checkpoint")
                    
            except Exception as e:
                st.error(f"Error reading checkpoint files: {str(e)}")
    else:
        st.info("No saved checkpoints yet")


st.title('Scipop topic model generation')

# Show loaded checkpoint info if available
if st.session_state.loaded_checkpoint is not None:
    metadata = st.session_state.loaded_checkpoint['metadata']
    st.info(f"📋 Loaded checkpoint: **{metadata['dataset_name']}** ({metadata['timestamp']}) - {metadata['topic_count']} topics, {metadata.get('outlier_percentage', 0):.1f}% outliers")

if st.session_state.step == 1:
    st.header('Upload publication data')
    file = st.file_uploader('Choose a file',
                            type=['csv', 'xlsx'],
                            key='uploader')

    if file is not None:
        st.session_state.uploaded = file
        st.success(f'Uploaded: {file.name}')

        # Cache file bytes to prevent re-reading on rerun (per PITFALLS.md)
        file_bytes = file.read()
        df = load_dataframe(file_bytes, file.name)

        st.write('Data preview')
        st.dataframe(df)

        # Store in session state with existence guard
        if 'df' not in st.session_state or st.session_state.df is None:
            st.session_state.df = df

        # Compute dataset fingerprint for checkpoint validation (Phase 07)
        st.session_state.dataset_fingerprint = cm_compute_fingerprint(df)
        st.write(f'Dataset fingerprint: `{st.session_state.dataset_fingerprint[:16]}...`')

    cols = st.columns([1, 1])
    with cols[0]:
        st.button('Next', use_container_width=True,
                  on_click=lambda: goto(2),
                  disabled=(st.session_state.uploaded is None or 
                           'df' not in st.session_state or 
                           st.session_state.df is None))
    with cols[1]:
        st.button('Cancel', use_container_width=True,
                  on_click=cancel_upload_cb)
elif st.session_state.step == 2:
    df = st.session_state.df
    st.header('Select data')
    
    pbtype = 'PublicationType'
    if pbtype in df.keys():
        st.subheader('Filter by publication type')
        original_count = len(df)
        st.write(f'**Original dataset:** {original_count} publications')
        st.write(df[pbtype].value_counts())
        
        selected_pbtypes = st.multiselect(
            label='Select the publication types to include',
            options=sorted(set(df[pbtype])),
            help='Choose one or more publication types. Publications matching any selected type will be included.'
        )
        
        if selected_pbtypes:
            df = df[df[pbtype].isin(selected_pbtypes)]
            df = df.reset_index(drop=True)  # drop=True to avoid 'index' column pollution
            filtered_count = len(df)
            
            st.write('---')
            st.write(f'**Filtered dataset:** {filtered_count} publications')
            st.write(df[pbtype].value_counts())
            
            # Show delta with color coding
            delta = filtered_count - original_count
            if delta < 0:
                st.warning(f'Removed {abs(delta)} publications ({abs(delta)/original_count*100:.1f}%)')
            elif delta == 0:
                st.info('No publications removed (all types selected)')
        else:
            st.info('⚠️ No publication types selected. Please select at least one type to proceed.')
            df = pd.DataFrame()  # Empty DataFrame to prevent downstream errors
    else:
        st.info(f'Dataset contains {len(df)} publications (no PublicationType column found)')
    
    # Compute and display dataset fingerprint after publication type filtering
    # (Fingerprint reflects dataset identity = which publications, not feature selection = which columns)
    if len(df) > 0:
        st.session_state.dataset_fingerprint = cm_compute_fingerprint(df)
        st.write('---')
        st.info(f'**Dataset fingerprint:** `{st.session_state.dataset_fingerprint[:16]}...`')
        st.caption('↑ Fingerprint reflects which publications are included (changes with publication type filter)')
    
    st.subheader('Select input columns for topic modeling')
    
    # Only show column selection if we have a filtered dataset
    if len(df) > 0:
        default_input_columns = [i for i in ['Title', 'Abstract', 'Keywords'] if i in df.keys()]
        
        input_columns = st.multiselect(
            label='Select columns to use for topic modeling',
            options=[col for col in df.keys() if col not in ['index', 'level_0']],  # Exclude index artifacts
            default=default_input_columns,
            help='Select one or more text columns. Topic model will analyze the combined text from all selected columns.'
        )
        
        st.session_state.input = input_columns
        
        if input_columns:
            st.success(f'✓ {len(input_columns)} column(s) selected: {", ".join(input_columns)}')
            
            # Preview combined text length
            combined_text_sample = df[input_columns[0]].iloc[0] if len(df) > 0 else ""
            st.write(f'Sample from first publication: `{combined_text_sample[:100]}...`')
        else:
            st.warning('⚠️ No columns selected. Please select at least one text column to proceed.')
    else:
        st.error('Cannot select columns: no publications in filtered dataset.')
        st.session_state.input = []
    
    # Store filtered DataFrame for downstream use
    st.session_state.df_filtered = df
    
    st.write('---')
    cols = st.columns([2, 1])
    with cols[0]:
        # Show validation status
        ready = (
            st.session_state.df_filtered is not None and
            len(st.session_state.df_filtered) > 0 and
            st.session_state.input is not None and
            len(st.session_state.input) > 0
        )
        
        if ready:
            st.success(f'✓ Ready to proceed with {len(st.session_state.df_filtered)} publications')
        else:
            st.error('❌ Cannot proceed: select publication types and input columns')
    
    with cols[1]:
        st.button('Next', use_container_width=True,
                  on_click=lambda: goto(3),
                  disabled=not ready)


# # Making sure we have a paper id and create a citation id.

# # In[6]:


# missing_idx = -1
# df_filtered['citationid'] = ''

# for idx, row in df_filtered.iterrows():
#     paperid = row['PID']
#     if paperid == '' or pd.isna(paperid):
#         df_filtered.loc[idx, 'PID'] = missing_idx
#         missing_idx -= 1
#     # There is no check here if the Name field contains the data as expected.
#     names = [n.strip() for n in row['Name'].split(';')]
#     lastnames = [n.split(',')[0].strip().replace(' ', '') for n in names]
#     # Very crude way to make citation ids unique
#     citationid = f'{lastnames[0]}_{idx}_{row["Year"]}'
#     df_filtered.loc[idx, 'citationid'] = citationid


# # Concatenating title and abstract to get richer data.

# # In[7]:


# df_filtered['input'] = df_filtered['Title'].str.cat(df_filtered['Abstract'], sep='. ', na_rep='')


# # Filtering out some low signal terms.

# # In[8]:


# df_filtered['input'] = df_filtered['input'].str.replace(r'\b(?:software|software engineering|development|research)\b', '',
#                                                         case=False, regex=True).str.replace(r"\s+", " ",
#                                                         regex=True).str.strip()


# # Create the input for the topic model (individual sentences), keeping track from which document the sentences comes from.

# # In[9]:


# tmp = []
# for _, row in df_filtered.iterrows():
#     for idx, sentence in enumerate(sent_tokenize(row['input'])):
#         tmp.append({'paperid': int(row['PID']), 'sentenceid': idx, 'sentence': sentence})
# input = pd.DataFrame(tmp)
# input


# # In[10]:


# sentences = input['sentence'].tolist()


# # The goal of parameter selection is to reduce the number of papers without a relevant topic. Relevant topics are all topics, except those created by noise terms in abstracts. In other words, we want to reduce the number of outliers as much as possible while still preserving meaningful topics.
# #
# # Dimensionality reduction parameters (see https://umap-learn.readthedocs.io/en/latest/parameters.html):
# #
# # n_neighbours = 15 (default). Balance between local and global structure in the data. Low values = local structure, high values = global structure
# #
# # min_dist = 0.1 (default). Controls how tightly points are packed together. Lower values mean tighter clusters.
# #
# # n_components = 2 (default). Number of dimensions to reduce to. Lower leads to micro clusters, higher to outliers.

# # In[11]:


# umap_model = UMAP(n_neighbors=15, n_components=3, min_dist=0.0, metric='cosine', random_state=42)


# # In[13]:


# hdbscan_model = HDBSCAN(min_cluster_size=25, min_samples=20, prediction_data=True)
# vectorizer_model = CountVectorizer(stop_words="english", min_df=2, ngram_range=(1, 2))
# representation_model = KeyBERTInspired(nr_repr_docs=10, random_state=42)

# #model = 'all-MiniLM-L6-v2'
# model = 'all-mpnet-base-v2'
# sentence_model = SentenceTransformer(model)
# embeddings = sentence_model.encode(sentences, show_progress_bar=False)


# topic_model = BERTopic(
#         umap_model=umap_model,
#         hdbscan_model= hdbscan_model,
#         vectorizer_model=vectorizer_model,
#         representation_model=representation_model,
#         embedding_model=model,
#         calculate_probabilities=True
# )

# topics, probs = topic_model.fit_transform(sentences, embeddings)


# # In[14]:


# for _, row in topic_model.get_topic_info().iterrows():
#     print(f'Topic: {row["Topic"]} / Count: {row["Count"]} / {row["Representation"]}\n')


# # In[581]:


# topics_to_remove = {-1, 20, 23, 24, 25, 27, 38, 44}


# # In[316]:


# #topic_model.merge_topics(docs=sentences, topics_to_merge=topics_to_remove)


# # In[456]:


# #custom_labels = topic_model.generate_topic_labels(nr_words=5, topic_prefix=False)
# #topic_frequency = topic_model.get_topic_freq()
# #custom_labels = [f"{f}_{l}" for f, l in zip(topic_frequency['Count'], custom_labels)]
# #topic_model.set_topic_labels(custom_labels)


# # In[15]:


# hierarchical_topics = topic_model.hierarchical_topics(sentences)


# # In[628]:


# fig = topic_model.visualize_hierarchy(hierarchical_topics=hierarchical_topics, title='<b>Topics in DIPT publications 2020-2025 (n=385)</b>')
# fig.write_html('../data/dipt/topics.html')
# fig


# # In[17]:


# print(topic_model.get_topic_tree(hierarchical_topics))


# # In[620]:


# topic_model.get_topic_info(48)["Representation"][0]


# # In[583]:


# output = input
# output['topic'] = topics
# output['prob'] = [p.max() if p is not None else None for p in probs]


# # In[584]:


# output = output.merge(topic_model.get_topic_info(), left_on='topic', right_on='Topic', how='left')


# # In[585]:


# output_by_paper = output.groupby('paperid', as_index=False).agg(topics=('topic', list), representations=('Representation', list))


# # Find papers where the only topics are the ones that ought to be removed.

# # In[586]:


# no_topic_papers = 0
# for _, row in output_by_paper.iterrows():
#     relevant_topics = [x for x in set(row['topics']) if x not in topics_to_remove]
#     if len(relevant_topics) == 0:
#         pid = row["paperid"]
#         p = df_filtered.query('PID == @pid')
#         assert(len(p) == 1)
#         print(f'{row["paperid"]} / {p.iloc[0]["Title"]} / {row["topics"]}')
#         no_topic_papers +=1
# print(f'Papers with no relevant topics: {no_topic_papers} ({no_topic_papers/len(df_filtered)*100:.2f}%)')


# # In[587]:


# output_by_topic = output.groupby('topic', as_index=False)\
#                         .agg(\
#                             representation=('Representation', list),\
#                             papers=('paperid', lambda s: s.unique().tolist()),\
#                             numpapers=('paperid', 'nunique'))
# #output_by_topic.sort_values(by="numpapers", inplace=True, ascending=False)
# print(topics_to_remove)
# output_by_topic


# # In[621]:


# topics = {}
# topics['testing'] = set([46, 17, 26, 33, 19, 7, 43])
# topics['data'] = set([10, 3, 4, 40, 32])
# topics['codequality'] = set([21, 13])
# topics['security'] = set([35, 9, 31, 37, 30])
# topics['requirements'] = set([12, 15, 1, 6, 8, 47])
# topics['agile'] = set([16, 14, 2, 22])
# topics['mix'] = set([11, 39, 5, 28])
# topics['startups'] = set([41, 48])
# topics['researchmethods'] = set([42, 29, 36, 18, 9, 45, 34])


# # In[627]:


# for name, ids in topics.items():
#     mask = (
#         output_by_paper['topics']
#           .explode()
#           .isin(ids)
#           .groupby(level=0).any()
#     )

#     papers_subset = output_by_paper[mask]
#     papers = df_filtered.merge(papers_subset, left_on='PID', right_on='paperid', how='right')
#     papers[['citationid', 'Name', 'Year', 'Title', 'Abstract', 'FullTextLink']].to_csv(f'../data/dipt/{name}.csv', index=False)

