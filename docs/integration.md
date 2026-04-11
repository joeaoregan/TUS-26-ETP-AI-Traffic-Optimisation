# Service Integration Guide

## Architecture

RL Service (`8000`) + LSTM Service (`8001`) work together for traffic optimization.

## Testing

Run the integration test:
```bash
python lstm-predictor-service/test_rl_integration.py
```

## API Endpoints

### RL Service

!!! success "POST `/predict_action`"
    Get signal phase

!!! success "POST `/reset_hidden`"
    Reset hidden states

!!! note "GET `/health`"
    Health check

### LSTM Service

!!! success "POST `/predict`"
    Density prediction

!!! success "POST `/predict-batch`"
    Batch predictions

!!! note "GET `/health`"
    Health check

## Configuration

See .env.example in each service directory.

```py title="rl-inference-service\.env.example"
# RL Inference Service Configuration

# Server
API_HOST=0.0.0.0
API_PORT=8000

# Model
MAPPO_AGENT_PATH=app/trained_models/agent.th

# Development mode
API_RELOAD=false

---

# AWS Deployment (Optional)

# EC2/ECS Task Definition
AWS_REGION=eu-west-1
AWS_INSTANCE_TYPE=t3.micro

# ECS Task Configuration
AWS_ECS_TASK_CPU=512
AWS_ECS_TASK_MEMORY=1024
AWS_ECS_CONTAINER_PORT=8000

# AppRunner (serverless container)
AWS_APPRUNNER_SERVICE_NAME=rl-inference-service
AWS_APPRUNNER_INSTANCE_ROLE_ARN=arn:aws:iam::ACCOUNT_ID:role/AppRunnerServiceRole

# Optional: Performance monitoring
AWS_XRAY_ENABLED=false
AWS_XRAY_DAEMON_ADDRESS=127.0.0.1:2000
```

```py title="rl-inference-service\.env.example"
# LSTM Traffic Predictor Configuration

# Server
API_HOST=0.0.0.0
API_PORT=8001

# Model paths (for Docker/production)
MODEL_PATH=app/trained_models/lstm_model.keras
SCALER_PATH=app/trained_models/scaler.pkl

# Logging
LOG_LEVEL=INFO

# Optional: Development mode (auto-reload on code changes)
API_RELOAD=false

---

# AWS Deployment (Optional)

# EC2/ECS Task Definition
AWS_REGION=eu-west-1
AWS_INSTANCE_TYPE=t3.micro

# S3 (for model storage/backup)
AWS_S3_BUCKET=lstm-traffic-models
AWS_S3_MODEL_KEY=lstm_model.keras
AWS_S3_SCALER_KEY=scaler.pkl

# CloudWatch Logging
AWS_CLOUDWATCH_LOG_GROUP=/aws/lstm-predictor
AWS_CLOUDWATCH_LOG_STREAM=inference-service

# Secrets Manager (for sensitive config)
AWS_SECRETS_MANAGER_NAME=lstm-predictor-config

# ECS Task Configuration
AWS_ECS_TASK_CPU=512
AWS_ECS_TASK_MEMORY=1024
AWS_ECS_CONTAINER_PORT=8001

# AppRunner (serverless container)
AWS_APPRUNNER_SERVICE_NAME=lstm-predictor-service
AWS_APPRUNNER_INSTANCE_ROLE_ARN=arn:aws:iam::ACCOUNT_ID:role/AppRunnerServiceRole

# Optional: Performance monitoring
AWS_XRAY_ENABLED=false
AWS_XRAY_DAEMON_ADDRESS=127.0.0.1:2000
```