import os

import tensorflow as tf
from colorama import Fore, init

init(autoreset=True)

# Get the directory of this script
script_dir = os.path.dirname(os.path.abspath(__file__))
base_dir = os.path.join(script_dir, '..')  # Go up to app/

# Paths relative to app/
keras_model_path = os.path.join(base_dir, 'trained_models/lstm_model.keras')
savedmodel_dir = os.path.join(base_dir, 'trained_models/lstm_model')

# Load and convert
model = tf.keras.models.load_model(keras_model_path)
model.export(savedmodel_dir)  # Use export() instead of save()

print(f"{Fore.GREEN}✓ Model exported to SavedModel format")
print(f"{Fore.GREEN}✓ Location: {savedmodel_dir}")
