# feature_engineering.py
import numpy as np
from sklearn.preprocessing import MinMaxScaler

def create_sequences(data, seq_length=3):
    """Create sequences for LSTM training"""
    X, y = [], []
    for i in range(len(data) - seq_length):
        X.append(data[i:i+seq_length])
        y.append(data[i+seq_length])
    return np.array(X), np.array(y)

def normalize_data(data):
    """Normalize using MinMaxScaler"""
    scaler = MinMaxScaler()
    return scaler.fit_transform(data), scaler

def denormalize_data(scaled_data, scaler):
    """Reverse normalization"""
    return scaler.inverse_transform(scaled_data)