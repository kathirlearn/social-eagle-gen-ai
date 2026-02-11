from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.vectors import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.docstore.document import Document

docs = [
    Document(page_content="The largest cat is a tiger."),
    Document(page_content="The capital of France is Paris."),
    Document(page_content="The tallest mountain is Everest.")
]

embeddings = OpenAIEmbeddings()
db = FAISS.from_documents(docs, embeddings)
llm = ChatOpenAI(temperature=0)

fusion_rag_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=db.as_retriever(),
    return_source_documents=False
)

print(fusion_rag_chain.run("What is the largest cat?"))