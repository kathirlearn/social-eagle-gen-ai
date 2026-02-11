import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize LLM
llm = ChatOpenAI(
    model="gpt-4o", 
    temperature=0.5, 
    api_key=os.getenv("OPENAI_API_KEY"))

# Initialize prompt template
prompt_template = PromptTemplate(
    input_variables=["code_task"],
    template="""
    You are a professional AI code assistant. Help the user with the following coding task. 
    {code_task}
    Provide clean, well-commented code and explanations if needed  .
    """)

# Create the chain (LCEL)
chain = prompt_template | llm

# Streamlit UI
st.title("AI Code Assistant")
st.write("Get help with your coding tasks!")

code_task = st.text_area("Enter your coding task:")

if st.button("Generate Code"):
    if code_task.strip() == "":
        st.warning("Please enter a coding task description.")
    else:
        with st.spinner("Processing..."):
            response = chain.invoke({"code_task": code_task})
            result = response.content if hasattr(response, "content") else str(response)
            st.subheader("Assistant Response")
            st.code(result, language="python")