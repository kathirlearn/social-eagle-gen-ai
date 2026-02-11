from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
import os
from dotenv import load_dotenv

load_dotenv()
llm = ChatOpenAI(model="gpt-4o", temperature=0.7, api_key=os.getenv("OPENAI_API_KEY"))

prompt_template = PromptTemplate(
    input_variables=["user_input"],
    template="""
    You are a helpful AI assistant. 
    User says: {user_input}
    Your response:"""
)

chain = prompt_template | llm   

if __name__ == "__main__":
    user_input = input("Ask me anything: ")
    response = chain.invoke({"user_input": user_input})
    print(f"AI says: {response.content}")











## This is a simple example of using LangChain to create an AI assistant that responds to user input.

# from langchain import OpenAI, LLMChain, PromptTemplate
# from langchain.prompts import ChatPromptTemplate
# import os
# from dotenv import load_dotenv

# load_dotenv()
# llm = OpenAI(model="gpt-4o", temperature=0.7, api_key=os.getenv("OPENAI_API_KEY"))

# prompt_template = PromptTemplate(
#     input_variables=["user_input"],
#     template="""
#     You are a helpful AI assistant. 
#     User says: {user_input}
#     Your response:"""
# )

# chain = LLMChain(llm=llm, prompt=prompt_template)   

# if __name__ == "__main__":
#     user_input = input("Ask me anything: ")
#     response = chain.run("user_input":user_input)
#     print(f"AI say: {response}")