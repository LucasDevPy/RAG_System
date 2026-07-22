import logging
from pypdf import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from app.core.config import settings

logger = logging.getLogger(__name__)

def extract_text_from_pdf(file_path: str) -> str:
    """Extracts raw text from a PDF file."""
    reader = PdfReader(file_path)
    return "".join(page.extract_text() for page in reader.pages)

def chunk_text(text: str, source_name: str) -> list[Document]:
    """Splits text into overlapping chunks with metadata for citations."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.chunk_size,
        chunk_overlap=settings.chunk_overlap,
        separators=["\n\n", "\n", ". ", " ", ""]
    )
    chunks = splitter.split_text(text)
    
    # Attach source metadata to each chunk for citation tracking
    return [Document(page_content=chunk, metadata={"source": source_name}) for chunk in chunks]