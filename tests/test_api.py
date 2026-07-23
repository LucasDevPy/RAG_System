import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    """Tests the health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_upload_invalid_file():
    """Tests that non-PDF files are rejected."""
    response = client.post("/upload", files={"file": ("test.txt", b"dummy content", "text/plain")})
    assert response.status_code == 400
    assert response.json()["detail"] == "Only PDF files are allowed."