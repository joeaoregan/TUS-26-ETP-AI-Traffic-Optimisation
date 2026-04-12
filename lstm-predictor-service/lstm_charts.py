"""
LSTM Traffic Predictor — Training & Performance Charts
Reads edgeData.xml, rebuilds the same training pipeline, and generates charts.
Run from project root:  conda run -n mappo python lstm-predictor-service/lstm_charts.py
"""

import xml.etree.ElementTree as ET
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.patches
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.optimizers import Adam
import os

OUT_DIR = 'SUMO/Results/LSTM'
os.makedirs(OUT_DIR, exist_ok=True)

EDGE_COLORS = ['#e74c3c', '#3498db', '#2ecc71', '#f39c12', '#9b59b6']
STYLE = {
    'figure.facecolor': '#0d1117',
    'axes.facecolor': '#161b22',
    'axes.edgecolor': '#30363d',
    'axes.labelcolor': '#c9d1d9',
    'axes.titlecolor': '#c9d1d9',
    'xtick.color': '#8b949e',
    'ytick.color': '#8b949e',
    'grid.color': '#21262d',
    'grid.linestyle': '--',
    'grid.alpha': 0.6,
    'text.color': '#c9d1d9',
    'legend.facecolor': '#21262d',
    'legend.edgecolor': '#30363d',
}

# ── Data ──────────────────────────────────────────────────────────────────────
print("Parsing edgeData.xml...")
tree = ET.parse('SUMO/Results/MAPPO/edgeData.xml')
root = tree.getroot()
edges_data = []
for interval in root.findall('interval'):
    t = float(interval.get('begin'))
    for edge in interval.findall('edge'):
        edges_data.append({
            'edge_id': edge.get('id'),
            'time': t,
            'density':     float(edge.get('density', 0)),
            'occupancy':   float(edge.get('occupancy', 0)),
            'waitingTime': float(edge.get('waitingTime', 0)),
            'timeLoss':    float(edge.get('timeLoss', 0)),
            'speed':       float(edge.get('speed', 0)),
        })
df = pd.DataFrame(edges_data)

top5 = df.groupby('edge_id')['density'].mean().nlargest(5).index.tolist()
df_top = df[df['edge_id'].isin(top5)].copy()
df_pivot = df_top.pivot_table(index='time', columns='edge_id', values='density', fill_value=0)
# Sort columns to match training order
df_pivot = df_pivot[top5]

hours = df_pivot.index / 3600
data = df_pivot.values

scaler = MinMaxScaler()
data_scaled = scaler.fit_transform(data)

SEQ_LEN = 3
def make_sequences(d, seq=SEQ_LEN):
    X, y = [], []
    for i in range(len(d) - seq):
        X.append(d[i:i+seq])
        y.append(d[i+seq])
    return np.array(X), np.array(y)

X, y = make_sequences(data_scaled)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

# ── Model ─────────────────────────────────────────────────────────────────────
print("Training LSTM model...")
tf.random.set_seed(42)
model = Sequential([
    LSTM(64, activation='relu', input_shape=(SEQ_LEN, data_scaled.shape[1])),
    Dropout(0.2),
    Dense(32, activation='relu'),
    Dropout(0.2),
    Dense(data_scaled.shape[1])
])
model.compile(optimizer=Adam(learning_rate=0.001), loss='mse', metrics=['mae'])

history = model.fit(
    X_train, y_train,
    epochs=50,
    batch_size=2,
    validation_data=(X_test, y_test),
    verbose=0,
)

y_pred_scaled = model.predict(X_test, verbose=0)
y_pred = scaler.inverse_transform(y_pred_scaled)
y_true = scaler.inverse_transform(y_test)

# Per-edge MAE and RMSE
mae_per_edge  = np.mean(np.abs(y_pred - y_true), axis=0)
rmse_per_edge = np.sqrt(np.mean((y_pred - y_true) ** 2, axis=0))

train_loss = history.history['loss']
val_loss   = history.history['val_loss']
train_mae  = history.history['mae']
val_mae    = history.history['val_mae']

print(f"Test Loss: {val_loss[-1]:.4f}  Test MAE: {val_mae[-1]:.4f}")

