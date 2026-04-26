# Key Features (Python Inference Service)

[Feature List](../features.md#python-rl-inference-service)

## Supported Junctions

The service manages these 5 junctions with the following action spaces:

1. **joinedS_265580996_300839357** - 4 valid phases (0, 1, 2, 3)
2. **300839359** - 2 valid phases (0, 1)
3. **265580972** - 2 valid phases (0, 1)
4. **1270712555** - 2 valid phases (0, 1)
5. **8541180897** - 2 valid phases (0, 1)

## Neural Network Architecture

The model uses a shared RNNAgent with the following structure:

- **Input Layer**: Concatenates observations + agent ID one-hot encoding
  - Observation vector: up to 19 floats (zero-padded to this size)
  - Agent ID one-hot: 5 floats (one per junction)
  - Total input: 24 floats

- **Hidden Layer**: GRUCell
  - Dimension: 128
  - Maintains stateful hidden state per junction across calls

- **Output Layer**: Fully connected
  - Outputs logits for all possible actions (4 max)
  - Masked by junction-specific action availability

- **Activation**: ReLU on first layer, softmax on output

## Observation Format

Each observation contains traffic state information including:
- Phase encoding (one-hot representation of current signal phase)
- Minimum green flag (whether minimum green time has elapsed)
- Lane queue lengths for approach lanes
- Vehicle wait times
- Gap detection values

Example observation sizes:
- joinedS junction: 19 floats (full-featured)
- Other junctions: ~8-10 floats (zero-padded to 19 internally)
