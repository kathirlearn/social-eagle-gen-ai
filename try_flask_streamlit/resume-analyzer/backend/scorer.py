# backend/scorer.py

import re
from sentence_transformers import SentenceTransformer, util
import matplotlib.pyplot as plt
import streamlit as st

# Load embedding model once
model = SentenceTransformer('all-MiniLM-L6-v2')


def clean_text(text):
    """Lowercase text and remove extra spaces"""
    return re.sub(r'\s+', ' ', text.lower())


def extract_skills(resume_text, skills_list):
    """
    Extract matched and missing skills from resume text.
    Handles multi-word skills, punctuation, and case-insensitive matching.
    """
    resume_text = clean_text(resume_text)
    skills_list = [skill.lower() for skill in skills_list]

    resume_words = re.findall(r'\b\w+\b', resume_text)

    matched_skills = []
    missing_skills = []

    for skill in skills_list:
        skill_words = skill.split()
        if all(word in resume_words for word in skill_words):
            matched_skills.append(skill)
        else:
            missing_skills.append(skill)

    return matched_skills, missing_skills


def compute_match(resume_text, job_text, skills_list):
    """
    Compute overall match score combining:
    - Skill coverage (70%)
    - Semantic similarity (30%)
    """
    if not resume_text or not job_text:
        return 0, [], []

    matched_skills, missing_skills = extract_skills(resume_text, skills_list)

    if resume_text.strip() and job_text.strip():
        resume_embedding = model.encode(clean_text(resume_text), convert_to_tensor=True)
        job_embedding = model.encode(clean_text(job_text), convert_to_tensor=True)
        similarity_score = util.cos_sim(resume_embedding, job_embedding).item()
    else:
        similarity_score = 0

    skill_score = (len(matched_skills) / len(skills_list)) * 100 if skills_list else 0
    match_score = round(0.7 * skill_score + 0.3 * similarity_score * 100, 2)

    return match_score, matched_skills, missing_skills


def plot_skill_match(matched_skills, missing_skills):
    """
    Plot a pie chart in Streamlit showing matched vs missing skills
    """
    labels = ['Matched Skills', 'Missing Skills']
    sizes = [len(matched_skills), len(missing_skills)]
    colors = ['#4CAF50', '#FF5722']

    fig, ax = plt.subplots(figsize=(6,6))
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors, startangle=90)
    ax.set_title("Skill Match Overview")
    ax.axis('equal')

    st.pyplot(fig)
