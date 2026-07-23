import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from app.main import app

client = TestClient(app)

def test_health_check():
    """Tests the health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_upload_invalid_file_type():
    """Tests that non-PDF files are rejected by FastAPI validation."""
    response = client.post("/upload", files={"file": ("test.txt", b"dummy content", "text/plain")})
    assert response.status_code == 400

@patch('app.api.routes.rag_app.invoke')
def test_chat_endpoint_structure(mock_invoke):
    """Tests that the chat endpoint returns the correct schema (mocked for CI)."""
    # 1. Mock the LangGraph invoke method to return a dummy response
    # This prevents the code from ever reaching OpenAI or ChromaDB
    mock_invoke.return_value = {
        "generation": "This is a mocked test answer.",
        "citations": ["test_document.pdf"]
    }
    
    # 2. Send the request
    valid_payload = {"question": "What is this document about?", "thread_id": "123"}
    response = client.post("/chat", json=valid_payload)
    
    # 3. Verify the response structure
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    assert "citations" in data
    assert data["answer"] == "This is a mocked test answer."