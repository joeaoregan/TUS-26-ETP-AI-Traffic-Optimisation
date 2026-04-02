# 2. Request-Response Flow Diagram

## **GET /api/traffic/action** (Auto-generated observations)

```mermaid
sequenceDiagram
    participant Client as External Client
    participant JG as Java Gateway<br/>Port 8080
    participant PS as Python Service<br/>Port 8000
    participant Model as RL Model<br/>PPO
    
    Client->>JG: GET /api/traffic/action
    
    Note over JG: Generate dummy<br/>observations (10 values)
    JG->>JG: Create random observation<br/>values [0-1]
    
    JG->>PS: POST /predict_action<br/>{"obs_data": [0.1, 0.2, ...]}
    
    Note over PS: Load model & predict
    PS->>Model: Call model.predict()
    Model-->>PS: Return action (0-3)
    
    Note over PS: Format response
    PS-->>JG: {"action": 2}
    
    Note over JG: Map action to signal
    JG->>JG: 2 → "GREEN"
    
    JG-->>Client: {<br/>"predictedAction": 2,<br/>"signalState": "GREEN",<br/>"timestamp": ...,<br/>"status": "success"<br/>}
```

## **POST /api/traffic/action** (Custom observations)

```mermaid
sequenceDiagram
    participant Client as External Client
    participant JG as Java Gateway<br/>Port 8080
    participant Val as Validator
    participant PS as Python Service<br/>Port 8000
    participant Model as RL Model<br/>PPO
    
    Client->>JG: POST /api/traffic/action<br/>{"observations": [0.1, 0.2, ...]}
    
    JG->>Val: Validate observations
    alt Validation Success
        Val-->>JG: ✓ Valid
    else Validation Failed
        Val-->>JG: ✗ Error: Empty/Null
        JG-->>Client: 400 Bad Request
    end
    
    JG->>PS: POST /predict_action<br/>{"obs_data": [0.1, 0.2, ...]}
    
    Note over PS: Process with model
    PS->>Model: Call model.predict()
    Model-->>PS: Return action
    
    PS-->>JG: {"action": 1}
    
    JG-->>Client: {<br/>"predictedAction": 1,<br/>"signalState": "YELLOW",<br/>"timestamp": ...,<br/>"status": "success"<br/>}
```

## **GET /api/traffic/health** (Health Check)

```mermaid
sequenceDiagram
    participant Client as External Client
    participant JG as Java Gateway<br/>Port 8080
    participant HealthCheck as Health Checker
    participant PS as Python Service<br/>Port 8000
    
    Client->>JG: GET /api/traffic/health
    
    JG->>HealthCheck: Check all services
    
    HealthCheck->>PS: GET /health
    
    alt Python Service "Up"
        PS-->>HealthCheck: {"status": "healthy"}
        HealthCheck-->>JG: ✓ All healthy
    else Python Service "Down"
        PS--xHealthCheck: Connection refused
        HealthCheck-->>JG: ⚠️ Degraded
    end
    
    JG-->>Client: {<br/>"status": "healthy",<br/>"inferenceService": "up",<br/>"timestamp": ...<br/>}
```