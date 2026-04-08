
# How to Use Each Component

## select_model.py

```bash
python select_model.py
# Shows all available models from Results/sweeps*
# Allows interactive selection
# Copies chosen model to rl-inference-service/app/trained_models/
```

## test_api.py

```bash
python test_api.py
# Requires services to be running (via docker-compose up)
# Tests all API endpoints
# Includes load testing capability
```

## start.bat / start.sh

```bash
start.bat  # Windows
./start.sh # Linux/Mac
# Builds and starts Docker services
# Displays service URLs
```

## docker-compose.yml

```yaml
# Services defined:
# - rl-inference (Python, port 8000)
# - java-gateway (Java, port 8080)
# Networking: traffic-network bridge
# Health checks: Enabled
```