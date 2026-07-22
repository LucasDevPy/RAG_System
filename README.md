# 📄 RAG PDF Chat System

![Python](https://img.shields.io/badge/Python-3.11-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.111-009688)
![LangGraph](https://img.shields.io/badge/LangGraph-Stateful_AI-FF4B4B)
[![Python CI](https://github.com/LucasDevPy/RAG_System/actions/workflows/test.yml/badge.svg)](https://github.com/LucasDevPy/RAG_System/actions/workflows/test.yml)

An enterprise-grade Retrieval-Augmented Generation (RAG) API that allows users to upload multiple PDFs and chat with them contextually. Built with **FastAPI**, **LangGraph**, and **ChromaDB**, featuring smart chunking, context re-ranking, and source citation tracking.

## 🏗️ Architecture

```mermaid
graph TD
    A[User Uploads PDF] --> B(FastAPI Endpoint)
    B --> C{PDF Processor}
    C -->|Smart Chunking| D[ChromaDB Vector Store]
    E[User Question] --> F[LangGraph State]
    F -->|Retrieve| D
    F -->|Re-rank| G[Flashrank Local Model]
    G -->|Top Context| H[OpenAI LLM]
    H -->|Answer + Citations| I[User]
````
## 🚀 Features
** Multi-PDF Support: Upload and query across multiple documents simultaneously.
** Smart Chunking: Recursive character splitting with overlap for optimal context preservation.
** Context Re-ranking: Uses flashrank to filter out noise and prioritize the most relevant chunks before LLM generation.
** Citations: The LLM explicitly cites which PDF the answer originated from.
** Stateful Chat: LangGraph MemorySaver maintains conversational history across turns.
** Embeddings Cache: In-memory caching to reduce OpenAI API costs during development and testing.


## 🛠️ Tech Stack
** Backend: FastAPI, Uvicorn
** AI Orchestration: LangGraph, LangChain
** Vector Database: ChromaDB (Persistent)
** LLM & Embeddings: OpenAI (gpt-4o-mini, text-embedding-3-small)
** Re-ranking: Flashrank (Lightweight local model)
**  Testing & CI: Pytest, GitHub Actions

## 📋 Prerequisites
** Python 3.11+
** Docker & Docker Compose (for containerized run)
** An OpenAI API Key

## 💻 How to Run Locally
1.Clone the repository:
```bash
    git clone <your-repo-url>
    cd RAG_System

2.Setup Environment:
```bash
    python -m venv .venv
    source .venv/Scripts/activate  
    pip install -r requirements.txt

3.Configure Secrets:
(Copy .env.example to .env and add your OpenAI API key)
```bash
    cp .env.example .env

4.Start the API:
```bash
    uvicorn app.main:app --reload

(Note: First run may take 10-15 seconds while Flashrank downloads its model)

5.Test the Application:
** Open http://localhost:8000/docs in your browser
** Upload a PDF:
-Scroll to POST /upload
-Click "Try it out" → "Choose File" → Select PDF → "Execute"
-Verify response: {"message": "Successfully processed...", "chunks_created": X}

** Ask a Question:
-Scroll to POST /chat
-Click "Try it out"
-Enter request body:
```json
{
  "question": "What is this document about?",
  "thread_id": "test_123"
}

** Click "Execute"
** Verify response contains answer and citations fields

## 🐳 How to Run with Docker
1. Ensure Docker Desktop is running (look for green "Engine running" indicator)
2. Start the container:
```bash
    docker compose up --build

(Note: First run may take 10-15 seconds while Flashrank downloads its model)

3. Test the Application:
** Open http://localhost:8000/docs in your browser
** Follow the exact same testing steps as in "How to Run Locally"

4. Stop the container:
** Press Ctrl+C in terminal
** Clean up: docker compose down

## 🧪 Testing
Run the test suite locally to verify integrity:
```bash
    pytest -v

## 📂 Project Structure
RAG_System/
├── app/
│   ├── api/          # FastAPI routes and endpoints
│   ├── core/         # Configuration and Pydantic settings
│   ├── graph/        # LangGraph state and workflow nodes
│   ├── services/     # PDF processing, Vector DB, Retriever logic
│   └── main.py       # FastAPI application entry point
├── tests/            # Pytest test suite
├── .github/          # GitHub Actions CI/CD workflows
├── Dockerfile        # Container definition
├── docker-compose.yml# Container orchestration
└── README.md         # Project documentation

## ⚠️ Important Notes
** First Run: The Flashrank model (3.26MB) downloads automatically on first use. This takes 10-15 seconds and may show as "downloading" in logs.

** No Browser? If http://localhost:8000/docs doesn't open:
1. Verify Docker Desktop shows "Engine running" (green indicator)
2. Check if container is running: docker ps
3. Confirm port mapping: 8000:8000 in docker-compose.yml

** PDF Processing: Only PDF files are accepted. Text extraction may fail for scanned documents.

## 📜 License
This project is licensed under the MIT License
