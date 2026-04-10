# Changelog

All notable changes to the AI-Driven Predictive Traffic Flow Optimisation System will be documented in this file.

## [2.1.0] - 2026-04-09

### Added
- **JWT Authentication:** Implemented stateless token-based security in Java API Gateway
  - HS256 HMAC signing for bearer tokens
  - Configurable token expiration (default 60 minutes)
  - Protected endpoints: `/api/traffic/action` (GET/POST), `/api/traffic/reset`
  - Public endpoints: `/api/auth/login`, `/api/traffic/health`, Swagger UI
  - New DTOs: `LoginRequest`, `LoginResponse`, `ErrorResponse`

- **LSTM Traffic Predictor Framework:** Foundation for time-series forecasting service
  - Architecture defined with FastAPI endpoints (`/health`, `/forecast`, `/model_info`)
  - Data pipeline ready (loader, preprocessor modules)
  - Configured for SUMO integration (edgeData.xml input)
  - Target: 15-minute ahead forecasting with MAE < 10%
  - Supports all 5 major junctions

- **SUMO Documentation:** Comprehensive service documentation added
  - `docs/sumo/architecture.md` — Network structure, file organization, data flow
  - `docs/sumo/key-features.md` — Traffic flows, route configuration, output formats

- **Enhanced Test Suite:** `test_api.py` updated with improved usability
  - Color-coded output (green/red/blue) for better readability
  - Test result tracking (e.g., "4/4 tests passed")
  - Boolean status returns for each test function
  - Requires: `colorama` package

- **Documentation Updates:**
  - `docs/index.md` — Added service documentation section, LSTM quick link, security section
  - `docs/features.md` — Updated feature matrix with JWT checkmarks and LSTM/SUMO status
  - `docs/api-gateway/index.md` — Added JWT authentication section with config table
  - `docs/api-gateway/endpoints.md` — Added `/api/auth/login` endpoint documentation
  - `docs/lstm/architecture.md` — Complete LSTM service architecture documentation
  - `docs/lstm/endpoints.md` — LSTM API endpoints (health, model_info, forecast)
  - `docs/lstm/key-features.md` — LSTM service features and capabilities
  - README.md files updated to reflect JWT integration in main branch

### Changed
- **System Architecture Description:** Updated to emphasize JWT authentication and LSTM forecasting
- **Feature Matrix:** Reorganized to reflect current implementation status
  - JWT moved from "optional" to "implemented"
  - LSTM endpoints marked as framework-ready (awaiting model training)
  - SUMO status clarified: "fully operational as standalone, not yet live-integrated with RL"

- **Java API Gateway README:** Enhanced testing section with colorama dependency and color output documentation

### Security
- JWT authentication now production-ready on main branch (previously in A00163691-JWTAuth branch)
- Stateless token management with configurable expiration
- Bearer token validation on all protected endpoints

---

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
- **Simulation Environment:** Integrated SUMO (Simulation of Urban MObility) configurations for the Athlone "Orange Loop".

### Changed
- **Monorepo Consolidation:** Merged standalone API branch into the main branch to establish a cohesive pipeline.
- **Dependency Management:** Updated Python requirements to include FastAPI, Pydantic v2, and Stable-Baselines3.

### Security
- **Data Integrity:** Initial implementation of TLS 1.3 for telemetry ingestion.
- **Authentication:** Added digital signature placeholders in `OpenApiConfig.java` to prevent data injection attacks.