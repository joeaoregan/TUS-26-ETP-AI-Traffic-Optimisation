#!/usr/bin/env python3
"""
API Test Client
Simple client to test the AI Traffic Control API
"""

import sys
import json
import requests
import time
from typing import List, Dict, Any
import random
from colorama import Fore, Back, Style, init
init(autoreset=True)

class TrafficAPIClient:
    """Client for the Traffic Control API."""
    
    def __init__(self, base_url: str = "http://localhost:8080"):
        self.base_url = base_url
        self.session = requests.Session()
        self.access_token = None

    def authenticate(self, username: str = "admin", password: str = "admin123") -> bool:
        """Authenticate and cache a bearer token for protected endpoints."""
        try:
            response = self.session.post(
                f"{self.base_url}/api/auth/login",
                json={"username": username, "password": password},
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()
            data = response.json()
            self.access_token = data.get("accessToken")
            return bool(self.access_token)
        except Exception as e:
            print(f"{Fore.RED}✗ Authentication failed: {e}")
            return False

    def _auth_headers(self) -> Dict[str, str]:
        if not self.access_token:
            raise RuntimeError("No access token available. Call authenticate() first.")
        return {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.access_token}"
        }
    
    def check_health(self) -> bool:
        """Check if the API is healthy."""
        try:
            response = self.session.get(f"{self.base_url}/api/traffic/health")
            response.raise_for_status()
            data = response.json()
            return data.get("status") == "healthy"
        except Exception as e:
            print(f"{Fore.RED}✗ Health check failed: {e}")
            return False
    
    def get_action(self) -> Dict[str, Any]:
        """Get traffic action with auto-generated observations."""
        response = self.session.get(
            f"{self.base_url}/api/traffic/action",
            headers=self._auth_headers()
        )
        response.raise_for_status()
        return response.json()
    
    def predict_action(self, observations: List[float], junction_id: str = "300839359") -> Dict[str, Any]:
        """Predict action with custom observations."""
        payload = {
            "junctionId": junction_id,
            "observations": observations
        }
        response = self.session.post(
            f"{self.base_url}/api/traffic/action",
            json=payload,
            headers=self._auth_headers()
        )
        response.raise_for_status()
        return response.json()
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the loaded model."""
        try:
            response = self.session.get("http://localhost:8000/model_info")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"{Fore.RED}✗ Could not fetch model info: {e}")
            return None


def print_response(response: Dict[str, Any], title: str = "Response") -> None:
    """Pretty print API response."""
    print(f"\n{title}:")
    print(json.dumps(response, indent=2))


def test_basic_functionality(client: TrafficAPIClient) -> bool:
    """Test basic API functionality."""
    print("=" * 60)
    print(f"{Fore.BLUE}TEST 1: Basic Functionality")
    print("=" * 60)
    
    try:
        # Test health
        print("\n1. Health Check...")
        if not client.check_health():
            print(f"{Fore.RED}✗ API health check failed")
            return False
        print(f"{Fore.GREEN}✓ API is healthy")
        
        # Test auto-generated action
        print("\n2. Get Traffic Action (auto-generated observations)...")
        response = client.get_action()
        print_response(response)
        print(f"{Fore.GREEN}✓ Got traffic action: {response.get('signalState')}")
        return True
    except Exception as e:
        print(f"{Fore.RED}✗ Error: {e}")
        return False


def test_custom_observations(client: TrafficAPIClient) -> bool:
    """Test with custom observations."""
    print("\n\n" + "=" * 60)
    print(f"{Fore.BLUE}TEST 2: Custom Observations")
    print("=" * 60)
    
    all_passed = True
    
    # Test 1: Low traffic
    print("\n1. Low Traffic Scenario (mostly zeros)...")
    low_traffic = [0.1 * random.random() for _ in range(10)]
    try:
        response = client.predict_action(low_traffic, junction_id="300839359")
        print_response(response)
        print(f"{Fore.GREEN}✓ Action for low traffic: {response.get('signalState')}")
    except Exception as e:
        print(f"{Fore.RED}✗ Error: {e}")
        all_passed = False
    
    # Test 2: High traffic
    print("\n2. High Traffic Scenario (mostly ones)...")
    high_traffic = [0.9 + 0.1 * random.random() for _ in range(10)]
    try:
        response = client.predict_action(high_traffic, junction_id="300839359")
        print_response(response)
        print(f"{Fore.GREEN}✓ Action for high traffic: {response.get('signalState')}")
    except Exception as e:
        print(f"{Fore.RED}✗ Error: {e}")
        all_passed = False
    
    # Test 3: Mixed traffic
    print("\n3. Mixed Traffic Scenario...")
    mixed_traffic = [random.random() for _ in range(10)]
    try:
        response = client.predict_action(mixed_traffic, junction_id="300839359")
        print_response(response)
        print(f"{Fore.GREEN}✓ Action for mixed traffic: {response.get('signalState')}")
    except Exception as e:
        print(f"{Fore.RED}✗ Error: {e}")
        all_passed = False
    
    return all_passed


def test_load_testing(client: TrafficAPIClient, num_requests: int = 10) -> bool:
    """Simple load test."""
    print("\n\n" + "=" * 60)
    # print(f"TEST 3: Load Testing ({num_requests} requests)")
    print(f"{Fore.BLUE}TEST 3: Load Testing ({num_requests} requests)")
    print("=" * 60)
    
    try:
        successful = 0
        failed = 0
        response_times = []
        
        print(f"\nSending {num_requests} requests...")
        
        for i in range(num_requests):
            try:
                start_time = time.time()
                response = client.get_action()
                elapsed = time.time() - start_time
                response_times.append(elapsed)
                successful += 1
                print(f"  Request {i+1}: {elapsed*1000:.2f}ms - {response.get('signalState')}")
            except Exception as e:
                failed += 1
                print(f"  Request {i+1}: FAILED - {e}")
        
        # Statistics
        print(f"\n{'='*60}")
        print(f"Load Test Results:")
        print(f"  Successful: {successful}/{num_requests}")
        print(f"  Failed: {failed}/{num_requests}")
        
        if response_times:
            avg_time = sum(response_times) / len(response_times)
            min_time = min(response_times)
            max_time = max(response_times)
            print(f"  Avg Response Time: {avg_time*1000:.2f}ms")
            print(f"  Min Response Time: {min_time*1000:.2f}ms")
            print(f"  Max Response Time: {max_time*1000:.2f}ms")
        
        return failed == 0  # Pass only if no failed requests
    except Exception as e:
        print(f"{Fore.RED}✗ Error: {e}")
        return False


def test_model_info(client: TrafficAPIClient) -> bool:
    """Test getting model information."""
    print("\n\n" + "=" * 60)
    # print("TEST 4: Model Information")
    print(f"{Fore.BLUE}TEST 4: Model Information")
    print("=" * 60)
    
    try:
        info = client.get_model_info()
        if info:
            print_response(info)
            print(f"{Fore.GREEN}✓ Model info retrieved successfully")
            return True
        else:
            print(f"{Fore.RED}✗ Could not retrieve model information")
            return False
    except Exception as e:
        print(f"{Fore.RED}✗ Error: {e}")
        return False


def main():
    """Main test function."""

    print("\n")
    print("╔" + "=" * 58 + "╗")
    # print("║" + " " * 15 + "AI Traffic Control API - Test Client" + " " * 7 + "║")
    print("║" + " " * 11 + f"{Fore.BLUE}AI Traffic Control API - Test Client{Style.RESET_ALL}" + " " * 11 + f"{Fore.WHITE}║")
    print("╚" + "=" * 58 + "╝")
    
    # Initialize client
    api_url = "http://localhost:8080"
    print(f"\nConnecting to API at {Fore.CYAN}{api_url}...")
    client = TrafficAPIClient(api_url)
    
    # Check if API is available
    if not client.check_health():
        print(f"{Fore.RED}\n✗ Cannot connect to API at {Fore.CYAN}{api_url}")
        print("Make sure the services are running with: docker-compose up")
        sys.exit(1)
    
    print(f"{Fore.GREEN}✓ Connected successfully!")

    if not client.authenticate():
        print(f"{Fore.RED}\n✗ Authentication failed. Check JWT_AUTH_USERNAME/JWT_AUTH_PASSWORD settings.")
        sys.exit(1)

    print(f"{Fore.GREEN}✓ JWT authentication succeeded!")
    
    # Track test completion
    tests_passed = 0
    total_tests = 4
   
    # Run tests and track results
    if test_basic_functionality(client):
        tests_passed += 1
    
    if test_custom_observations(client):
        tests_passed += 1
    
    if test_load_testing(client, num_requests=5):
        tests_passed += 1
    
    if test_model_info(client):
        tests_passed += 1
    
    print("\n\n" + "=" * 60)
    # print(f"All tests completed! {tests_passed}/{total_tests}")
    if tests_passed == total_tests:
        print(f"{Fore.GREEN}✓ All tests passed successfully!")
    else:
        print(f"{Fore.RED}✗ Some tests failed. Passed {tests_passed}/{total_tests}")
    print("=" * 60 + "\n")
    
    # Exit with appropriate code
    sys.exit(0 if tests_passed == total_tests else 1)


if __name__ == "__main__":
    main()
