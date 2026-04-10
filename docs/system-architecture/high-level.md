# 1. High-Level System Architecture


```code
┌─────────────────────────────────────────────────────────────────────────────┐
│                 AI TRAFFIC CONTROL SYSTEM ARCHITECTURE                │
└─────────────────────────────────────────────────────────────────────────────┘

           ┌──────────────────────────────────┐
           │         CLIENT LAYER          │
           │  Web • Mobile • External API  │
           └─────────────────┬────────────────┘
                           │
                           │ HTTPS (TLS 1.3)
                           │
         ┌───────────────────▼──────────────────┐
         │  JAVA API GATEWAY (Port 8080)     │
         │       Spring Boot 3.2.3           │
         ├──────────────────────────────────────┤
         │  • JWT Authentication (HS256)     │
         │  • Request Validation             │
         │  • Fallback Logic (RED signal)    │
         │  • Circuit Breaker Pattern        │
         └───────────────────┬──────────────────┘
                           │
                ┌───────────┴─────────────┐
                │                       │
    ┌────────────▼────────┐   ┌────────────▼────────────┐
    │  HEALTH CHECK     │   │  PREDICTION REQUESTS  │
    │  /health          │   │  /traffic/action      │
    └─────────────────────┘   └─┬───────────────────────┘
                              │
                  ┌────────────▼────────────┐
                  │ INFERENCE SERVICE     │
                  │  (Port 8000)          │
                  │  Python/FastAPI       │
                  ├─────────────────────────┤
                  │ • MAPPO RL Model      │
                  │ • 5-Junction Support  │
                  │ • GRU State Mgmt      │
                  │ • Action Masking      │
                  └────────────┬────────────┘
                              │
                ┌──────────────┴────────────┐
                │                         │
    ┌────────────▼──────────┐   ┌────────────▼────────────┐
    │  LSTM PREDICTOR     │   │  ACTION SELECTION     │
    │  (Port 8001)        │   │  (MAPPO Output)       │
    │  Python/FastAPI     │   │                       │
    ├───────────────────────┤   │ Actions:              │
    │ • Time-series LSTM  │   │ 0: RED                │
    │ • 15-min Forecast   │   │ 1: YELLOW             │
    │ • MAE < 10%         │   │ 2: GREEN              │
    │ • Data Pipeline     │   │ 3: GREEN_EXTENDED     │
    └───────────────────────┘   └────────────┬────────────┘
                                          │
                                          │ Signal State
                                          │
                              ┌────────────▼────────────┐
                              │  RESPONSE TO CLIENT   │
                              │ {                     │
                              │   action: 0-3,        │
                              │   signalState: "RED", │
                              │   confidence: 0.87    │
                              │ }                     │
                              └─────────────────────────┘


┌────────────────────────────────────────────────────────────────────────────────┐
│                          SUPPORTING SYSTEMS                             │
├────────────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌───────────────────────┐  ┌────────────────────┐  ┌──────────────────────┐  │
│  │  SUMO SIMULATOR     │  │   DOCKER         │  │  MONITORING        │  │
│  │  (SUMO v1.26)       │  │   COMPOSE        │  │  (Logs, Metrics)   │  │
│  ├───────────────────────┤  ├────────────────────┤  ├──────────────────────┤  │
│  │ • Road Network      │  │ • Multi-service  │  │ • Health Checks    │  │
│  │ • 7 Routes          │  │   Orchestration  │  │ • Performance      │  │
│  │ • 12-hour Sim       │  │ • Local Dev      │  │ • Error Tracking   │  │
│  │ • edgeData.xml      │  │ • Production     │  │ • Request Logs     │  │
│  └───────────────────────┘  └────────────────────┘  └──────────────────────┘  │
│                                                                         │
└────────────────────────────────────────────────────────────────────────────────┘
```

``` code
DATA FLOW EXAMPLE
─────────────────

Client Request:
  POST /api/traffic/action
  {
    "junctionId": "300839359",
    "observations": [0.12, 0.33, ..., 0.81]
  }
              │
              │ (JWT validated, parsed)
              ▼
  API Gateway (Spring Boot)
              │
              │ (forward to inference service)
              ▼
  Inference Service (FastAPI)
              │
              ├─► MAPPO Model (5 junctions)
              │        │
              │        └─► GRU Hidden State (per-junction)
              │
              ├─► Action Output: 0-3
              │
              └─► Confidence: 0.0-1.0
                        │
                        │ (signal state mapping)
                        ▼
  API Gateway Response:
  {
    "junctionId": "300839359",
    "predictedAction": 1,
    "signalState": "YELLOW",
    "confidence": 0.87,
    "timestamp": 1710000000000
  }
              │
              ▼
  Client
```


``` mermaid
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