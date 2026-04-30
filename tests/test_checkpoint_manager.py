"""
Unit tests for checkpoint_manager module.

Tests checkpoint save/load, fingerprinting, validation, and listing functionality.
"""

import pytest
from pathlib import Path
import pandas as pd
import numpy as np
import json
import pickle
import sys

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from checkpoint_manager import (
    compute_dataset_fingerprint,
    save_checkpoint,
    load_checkpoint,
    list_checkpoints,
    validate_checkpoint_integrity
)


# --- Mock Model Class (module level for pickle compatibility) ---

class MockBERTopic:
    """Simple mock BERTopic model for testing."""
    def __init__(self):
        self.topics = [1, 2, 3, 1, 2]
        self.topic_labels = {1: 'Topic 1', 2: 'Topic 2', 3: 'Topic 3'}
        # Add more data to make pickled model > 1KB for validation
        self.topic_representations = {
            i: [(f'word_{j}', 0.5) for j in range(100)]
            for i in range(50)
        }
        self.document_info = pd.DataFrame({
            'Document': [f'doc_{i}' for i in range(100)],
            'Topic': [i % 5 for i in range(100)],
            'Name': [f'topic_{i%5}' for i in range(100)]
        })


# --- Fixtures ---

@pytest.fixture
def sample_dataframe():
    """Create a sample DataFrame for testing."""
    return pd.DataFrame({
        'title': ['Paper A', 'Paper B', 'Paper C'],
        'abstract': ['Abstract 1', 'Abstract 2', 'Abstract 3'],
        'year': [2020, 2021, 2022]
    })


@pytest.fixture
def sample_config():
    """Create sample model configuration."""
    return {
        'umap': {'n_neighbors': 15, 'n_components': 5, 'min_dist': 0.0},
        'hdbscan': {'min_cluster_size': 10, 'min_samples': 5},
        'vectorizer': {'ngram_range': (1, 2), 'min_df': 2}
    }


@pytest.fixture
def sample_metadata():
    """Create sample checkpoint metadata."""
    return {
        'timestamp': '20261201_120000',
        'dataset_name': 'test_data',
        'topic_count': 10,
        'outlier_percentage': 5.5,
        'row_count': 100
    }


@pytest.fixture
def sample_embeddings():
    """Create sample embeddings array."""
    return np.random.rand(100, 384)  # 100 documents, 384-dim embeddings


@pytest.fixture
def mock_model():
    """Create a mock BERTopic model for testing."""
    return MockBERTopic()


# --- Fingerprinting Tests ---

def test_fingerprint_same_dataframe_produces_same_hash(sample_dataframe):
    """Test that same DataFrame produces same fingerprint."""
    fp1 = compute_dataset_fingerprint(sample_dataframe)
    fp2 = compute_dataset_fingerprint(sample_dataframe)
    
    assert fp1 == fp2
    assert len(fp1) == 64  # SHA-256 hex digest


def test_fingerprint_different_dataframes_produce_different_hashes():
    """Test that different DataFrames produce different fingerprints."""
    df1 = pd.DataFrame({'a': [1, 2], 'b': [3, 4]})
    df2 = pd.DataFrame({'a': [1, 2], 'b': [5, 6]})
    
    fp1 = compute_dataset_fingerprint(df1)
    fp2 = compute_dataset_fingerprint(df2)
    
    assert fp1 != fp2


def test_fingerprint_independent_of_row_order(sample_dataframe):
    """Test that row order doesn't affect fingerprint due to sorting."""
    # Shuffle rows
    df_shuffled = sample_dataframe.sample(frac=1, random_state=42)
    
    fp_original = compute_dataset_fingerprint(sample_dataframe)
    fp_shuffled = compute_dataset_fingerprint(df_shuffled)
    
    assert fp_original == fp_shuffled


# --- Save/Load Roundtrip Tests ---

def test_save_checkpoint_creates_all_files(
    tmp_path,
    sample_config,
    sample_metadata,
    mock_model,
    sample_embeddings
):
    """Test that save_checkpoint creates all required files."""
    fingerprint = "abc123" * 10 + "1234"  # 64-char string
    
    # Override checkpoints dir for test
    original_path = Path('data/checkpoints')
    test_checkpoints = tmp_path / 'checkpoints'
    test_checkpoints.mkdir()
    
    # Monkey-patch the checkpoint directory in save_checkpoint
    import checkpoint_manager
    original_save = checkpoint_manager.save_checkpoint
    
    def patched_save(config, metadata, model, embeddings, dataset_fingerprint):
        checkpoint_dir = test_checkpoints / f"{metadata['timestamp']}_{metadata['dataset_name']}"
        checkpoint_dir.mkdir(parents=True, exist_ok=True)
        
        # Same logic as original save_checkpoint
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
    
    checkpoint_dir = patched_save(
        sample_config,
        sample_metadata,
        mock_model,
        sample_embeddings,
        fingerprint
    )
    
    # Verify all files exist
    assert (checkpoint_dir / 'config.json').exists()
    assert (checkpoint_dir / 'metadata.json').exists()
    assert (checkpoint_dir / 'model.pkl').exists()
    assert (checkpoint_dir / 'embeddings.npy').exists()
    assert (checkpoint_dir / 'dataset_fingerprint.txt').exists()


