#guess what to retrieve first, then retrieve, then reason, then correct
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.vectors import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.docstore.document import Document    
from langchain_core.prompts import PromptTemplate

llm = ChatOpenAI(temperature=0)

def speculative_rag(question):
    guess_prompt = PromptTemplate.from_template("extract keyword for {question}")
    guess_chain = guess_prompt | llm
    resp = guess_chain.invoke({"question": question})
    keyword = resp.content if hasattr(resp, "content") else str(resp)

    docs = [
        Document(page_content="The largest cat is a tiger."),
    ]

    db = FAISS.from_documents(docs, OpenAIEmbeddings())
    qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=db.as_retriever())
    
    return qa_chain.run(f"What is the {keyword}?")

print(speculative_rag("What is the largest cat?"))