import requests
import json

BASE_LSTM = "http://localhost:8001"
BASE_RL = "http://localhost:8000"

print("=" * 60)
print("Testing RL + LSTM Integration")
print("=" * 60)

# Test 1: Health checks
print("\n1. Health Checks")
try:
    lstm_health = requests.get(f"{BASE_LSTM}/health").json()
    rl_health = requests.get(f"{BASE_RL}/health").json()
    print(f"   ✓ LSTM: {lstm_health['status']}")
    print(f"   ✓ RL:   {rl_health['status']}")
except Exception as e:
    print(f"   ✗ Error: {e}")

# Test 2: RL predict
print("\n2. RL Prediction")
try:
    payload = {
        "junction_id": "joinedS_265580996_300839357",
        "obs_data": [0.0] * 19
    }
    response = requests.post(f"{BASE_RL}/predict_action", json=payload)
    result = response.json()
    print(f"   ✓ Action: {result['action']}, Confidence: {result['confidence']:.3f}")
except Exception as e:
    print(f"   ✗ Error: {e}")

# Test 3: LSTM predict
print("\n3. LSTM Prediction")
try:
    payload = {
        "historical_data": [[1, 2, 3, 4], [5, 6, 7, 8]],
        "sequence_length": 2
    }
    response = requests.post(f"{BASE_LSTM}/predict", json=payload)
    result = response.json()
    print(f"   ✓ Prediction: {result['prediction']}")
except Exception as e:
    print(f"   ✗ Error: {e}")

print("\n" + "=" * 60)
print("Integration test complete!")
print("=" * 60)