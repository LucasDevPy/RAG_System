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

# Mock the classes exactly where they are imported and used in our app
@patch('app.graph.rag_graph.ChatOpenAI')
@patch('app.services.retriever.get_vector_store')
def test_chat_endpoint_structure(mock_get_vector_store, mock_chat_openai_class):
    """Tests the chat endpoint returns the correct schema (mocked for CI)."""
    
    # 1. Mock the vector store to return dummy documents
    mock_store = MagicMock()
    mock_doc = MagicMock()
    mock_doc.page_content = "Dummy context for testing."
    mock_doc.metadata = {"source": "test_document.pdf"}
    mock_store.similarity_search.return_value = [mock_doc]
    mock_get_vector_store.return_value = mock_store

    # 2. Mock the ChatOpenAI class and its invoke method
    mock_llm_instance = MagicMock()
    mock_response = MagicMock()
    mock_response.content = "This is a mocked test answer."
    mock_llm_instance.invoke.return_value = mock_response
    mock_chat_openai_class.return_value = mock_llm_instance

    # 3. Send the request
    payload = {"question": "What is this document about?", "thread_id": "test_1"}
    response = client.post("/chat", json=payload)
    
    # 4. Verify the response structure
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    assert "citations" in data
    assert data["answer"] == "This is a mocked test answer."