"""
Checkpoint management module for BERTopic model persistence.

Handles checkpoint save/load, dataset fingerprinting, and integrity validation
to enable reproducible topic modeling across sessions.
"""

from pathlib import Path
import pickle
import json
import hashlib
import numpy as np
import pandas as pd
from datetime import datetime
from bertopic import BERTopic

# Project root: parent of src/ directory
PROJECT_ROOT = Path(__file__).parent.parent
CHECKPOINTS_DIR = PROJECT_ROOT / 'data' / 'checkpoints'


def compute_dataset_fingerprint(df: pd.DataFrame) -> str:
    """
    Compute stable SHA-256 fingerprint of a DataFrame.
    
    Sorts DataFrame by all columns to ensure stable ordering regardless of
    input row order, then serializes to CSV and hashes the result.
    
    Args:
        df: DataFrame to fingerprint
        
    Returns:
        64-character hex digest string
    """
    # Sort by all columns for stable ordering
    df_sorted = df.sort_values(by=list(df.columns))
    
    # Serialize to CSV string (without index)
    csv_string = df_sorted.to_csv(index=False)
    
    # Compute SHA-256 hash
    fingerprint = hashlib.sha256(csv_string.encode('utf-8')).hexdigest()
    
    return fingerprint


def save_checkpoint(
    config: dict,
    metadata: dict,
    model: BERTopic,
    embeddings: np.ndarray,
    dataset_fingerprint: str
) -> Path:
    """
    Save complete checkpoint to filesystem.
    
    Creates directory structure: data/checkpoints/{timestamp}_{dataset_name}/
    containing all required checkpoint files.
    
    Args:
        config: Model configuration dict (UMAP, HDBSCAN, vectorizer params)
        metadata: Checkpoint metadata (timestamp, dataset_name, topic_count, etc.)
        model: Trained BERTopic model instance
        embeddings: Document embeddings array
        dataset_fingerprint: SHA-256 fingerprint of source dataset
        
    Returns:
        Path to created checkpoint directory
    """
    # Create checkpoint directory name
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    dataset_name = metadata.get('dataset_name', 'unknown').replace(' ', '_')
    checkpoint_name = f"{timestamp}_{dataset_name}"
    
    checkpoint_dir = CHECKPOINTS_DIR / checkpoint_name
    checkpoint_dir.mkdir(parents=True, exist_ok=True)
    
    try:
        # Save config as JSON
        with open(checkpoint_dir / 'config.json', 'w') as f:
            json.dump(config, f, indent=2)
        
        # Save metadata as JSON
        with open(checkpoint_dir / 'metadata.json', 'w') as f:
            json.dump(metadata, f, indent=2)
        
        # Save model using pickle protocol 5
        with open(checkpoint_dir / 'model.pkl', 'wb') as f:
            pickle.dump(model, f, protocol=5)
        
        # Save embeddings
        np.save(checkpoint_dir / 'embeddings.npy', embeddings)
        
        # Save dataset fingerprint
        with open(checkpoint_dir / 'dataset_fingerprint.txt', 'w') as f:
            f.write(dataset_fingerprint)
        
        return checkpoint_dir
        
    except Exception as e:
        # Clean up partial checkpoint on failure
        if checkpoint_dir.exists():
            import shutil
            shutil.rmtree(checkpoint_dir)
        raise RuntimeError(f"Failed to save checkpoint: {str(e)}") from e


def list_checkpoints() -> list[dict]:
    """
    List all available checkpoints with metadata.
    
    Scans data/checkpoints/ directory and loads metadata for each checkpoint.
    
    Returns:
        List of checkpoint dicts sorted by timestamp (newest first).
        Each dict contains: path, timestamp, dataset_name, topic_count,
        outlier_percentage, row_count
    """
    if not CHECKPOINTS_DIR.exists():
        return []
    
    checkpoints = []
    
    for checkpoint_dir in CHECKPOINTS_DIR.iterdir():
        if not checkpoint_dir.is_dir():
            continue
        
        metadata_file = checkpoint_dir / 'metadata.json'
        
        if not metadata_file.exists():
            # Skip corrupted checkpoints without metadata
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
            # Skip corrupted checkpoints
            continue
    
    # Sort by timestamp descending (newest first)
    checkpoints.sort(key=lambda x: x['timestamp'], reverse=True)
    
    return checkpoints


