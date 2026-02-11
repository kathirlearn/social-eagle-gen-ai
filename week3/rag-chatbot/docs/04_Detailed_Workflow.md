# 🔄 Detailed Workflow

This section explains the step-by-step execution flow of the system.

---

## 📥 Step 1: Document Upload & Processing

- User uploads a PDF or TXT file
- Text is extracted from the document
- Text is split into chunks using overlap to preserve context
- Each chunk is converted into embeddings
- Embeddings are stored in FAISS

---

## ❓ Step 2: User Query Handling

- User submits a natural language question
- FAISS performs similarity search on stored embeddings
- Top-K relevant document chunks are retrieved

---

## 🧠 Step 3: RAG Answer Generation

- Retrieved chunks are passed as context to the LLM
- LLM generates an answer strictly based on document context
- Prompt instructs the model to avoid hallucination

---

## 📊 Step 4: Confidence Evaluation

The system evaluates:
- Vector similarity score threshold
- Presence of low-confidence phrases such as:
  - "Not mentioned in document"
  - "Insufficient context"

If confidence is low → fallback is triggered

---

## 🌐 Step 5: Web Search Fallback

- Query is sent to SerpAPI (Google Search)
- Top web snippets are collected
- LLM summarizes web results into a final answer

---

## ✅ Final Response

- User receives the most reliable answer possible
- Document-based if available
- Web-based if document knowledge is insufficient

---

## 🎯 Design Goal

Minimize hallucinations while maximizing answer accuracy using a hybrid knowledge approach.
