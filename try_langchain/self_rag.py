from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.vectors import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter


loader = TextLoader("notes.txt")
docs=loader.load()
text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
chunks = text_splitter.split_documents(docs)

embeddings = OpenAIEmbeddings()
vector_store = FAISS.from_documents(chunks, embeddings)
retriever = vector_store.as_retriever()

llm = ChatOpenAI(temperature=0)

qa = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)

def self_rag_query(question):
    print("First attempt without retrieval")
    first_answer = llm.predict(f"Q:{question}\nA")

    if "I'm not sure" in first_answer or len(first_answer) < 30:
        print("Low confidence, Retrieving context and trying again...")
        improved_answer = qa.run(question)
        return improved_answer
    else:
        return first_answer
    
response = self_rag_query("What is the capital of France?")
print("\nFinal Answer:", response)