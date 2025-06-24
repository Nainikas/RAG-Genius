# RAG-Genius

**A private, offline Q&A system for your documents, powered by FAISS, LangChain, and GPT-4 (or local LLaMA).**

## Features

- **PDF ingestion**: Chunk, embed, and index any PDF corpus.
- **Vector search**: Ultra-fast retrieval over FAISS.
- **Flexible inference**: Use OpenAI GPT-4 API or spin up a local LLaMA-based model.
- **Customizable retrieval**: Tweak k-retrieval, chunk sizes, overlap.
- **Streamlit UI**: Simplest web front-end for demos.

## Quickstart

1. **Clone**  
   ```bash
   git clone git@github.com:you/RAG-Genius.git
   cd RAG-Genius
   
2. **Configure**
   Copy your PDFs into data/pdfs/
   Create .env with your OpenAI key (if using GPT-4):
   ```bash
   OPENAI_API_KEY=sk-...

3. **Install & Run**
   ```bash
   docker build -t rag-genius .
   docker run -p 8501:8501 rag-genius
   ```
   Then visit http://localhost:8501.

**Project layout**
/src: ingestion, vector store, retrieval and inference logic

/app: Streamlit demo

/tests: unit tests for each module

Dockerfile + requirements.txt for containerized deploy

