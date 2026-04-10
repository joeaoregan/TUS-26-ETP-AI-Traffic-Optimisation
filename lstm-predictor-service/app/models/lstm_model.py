# lstm_model.py
# Prepares the data from SUMO edgeData.xml and builds an LSTM model for traffic prediction.

# import torch
# import torch.nn as nn

import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
import xml.etree.ElementTree as ET

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
            'occupancy': float(edge.get('occupancy', 0)),
            'waitingTime': float(edge.get('waitingTime', 0))
        })

df = pd.DataFrame(edges_data)

# Focus on top 5 congested edges
top_edges = df.groupby('edge_id')['density'].mean().nlargest(5).index.tolist()
df_filtered = df[df['edge_id'].isin(top_edges)].copy()

print(f"Building LSTM for edges: {top_edges}")
print(f"Total records: {len(df_filtered)}")

# Prepare data: pivot to get each edge as a feature
df_pivot = df_filtered.pivot_table(index='time', columns='edge_id', values='density', fill_value=0)
print(f"\nSequence shape: {df_pivot.shape}")
print(df_pivot)

# Normalize
scaler = MinMaxScaler()
data_scaled = scaler.fit_transform(df_pivot.values)

print("\nData ready for LSTM training")
print(f"Shape: {data_scaled.shape}")