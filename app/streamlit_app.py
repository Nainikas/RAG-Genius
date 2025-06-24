import sys, os

# Ensure the project root is on Python path so `src` imports work
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

import streamlit as st
from src.ingestion import PDFIngestor
from src.cache_manager import CacheManager
from src.embeddings import get_embedding
from src.inference import Inference

st.set_page_config(page_title="RAG-Genius")

# Debug banner
st.markdown("##RAG-Genius app loaded!")

# Sidebar: full ingestion
if st.sidebar.button("Ingest all PDFs"):
    PDFIngestor().ingest()
    st.sidebar.success("Indexed all PDFs!")

# Sidebar settings
split_size = st.sidebar.slider("Chunk size", 500, 2000, 1000)
overlap    = st.sidebar.slider("Chunk overlap", 0, 500, 200)
k_val      = st.sidebar.slider("Retriever k", 1, 10, 4)

# Sidebar: incremental ingest
st.sidebar.write("### Add a new PDF")
new_pdf = st.sidebar.file_uploader("Upload PDF", type="pdf")
if new_pdf:
    save_path = f"./data/pdfs/{new_pdf.name}"
    with open(save_path, "wb") as f:
        f.write(new_pdf.getbuffer())
    cm = CacheManager(get_embedding())
    splitter = PDFIngestor(pdf_folder=None, split_size=split_size, overlap=overlap).splitter
    cm.incremental_ingest(save_path, splitter)
    st.sidebar.success(f"Added {new_pdf.name}")

# Main UI
st.title("RAG-Genius Q&A")
question = st.text_input("Enter your question:")
if st.button("Ask") and question:
    inf = Inference()
    with st.spinner("Thinking…"):
        res = inf.answer(question)

    st.subheader("Answer")
    st.write(res["result"])

    st.subheader("Sources")
    for doc in res["source_documents"]:
        src = doc.metadata.get("source", "unknown")
        snippet = doc.page_content[:200].replace("\n", " ")
        st.markdown(f"- **{src}**: {snippet}…")
