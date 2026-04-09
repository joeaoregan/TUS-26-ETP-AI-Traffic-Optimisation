# lstm_train.py
# Prepares the data from SUMO edgeData.xml and builds an LSTM model for traffic prediction. 
# Focuses on the top 5 most congested edges based on density.

import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.optimizers import Adam
import xml.etree.ElementTree as ET
import pickle
import os

# Parse edgeData.xml
tree = ET.parse('SUMO/Results/MAPPO/edgeData.xml')
root = tree.getroot()

edges_data = []
for interval in root.findall('interval'):
    interval_begin = float(interval.get('begin'))
    for edge in interval.findall('edge'):
        edges_data.append({
            'edge_id': edge.get('id'),
            'time': interval_begin,
            'density': float(edge.get('density', 0)),
        })

df = pd.DataFrame(edges_data)

# Focus on top 5 congested edges
top_edges = df.groupby('edge_id')['density'].mean().nlargest(5).index.tolist()
df_filtered = df[df['edge_id'].isin(top_edges)].copy()

# Prepare data
df_pivot = df_filtered.pivot_table(index='time', columns='edge_id', values='density', fill_value=0)
data = df_pivot.values

# Normalize
scaler = MinMaxScaler()
data_scaled = scaler.fit_transform(data)

# Create sequences for LSTM
def create_sequences(data, seq_length=3):
    X, y = [], []
    for i in range(len(data) - seq_length):
        X.append(data[i:i+seq_length])
        y.append(data[i+seq_length])
    return np.array(X), np.array(y)

seq_length = 3
X, y = create_sequences(data_scaled, seq_length)

print(f"X shape: {X.shape}, y shape: {y.shape}")

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

print(f"Training set: {X_train.shape}, Test set: {X_test.shape}")

# Build LSTM model
model = Sequential([
    LSTM(64, activation='relu', input_shape=(seq_length, data_scaled.shape[1])),
    Dropout(0.2),
    Dense(32, activation='relu'),
    Dropout(0.2),
    Dense(data_scaled.shape[1])
])

model.compile(optimizer=Adam(learning_rate=0.001), loss='mse', metrics=['mae'])

print("\nTraining LSTM...")
history = model.fit(
    X_train, y_train,
    epochs=50,
    batch_size=2,
    validation_data=(X_test, y_test),
    verbose=1
)

# Evaluate
test_loss, test_mae = model.evaluate(X_test, y_test)
print(f"\nTest Loss: {test_loss:.4f}, Test MAE: {test_mae:.4f}")

# Save model
model_path = 'lstm-predictor-service/app/trained_models/lstm_model.h5'
scaler_path = 'lstm-predictor-service/app/trained_models/scaler.pkl'

os.makedirs(os.path.dirname(model_path), exist_ok=True)
# model.save(model_path) # HDF5 format is deprecated, using TensorFlow SavedModel format instead
# model.save(model_path, save_format='tf')
model_path = 'lstm-predictor-service/app/trained_models/lstm_model.keras'
model.save(model_path)
pickle.dump(scaler, open(scaler_path, 'wb'))

print(f"\nModel saved to {model_path}")
print(f"Scaler saved to {scaler_path}")