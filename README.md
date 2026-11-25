📄 PDF Chatbot (RAG + Gemini)

A lightweight Streamlit PDF Chatbot powered by Retrieval-Augmented Generation (RAG) and Google Gemini (gemini-2.5-flash). Upload any text-based PDF, ask questions in natural language, and get context-aware answers grounded in your document.

✨ Features

PDF Upload & Parsing: Extracts text page by page using pypdf.

Smart Chunking: Splits text into overlapping chunks (700 words with an 80-word overlap) to preserve context.

Semantic Search: Embeds chunks using SentenceTransformer (all-MiniLM-L6-v2) and stores them in an in-memory ChromaDB collection.

AI-Powered Q&A: Retrieves the top 3 most relevant passages for any question and generates answers using Gemini (models/gemini-2.5-flash).

Session Caching: Indexes each uploaded PDF once per session so follow-up questions respond quickly.

🛠️ Tech Stack

Frontend / UI: Streamlit

PDF Extraction: pypdf

Embeddings: Sentence-Transformers (all-MiniLM-L6-v2)

Vector Database: ChromaDB

LLM: Google Generative AI (models/gemini-2.5-flash)

🚀 Getting Started

1. Prerequisites

Python 3.9+

A Google Gemini API Key (get one from Google AI Studio)

2. Installation

Clone or download this repository, then install the required dependencies:

pip install streamlit pypdf sentence-transformers chromadb google-generativeai


3. Configure Your API Key

Open pdf_chat.py and paste your Gemini API key into the api_key variable:

api_key = "YOUR_GEMINI_API_KEY"


Security Tip: Avoid committing your actual API key to public repositories.

4. Run the Application

streamlit run pdf_chat.py


Open the local URL displayed in your terminal (typically http://localhost:8501).

📖 Usage

Click Upload a PDF and select a .pdf file.

Wait for the "PDF indexed! Ask your questions below." confirmation message.

Type your question into the text box and press Enter to receive an answer based on the PDF's contents.

⚠️ Limitations

Works best with text-based PDFs (scanned/image-only PDFs require OCR before extraction).

Uses an in-memory ChromaDB instance, so indexed documents reset when the app restarts.
