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

qa_prompt = PromptTemplate(
    input_variables=["role","jd","qa"],
    template="""
    You are a senior technical interviewer.
    Given this Job Role: {role}
    And this Job Description: {jd}


    Generate {qa} **Technical** mock interview questions that are relevant to the role and job description.
    Only include questions that test technical skills and knowledge, or problem-solving abilities.
    Do NOT include situational or behavioral questions.

    For each question, also provide a clear, strong sample answer.

    Number them 1 to 5, and format like this:
    1. Question: [Question text]
    Answer: [Sample answer text]
    """
)

mock_interview_chain = qa_prompt | llm

st.title("AI Mock Interview Question Generator")

role = st.text_input("Enter the Job Role (e.g., Software Engineer)")
jd = st.text_area("Enter the Job Description")
qa = st.number_input("Number of Q & A pairs to generate", min_value=1, max_value=20, value=5)  # Allow user to specify number of Q&A pairs

if st.button("Generate Q & A"):
    if role.strip() == "" or jd.strip() == "":
        st.warning("Please enter both the job role and job description.")
    else:
        with st.spinner("Generating questions and answers..."):
            response = mock_interview_chain.invoke({"role": role, "jd": jd, "qa": qa})
            result = response.content if hasattr(response, "content") else str(response)
            st.subheader("Generated Mock Interview Questions and Answers")
            st.write(result)