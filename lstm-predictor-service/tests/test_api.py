"""Tests for the LSTM Predictor Service API.

These tests mock the model and scaler so TensorFlow is not required.
"""
import os
import sys
import pytest
from unittest.mock import patch, MagicMock, PropertyMock
import numpy as np

# Set working directory to service root where app/images lives
os.chdir(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


@pytest.fixture
def client():
    """Create test client with mocked model and scaler."""
    # Mock tensorflow before importing app.main
    mock_tf = MagicMock()
    mock_keras = MagicMock()
    mock_joblib = MagicMock()

    with patch.dict("sys.modules", {
        "tensorflow": mock_tf,
        "tensorflow.keras": mock_keras,
        "tensorflow.keras.models": MagicMock(),
        "joblib": mock_joblib,
    }):
        import app.main as main_module
        from fastapi.testclient import TestClient

        # Mock model
        mock_model = MagicMock()
        mock_model.predict.return_value = np.array([[22.45, 11.23, 7.89, 5.34, 4.12]])
        main_module.model = mock_model

        # Mock scaler
        mock_scaler = MagicMock()
        mock_scaler.transform.return_value = np.array([
            [0.3, 0.2, 0.1, 0.08, 0.06],
            [0.5, 0.22, 0.18, 0.11, 0.09],
            [0.4, 0.19, 0.11, 0.09, 0.08],
        ])
        mock_scaler.inverse_transform.return_value = np.array([[22.45, 11.23, 7.89, 5.34, 4.12]])
        main_module.scaler = mock_scaler

        yield TestClient(main_module.app, raise_server_exceptions=False)

        main_module.model = None
        main_module.scaler = None


class TestHealthEndpoint:
    def test_health_returns_200(self, client):
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"


class TestPredictEndpoint:
    def test_valid_prediction(self, client):
        response = client.post("/predict", json={
            "data": [
                [18.93, 10.13, 5.23, 4.14, 3.08],
                [24.02, 11.01, 8.98, 5.42, 4.26],
                [22.14, 9.34, 5.62, 4.57, 3.81],
            ]
        })
        assert response.status_code == 200
        data = response.json()
        assert "prediction" in data
        assert len(data["prediction"]) == 5

    def test_missing_data_returns_422(self, client):
        response = client.post("/predict", json={})
        assert response.status_code == 422


class TestBatchPredictEndpoint:
    def test_valid_batch(self, client):
        sequence = [
            [18.93, 10.13, 5.23, 4.14, 3.08],
            [24.02, 11.01, 8.98, 5.42, 4.26],
            [22.14, 9.34, 5.62, 4.57, 3.81],
        ]
        response = client.post("/predict-batch", json={
            "sequences": [sequence, sequence]
        })
        assert response.status_code == 200
        data = response.json()
        assert "predictions" in data
        assert data["num_predictions"] == 2


class TestMetricsEndpoint:
    def test_metrics_returns_200(self, client):
        response = client.get("/metrics")
        assert response.status_code == 200
        data = response.json()
        assert "total_predictions" in data
