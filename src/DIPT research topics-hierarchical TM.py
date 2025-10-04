#!/usr/bin/env python
# coding: utf-8

# In[1]:

from pathlib import Path
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

with st.sidebar:
    st.markdown("### Progress")
    steps = [
        ('Upload data', st.session_state.step > 1),
        ('Select data', st.session_state.step > 2),
        #("3. Train / Analyze", st.session_state.step > 3 or st.session_state.result is not None),
        #("4. Review results", st.session_state.step == 4),
    ]
    for label, done in steps:
        icon = ':material/check:' if done else ':material/hourglass:'
        color = 'green' if done else 'orange'
        st.badge(label, icon=icon, color=color)


st.title('Scipop topic model generation')

if st.session_state.step == 1:
    st.header('Upload publication data')
    file = st.file_uploader('Choose a file',
                            type=['csv', 'xlsx'],
                            key='uploader')

    if file is not None:
        st.session_state.uploaded = file
        st.success(f'Uploaded: {file.name}')

        if file.name.endswith('.csv'):
            df = pd.read_csv(file)
        else:
            df = pd.read_excel(file)

        st.write('Data preview')
        st.dataframe(df)

        st.session_state.df = df

    cols = st.columns([1, 1])
    with cols[0]:
        st.button('Next', use_container_width=True,
                  on_click=lambda: goto(2),
                  disabled=st.session_state.uploaded is None)
    with cols[1]:
        st.button('Cancel', use_container_width=True,
                  on_click=cancel_upload_cb)
elif st.session_state.step == 2:
    df = st.session_state.df
    st.header('Select data')
    st.write('Publication types in the data set')

    pbtype = 'PublicationType'
    if pbtype in df.keys():
        st.write(df[pbtype].value_counts())

        selected_pbtypes = st.multiselect(label='Select the publication types',
                                          options=set(df[pbtype]))

        df = df[df[pbtype].isin(selected_pbtypes)]
        df = df.reset_index()
        st.write('Publication types in the filtered data set')
        st.write(df[pbtype].value_counts())
        st.write(f'Total publications: {len(df)}')
    else:
        st.write(len(df))

    st.session_state.df_filtered = df

    default_input_columns = [i for i in ['Title', 'Abstract'] if i in df.keys()]
    input_columns = st.multiselect(
        label='Select the input columns for the topic model',
        options=df.keys(),
        default=default_input_columns)

    st.session_state.input = input_columns

    cols = st.columns([1])
    with cols[0]:
        st.button('Next', use_container_width=True,
                  on_click=lambda: goto(3),
                  disabled=len(st.session_state.df_filtered) == 0)


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

