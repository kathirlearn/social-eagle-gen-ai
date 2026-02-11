from serpapi import GoogleSearch
from langchain_openai import ChatOpenAI
from config.settings import SERPAPI_API_KEY

llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0
)

def web_search_answer(query):
    params = {
        "engine": "google",
        "q": query,
        "api_key": SERPAPI_API_KEY
    }

    search = GoogleSearch(params)
    results = search.get_dict()

    snippets = []
    for result in results.get("organic_results", [])[:5]:
        snippet = result.get("snippet")
        if snippet:
            snippets.append(snippet)

    web_context = "\n".join(snippets)

    prompt = f"""
Answer the question using the web search results below.

Web Results:
{web_context}

Question:
{query}
"""

    return llm.invoke(prompt).content
