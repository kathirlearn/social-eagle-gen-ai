import streamlit as st
from ingestion.document_loader import load_document
from vectorstore.faiss_store import create_vector_store
from rag.rag_chain import answer_question
from utils.helpers import save_uploaded_file

st.set_page_config(
    page_title="RAG Document Chatbot",
    layout="wide"
)

st.title("📚 RAG-Based Document Chatbot")
st.caption("Ask questions from uploaded documents with web fallback")

if "vector_store" not in st.session_state:
    st.session_state.vector_store = None

uploaded_file = st.file_uploader(
    "Upload a PDF or TXT file",
    type=["pdf", "txt"]
)

if uploaded_file:
    file_path = save_uploaded_file(uploaded_file)
    documents = load_document(file_path)
    st.session_state.vector_store = create_vector_store(documents)
    st.success("✅ Document indexed successfully")

query = st.text_input("Ask a question")

if query and st.session_state.vector_store:
    with st.spinner("Thinking..."):
        answer = answer_question(query, st.session_state.vector_store)
        st.markdown("### 🤖 Answer")
        st.write(answer)
