import os
import shutil
import pytest
from src.ingestion import PDFIngestor

@pytest.fixture(autouse=True)
def clean_cache(tmp_path, monkeypatch):
    cache_dir = tmp_path / "cache"
    pdfs_dir  = tmp_path / "pdfs"
    pdfs_dir.mkdir()
    monkeypatch.setenv("CACHE_DIR", str(cache_dir))
    monkeypatch.setenv("PDF_DIR", str(pdfs_dir))
    # Copy your RAG_Research.pdf for testing
    shutil.copy("tests/RAG_Research.pdf", pdfs_dir / "RAG_Research.pdf")
    yield

def test_ingest_creates_faiss_index():
    ingestor = PDFIngestor()
    ingestor.ingest()
    cache_dir = os.getenv("CACHE_DIR")
    files = os.listdir(cache_dir)
    assert any(f.endswith(".faiss") or f.endswith(".index") for f in files)
