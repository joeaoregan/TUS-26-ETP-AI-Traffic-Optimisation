# Changelog
All notable changes to the AI-Driven Predictive Traffic Flow Optimisation System will be documented in this file.

## [2.0.0] - 2026-03-31

### Changed
- **RL Model:** Replaced single-agent PPO (Stable-Baselines3, `model.zip`) with MAPPO v4 (EPyMARL, `agent.th`) — shared GRU RNNAgent controlling 5 junctions simultaneously.
- **Python inference service:** `main.py` rewritten to load EPyMARL `RNNAgent` (PyTorch) instead of SB3 PPO. Architecture: `fc1(24→128) → GRUCell(128→128) → fc2(128→4)`.
- **POST `/predict_action` payload:** Now requires `junction_id` (string) and `obs_data` (float[]). Previously only `obs_data` was needed.
- **POST `/api/traffic/action` payload (Java):** Now requires `junctionId` (string) and `observations` (float[], max 19). Previously only `observations` was needed.
- **Response payload:** Both services now include `junctionId` / `junction_id` in the prediction response.
- **Environment variable:** `MODEL_PATH`, `OBSERVATION_SHAPE_DIM`, `NUM_AGENTS` replaced by `MAPPO_AGENT_PATH`.
- **Observation dimension:** 9 → up to 19 (padded to max junction obs size internally).
- **Agent count:** 1 → 5 (one per controlled junction).
- **Docker images:** Versioned as `rl-inference-service:2.0.0` and `traffic-api-gateway:2.0.0`.

### Added
- **POST `/reset_hidden`** (Python) and **POST `/api/traffic/reset`** (Java): Reset MAPPO GRU hidden states between simulation runs.
- **GET `/model_info`:** Now returns full junction map with agent indices and action masks.
- **GRU hidden state management:** Per-junction recurrent state maintained between `/predict_action` calls within a simulation run.

### Removed
- `stable-baselines3` and `shimmy` dependencies from `requirements.txt`.
- `MODEL_PATH`, `OBSERVATION_SHAPE_DIM`, `NUM_AGENTS` environment variables.

### Performance
- Mean waiting time reduced **69.8%** vs fixed-time baseline (28.8 s → 8.7 s) with MAPPO v4 model.
- 100% episode completion rate (vs 13.3% for previous IPPO model).

---

## [1.0.0] - 2026-03-21
### Added
- **Microservices Architecture:** Integrated Java Spring Boot API Gateway and Python RL-Inference service.
- **ML Pipeline:** Support for PPO (Proximal Policy Optimization) model inference.
- [cite_start]**Simulation Environment:** Integrated SUMO (Simulation of Urban MObility) configurations for the Athlone "Orange Loop"[cite: 101, 161, 424].

### Changed
- [cite_start]**Monorepo Consolidation:** Merged standalone API branch into the main branch to establish a cohesive pipeline[cite: 64, 455].
- **Dependency Management:** Updated Python requirements to include FastAPI, Pydantic v2, and Stable-Baselines3.

### Security
- [cite_start]**Data Integrity:** Initial implementation of TLS 1.3 for telemetry ingestion[cite: 424].
- [cite_start]**Authentication:** Added digital signature placeholders in `OpenApiConfig.java` to prevent data injection attacks[cite: 43, 63, 500].