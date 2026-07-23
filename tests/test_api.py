import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
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

@patch('langchain_openai.ChatOpenAI.invoke')
@patch('app.services.vector_store.get_vector_store')
def test_chat_endpoint_structure(mock_get_store, mock_llm_invoke):
    """Tests the chat endpoint returns the correct schema (mocked for CI)."""
    # 1. Mock the Vector Store so it doesn't try to connect to ChromaDB/OpenAI
    mock_store = MagicMock()
    mock_get_store.return_value = mock_store
    
    # 2. Mock the LLM response
    mock_response = MagicMock()
    mock_response.content = "This is a mocked test answer."
    mock_llm_invoke.return_value = mock_response
    
    # 3. Send the request
    payload = {"question": "What is this document about?", "thread_id": "test_1"}
    response = client.post("/chat", json=payload)
    
    # 4. Verify the response structure
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    assert "citations" in data