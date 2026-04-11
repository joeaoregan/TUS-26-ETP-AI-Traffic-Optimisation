import requests
import json
from colorama import Fore, Back, Style, init

init(autoreset=True)

BASE_LSTM = "http://localhost:8001"
BASE_RL = "http://localhost:8000"

print(f"\n{Back.CYAN}{Fore.BLACK}{'=' * 60}")
print(f"{Back.CYAN}{Fore.BLACK}{' '*16}Testing RL + LSTM Integration{' '*15}")
print(f"{Back.CYAN}{Fore.BLACK}{'=' * 60}{Style.RESET_ALL}\n")

# Test 1: Health checks
print(f"{Fore.BLUE}1. Health Checks{Style.RESET_ALL}")
try:
    lstm_health = requests.get(f"{BASE_LSTM}/health").json()
    rl_health = requests.get(f"{BASE_RL}/health").json()
    print(f"   {Fore.GREEN}✓ LSTM: {lstm_health['status']}{Style.RESET_ALL}")
    print(f"   {Fore.GREEN}✓ RL:   {rl_health['status']}{Style.RESET_ALL}")
except Exception as e:
    print(f"   {Fore.RED}✗ Error: {e}{Style.RESET_ALL}")

# Test 2: RL predict
print(f"\n{Fore.BLUE}2. RL Prediction{Style.RESET_ALL}")
try:
    payload = {
        "junction_id": "joinedS_265580996_300839357",
        "obs_data": [0.0] * 19
    }
    response = requests.post(f"{BASE_RL}/predict_action", json=payload)
    result = response.json()
    print(f"   {Fore.GREEN}✓ Action: {result['action']}, Confidence: {result['confidence']:.3f}{Style.RESET_ALL}")
except Exception as e:
    print(f"   {Fore.RED}✗ Error: {e}{Style.RESET_ALL}")

# Test 3: LSTM predict
print(f"\n{Fore.BLUE}3. LSTM Prediction{Style.RESET_ALL}")
try:
    payload = {
        "data": [
            [18.93, 10.13, 5.23, 4.14, 3.08],
            [24.02, 11.01, 8.98, 5.42, 4.26],
            [22.14, 9.34, 5.62, 4.57, 3.81]
        ]
    }
    response = requests.post(f"{BASE_LSTM}/predict", json=payload)
    result = response.json()
    print(f"   {Fore.GREEN}✓ Prediction: {result['prediction']}{Style.RESET_ALL}")
except Exception as e:
    print(f"   {Fore.RED}✗ Error: {e}{Style.RESET_ALL}")

print(f"\n{'=' * 60}")
print(f"{Back.GREEN}{Fore.BLACK}{' '*17}Integration test complete!{' '*17}")
print(f"{'=' * 60}{Style.RESET_ALL}\n")