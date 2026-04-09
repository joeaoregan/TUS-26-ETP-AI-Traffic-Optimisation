# Components


## 1. Python FastAPI Service (RL Inference Service)

- **Port:** 8000
- **Purpose:** Loads and serves trained PPO models for action prediction
- **Key Endpoints:**
  - `GET /health` - Health check
  - `POST /predict_action` - Action prediction endpoint
  - `GET /model_info` - Model information

## 2. Java Spring Boot API Gateway

- **Port:** 8080
- **Purpose:** REST API gateway that communicates with the Python service
- **Key Endpoints:**
  - `GET /api/traffic/health` - Health check
  - `GET /api/traffic/action` - Get traffic action (generates dummy observations)
  - `POST /api/traffic/action` - Predict action with custom observations

## 3. Docker Compose

- Orchestrates both services
- Manages networking and dependencies
- Provides health checks and monitoring

The Java Gateway receives raw vehicle counts, transforms them into an observation vector, and forwards them to the Python service for a decision.