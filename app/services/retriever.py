import logging
from flashrank import Ranker, RerankResult
from langchain.schema import Document
from app.services.vector_store import get_vector_store

logger = logging.getLogger(__name__)
# Initialize the lightweight local re-ranker
ranker = Ranker()

def retrieve_and_rerank(query: str, top_k: int = 5, rerank_top_n: int = 3) -> list[Document]:
    """Retrieves documents from vector store and re-ranks them for better context."""
    vectorstore = get_vector_store()
    
    # 1. Initial broad retrieval
    retrieved_docs = vectorstore.similarity_search(query, k=top_k)
    
    if not retrieved_docs:
        return []

    # 2. Format for Flashrank
    passages = [{"id": i, "text": doc.page_content, "meta": doc.metadata} for i, doc in enumerate(retrieved_docs)]
    
    # 3. Re-rank
    rerank_results: list[RerankResult] = ranker.rerank(query=query, passages=passages, top_n=rerank_top_n)
    
    # 4. Map back to Langchain Documents
    final_docs = []
    for res in rerank_results:
        original_doc = retrieved_docs[res.document["id"]]
        final_docs.append(original_doc)
        
    return final_docs