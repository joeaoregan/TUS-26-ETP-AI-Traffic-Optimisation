### Get Traffic Action (Auto-generated observations)
First, authenticate and store the JWT:

```bash
TOKEN=$(curl -s -X POST http://localhost:8080/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}' | jq -r '.accessToken')
```

Then call the protected endpoint:

```bash
curl -X GET http://localhost:8080/api/traffic/action \
  -H "Authorization: Bearer $TOKEN"
```

### 🎯 Get Traffic Action (Demo — random junction)
```bash
curl -X GET http://localhost:8080/api/traffic/action
```

Response:

```json
{
  "junctionId": "300839359",
  "predictedAction": 1,
  "signalState": "YELLOW",
  "timestamp": 1684756800000,
  "status": "success"
}
```

---

### 🔮 Predict Action with Custom Observations
```bash
curl -X POST http://localhost:8080/api/traffic/action \
  -H "Content-Type: application/json" \
  -d '{
    "junctionId": "joinedS_265580996_300839357",
    "observations": [1.0, 0.0, 0.0, 0.0, 1.0, 0.12, 0.08, 0.33, 0.41,
                     0.22, 0.55, 0.18, 0.62, 0.70, 0.81, 0.50, 0.35, 0.44, 0.29],
    "metadata": "morning-peak"
  }'
```

Response:

```json
{
  "junctionId": "joinedS_265580996_300839357",
  "predictedAction": 2,
  "signalState": "GREEN",
  "timestamp": 1684756800000,
  "status": "success"
}
```

**Known junction IDs:**

| Junction ID | Phases | Observation size |
|---|---|---|
| `joinedS_265580996_300839357` | 4 | 19 |
| `300839359` | 2 | ~8 |
| `265580972` | 2 | ~8 |
| `1270712555` | 2 | ~8 |
| `8541180897` | 2 | ~8 |

Observations smaller than 19 are zero-padded internally. `junctionId` is required.

---

### 🔄 Reset Hidden States
Call at the start of each new simulation run to clear MAPPO GRU memory.

```bash
curl -X POST http://localhost:8080/api/traffic/reset
```

Response:

```json
{
  "status": "ok",
  "message": "Hidden states reset for all junctions"
}
```

---

### 💚 Health Check
```bash
curl http://localhost:8080/api/traffic/health
```

Response:

```json
{
  "status": "healthy",
  "inferenceService": "up",
  "timestamp": 1684756800000
}
```
