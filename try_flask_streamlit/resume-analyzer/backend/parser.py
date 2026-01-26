import pdfplumber
from docx import Document
from skills_db import SKILLS

def extract_text(file):
    text = ""
    if file.filename.endswith(".pdf"):
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                text += page.extract_text() + "\n"
    elif file.filename.endswith(".docx"):
        doc = Document(file)
        for para in doc.paragraphs:
            text += para.text + "\n"
    else:
        text = file.read().decode("utf-8")
    return text.lower()

def extract_skills(text, custom_skills=None):
    skills_db = SKILLS.copy()
    if custom_skills:
        skills_db += [s.lower() for s in custom_skills]
    return [skill for skill in skills_db if skill in text]

def skill_gap(resume_skills, jd_skills):
    return list(set(jd_skills) - set(resume_skills))
