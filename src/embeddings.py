import os
from langchain.embeddings import OpenAIEmbeddings, HuggingFaceEmbeddings

def get_embedding():
    mode = os.getenv('EMB_MODEL', 'openai')
    if mode == 'hf':
        return HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')
    return OpenAIEmbeddings()
# Default to OpenAI embeddings if not specified
# This allows for easy switching between OpenAI and HuggingFace embeddings