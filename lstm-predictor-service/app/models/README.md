# Models Module

## Overview
Contains model definitions, training scripts, and preprocessing utilities for the LSTM traffic forecaster.

## Files

- **`preprocessor.py`** — Data preprocessing pipeline
  - `DataPreprocessor` class for scaler management
  - Normalization, denormalization, sequence creation
  - See [`app/utils/README.md`](../utils/README.md) for detailed docs

- **`lstm_train.py`** — Model training script
  - Trains LSTM on SUMO edge data
  - Persists model to `app/trained_models/`
  - Run: `python app/models/lstm_train.py`

## Usage

See `app/trained_models/README.md` for inference examples.