import logging
import chromadb
from chromadb.config import Settings as ChromaSettings
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.schema import Document
from app.core.config import settings

logger = logging.getLogger(__name__)

# Simple in-memory cache to save OpenAI API costs during development
_embedding_cache = {}

class CachedEmbeddings(OpenAIEmbeddings):
    """Wrapper around OpenAIEmbeddings to cache results in memory."""
    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        embeddings = []
        texts_to_embed = []
        indices_to_embed = []

        for i, text in enumerate(texts):
            if text in _embedding_cache:
                embeddings.append(_embedding_cache[text])
            else:
                texts_to_embed.append(text)
                indices_to_embed.append(i)
                embeddings.append(None) # Placeholder

        if texts_to_embed:
            new_embeddings = super().embed_documents(texts_to_embed)
            for idx, text, emb in zip(indices_to_embed, texts_to_embed, new_embeddings):
                _embedding_cache[text] = emb
                embeddings[idx] = emb
                
        return embeddings

def get_vector_store() -> Chroma:
    """Initializes and returns the ChromaDB vector store."""
    client = chromadb.PersistentClient(path="./chroma_db", settings=ChromaSettings(anonymized_telemetry=False))
    embeddings = CachedEmbeddings(model=settings.embedding_model, openai_api_key=settings.openai_api_key)
    
    return Chroma(
        client=client,
        collection_name="rag_documents",
        embedding_function=embeddings
    )

def add_documents_to_store(docs: list[Document]):
    """Adds document chunks to the vector store."""
    vectorstore = get_vector_store()
    vectorstore.add_documents(docs)
    logger.info(f"Added {len(docs)} chunks to vector store.")