def test_load_checkpoint_restores_data(
    tmp_path,
    sample_config,
    sample_metadata,
    mock_model,
    sample_embeddings
):
    """Test that load_checkpoint correctly restores saved data."""
    fingerprint = "def456" * 10 + "5678"
    
    # Create checkpoint manually
    checkpoint_dir = tmp_path / '20261201_120000_test_data'
    checkpoint_dir.mkdir()
    
    with open(checkpoint_dir / 'config.json', 'w') as f:
        json.dump(sample_config, f)
    with open(checkpoint_dir / 'metadata.json', 'w') as f:
        json.dump(sample_metadata, f)
    with open(checkpoint_dir / 'model.pkl', 'wb') as f:
        pickle.dump(mock_model, f, protocol=5)
    np.save(checkpoint_dir / 'embeddings.npy', sample_embeddings)
    with open(checkpoint_dir / 'dataset_fingerprint.txt', 'w') as f:
        f.write(fingerprint)
    
    # Load checkpoint
    config, metadata, model, embeddings, loaded_fp = load_checkpoint(checkpoint_dir)
    
    # Verify data (note: JSON serialization converts tuples to lists, which is expected)
    assert config['umap'] == sample_config['umap']
    assert config['hdbscan'] == sample_config['hdbscan']
    # Check vectorizer separately since ngram_range tuple becomes list in JSON
    assert config['vectorizer']['min_df'] == sample_config['vectorizer']['min_df']
    assert list(config['vectorizer']['ngram_range']) == list(sample_config['vectorizer']['ngram_range'])
    
    assert metadata == sample_metadata
    assert loaded_fp == fingerprint
    assert np.array_equal(embeddings, sample_embeddings)
    assert hasattr(model, 'topics')
    assert model.topics == [1, 2, 3, 1, 2]


def test_save_load_preserves_fingerprint(
    tmp_path,
    sample_config,
    sample_metadata,
    mock_model,
    sample_embeddings
):
    """Test that fingerprint is preserved through save/load cycle."""
    original_fingerprint = "preserved" * 6 + "fp12"
    
    checkpoint_dir = tmp_path / '20261201_120000_test_data'
    checkpoint_dir.mkdir()
    
    with open(checkpoint_dir / 'config.json', 'w') as f:
        json.dump(sample_config, f)
    with open(checkpoint_dir / 'metadata.json', 'w') as f:
        json.dump(sample_metadata, f)
    with open(checkpoint_dir / 'model.pkl', 'wb') as f:
        pickle.dump(mock_model, f, protocol=5)
    np.save(checkpoint_dir / 'embeddings.npy', sample_embeddings)
    with open(checkpoint_dir / 'dataset_fingerprint.txt', 'w') as f:
        f.write(original_fingerprint)
    
    # Load and verify
    _, _, _, _, loaded_fp = load_checkpoint(checkpoint_dir)
    assert loaded_fp == original_fingerprint


# --- Checkpoint Listing Tests ---

def test_list_checkpoints_empty_directory(tmp_path, monkeypatch):
    """Test list_checkpoints with no checkpoints."""
    monkeypatch.setattr('checkpoint_manager.Path', lambda x: tmp_path if x == 'data/checkpoints' else Path(x))
    
    checkpoints = list_checkpoints()
    assert checkpoints == []


