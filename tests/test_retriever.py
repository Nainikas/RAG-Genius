import os
import shutil
import pytest
from src.ingestion import PDFIngestor
from src.retriever import get_retriever

@pytest.fixture(autouse=True)
def setup(tmp_path, monkeypatch):
    cache_dir = tmp_path / "cache"
    pdfs_dir  = tmp_path / "pdfs"
    pdfs_dir.mkdir()
    monkeypatch.setenv("CACHE_DIR", str(cache_dir))
    monkeypatch.setenv("PDF_DIR", str(pdfs_dir))
    # Copy your PDF
    shutil.copy("tests/RAG_Research.pdf", pdfs_dir / "RAG_Research.pdf")
    # Ingest to build index
    PDFIngestor().ingest()
    yield

def test_retriever_returns_documents():
    retriever = get_retriever(k=2)
    results = retriever.get_relevant_documents("RAG")  # pick a word in your PDF
    assert len(results) > 0
    assert "RAG_Research.pdf" in results[0].metadata["source"]
