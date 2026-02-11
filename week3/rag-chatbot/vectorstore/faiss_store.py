from langchain_openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS

def create_vector_store(documents):
    embeddings = OpenAIEmbeddings()
    vector_store = FAISS.from_documents(documents, embeddings)
    return vector_store