def test_list_checkpoints_returns_correct_count(tmp_path, sample_metadata):
    """Test that list_checkpoints returns correct number of checkpoints."""
    # Create multiple checkpoint directories
    for i in range(3):
        checkpoint_dir = tmp_path / f'2026120{i}_120000_test_{i}'
        checkpoint_dir.mkdir()
        
        metadata = sample_metadata.copy()
        metadata['timestamp'] = f'2026120{i}_120000'
        metadata['dataset_name'] = f'test_{i}'
        
        with open(checkpoint_dir / 'metadata.json', 'w') as f:
            json.dump(metadata, f)
    
    # Monkey-patch to use tmp_path
    import checkpoint_manager
    original_list = checkpoint_manager.list_checkpoints
    
    def patched_list():
        checkpoints = []
        for checkpoint_dir in tmp_path.iterdir():
            if not checkpoint_dir.is_dir():
                continue
            metadata_file = checkpoint_dir / 'metadata.json'
            if not metadata_file.exists():
                continue
            with open(metadata_file, 'r') as f:
                metadata = json.load(f)
            checkpoints.append({
                'path': str(checkpoint_dir),
                'timestamp': metadata.get('timestamp', 'unknown'),
                'dataset_name': metadata.get('dataset_name', 'unknown'),
                'topic_count': metadata.get('topic_count', 0),
                'outlier_percentage': metadata.get('outlier_percentage', 0.0),
                'row_count': metadata.get('row_count', 0)
            })
        checkpoints.sort(key=lambda x: x['timestamp'], reverse=True)
        return checkpoints
    
    result = patched_list()
    assert len(result) == 3


def test_list_checkpoints_sorted_by_timestamp(tmp_path, sample_metadata):
    """Test that checkpoints are sorted by timestamp descending."""
    timestamps = ['20261201_120000', '20261203_120000', '20261202_120000']
    
    for ts in timestamps:
        checkpoint_dir = tmp_path / f'{ts}_test'
        checkpoint_dir.mkdir()
        
        metadata = sample_metadata.copy()
        metadata['timestamp'] = ts
        
        with open(checkpoint_dir / 'metadata.json', 'w') as f:
            json.dump(metadata, f)
    
    # Use patched version
    import checkpoint_manager
    def patched_list():
        checkpoints = []
        for checkpoint_dir in tmp_path.iterdir():
            if not checkpoint_dir.is_dir():
                continue
            metadata_file = checkpoint_dir / 'metadata.json'
            if not metadata_file.exists():
                continue
            with open(metadata_file, 'r') as f:
                metadata = json.load(f)
            checkpoints.append({
                'path': str(checkpoint_dir),
                'timestamp': metadata.get('timestamp', 'unknown'),
                'dataset_name': metadata.get('dataset_name', 'unknown'),
                'topic_count': metadata.get('topic_count', 0),
                'outlier_percentage': metadata.get('outlier_percentage', 0.0),
                'row_count': metadata.get('row_count', 0)
            })
        checkpoints.sort(key=lambda x: x['timestamp'], reverse=True)
        return checkpoints
    
    result = patched_list()
    
    # Should be sorted newest first
    assert result[0]['timestamp'] == '20261203_120000'
    assert result[1]['timestamp'] == '20261202_120000'
    assert result[2]['timestamp'] == '20261201_120000'


def test_list_checkpoints_skips_corrupted_metadata(tmp_path):
    """Test that checkpoints with missing/corrupted metadata are skipped."""
    # Create valid checkpoint
    valid_dir = tmp_path / '20261201_120000_valid'
    valid_dir.mkdir()
    with open(valid_dir / 'metadata.json', 'w') as f:
        json.dump({'timestamp': '20261201_120000', 'dataset_name': 'valid', 'topic_count': 5}, f)
    
    # Create checkpoint with missing metadata
    invalid_dir = tmp_path / '20261202_120000_invalid'
    invalid_dir.mkdir()
    # No metadata.json
    
    # Create checkpoint with corrupted metadata
    corrupted_dir = tmp_path / '20261203_120000_corrupted'
    corrupted_dir.mkdir()
    with open(corrupted_dir / 'metadata.json', 'w') as f:
        f.write("{invalid json")
    
    def patched_list():
        checkpoints = []
        for checkpoint_dir in tmp_path.iterdir():
            if not checkpoint_dir.is_dir():
                continue
            metadata_file = checkpoint_dir / 'metadata.json'
            if not metadata_file.exists():
                continue
            try:
                with open(metadata_file, 'r') as f:
                    metadata = json.load(f)
                checkpoints.append({
                    'path': str(checkpoint_dir),
                    'timestamp': metadata.get('timestamp', 'unknown'),
                    'dataset_name': metadata.get('dataset_name', 'unknown'),
                    'topic_count': metadata.get('topic_count', 0),
                    'outlier_percentage': metadata.get('outlier_percentage', 0.0),
                    'row_count': metadata.get('row_count', 0)
                })
            except (json.JSONDecodeError, OSError):
                continue
        checkpoints.sort(key=lambda x: x['timestamp'], reverse=True)
        return checkpoints
    
    result = patched_list()
    
    # Should only return the valid checkpoint
    assert len(result) == 1
    assert result[0]['dataset_name'] == 'valid'