def validate_checkpoint_integrity(checkpoint_dir: Path) -> tuple[bool, list[str]]:
    """
    Validate checkpoint file integrity.
    
    Checks for required files, file sizes, and pickle load success.
    
    Args:
        checkpoint_dir: Path to checkpoint directory
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    
    if not checkpoint_dir.exists():
        return False, [f"Checkpoint directory does not exist: {checkpoint_dir}"]
    
    # Check required files exist
    required_files = [
        'config.json',
        'metadata.json',
        'model.pkl',
        'embeddings.npy',
        'dataset_fingerprint.txt'
    ]
    
    for filename in required_files:
        filepath = checkpoint_dir / filename
        if not filepath.exists():
            errors.append(f"Missing required file: {filename}")
    
    # If any files are missing, return early
    if errors:
        return False, errors
    
    # Check file sizes
    model_file = checkpoint_dir / 'model.pkl'
    embeddings_file = checkpoint_dir / 'embeddings.npy'
    
    if model_file.stat().st_size < 1024:  # < 1KB
        errors.append("model.pkl is suspiciously small (< 1KB)")
    
    if embeddings_file.stat().st_size < 100:  # < 100 bytes
        errors.append("embeddings.npy is suspiciously small (< 100 bytes)")
    
    # Try loading pickle to detect corruption
    try:
        with open(model_file, 'rb') as f:
            pickle.load(f)
    except (pickle.UnpicklingError, EOFError, OSError, AttributeError, ModuleNotFoundError) as e:
        errors.append(f"Corrupted pickle file: {str(e)}")
    
    # Try loading embeddings
    try:
        np.load(embeddings_file)
    except (OSError, ValueError) as e:
        errors.append(f"Corrupted embeddings file: {str(e)}")
    
    # Try loading JSON files
    for json_file in ['config.json', 'metadata.json']:
        try:
            with open(checkpoint_dir / json_file, 'r') as f:
                json.load(f)
        except json.JSONDecodeError as e:
            errors.append(f"Corrupted {json_file}: {str(e)}")
    
    is_valid = len(errors) == 0
    return is_valid, errors


def load_checkpoint(checkpoint_dir: Path) -> tuple[dict, dict, BERTopic, np.ndarray, str]:
    """
    Load complete checkpoint from filesystem.
    
    Validates integrity first, then loads all checkpoint components.
    
    Args:
        checkpoint_dir: Path to checkpoint directory
        
    Returns:
        Tuple of (config, metadata, model, embeddings, dataset_fingerprint)
        
    Raises:
        ValueError: If checkpoint validation fails
        OSError: If file operations fail
    """
    # Validate integrity first
    is_valid, errors = validate_checkpoint_integrity(checkpoint_dir)
    
    if not is_valid:
        error_msg = f"Checkpoint validation failed: {', '.join(errors)}"
        raise ValueError(error_msg)
    
    try:
        # Load config
        with open(checkpoint_dir / 'config.json', 'r') as f:
            config = json.load(f)
        
        # Load metadata
        with open(checkpoint_dir / 'metadata.json', 'r') as f:
            metadata = json.load(f)
        
        # Load model
        with open(checkpoint_dir / 'model.pkl', 'rb') as f:
            model = pickle.load(f)
        
        # Load embeddings
        embeddings = np.load(checkpoint_dir / 'embeddings.npy')
        
        # Load dataset fingerprint
        with open(checkpoint_dir / 'dataset_fingerprint.txt', 'r') as f:
            dataset_fingerprint = f.read().strip()
        
        return config, metadata, model, embeddings, dataset_fingerprint
        
    except Exception as e:
        raise OSError(f"Failed to load checkpoint: {str(e)}") from e
