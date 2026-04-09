# Key Features (Java API Gateway)

[Feature List](../features.md#java-api-gateway)

- **Dual Prediction Modes**:
  - **Demo Mode** (`GET /api/traffic/action`): Generates random observations for quick testing
  - **Custom Mode** (`POST /api/traffic/action`): Accepts real or experimental observation vectors

- **Flexible Observations**: Supports variable-length observation vectors (up to 19 floats per junction)

- **Multiple Junction Support**: Preconfigured for 5 known traffic junctions:
  - `joinedS_265580996_300839357`
  - `300839359`
  - `265580972`
  - `1270712555`
  - `8541180897`

- **Signal State Mapping**: Translates RL model outputs (0-3) to human-readable states:
  - `0` → RED
  - `1` → YELLOW
  - `2` → GREEN
  - `3` → GREEN_EXTENDED
  - `default` → UNKNOWN

- **Graceful Degradation**: Falls back to RED signal when inference service is unavailable

- **Stateful Inference**: Includes endpoints to reset GRU hidden states for multi-step simulations