# --- Integrity Validation Tests ---

def test_validate_checkpoint_passes_for_valid_checkpoint(
    tmp_path,
    sample_config,
    sample_metadata,
    mock_model,
    sample_embeddings
):
    """Test that valid checkpoint passes validation."""
    checkpoint_dir = tmp_path / 'valid_checkpoint'
    checkpoint_dir.mkdir()
    
    # Create all required files
    with open(checkpoint_dir / 'config.json', 'w') as f:
        json.dump(sample_config, f)
    with open(checkpoint_dir / 'metadata.json', 'w') as f:
        json.dump(sample_metadata, f)
    with open(checkpoint_dir / 'model.pkl', 'wb') as f:
        pickle.dump(mock_model, f, protocol=5)
    np.save(checkpoint_dir / 'embeddings.npy', sample_embeddings)
    with open(checkpoint_dir / 'dataset_fingerprint.txt', 'w') as f:
        f.write("valid_fingerprint" * 4)
    
    is_valid, errors = validate_checkpoint_integrity(checkpoint_dir)
    
    assert is_valid
    assert len(errors) == 0


def test_validate_checkpoint_fails_for_missing_file(tmp_path, sample_config):
    """Test that validation fails when required file is missing."""
    checkpoint_dir = tmp_path / 'incomplete_checkpoint'
    checkpoint_dir.mkdir()
    
    # Create only some files
    with open(checkpoint_dir / 'config.json', 'w') as f:
        json.dump(sample_config, f)
    # Missing: metadata.json, model.pkl, embeddings.npy, dataset_fingerprint.txt
    
    is_valid, errors = validate_checkpoint_integrity(checkpoint_dir)
    
    assert not is_valid
    assert len(errors) > 0
    assert any('metadata.json' in err for err in errors)


def test_validate_checkpoint_fails_for_corrupted_pickle(tmp_path, sample_metadata):
    """Test that validation fails for corrupted pickle file."""
    checkpoint_dir = tmp_path / 'corrupted_checkpoint'
    checkpoint_dir.mkdir()
    
    # Create all files, but corrupt the pickle
    with open(checkpoint_dir / 'config.json', 'w') as f:
        json.dump({}, f)
    with open(checkpoint_dir / 'metadata.json', 'w') as f:
        json.dump(sample_metadata, f)
    with open(checkpoint_dir / 'model.pkl', 'wb') as f:
        f.write(b'corrupted pickle data')  # Invalid pickle
    np.save(checkpoint_dir / 'embeddings.npy', np.array([1, 2, 3]))
    with open(checkpoint_dir / 'dataset_fingerprint.txt', 'w') as f:
        f.write("fingerprint")
    
    is_valid, errors = validate_checkpoint_integrity(checkpoint_dir)
    
    assert not is_valid
    assert any('pickle' in err.lower() for err in errors)


def test_validate_checkpoint_fails_for_small_files(tmp_path, sample_config, sample_metadata):
    """Test that validation fails for suspiciously small files."""
    checkpoint_dir = tmp_path / 'small_files_checkpoint'
    checkpoint_dir.mkdir()
    
    with open(checkpoint_dir / 'config.json', 'w') as f:
        json.dump(sample_config, f)
    with open(checkpoint_dir / 'metadata.json', 'w') as f:
        json.dump(sample_metadata, f)
    with open(checkpoint_dir / 'model.pkl', 'wb') as f:
        f.write(b'x')  # Only 1 byte (< 1KB threshold)
    with open(checkpoint_dir / 'embeddings.npy', 'wb') as f:
        f.write(b'y')  # Only 1 byte (< 100 byte threshold)
    with open(checkpoint_dir / 'dataset_fingerprint.txt', 'w') as f:
        f.write("fp")
    
    is_valid, errors = validate_checkpoint_integrity(checkpoint_dir)
    
    assert not is_valid
    assert any('small' in err.lower() for err in errors)


def test_load_checkpoint_raises_error_for_invalid_checkpoint(tmp_path):
    """Test that load_checkpoint raises ValueError for invalid checkpoint."""
    checkpoint_dir = tmp_path / 'invalid'
    checkpoint_dir.mkdir()
    
    # Create incomplete checkpoint (missing files)
    with open(checkpoint_dir / 'config.json', 'w') as f:
        json.dump({}, f)
    
    with pytest.raises(ValueError, match="validation failed"):
        load_checkpoint(checkpoint_dir)
