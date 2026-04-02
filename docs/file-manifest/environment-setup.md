# Environment Setup

## Prerequisites Installed

- Docker & Docker Compose (for containerized deployment)
- Python 3.9+ (for running select_model.py and test_api.py)
- Java 17+ (optional, for local Java development)
- Maven (optional, for building Java locally)

## Directories Created

```
ai-traffic-api/
├── rl-inference-service/
│   ├── app/
│   │   └── models/         (will contain model.zip)
│   └── (config files)
└── java-api-gateway/
    ├── src/main/
    │   ├── java/...
    │   └── resources/
    └── (config files)
```

## Volumes/Mounts (Docker)

- Python models: `./rl-inference-service/app/trained_models:/app/trained_models`
- Java application: Built into container image