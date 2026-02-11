import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
import os
from dotenv import load_dotenv

load_dotenv()

# Page configuration
st.set_page_config(page_title="AI Assistant", layout="centered")
st.title("🤖 AI Assistant")

# Initialize LLM
@st.cache_resource
def get_llm():
    return ChatOpenAI(
        model="gpt-4o", 
        temperature=0.7, 
        api_key=os.getenv("OPENAI_API_KEY")
    )

# Initialize prompt template
@st.cache_resource
def get_chain():
    llm = get_llm()
    prompt_template = PromptTemplate(
        input_variables=["user_input"],
        template="""
    You are a helpful AI assistant. 
    User says: {user_input}
    Your response:"""
    )
    return prompt_template | llm

# Get user input
user_input = st.text_input("Ask me anything:")

# Process input when user submits
if user_input:
    with st.spinner("Thinking..."):
        chain = get_chain()
        response = chain.invoke({"user_input": user_input})
        st.success("Done!")
        st.write(f"**AI says:** {response.content}")
