# 📄 RAG PDF Chat System

![Python](https://img.shields.io/badge/Python-3.11-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.111-009688)
![LangGraph](https://img.shields.io/badge/LangGraph-Stateful_AI-FF4B4B)
[![Python CI](https://github.com/dasil/RAG_System/actions/workflows/test.yml/badge.svg)](https://github.com/dasil/RAG_System/actions/workflows/test.yml)

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


🚀 Features
Multi-PDF Support: Upload and query across multiple documents simultaneously.
Smart Chunking: Recursive character splitting with overlap for optimal context preservation.
Context Re-ranking: Uses flashrank to filter out noise and prioritize the most relevant chunks before LLM generation.
Citations: The LLM explicitly cites which PDF the answer originated from.
Stateful Chat: LangGraph MemorySaver maintains conversational history across turns.
Embeddings Cache: In-memory caching to reduce OpenAI API costs during development and testing.
🛠️ Tech Stack
Backend: FastAPI, Uvicorn
AI Orchestration: LangGraph, LangChain
Vector Database: ChromaDB (Persistent)
LLM & Embeddings: OpenAI (gpt-4o-mini, text-embedding-3-small)
Re-ranking: Flashrank (Lightweight local model)
Testing & CI: Pytest, GitHub Actions

📋 Prerequisites
Python 3.11+
Docker & Docker Compose (for containerized run)
An OpenAI API Key

💻 How to Run Locally
Clone the repository:
   git clone <your-repo-url>
   cd RAG_System

Setup Environment:
   python -m venv .venv
   source .venv/Scripts/activate  # On Windows Git Bash
   pip install -r requirements.txt

Configure Secrets:
Copy .env.example to .env and add your OpenAI API key.
   cp .env.example .env

Run the API:
   uvicorn app.main:app --reload

Access the interactive Swagger UI at: http://localhost:8000/docs

🧪 Testing
Run the test suite locally to verify integrity:
    pytest -v

📂 Project Structure
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