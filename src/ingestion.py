import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from src.embeddings import get_embedding

load_dotenv()

class PDFIngestor:
    def __init__(self, pdf_folder: str = None, split_size=1000, overlap=200):
        # Resolve PDF folder at runtime (allows pytest to override via PDF_DIR)
        self.pdf_folder = pdf_folder or os.getenv("PDF_DIR", "./data/pdfs")
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=split_size, chunk_overlap=overlap
        )
        self.embedding_fn = get_embedding()

    def ingest(self):
        # Resolve cache dir at runtime (allows pytest to override via CACHE_DIR)
        cache_dir = os.getenv("CACHE_DIR", "./data/cache")

        docs = []
        for fname in os.listdir(self.pdf_folder):
            if not fname.lower().endswith(".pdf"):
                continue
            path = os.path.join(self.pdf_folder, fname)
            loader = PyPDFLoader(path)
            pages = loader.load_and_split(self.splitter)
            for p in pages:
                p.metadata["source"] = fname
            docs.extend(pages)

        index = FAISS.from_documents(docs, self.embedding_fn)
        os.makedirs(cache_dir, exist_ok=True)
        index.save_local(cache_dir)
        print(f"Indexed {len(docs)} chunks to {cache_dir}")

if __name__ == "__main__":
    PDFIngestor().ingest()
# This script is designed to be run directly, e.g. `python src/ingestion.py`
# It will index all PDFs in the configured PDF_DIR and save the FAISS index to CACHE