# Local Development

## 🧪 Testing Endpoints Locally

### Java Gateway (Port 8080)

```bash
# 1. Login and get JWT token
TOKEN=$(curl -s -X POST http://localhost:8080/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}')

# 2. Test health (no auth needed)
curl http://localhost:8080/api/traffic/health

# 3. Get demo prediction (requires JWT)
curl -H "Authorization: Bearer $TOKEN" \
  http://localhost:8080/api/traffic/action

# 4. Custom prediction
curl -X POST -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "junctionId":"300839359",
    "observations":[0.0,1.0,0.0,0.0,0.0,1.0,0.0,1.0,0.12,0.08,0.33,0.41,0.22,0.55,0.18,0.62,0.70,0.81,0.50]
  }' \
  http://localhost:8080/api/traffic/action

# 5. Reset hidden states
curl -X POST -H "Authorization: Bearer $TOKEN" \
  http://localhost:8080/api/traffic/reset
```

### Python Inference Service (Port 8000)

```bash
# Health check
curl http://localhost:8000/health

# Model info
curl http://localhost:8000/model_info

# Predict action
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{
    "junction_id":"300839359",
    "obs_data":[0.0,1.0,1.0,0.12,0.33,0.41,0.22,0.55,0.18,0.62,0.70,0.81,0.50,0.5,0.4,0.3,0.2,0.1,0.05]
  }' \
  http://localhost:8000/predict_action

# Reset hidden states
curl -X POST http://localhost:8000/reset_hidden
```

### LSTM Predictor (Port 8000 or 8001)

```bash
# Health check
curl http://localhost:8000/health

# Model info
curl http://localhost:8000/model-info

# Predict density
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{
    "data":[
      [18.93,10.13,5.23,4.14,3.08],
      [24.02,11.01,8.98,5.42,4.26],
      [22.14,9.34,5.62,4.57,3.81]
    ]
  }' \
  http://localhost:8000/predict
```

---

## Pretty-Print JSON Output

**Note**: Install `jq` for pretty JSON formatting:
- **Mac**: `brew install jq`
- **Linux**: `apt-get install jq` or `sudo apt install jq`
- **Windows**: Download from https://stedolan.github.io/jq/download/ or `choco install jq` (if using Chocolatey)

**Example**:
```bash
curl http://localhost:8000/health | jq
```

Output:
```json
{
  "status": "healthy",
  "model_loaded": true,
  "junctions": [
    "joinedS_265580996_300839357",
    "300839359",
    "265580972",
    "1270712555",
    "8541180897"
  ]
}
```