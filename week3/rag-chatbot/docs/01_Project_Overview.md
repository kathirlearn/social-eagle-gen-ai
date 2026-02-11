# 📚 RAG-Based Document Chatbot with Web Search Fallback

This project is a **Retrieval-Augmented Generation (RAG) based chatbot** that allows users to upload documents (PDF or TXT) and ask questions based on the content of those documents.

If the system determines that the retrieved document context is **insufficient, incomplete, or unreliable**, it automatically falls back to **real-time web search using SerpAPI** to generate an accurate response.

This project is built as a **demo/interview-ready application** to showcase practical understanding of:
- Large Language Models (LLMs)
- Embeddings and vector databases
- Retrieval-Augmented Generation (RAG)
- Hallucination mitigation strategies
- Hybrid knowledge systems (documents + web)

---

## ✨ Key Features

- Upload and process **PDF and TXT documents**
- Semantic search using **OpenAI embeddings**
- Fast vector similarity search using **FAISS**
- Intelligent fallback to **live web search (SerpAPI)**
- Clean, modular, production-style codebase
- Interactive **Streamlit UI**

---

## 🧠 Tech Stack

- **LangChain** – RAG orchestration
- **OpenAI Embeddings & Chat Models**
- **FAISS** – Vector database
- **SerpAPI** – Web search fallback
- **Streamlit** – User interface
- **Python-dotenv** – Secure API key management

---

## 🎯 Use Cases

- Chat with books, manuals, or research papers
- Enterprise document Q&A systems
- Knowledge assistants with reduced hallucination
- Demonstration of real-world RAG pipelines
