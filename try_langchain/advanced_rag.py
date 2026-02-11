# Advanced RAG (guess, retrieve, reason, correct)

embeddings = OpenAIEmbeddings()
def advanced_rag(question):
    guess_topic = llm.predict(f"What is the main topic of: { question}?")

    docs = [
        Document(page_content="The largest cat is a tiger."),
        Document(page_content="The capital of France is Paris."),
        Document(page_content="The tallest mountain is Everest."),
        Document(page_content="The main topic of the question is about cats."),
    ]

    db = FAISS.from_documents(docs, embeddings)

    qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=db.as_retriever())
    result = qa_chain.run(question)

    return f"Topic: {guess_topic}\nAnswer based on retrieved documents: {result}"

print(advanced_rag("What is the largest cat?"))