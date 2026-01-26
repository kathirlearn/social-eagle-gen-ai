# frontend/streamlit_app.py

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

from scorer import compute_match, plot_skill_match
from suggestions import generate_suggestions_llm

import streamlit as st
import pandas as pd
import pdfplumber
import docx

# --- Helper Functions ---
def extract_text_from_file(uploaded_file):
    if uploaded_file.name.endswith(".pdf"):
        with pdfplumber.open(uploaded_file) as pdf:
            text = "\n".join([page.extract_text() or "" for page in pdf.pages])
        return text
    elif uploaded_file.name.endswith(".docx"):
        doc = docx.Document(uploaded_file)
        return "\n".join([para.text for para in doc.paragraphs])
    else:
        return None

# --- Page Setup ---
st.set_page_config(page_title="Resume Analyzer", layout="wide")
st.title("📄 Resume Analyzer")

# --- Input Section ---
uploaded_file = st.file_uploader("Upload Resume (PDF or DOCX)", type=["pdf", "docx"])
resume_text_input = st.text_area("Or paste Resume Text", height=200)

resume_text = ""
if uploaded_file:
    resume_text = extract_text_from_file(uploaded_file)
elif resume_text_input:
    resume_text = resume_text_input

job_text = st.text_area("Paste Job Description Here", height=200)

skills_input = st.text_area(
    "Enter skills (comma-separated)", 
    "Python, SQL, Machine Learning, AWS, JavaScript"
)
skills_list = [s.strip() for s in skills_input.split(",") if s.strip()]

# --- Analyze Button ---
if st.button("Analyze Resume"):
    if not resume_text:
        st.error("Please provide a resume text or upload a file.")
    else:
        try:
            # Compute match score and skills
            match_score, matched_skills, missing_skills = compute_match(resume_text, job_text, skills_list)

            # Display results
            st.subheader(f"Match Score: {match_score}%")
            st.write("✅ Matched Skills:", matched_skills)
            st.write("❌ Missing Skills:", missing_skills)

            # Plot skill match pie chart
            plot_skill_match(matched_skills, missing_skills)

            # Generate GPT suggestions
            st.subheader("💡 GPT Suggestions for Improvement")
            suggestion = generate_suggestions_llm(resume_text, missing_skills)
            st.write(suggestion)

            # CSV Download for skills
            max_len = max(len(matched_skills), len(missing_skills))
            df = pd.DataFrame({
                "Matched Skills": matched_skills + [""] * (max_len - len(matched_skills)),
                "Missing Skills": missing_skills + [""] * (max_len - len(missing_skills)),
            })
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button("Download Skills CSV", csv, "skills.csv", "text/csv")

        except Exception as e:
            st.error(f"Error analyzing resume: {e}")
