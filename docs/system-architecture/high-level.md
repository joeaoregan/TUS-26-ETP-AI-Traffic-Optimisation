# 1. High-Level System Architecture

```mermaid
graph TB
    Client["🚗 Client Applications<br/>(SUMO Simulation<br/>External Systems<br/>Mobile Apps)"]
    
    subgraph Docker["🐳 Docker Container Network"]
        subgraph JavaService["Java API Gateway<br/>Spring Boot 3.2<br/>Port 8080"]
            Controller["TrafficController<br/>REST Endpoints"]
            ServiceClient["RlInferenceClient<br/>HTTP Client"]
        end
        
        subgraph PythonService["Python FastAPI Service<br/>Port 8000"]
            API["FastAPI App<br/>uvicorn"]
            ModelLoader["Model Loader<br/>PPO Model"]
            Predictor["Predictor<br/>stable-baselines3"]
        end
    end
    
    ModelStorage["📦 Trained Models<br/>Results/sweeps/*<br/>model.zip"]
    
    Client -->|HTTP:8080| Controller
    Controller -->|HTTP:8000| ServiceClient
    ServiceClient -->|HTTP Request| API
    API --> ModelLoader
    ModelLoader -->|Load| ModelStorage
    ModelLoader --> Predictor
    Predictor -->|Prediction| API
    API -->|JSON Response| ServiceClient
    ServiceClient -->|Response| Controller
    Controller -->|JSON Response| Client
    
    style Docker fill:#e1f5ff
    style JavaService fill:#fff3e0
    style PythonService fill:#f3e5f5
    style ModelStorage fill:#e8f5e9
```