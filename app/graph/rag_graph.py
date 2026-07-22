import logging
from typing import TypedDict, Annotated, List
from langchain_openai import ChatOpenAI
from langchain.schema import Document, SystemMessage, HumanMessage
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from app.core.config import settings
from app.services.retriever import retrieve_and_rerank

logger = logging.getLogger(__name__)

class GraphState(TypedDict):
    """Defines the state of our RAG graph."""
    question: str
    chat_history: list[dict]
    documents: list[Document]
    generation: str
    citations: list[str]

def retrieve_node(state: GraphState) -> dict:
    """Retrieves and re-ranks documents based on the question."""
    question = state["question"]
    docs = retrieve_and_rerank(question)
    return {"documents": docs}

def generate_node(state: GraphState) -> dict:
    """Generates an answer using the LLM and retrieved context."""
    question = state["question"]
    docs = state["documents"]
    history = state.get("chat_history", [])
    
    context = "\n\n".join([f"[Source: {doc.metadata['source']}]\n{doc.page_content}" for doc in docs])
    
    llm = ChatOpenAI(model=settings.openai_model, temperature=0, openai_api_key=settings.openai_api_key)
    
    messages = [
        SystemMessage(content=f"You are a helpful assistant. Answer the question based ONLY on the following context. If the answer is not in the context, say you don't know. Always cite the source.\n\nContext:\n{context}"),
    ]
    
    # Add chat history for conversational context
    for msg in history:
        if msg["role"] == "user": messages.append(HumanMessage(content=msg["content"]))
        else: messages.append(SystemMessage(content=msg["content"])) # Simplified for example
        
    messages.append(HumanMessage(content=question))
    
    response = llm.invoke(messages)
    
    # Extract unique citations
    citations = list(set([doc.metadata["source"] for doc in docs]))
    
    return {"generation": response.content, "citations": citations}

def build_rag_graph():
    """Constructs and compiles the LangGraph workflow."""
    workflow = StateGraph(GraphState)
    
    workflow.add_node("retrieve", retrieve_node)
    workflow.add_node("generate", generate_node)
    
    workflow.set_entry_point("retrieve")
    workflow.add_edge("retrieve", "generate")
    workflow.add_edge("generate", END)
    
    # MemorySaver allows the graph to maintain chat history across invocations
    memory = MemorySaver()
    return workflow.compile(checkpointer=memory)

rag_app = build_rag_graph()