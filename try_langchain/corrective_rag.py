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

def corrective_rag(question):
    first_guess = llm.predict(f"Try to answer:{question}")

    docs = [Document(page_content="The largest cat is a tiger.")]
    db = FAISS.from_documents(docs, embeddings)

    qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=db.as_retriever())
    correction = qa_chain.run(question)

    return f"Original answer:{first_guess}\nCorrected using documents:{correction}"
    
print(corrective_rag("What is the largest cat?"))