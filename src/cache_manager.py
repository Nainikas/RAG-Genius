import os
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS

load_dotenv()

class CacheManager:
    def __init__(self, embedding_fn):
        # Resolve cache dir at runtime
        cache_dir = os.getenv("CACHE_DIR", "./data/cache")

        if os.path.isdir(cache_dir):
            self.index = FAISS.load_local(
                cache_dir,
                embedding_fn,
                allow_dangerous_deserialization=True
            )
        else:
            self.index = None
        self.embedding_fn = embedding_fn

    def incremental_ingest(self, pdf_path, splitter):
        from langchain_community.document_loaders import PyPDFLoader

        cache_dir = os.getenv("CACHE_DIR", "./data/cache")

        pages = PyPDFLoader(pdf_path).load_and_split(splitter)
        for p in pages:
            p.metadata["source"] = os.path.basename(pdf_path)

        if self.index:
            self.index.add_documents(pages)
        else:
            self.index = FAISS.from_documents(pages, self.embedding_fn)

        os.makedirs(cache_dir, exist_ok=True)
        self.index.save_local(cache_dir)
        print(f"Added {len(pages)} chunks from {pdf_path} to {cache_dir}")
