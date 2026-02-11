
---

## 📄 `docs/03_Architecture_Workflow.md`
### (Architecture & Workflow Explanation)

```md
# 🏗️ Architecture & Workflow

This project follows a **modular RAG architecture** with a hybrid retrieval strategy.

---

## 🔷 High-Level Architecture

User
↓
Streamlit UI
↓
Document Upload (PDF/TXT)
↓
Text Chunking
↓
OpenAI Embeddings
↓
FAISS Vector Database
↓
User Query
↓
Similarity Search (Top-K)
↓
LLM Answer Generation
↓
Confidence Check
├─ If sufficient → Return Answer
└─ If insufficient → SerpAPI Web Search → Return Answer


---

## 🧩 Architectural Components

### 1. UI Layer
- Built with Streamlit
- Handles file upload and user queries

### 2. Ingestion Layer
- Loads PDF/TXT documents
- Splits text into overlapping chunks

### 3. Vector Store Layer
- Converts chunks into embeddings
- Stores vectors using FAISS

### 4. RAG Layer
- Retrieves relevant chunks
- Generates answers using LLM
- Performs confidence evaluation

### 5. Web Search Layer
- Uses SerpAPI for real-time Google search
- Summarizes results via LLM

---

## 🔐 Security
- API keys managed using `.env`
- `.env` excluded from version control
