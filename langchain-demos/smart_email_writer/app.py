import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
import os
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(
    model="gpt-4o", 
    temperature=0.5, 
    api_key=os.getenv("OPENAI_API_KEY"))

prompt = PromptTemplate(
    input_variables=["bullet_points"],
    template="""
You are an expert email writer. Using the following bullet points, draft a professional and friendly email:
{bullet_points}
Make sure the email has a greeting, well-structured, clear structure, polite and closing.
""")

create_email_chain = prompt | llm

st.title("Smart Email Writer")
st.write("Enter bullet points to generate a professional email.")

bullet_points = st.text_area("Bullet Points (one per line):", height=250)

if st.button("Generate Email"):
    if bullet_points.strip() == "":
        st.warning("Please enter some bullet points.")
    else:
        with st.spinner("Generating email..."):
            response = create_email_chain.invoke({"bullet_points": bullet_points})
            email_content = response.content if hasattr(response, "content") else str(response)
            st.subheader("Generated Email")
            st.write(email_content)


