from app.services.pdf_processor import chunk_text

def test_chunk_text_metadata():
    """Tests that chunking correctly assigns source metadata."""
    text = "This is a test document. " * 100
    chunks = chunk_text(text, source_name="test.pdf")
    
    assert len(chunks) > 0
    assert all(chunk.metadata["source"] == "test.pdf" for chunk in chunks)