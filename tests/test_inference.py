import os
import shutil
import pytest
from src.ingestion import PDFIngestor
from src.inference import Inference

@pytest.fixture(autouse=True)
def setup(tmp_path, monkeypatch):
    cache_dir = tmp_path / "cache"
    pdfs_dir  = tmp_path / "pdfs"
    pdfs_dir.mkdir()
    monkeypatch.setenv("CACHE_DIR", str(cache_dir))
    monkeypatch.setenv("PDF_DIR", str(pdfs_dir))
    # Copy the PDF
    shutil.copy("tests/RAG_Research.pdf", pdfs_dir / "RAG_Research.pdf")
    # Build the index
    PDFIngestor().ingest()
    yield

def test_inference_answer():
    inf = Inference()
    resp = inf.answer("RAG")
    assert isinstance(resp["result"], str)
    assert len(resp["source_documents"]) > 0
    assert "RAG_Research.pdf" in resp["source_documents"][0].metadata["source"]
