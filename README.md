# RAG-Genius

**A private, offline Q&A system for your documents, powered by FAISS, LangChain, and GPT-4 (or local LLaMA).**

Final Product:
![Screenshot 2025-06-24 025539](https://github.com/user-attachments/assets/748d8d9f-d3fe-47dd-a9d5-ce6ca063ba9e)
![Screenshot 2025-06-24 025700](https://github.com/user-attachments/assets/040b21f1-3739-44a2-851d-0ed3874da910)

---

## 🚀 Features

- **PDF ingestion**: Chunk, embed, and index any PDF corpus.  
- **Vector search**: Ultra-fast retrieval over FAISS.  
- **Flexible inference**: Use OpenAI GPT-4 API or spin up a local LLaMA-based model.  
- **Customizable retrieval**: Tweak chunk size, overlap, and top-k retrieval.  
- **Incremental indexing**: Add new PDFs without re-indexing everything.  
- **Streamlit UI**: Fully interactive demo with ingestion, uploads, and Q&A.  
- **Automated tests**: Pytest suite covers ingestion, caching, retrieval, and end-to-end QA.

---

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
   ```
3. **Creating Environment**
   View env_sample. Make sure to protect your key before uploading it on an open-source!

4. **Install & run locally**
   ```bash
   # Create virtualenv and install
   python -m venv venv
   source venv/bin/activate        # macOS/Linux
   .\venv\Scripts\Activate.ps1     # Windows PowerShell
   
   pip install --upgrade pip
   pip install -r requirements.txt
   
   # Ingest your PDFs
   python -m src.ingestion
   
   # Start the Streamlit UI
   python -m streamlit run app/streamlit_app.py
   ```
   Visit http://localhost:8501 to ask questions against your documents.

---

**Project layout**

/src: ingestion, vector store, retrieval and inference logic

/app: Streamlit demo

/tests: unit tests for each module

Dockerfile + requirements.txt for containerized deploy

---

**Automated Tests**
The pytest suite spins up isolated temp folders, ingests a sample PDF, and verifies:

1. Ingestion writes FAISS files.
2. CacheManager supports incremental adds
3. Retriever returns relevant chunks
4. Inference produces answers with source docs

Run them with:
```bash
pytest -q
```

---

**Docker**
docker build -t rag-genius .
docker run -p 8501:8501 --env-file .env rag-genius

**Git Ignore**
```bash
# Secrets & env
.env

# FAISS index cache
/data/cache/

# Raw PDFs (if you want to keep them local)
/data/pdfs/

# Python caches
__pycache__/
*.py[cod]

# Virtualenv
venv/
```

**ENJOY!**
