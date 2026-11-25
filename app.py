import re
import tempfile
import time

import chromadb
import google.generativeai as genai
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
import streamlit as st

st.title("PDF Chatbot")

api_key = "AQ.Ab8RN6J6YE1ErsPlYvuiUMzDqSwA7Cl_W7fmZ_WhutkbSPapWQ"

# 1. Setup models & vector DB
embedder = SentenceTransformer("all-MiniLM-L6-v2")
chroma_client = chromadb.Client()
genai.configure(api_key=api_key)
model = genai.GenerativeModel("models/gemini-2.5-flash")


def extract_pdf_text(file_bytes: bytes) -> str:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(file_bytes)
        tmp_path = tmp.name
    reader = PdfReader(tmp_path)
    return "\n".join(page.extract_text() or "" for page in reader.pages)


def chunk_text(text: str, chunk_size: int = 700, overlap: int = 80):
    words = text.split()
    chunks = []
    i = 0
    while i < len(words):
        chunks.append(" ".join(words[i : i + chunk_size]))
        i += chunk_size - overlap
    return chunks


# 2. Upload PDF & index chunks
uploaded_pdf = st.file_uploader("Upload a PDF", type=["pdf"])

if uploaded_pdf is not None:
    col_name = "pdf_" + re.sub(r"[^a-zA-Z0-9_-]", "_", uploaded_pdf.name)
    if st.session_state.get("indexed_file") != uploaded_pdf.name:
        text = extract_pdf_text(uploaded_pdf.getvalue())
        chunks = chunk_text(text)
        collection = chroma_client.get_or_create_collection(name=col_name)
        ts = int(time.time())
        for idx, chunk in enumerate(chunks):
            emb = embedder.encode(chunk).tolist()
            collection.add(ids=[f"{idx}_{ts}"], embeddings=[emb], documents=[chunk])
        st.session_state["collection"] = collection
        st.session_state["indexed_file"] = uploaded_pdf.name
        st.success("PDF indexed! Ask your questions below.")

# 3. Chat with the PDF
if "collection" in st.session_state:
    question = st.text_input("Ask a question about the PDF:")
    if question:
        q_emb = embedder.encode(question).tolist()
        results = st.session_state["collection"].query(query_embeddings=[q_emb], n_results=3)
        context = "\n\n".join(results.get("documents", [[]])[0])

        prompt = f"""Answer the question using the PDF context below.

Context:
{context}

Question:
{question}
"""
        response = model.generate_content(prompt)
        st.write(response.text)