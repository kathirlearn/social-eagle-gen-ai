import PyPDF2
from docx import Document
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
    input_variables=["resume_text", "job_title", "company"],
    template="""You are an expert career coach and writer.
    write a professional, personalized cover letter for the following job application.
    Job Title:{job_title}
    Company:{company}

    Use the following resume information:
   {resume_text}
   Keep the tone formal but friendly, and make sure to highlight the most relevant experiences and enthusiasm for the role.
  Use a professional and engaging tone, and include a strong opening and closing statement.
""")

create_cover_letter_chain = prompt | llm

st.title("AI Cover Letter Generator")
st.write("Enter your resume details and the job information to generate a personalized cover letter.")

upload_resume = st.file_uploader("Upload your resume (PDF or TXT format)", type=["txt","pdf","docx"])
job_title = st.text_input("Job Title (e.g., Software Engineer)")
company = st.text_input("Company Name (Optional)(e.g., Tech Innovators Inc.)")

if st.button("Generate Cover Letter"):
    if not upload_resume or job_title.strip() == "":
        st.warning("Please upload your resume and enter the job title.")
    else:
        with st.spinner("Generating cover letter..."):
            resume_text = ""
            if upload_resume.name.endswith(".txt"):
                resume_text = upload_resume.read().decode("utf-8")
                
            elif upload_resume.name.endswith((".pdf")):
               pdf_reader = PyPDF2.PdfReader(upload_resume)
            #    resume_text = "\n".join(page.extract_text() for page in pdf_reader.pages)
               resume_text = ""
               for page in pdf_reader.pages:
                resume_text += page.extract_text()

            elif upload_resume.name.endswith((".docx")):
                doc = Document(upload_resume)
                resume_text = "\n".join(paragraph.text for paragraph in doc.paragraphs)
            else:
                st.warning("Unsupported file format. Please upload a TXT, PDF, or DOCX file.")
                resume_text = ""
                st.stop()

            if resume_text:     
                response = create_cover_letter_chain.invoke({
                    "resume_text": resume_text,
                    "job_title": job_title,
                    "company": company if company.strip() != "" else "the company"
                })
            cover_letter = response.content if hasattr(response, "content") else str(response)
            st.subheader("Generated Cover Letter")
            st.write(cover_letter)







# if st.button("Generate Cover Letter"):
#     if not upload_resume or job_title.strip() == "":
#         st.warning("Please upload your resume and enter the job title.")
#     else:
#         with st.spinner("Generating cover letter..."):
#             resume_text = ""
#             if upload_resume.type == "text/plain":
#                 resume_text = upload_resume.read().decode("utf-8")
#             elif upload_resume.type in ["application/pdf", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"]:
#                 st.warning("Currently only TXT format is supported for resume. Please convert your resume to TXT format and try again.")
#                 st.stop()
            
#             response = create_cover_letter_chain.invoke({
#                 "resume_text": resume_text,
#                 "job_title": job_title,
#                 "company": company
#             })
#             cover_letter = response.content if hasattr(response, "content") else str(response)
#             st.subheader("Generated Cover Letter")
#             st.write(cover_letter)