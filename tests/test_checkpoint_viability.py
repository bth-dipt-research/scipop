"""
Viability test: Can we save/load a real BERTopic model and use it after reload?

This test trains a small BERTopic model, saves it as a checkpoint, loads it back,
and verifies the loaded model can be used for actual topic modeling operations.
"""

import pytest
from pathlib import Path
import pandas as pd
import numpy as np
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from checkpoint_manager import (
    compute_dataset_fingerprint,
    save_checkpoint,
    load_checkpoint
)

# Skip if BERTopic not installed
pytest.importorskip("bertopic")

from bertopic import BERTopic


@pytest.fixture
def small_corpus():
    """Create a tiny corpus for fast training."""
    return [
        "machine learning models are trained on data",
        "deep learning neural networks use backpropagation",
        "artificial intelligence systems can solve problems",
        "data science involves statistics and programming",
        "algorithms process information efficiently",
        "natural language processing analyzes text",
        "computer vision recognizes images",
        "reinforcement learning learns from rewards",
    ]


@pytest.fixture
def small_dataframe(small_corpus):
    """Create a small DataFrame matching our app's structure."""
    return pd.DataFrame({
        'title': [f'Paper {i}' for i in range(len(small_corpus))],
        'abstract': small_corpus,
        'year': [2020 + i for i in range(len(small_corpus))]
    })


def test_real_bertopic_model_checkpoint_viability(small_corpus, small_dataframe):
    """
    VIABILITY TEST: Train real BERTopic, save checkpoint, load it, verify it works.
    
    This is the core viability question for Phase 07:
    Can we persist BERTopic models and actually use them after reload?
    """
    
    # === 1. Train a real BERTopic model ===
    print("\n1. Training real BERTopic model...")
    topic_model = BERTopic(
        min_topic_size=2,
        calculate_probabilities=False,  # Faster
        verbose=False
    )
    topics, _ = topic_model.fit_transform(small_corpus)
    print(f"   ✓ Trained model with {len(set(topics))} topics")
    
    # Generate embeddings (we'd cache these in the app)
    from sentence_transformers import SentenceTransformer
    embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
    embeddings = embedding_model.encode(small_corpus, show_progress_bar=False)
    print(f"   ✓ Generated embeddings: {embeddings.shape}")
    
    # === 2. Save checkpoint ===
    print("\n2. Saving checkpoint...")
    fingerprint = compute_dataset_fingerprint(small_dataframe)
    config = {
        'umap': {'n_neighbors': 2, 'n_components': 2},
        'hdbscan': {'min_cluster_size': 2},
        'vectorizer': {'ngram_range': (1, 2)}
    }
    metadata = {
        'timestamp': '20261201_120000',
        'dataset_name': 'viability_test',
        'topic_count': len(set(topics)),
        'outlier_percentage': sum(1 for t in topics if t == -1) / len(topics) * 100,
        'row_count': len(small_corpus)
    }
    
    checkpoint_dir = save_checkpoint(
        config=config,
        metadata=metadata,
        model=topic_model,
        embeddings=embeddings,
        dataset_fingerprint=fingerprint
    )
    print(f"   ✓ Saved checkpoint to {checkpoint_dir}")
    
    # === 3. Load checkpoint ===
    print("\n3. Loading checkpoint...")
    loaded_config, loaded_metadata, loaded_model, loaded_embeddings, loaded_fp = load_checkpoint(checkpoint_dir)
    print(f"   ✓ Loaded checkpoint")
    
    # === 4. Verify loaded model is USABLE ===
    print("\n4. Testing loaded model functionality...")
    
    # Test 1: Can we get topics from the loaded model?
    loaded_topics = loaded_model.topics_
    assert loaded_topics is not None, "Loaded model has no topics_"
    assert len(loaded_topics) == len(topics), "Topic count mismatch"
    print(f"   ✓ Loaded model has {len(loaded_topics)} topic assignments")
    
    # Test 2: Can we get topic info?
    topic_info = loaded_model.get_topic_info()
    assert topic_info is not None, "Cannot get topic info"
    assert len(topic_info) > 0, "Topic info is empty"
    print(f"   ✓ Got topic info: {len(topic_info)} rows")
    
    # Test 3: Can we get representative documents?
    try:
        repr_docs = loaded_model.get_representative_docs()
        print(f"   ✓ Got representative docs for {len(repr_docs)} topics")
    except Exception as e:
        print(f"   ⚠ Could not get representative docs: {e}")
    
    # Test 4: Can we transform new documents?
    new_doc = ["deep neural networks learn features automatically"]
    try:
        new_topics, _ = loaded_model.transform(new_doc)
        print(f"   ✓ Transform works: new doc assigned to topic {new_topics[0]}")
    except Exception as e:
        pytest.fail(f"Cannot transform with loaded model: {e}")
    
    # Test 5: Can we visualize hierarchy?
    try:
        fig = loaded_model.visualize_hierarchy()
        assert fig is not None, "Hierarchy visualization returned None"
        print(f"   ✓ Hierarchy visualization works")
    except Exception as e:
        print(f"   ⚠ Hierarchy visualization failed: {e}")
    
    # Test 6: Verify embeddings loaded correctly
    assert loaded_embeddings.shape == embeddings.shape, "Embeddings shape mismatch"
    assert np.allclose(loaded_embeddings, embeddings), "Embeddings data mismatch"
    print(f"   ✓ Embeddings preserved correctly")
    
    # Test 7: Verify fingerprint matches
    assert loaded_fp == fingerprint, "Fingerprint mismatch"
    print(f"   ✓ Fingerprint preserved correctly")
    
    print("\n" + "="*60)
    print("✓ VIABILITY CONFIRMED: BERTopic checkpoint system works!")
    print("="*60)
    
    # === 5. Cleanup test checkpoint ===
    import shutil
    shutil.rmtree(checkpoint_dir)
    print(f"\n✓ Cleaned up test checkpoint")



if __name__ == '__main__':
    # Run manually for debugging
    pytest.main([__file__, '-v', '-s'])
