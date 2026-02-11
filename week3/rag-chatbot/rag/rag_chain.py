from langchain_openai import ChatOpenAI
from config.settings import TOP_K, SIMILARITY_THRESHOLD
from rag.confidence import is_low_confidence
from web_search.serpapi_search import web_search_answer

llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0
)

def answer_question(query, vector_store):
    docs_and_scores = vector_store.similarity_search_with_score(
        query,
        k=TOP_K
    )

    if not docs_and_scores:
        return web_search_answer(query)

    docs, scores = zip(*docs_and_scores)

    if max(scores) < SIMILARITY_THRESHOLD:
        return web_search_answer(query)

    context = "\n\n".join(doc.page_content for doc in docs)

    prompt = f"""
Answer the question using ONLY the context below.
If the answer does not exist in the context, say so clearly.

Context:
{context}

Question:
{query}
"""

    answer = llm.invoke(prompt).content

    if is_low_confidence(answer):
        return web_search_answer(query)

    return answer
