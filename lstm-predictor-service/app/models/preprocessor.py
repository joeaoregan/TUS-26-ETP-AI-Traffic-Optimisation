# preprocessor.py
"""
Data preprocessing pipeline for LSTM model training and inference.
Handles normalization, sequence creation, and scaler persistence.
"""

import numpy as np
import pickle
from pathlib import Path
from sklearn.preprocessing import MinMaxScaler
from typing import Tuple, Optional
from colorama import Fore, init

init(autoreset=True)


class DataPreprocessor:
    """
    Handles data normalization and sequence creation for LSTM.
    Persists scaler for consistent train/inference pipeline.
    """
    
    def __init__(self, scaler_path: str = "app/trained_models/scaler.pkl"):
        """
        Initialize preprocessor.
        
        Args:
            scaler_path: Path to save/load MinMaxScaler
        """
        self.scaler_path = Path(scaler_path)
        self.scaler = None
        self._load_or_create_scaler()
    
    def _load_or_create_scaler(self):
        """Load existing scaler or create new one."""
        if self.scaler_path.exists():
            with open(self.scaler_path, 'rb') as f:
                self.scaler = pickle.load(f)
            print(f"{Fore.GREEN}✓ Loaded scaler from {self.scaler_path}")
        else:
            self.scaler = MinMaxScaler(feature_range=(0, 1))
            print(f"{Fore.GREEN}✓ Created new MinMaxScaler")
    
    def fit_scaler(self, data: np.ndarray) -> np.ndarray:
        """
        Fit scaler on training data and persist.
        
        Args:
            data: Training data (N, n_features)
            
        Returns:
            Normalized data
        """
        normalized = self.scaler.fit_transform(data)
        self._save_scaler()
        print(f"{Fore.GREEN}✓ Fitted scaler on {data.shape[0]} samples, {data.shape[1]} features")
        return normalized
    
    def normalize(self, data: np.ndarray) -> np.ndarray:
        """
        Normalize data using fitted scaler.
        
        Args:
            data: Raw data (N, n_features)
            
        Returns:
            Normalized data (0-1 range)
        """
        if self.scaler is None:
            raise ValueError("Scaler not fitted. Call fit_scaler() first.")
        return self.scaler.transform(data)
    
    def denormalize(self, normalized_data: np.ndarray) -> np.ndarray:
        """
        Reverse normalization (convert back to original scale).
        
        Args:
            normalized_data: Normalized data (0-1 range)
            
        Returns:
            Data in original scale
        """
        if self.scaler is None:
            raise ValueError("Scaler not fitted. Call fit_scaler() first.")
        return self.scaler.inverse_transform(normalized_data)
    
    def _save_scaler(self):
        """Persist scaler to disk."""
        self.scaler_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.scaler_path, 'wb') as f:
            pickle.dump(self.scaler, f)
        print(f"{Fore.GREEN}✓ Saved scaler to {self.scaler_path}")
    
    @staticmethod
    def create_sequences(data: np.ndarray, seq_length: int = 3) -> Tuple[np.ndarray, np.ndarray]:
        """
        Create sliding window sequences for LSTM training.
        
        Converts time series into supervised learning format:
            Input:  [t-2, t-1, t]
            Output: [t+1]
        
        Args:
            data: Normalized time series (N, n_features)
            seq_length: Number of timesteps per sequence (default: 3)
            
        Returns:
            X: Input sequences (N_samples, seq_length, n_features)
            y: Target values (N_samples, n_features)
        """
        X, y = [], []
        
        for i in range(len(data) - seq_length):
            X.append(data[i:i + seq_length])  # 3 timesteps
            y.append(data[i + seq_length])     # next timestep
        
        X = np.array(X)
        y = np.array(y)
        
        print(f"{Fore.GREEN}✓ Created {len(X)} sequences (seq_length={seq_length})")
        print(f"{Fore.CYAN}  X shape: {X.shape}  (samples, timesteps, features)")
        print(f"{Fore.CYAN}  y shape: {y.shape}  (samples, features)")
        
        return X, y
    
    @staticmethod
    def create_sequences_with_validation_split(
        data: np.ndarray,
        seq_length: int = 3,
        train_split: float = 0.8
    ) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        """
        Create sequences with temporal train/validation split.
        
        ⚠️ Uses temporal split (no shuffle) to preserve time-series integrity.
        
        Args:
            data: Normalized time series (N, n_features)
            seq_length: Number of timesteps per sequence
            train_split: Fraction for training (default: 0.8 → 80% train, 20% val)
            
        Returns:
            X_train, X_val, y_train, y_val
        """
        X, y = DataPreprocessor.create_sequences(data, seq_length)
        
        split_idx = int(len(X) * train_split)
        
        X_train, X_val = X[:split_idx], X[split_idx:]
        y_train, y_val = y[:split_idx], y[split_idx:]
        
        print(f"{Fore.GREEN}✓ Temporal split: {len(X_train)} train, {len(X_val)} validation")
        
        return X_train, X_val, y_train, y_val


# Utility functions (standalone usage)

def prepare_prediction_input(
    historical_data: list,
    preprocessor: DataPreprocessor,
    seq_length: int = 3
) -> np.ndarray:
    """
    Prepare raw prediction input for LSTM inference.
    
    Args:
        historical_data: List of recent measurements [[t-2], [t-1], [t]]
        preprocessor: Fitted DataPreprocessor instance
        seq_length: Expected sequence length (typically 3)
        
    Returns:
        Normalized, shaped input ready for model.predict()
    """
    if len(historical_data) != seq_length:
        raise ValueError(f"Expected {seq_length} timesteps, got {len(historical_data)}")
    
    # Convert to numpy array
    data_array = np.array(historical_data, dtype=np.float32)
    
    # Normalize
    normalized = preprocessor.normalize(data_array)
    
    # Add batch dimension: (seq_length, n_features) → (1, seq_length, n_features)
    batch_input = np.expand_dims(normalized, axis=0)
    
    print(f"{Fore.GREEN}✓ Prepared prediction input: {batch_input.shape}")
    
    return batch_input