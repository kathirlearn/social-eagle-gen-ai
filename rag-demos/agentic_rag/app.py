import os
import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from openai import OpenAI
import requests
from sentence_transformers import SentenceTransformer
import faiss

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SERPAPI_KEY = os.getenv("SERPAPI_KEY")

client = OpenAI()

# == Load pdf & extract text == #
@st.cache_resource
def load_pdfs_and_create_index(pdf_paths):
    docs =[]
    for path in pdf_paths:
        try:
            reader = PdfReader(path)
            text = "\n".join(page.extract_text() for page in reader.pages if page.extract_text())
            # text = ""
            # for page in reader.pages:
            #     text += page.extract_text() or ""
            docs.append(text)
        except Exception as e:
            st.error(f"Error reading {path}: {str(e)}")

    chunks = []
    for doc in docs:
        for i in range(0, len(doc), 500):
            chunk = (doc[i:i+500])
            if chunk.strip():
                chunks.append(chunk)

    model = SentenceTransformer('all-MiniLM-L6-v2')
    vectors = model.encode(chunks)

    index = faiss.IndexFlatL2(vectors.shape[1])
    index.add(vectors)

    return chunks, index, model

# == retrieve == #
def retrieve(query, chunks, index, model, top_k=3):
    query_vec = model.encode([query])
    D, I = index.search(query_vec, top_k)
    return [chunks[i] for i in I[0]]

# === verifier === #
def is_answer_sufficient(query, answer):
    prompt = f"""
    Question: {query}
    Answer: {answer}
    Is the retrieved answer sufficient, accurate and complete? reply with YES or NO and a short reason.
    """
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content

# === Fallback: SerpAPI via requests === #
def search_web(query):
    url = "https://serpapi.com/search.json"
    params = {
        "q": query,
        "api_key": SERPAPI_KEY,
        "engine": "google"
    }
    resp = requests.get(url, params=params)
    results = resp.json()
    organic = results.get("organic_results", [])
    snippets = []
    for r in organic:
        snippet = r.get("snippet") or r.get("title")
        if snippet:
            snippets.append(snippet)

    if snippets:
        return "\n".join(snippets)
    else:
        # if search failed , ask llm to answer from scratch
        fallback_prompt = f"""
        The web search for the questions "{query}" returned no relevant results. 
        Please generate a helpful answer to this questions using your general knowledge.
        """
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": fallback_prompt}]
        )
        return response.choices[0].message.content
    
# == Orchestrator == #
def answer_query(query, chunks, index, model):
    retrieved = retrieve(query, chunks, index, model)
    combined_answer = "\n\n".join(retrieved)

    verdict = is_answer_sufficient(query, combined_answer)

    if "YES" in verdict.upper():
        return f"Answer from PDFs:\n\n{combined_answer} \n\n(Verifier: {verdict})"
    else:
        serp_result = serp_search(query)
        return f"Answer from Web Search:\n\n{serp_result} \n\n(Verifier: {verdict})"
    
# == Streamlit UI == #
st.title("Agentic RAG App (No Framework): Ask your PDF Anything!")

uploaded_files = st.file_uploader("Upload PDF files", type=["pdf"], accept_multiple_files=True)

if uploaded_files:
    with st.spinner("Processing PDFs..."):
        pdf_paths = []
        for uploaded_file in uploaded_files:
            path = f"/tmp/{uploaded_file.name}"
            with open(path, "wb") as f:
                f.write(uploaded_file.read())
            pdf_paths.append(path)

        chunks, index, model = load_pdfs_and_create_index(pdf_paths)
    st.success(f"Processed {len(uploaded_files)} PDFs into {len(chunks)} text chunks.")

    query = st.text_input("Ask a question about your PDF content:")

    if st.button("Get Answer") and query:
        with st.spinner("Generating answer..."):
            answer = answer_query(query, chunks, index, model)
        st.markdown(answer)