# ─────────────────────────────────────────────────────────────────────────────
# CHART 1 — Raw Traffic Density (top 5 edges over time)
# ─────────────────────────────────────────────────────────────────────────────
print("Chart 1: Raw traffic density...")
with plt.rc_context(STYLE):
    fig, ax = plt.subplots(figsize=(12, 5))
    for i, edge in enumerate(top5):
        ax.plot(hours, df_pivot[edge].values, marker='o', linewidth=2,
                color=EDGE_COLORS[i], label=edge, markersize=5)
    ax.set_title('Traffic Density Over Time — Top 5 Congested Edges', fontsize=14, pad=12)
    ax.set_xlabel('Simulation Time (hours)')
    ax.set_ylabel('Density (vehicles/km)')
    ax.legend(fontsize=9, loc='upper right')
    ax.grid(True)
    fig.tight_layout()
    out = f'{OUT_DIR}/chart1_density_over_time.png'
    fig.savefig(out, dpi=150, bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.close(fig)
    print(f"  Saved {out}")

# ─────────────────────────────────────────────────────────────────────────────
# CHART 2 — Training & Validation Loss / MAE
# ─────────────────────────────────────────────────────────────────────────────
print("Chart 2: Training curves...")
with plt.rc_context(STYLE):
    fig, axes = plt.subplots(1, 2, figsize=(13, 5))

    ax = axes[0]
    ax.plot(train_loss, color='#3498db', linewidth=2, label='Train Loss')
    ax.plot(val_loss,   color='#e74c3c', linewidth=2, label='Val Loss', linestyle='--')
    ax.set_title('Training vs Validation Loss (MSE)', fontsize=13)
    ax.set_xlabel('Epoch')
    ax.set_ylabel('MSE Loss')
    ax.legend()
    ax.grid(True)

    ax = axes[1]
    ax.plot(train_mae, color='#2ecc71', linewidth=2, label='Train MAE')
    ax.plot(val_mae,   color='#f39c12', linewidth=2, label='Val MAE', linestyle='--')
    ax.set_title('Training vs Validation MAE', fontsize=13)
    ax.set_xlabel('Epoch')
    ax.set_ylabel('MAE')
    ax.legend()
    ax.grid(True)

    fig.suptitle('LSTM Model — Training History (50 epochs)', fontsize=14, y=1.01)
    fig.tight_layout()
    out = f'{OUT_DIR}/chart2_training_history.png'
    fig.savefig(out, dpi=150, bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.close(fig)
    print(f"  Saved {out}")

# ─────────────────────────────────────────────────────────────────────────────
# CHART 3 — Predicted vs Actual density (all 5 edges)
# ─────────────────────────────────────────────────────────────────────────────
print("Chart 3: Predicted vs actual...")
with plt.rc_context(STYLE):
    fig, axes = plt.subplots(2, 3, figsize=(15, 8))
    axes = axes.flatten()

    for i in range(5):
        ax = axes[i]
        x = np.arange(len(y_true))
        ax.plot(x, y_true[:, i], color=EDGE_COLORS[i], linewidth=2, marker='o',
                markersize=5, label='Actual')
        ax.plot(x, y_pred[:, i], color='white', linewidth=1.5, marker='x',
                markersize=6, linestyle='--', label='Predicted')
        ax.set_title(f'{top5[i]}', fontsize=10)
        ax.set_xlabel('Test Sample')
        ax.set_ylabel('Density (veh/km)')
        ax.legend(fontsize=8)
        ax.grid(True)

    # Hide the 6th subplot
    axes[5].set_visible(False)

    fig.suptitle('LSTM — Predicted vs Actual Density (Test Set)', fontsize=14)
    fig.tight_layout()
    out = f'{OUT_DIR}/chart3_predicted_vs_actual.png'
    fig.savefig(out, dpi=150, bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.close(fig)
    print(f"  Saved {out}")

# ─────────────────────────────────────────────────────────────────────────────
# CHART 4 — Per-Edge MAE & RMSE bar chart
# ─────────────────────────────────────────────────────────────────────────────
print("Chart 4: Per-edge error metrics...")
with plt.rc_context(STYLE):
    fig, ax = plt.subplots(figsize=(11, 5))

    x = np.arange(len(top5))
    w = 0.35
    bars1 = ax.bar(x - w/2, mae_per_edge,  width=w, color=EDGE_COLORS, label='MAE',
                   alpha=0.85, edgecolor='#30363d')
    bars2 = ax.bar(x + w/2, rmse_per_edge, width=w, color=EDGE_COLORS, label='RMSE',
                   alpha=0.5,  edgecolor='#30363d', hatch='//')

    for bar in bars1:
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.02,
                f'{bar.get_height():.3f}', ha='center', va='bottom', fontsize=8)
    for bar in bars2:
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.02,
                f'{bar.get_height():.3f}', ha='center', va='bottom', fontsize=8)

    short_labels = [e[-10:] if len(e) > 10 else e for e in top5]
    ax.set_xticks(x)
    ax.set_xticklabels(short_labels, rotation=15, ha='right')
    ax.set_title('Per-Edge Prediction Error — MAE vs RMSE (Test Set)', fontsize=13)
    ax.set_ylabel('Error (vehicles/km)')
    ax.legend()
    ax.grid(True, axis='y')

    fig.tight_layout()
    out = f'{OUT_DIR}/chart4_per_edge_error.png'
    fig.savefig(out, dpi=150, bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.close(fig)
    print(f"  Saved {out}")

# ─────────────────────────────────────────────────────────────────────────────
# CHART 5 — Average density per edge (bar)
# ─────────────────────────────────────────────────────────────────────────────
print("Chart 5: Average density per edge...")
with plt.rc_context(STYLE):
    avg_density = df_top.groupby('edge_id')['density'].mean()[top5]
    avg_wait    = df_top.groupby('edge_id')['waitingTime'].mean()[top5]

    fig, axes = plt.subplots(1, 2, figsize=(13, 5))

    ax = axes[0]
    bars = ax.bar(range(5), avg_density.values, color=EDGE_COLORS, edgecolor='#30363d', alpha=0.9)
    for bar, val in zip(bars, avg_density.values):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
                f'{val:.1f}', ha='center', va='bottom', fontsize=9)
    ax.set_xticks(range(5))
    ax.set_xticklabels(short_labels, rotation=15, ha='right')
    ax.set_title('Average Traffic Density per Edge', fontsize=12)
    ax.set_ylabel('Density (veh/km)')
    ax.grid(True, axis='y')

    ax = axes[1]
    bars = ax.bar(range(5), avg_wait.values, color=EDGE_COLORS, edgecolor='#30363d', alpha=0.9)
    for bar, val in zip(bars, avg_wait.values):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                f'{val:.0f}s', ha='center', va='bottom', fontsize=9)
    ax.set_xticks(range(5))
    ax.set_xticklabels(short_labels, rotation=15, ha='right')
    ax.set_title('Average Waiting Time per Edge', fontsize=12)
    ax.set_ylabel('Waiting Time (seconds)')
    ax.grid(True, axis='y')

    fig.suptitle('Edge Traffic Characteristics (SUMO Simulation)', fontsize=14)
    fig.tight_layout()
    out = f'{OUT_DIR}/chart5_edge_characteristics.png'
    fig.savefig(out, dpi=150, bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.close(fig)
    print(f"  Saved {out}")

# ─────────────────────────────────────────────────────────────────────────────
# CHART 6 — Model summary card
# ─────────────────────────────────────────────────────────────────────────────
print("Chart 6: Model summary card...")
with plt.rc_context(STYLE):
    fig = plt.figure(figsize=(10, 5))
    gs  = gridspec.GridSpec(1, 2, width_ratios=[1.2, 1])

    # Left: architecture diagram
    ax_arch = fig.add_subplot(gs[0])
    ax_arch.set_xlim(0, 10)
    ax_arch.set_ylim(0, 10)
    ax_arch.axis('off')
    ax_arch.set_title('Model Architecture', fontsize=12, pad=8)

    layers = [
        ('Input',    '(3, 5)',          '#5dade2'),
        ('LSTM 64',  'relu, seq→vec',   '#2ecc71'),
        ('Dropout',  'p=0.2',           '#95a5a6'),
        ('Dense 32', 'relu',            '#e67e22'),
        ('Dropout',  'p=0.2',           '#95a5a6'),
        ('Output',   '(5,) densities',  '#e74c3c'),
    ]
    y_positions = np.linspace(8.5, 1.5, len(layers))
    for (name, desc, color), y in zip(layers, y_positions):
        ax_arch.add_patch(matplotlib.patches.FancyBboxPatch((1, y-0.35), 8, 0.7,
            boxstyle='round,pad=0.1', facecolor=color, edgecolor='#30363d', alpha=0.85))
        ax_arch.text(5, y, f'{name}  —  {desc}', ha='center', va='center',
                     fontsize=9, color='white', fontweight='bold')
        if y > y_positions[-1]:
            ax_arch.annotate('', xy=(5, y - 0.4), xytext=(5, y - 0.9),
                arrowprops=dict(arrowstyle='->', color='#8b949e', lw=1.5))

    # Right: metrics table
    ax_m = fig.add_subplot(gs[1])
    ax_m.axis('off')
    ax_m.set_title('Performance Metrics', fontsize=12, pad=8)

    rows = [
        ['Metric', 'Value'],
        ['Input shape', '(3 × 5)'],
        ['Output shape', '(5,)'],
        ['Epochs', '50'],
        ['Batch size', '2'],
        ['Optimizer', 'Adam (lr=0.001)'],
        ['Loss fn', 'MSE'],
        [f'Test Loss', f'{val_loss[-1]:.4f}'],
        [f'Test MAE', f'{val_mae[-1]:.4f}'],
        ['Train samples', str(len(X_train))],
        ['Test samples', str(len(X_test))],
    ]
    tbl = ax_m.table(cellText=rows[1:], colLabels=rows[0],
                     loc='center', cellLoc='center')
    tbl.auto_set_font_size(False)
    tbl.set_fontsize(9)
    tbl.scale(1.1, 1.4)
    for (row, col), cell in tbl.get_celld().items():
        cell.set_facecolor('#21262d' if row % 2 == 0 else '#161b22')
        cell.set_edgecolor('#30363d')
        cell.set_text_props(color='#c9d1d9')
        if row == 0:
            cell.set_facecolor('#1f6feb')
            cell.set_text_props(color='white', fontweight='bold')

    fig.suptitle('LSTM Traffic Predictor — Model Summary', fontsize=13, y=1.01)
    fig.tight_layout()
    out = f'{OUT_DIR}/chart6_model_summary.png'
    fig.savefig(out, dpi=150, bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.close(fig)
    print(f"  Saved {out}")

print(f"\nAll charts saved to {OUT_DIR}/")
