import os
from dotenv import load_dotenv
from src.embeddings import get_embedding
from langchain_community.vectorstores import FAISS

load_dotenv()

def get_retriever(k: int = 4):
    cache_dir = os.getenv("CACHE_DIR", "./data/cache")
    embedding_fn = get_embedding()
    index = FAISS.load_local(
        cache_dir,
        embedding_fn,
        allow_dangerous_deserialization=True
    )
    return index.as_retriever(search_kwargs={"k": k})
