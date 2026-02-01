import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.config import settings

client = TestClient(app)

def test_health_check():
    """Test health endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_analyze_missing_api_key():
    """Test that missing API key returns 401."""
    response = client.post("/analyze", json={
        "language": "Auto",
        "audioFormat": "webm",
        "audioBase64": "fake_base64_data"
    })
    assert response.status_code == 401  # Missing/invalid API key

def test_analyze_invalid_api_key():
    """Test that wrong API key returns 401."""
    response = client.post(
        "/analyze",
        json={
            "language": "Auto",
            "audioFormat": "webm",
            "audioBase64": "fake_base64_data"
        },
        headers={"x-api-key": "wrong-key"}
    )
    assert response.status_code == 401
    assert "Invalid API key" in response.json()["detail"]

def test_root_endpoint():
    """Test root endpoint returns API info."""
    response = client.get("/")
    assert response.status_code == 200
    assert "projwhitehat" in response.json()["message"]