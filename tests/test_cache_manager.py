import os
import shutil
import pytest
from src.cache_manager import CacheManager
from src.ingestion import PDFIngestor
from src.embeddings import get_embedding

@pytest.fixture(autouse=True)
def setup_env(tmp_path, monkeypatch):
    cache_dir = tmp_path / "cache"
    pdfs_dir  = tmp_path / "pdfs"
    pdfs_dir.mkdir()
    monkeypatch.setenv("CACHE_DIR", str(cache_dir))
    monkeypatch.setenv("PDF_DIR", str(pdfs_dir))
    # Copy the same PDF twice
    shutil.copy("tests/RAG_Research.pdf", pdfs_dir / "one.pdf")
    shutil.copy("tests/RAG_Research.pdf", pdfs_dir / "two.pdf")
    yield

def test_incremental_ingest():
    ing = PDFIngestor()
    ing.ingest()
    cm = CacheManager(get_embedding())
    splitter = ing.splitter
    cm.incremental_ingest(str(os.getenv("PDF_DIR") + "/two.pdf"), splitter)
    cache_dir = os.getenv("CACHE_DIR")
    files = os.listdir(cache_dir)
    assert len(files) >= 2
