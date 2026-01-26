# backend/suggestions.py

import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


def generate_suggestions_llm(resume_text, missing_skills):
    """
    Generate resume improvement suggestions using OpenAI GPT
    (Updated for openai>=1.0.0)
    """
    if not missing_skills:
        return "Your resume already covers all required skills!"

    prompt = f"""
I have the following resume text:
{resume_text}

And these missing skills: {', '.join(missing_skills)}.

Suggest improvements and actionable advice to include these missing skills
in a professional way.
"""

    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )

        suggestion = response.choices[0].message.content
        return suggestion

    except Exception as e:
        return f"Error generating suggestions: {e}"
