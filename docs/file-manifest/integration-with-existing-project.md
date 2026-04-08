# Integration with Existing Project

## Location in Project

```
my-network/
├── ai-traffic-api/                 ← NEW API files here
├── Results/
│   ├── sweeps/                     ← Existing trained models
│   ├── sweeps_2/ through sweeps_9/
│   └── (other directories)
├── train_ppo_agent.py              ← Can call API
└── ... (other files)
```

## Data Flow Integration

```
train_ppo_agent.py
    ↓
Can now use:
    ↓
ai-traffic-api/
├── select_model.py          (Choose best model)
└── test_api.py              (Verify predictions)
    ↓
Docker services running:
├── Python FastAPI Service   (Model inference)
└── Java API Gateway         (REST interface)
    ↓
External system or SUMO can call:
    http://localhost:8080/api/traffic/action
```