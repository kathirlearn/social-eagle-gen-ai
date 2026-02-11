import streamlit as st
from PyPDF2 import PdfReader
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain_community.chains import RetrievalQA
from langchain_text_splitters import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
import os

load_dotenv()

llm = ChatOpenAI(api_key=os.getenv("OPENAI_API_KEY"), model_name="gpt-4o", temperature=0.2)
embeddings = OpenAIEmbeddings()

st.title("RAG App: Ask your PDF Anything!")
uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

if uploaded_file is not None:
    raw_text = ""

    try:
        pdf_reader = PdfReader(uploaded_file)
        for page in pdf_reader.pages:
            text = page.extract_text()
            if text:
                raw_text += text

    except Exception as e:
        st.error(f"Error reading PDF: {str(e)}")
    
    if not raw_text.strip():
        st.error("Could not extract any text from this PDF.\n\n"
                 "It may be a scanned image PDF with no slectable text.\n\n"
                 "please use a text-based PDF or run OCR first.")
    else:
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        chunks = text_splitter.split_text(raw_text)

        if not chunks:
            st.error("No text chunks were created from the PDF. Please check the content of the PDF.")
        else:
            st.success(f"PDF processed successfully! Created {len(chunks)} text chunks.")
            vector_store = FAISS.from_texts(chunks, embeddings=embeddings)

            qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=vector_store.as_retriever())
            question = st.text_input("Ask a question about your PDF content:")

            if question:
                with st.spinner("Generating answer..."):
                    answer = qa.run(question)
                st.subheader("Answer")
                st.write(answer)


