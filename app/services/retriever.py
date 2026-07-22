import logging
from typing import List
from flashrank import Ranker, RerankRequest
from langchain.schema import Document
from app.services.vector_store import get_vector_store

logger = logging.getLogger(__name__)

# Initialize the lightweight local re-ranker (downloads a tiny ~4MB model on first run)
ranker = Ranker()

def retrieve_and_rerank(query: str, top_k: int = 5, rerank_top_n: int = 3) -> List[Document]:
    """Retrieves documents from vector store and re-ranks them for better context."""
    vectorstore = get_vector_store()
    
    # 1. Initial broad retrieval
    retrieved_docs = vectorstore.similarity_search(query, k=top_k)
    
    if not retrieved_docs:
        return []

    # 2. Format for Flashrank (requires id, text, and optional meta)
    passages = [
        {"id": i, "text": doc.page_content, "meta": doc.metadata} 
        for i, doc in enumerate(retrieved_docs)
    ]
    
    # 3. Re-rank using the modern RerankRequest object
    rerank_request = RerankRequest(query=query, passages=passages)
    rerank_results = ranker.rerank(rerank_request)
    
    # 4. Map the top re-ranked results back to Langchain Documents
    final_docs = []
    for res in rerank_results[:rerank_top_n]:
        original_doc = retrieved_docs[res["id"]]
        final_docs.append(original_doc)
        
    return final_docs