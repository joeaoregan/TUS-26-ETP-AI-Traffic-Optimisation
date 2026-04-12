# lstm_train.py
# Prepares the data from SUMO edgeData.xml and builds an LSTM model for traffic prediction.
# Focuses on the top 5 most congested edges based on density.

import os
import xml.etree.ElementTree as ET

import joblib
import numpy as np
import pandas as pd
import tensorflow as tf
from colorama import Fore, init
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.layers import Dense, Dropout, Input, LSTM
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import Adam

init(autoreset=True)

os.environ["TF_KERAS"] = "1"

# Configuration
EDGE_DATA_XML = "SUMO/Results/MAPPO/edgeData.xml"
SEQ_LENGTH = 3
TOP_N_EDGES = 5

EPOCHS = 50
BATCH_SIZE = 2
LEARNING_RATE = 0.001

MODEL_DIR = "lstm-predictor-service/app/trained_models"
WEIGHTS_FILENAME = "lstm_model.weights.h5"
SCALER_FILENAME = "scaler.joblib"

# Optional exports (ONLY enable if verified they load in the target environment)
EXPORT_KERAS_MODEL = False      # writes lstm_model.keras
EXPORT_SAVEDMODEL = False       # writes lstm_model_tf/ (SavedModel directory)

# Helper function to create sequences for LSTMs
def create_sequences(data: np.ndarray, seq_length: int = 3):
    X, y = [], []
    for i in range(len(data) - seq_length):
        X.append(data[i : i + seq_length])
        y.append(data[i + seq_length])
    return np.array(X), np.array(y)


# Load + prepare data
# -------------------
# Parse edgeData.xml
# tree = ET.parse('SUMO/Results/MAPPO/edgeData.xml')
tree = ET.parse(EDGE_DATA_XML)
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
top_edges = df.groupby('edge_id')['density'].mean().nlargest(TOP_N_EDGES).index.tolist()
df_filtered = df[df['edge_id'].isin(top_edges)].copy()

# Prepare data
df_pivot = df_filtered.pivot_table(index='time', columns='edge_id', values='density', fill_value=0)
data = df_pivot.values

# Normalize
scaler = MinMaxScaler()
data_scaled = scaler.fit_transform(data)

# Create sequences for LSTM
seq_length = SEQ_LENGTH
X, y = create_sequences(data_scaled, seq_length)

print(f"X shape: {X.shape}, y shape: {y.shape}")

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

print(f"Training set: {X_train.shape}, Test set: {X_test.shape}")

# Build LSTM model
# ----------------
n_features = data_scaled.shape[1]

# Build LSTM model
model = Sequential([
    Input(shape=(seq_length, n_features)),
    LSTM(64, activation='relu'),
    Dropout(0.2),
    Dense(32, activation='relu'),
    Dropout(0.2),
    Dense(n_features),
])

model.compile(optimizer=Adam(learning_rate=LEARNING_RATE), loss='mse', metrics=['mae'])

print("\nTraining LSTM...")
history = model.fit(
    X_train, y_train,
    epochs=EPOCHS,
    batch_size=BATCH_SIZE,
    validation_data=(X_test, y_test),
    verbose=1,
)

# Evaluate
test_loss, test_mae = model.evaluate(X_test, y_test)
print(f"\n{Fore.YELLOW}Test Loss: {test_loss:.4f}, Test MAE: {test_mae:.4f}")

# Extra metrics (scaled space)
y_pred = model.predict(X_test, verbose=0)

y_test_2d = y_test.reshape(y_test.shape[0], -1)
y_pred_2d = y_pred.reshape(y_pred.shape[0], -1)

mae_scaled = mean_absolute_error(y_test_2d, y_pred_2d)
rmse_scaled = np.sqrt(mean_squared_error(y_test_2d, y_pred_2d))

print(f"{Fore.YELLOW}Test MAE (scaled, sklearn):  {mae_scaled:.6f}")
print(f"{Fore.YELLOW}Test RMSE (scaled, sklearn): {rmse_scaled:.6f}")

# Create model directory
model_dir = MODEL_DIR
os.makedirs(model_dir, exist_ok=True)

# Save model in multiple formats
print(f"\n{Fore.CYAN}=== Saving Models ===")

# # 1. HDF5 (legacy - keep for documentation)
# hdf5_path = os.path.join(model_dir, 'lstm_model.h5')
# # model.save(hdf5_path)  # Commented out - using newer formats instead
# print(f"{Fore.LIGHTBLACK_EX}[SKIPPED] HDF5 format (legacy)")

# # 2. Keras native format (modern, efficient)
# keras_path = os.path.join(model_dir, 'lstm_model.keras')
# model.save(keras_path)
# print(f"{Fore.GREEN}✓ Keras format saved to {keras_path}")

# # 3. TensorFlow SavedModel (production deployment)
# # Note: Keras 3 uses model.export() instead of save_format='tf'
# tf_path = os.path.join(model_dir, 'lstm_model_tf')
# model.export(tf_path)
# print(f"{Fore.GREEN}✓ TensorFlow SavedModel saved to {tf_path}")

# # Save scaler
# scaler_path = os.path.join(model_dir, 'scaler.pkl')
# pickle.dump(scaler, open(scaler_path, 'wb'))
# print(f"{Fore.GREEN}✓ Scaler saved to {scaler_path}")

# print(f"\n{Fore.CYAN}=== Training Complete ===")
# print(f"{Fore.YELLOW}Models ready for inference in: {model_dir}")

# Save weights only (avoids Keras 3.x serialization issues)

# weights_path = os.path.join(model_dir, 'lstm_model_weights.h5')
weights_path = os.path.join(model_dir, WEIGHTS_FILENAME)
model.save_weights(weights_path)
print(f"{Fore.GREEN}✓ Weights saved to {weights_path}")

# Save scaler
# scaler_path = os.path.join(model_dir, 'scaler.pkl')
# pickle.dump(scaler, open(scaler_path, 'wb'))
# print(f"{Fore.GREEN}✓ Scaler saved to {scaler_path}")

# Save scaler using joblib (more robust than pickle)
scaler_path = os.path.join(model_dir, SCALER_FILENAME)
joblib.dump(scaler, scaler_path)
print(f"{Fore.GREEN}✓ Scaler saved to {scaler_path}")

# Optional exports (only if you explicitly enable them)
if EXPORT_KERAS_MODEL:
    keras_path = os.path.join(model_dir, "lstm_model.keras")
    model.save(keras_path)
    print(f"{Fore.GREEN}✓ Keras format saved to {keras_path}")

if EXPORT_SAVEDMODEL:
    tf_path = os.path.join(model_dir, "lstm_model_tf")
    try:
        model.export(tf_path)
        print(f"{Fore.GREEN}✓ TensorFlow SavedModel exported to {tf_path}")
    except Exception as e:
        print(f"{Fore.RED}[WARN] SavedModel export failed: {e}")

print(f"\n{Fore.CYAN}=== Training Complete ===")
print(f"{Fore.YELLOW}Models ready for inference in: {model_dir}")