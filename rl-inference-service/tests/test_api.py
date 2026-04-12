"""Tests for the RL Inference Service API."""
import os
import sys
import pytest
from unittest.mock import patch, MagicMock

# Ensure we run from the app dir so static/templates dirs are found
os.chdir(os.path.join(os.path.dirname(__file__), "..", "app"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


@pytest.fixture
def client():
    """Create test client with a real lightweight agent (no .th file needed)."""
    import torch
    from fastapi.testclient import TestClient

    # Patch load_agent to prevent it trying to load the .th file on startup
    with patch.dict("os.environ", {"MAPPO_AGENT_PATH": "/fake/agent.th"}):
        # Import the module — static/templates dirs exist relative to service root
        import app.main as main_module
        from app.main import RNNAgent, TRAFFIC_LIGHTS

        # Replace the startup-loaded agent with a real lightweight one
        agent = RNNAgent(input_shape=24, hidden_dim=128, n_actions=4)
        agent.eval()
        main_module.agent = agent
        main_module.hidden_states = {tl: agent.init_hidden() for tl in TRAFFIC_LIGHTS}

        yield TestClient(main_module.app, raise_server_exceptions=False)

        main_module.agent = None
        main_module.hidden_states = {}


class TestHealthEndpoint:
    def test_health_returns_200(self, client):
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["model_loaded"] is True
        assert len(data["junctions"]) == 5


class TestPredictAction:
    def test_valid_junction_returns_action(self, client):
        response = client.post("/predict_action", json={
            "junction_id": "300839359",
            "obs_data": [0.1] * 8
        })
        assert response.status_code == 200
        data = response.json()
        assert "action" in data
        assert data["action"] in [0, 1]  # This junction only has 2 valid actions
        assert 0.0 <= data["confidence"] <= 1.0

    def test_main_junction_allows_4_actions(self, client):
        response = client.post("/predict_action", json={
            "junction_id": "joinedS_265580996_300839357",
            "obs_data": [0.1] * 19
        })
        assert response.status_code == 200
        assert response.json()["action"] in [0, 1, 2, 3]

    def test_unknown_junction_returns_404(self, client):
        response = client.post("/predict_action", json={
            "junction_id": "nonexistent",
            "obs_data": [0.1] * 10
        })
        assert response.status_code == 404

    def test_oversized_observation_returns_400(self, client):
        response = client.post("/predict_action", json={
            "junction_id": "300839359",
            "obs_data": [0.1] * 25
        })
        assert response.status_code == 400

    def test_small_observation_is_zero_padded(self, client):
        response = client.post("/predict_action", json={
            "junction_id": "300839359",
            "obs_data": [0.5, 0.3]
        })
        assert response.status_code == 200


class TestResetHidden:
    def test_reset_returns_ok(self, client):
        response = client.post("/reset_hidden")
        assert response.status_code == 200
        assert response.json()["status"] == "ok"


class TestModelInfo:
    def test_model_info_returns_architecture(self, client):
        response = client.get("/model_info")
        assert response.status_code == 200
        data = response.json()
        assert data["architecture"] == "RNNAgent (GRU)"
        assert data["input_shape"] == 24
        assert data["hidden_dim"] == 128
        assert data["n_actions"] == 4
        assert data["n_agents"] == 5
