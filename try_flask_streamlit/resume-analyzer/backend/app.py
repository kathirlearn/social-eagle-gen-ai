# backend/app.py

from flask import Flask, request, jsonify
from parser import extract_text, extract_skills, skill_gap
from scorer import compute_match
from suggestions import generate_suggestions_llm
import pandas as pd
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

app = Flask(__name__)

@app.route("/analyze", methods=["POST"])
def analyze():
    try:
        # Get resume file and JD
        resume_file = request.files.get("resume")
        jd_text = request.form.get("job_description", "")
        custom_skills_input = request.form.get("custom_skills", "")

        if not resume_file or not jd_text.strip():
            return jsonify({"error": "Resume or Job Description missing"}), 400

        # Parse custom skills from comma-separated string
        custom_skills = [s.strip() for s in custom_skills_input.split(",") if s.strip()]

        # Extract text from resume
        resume_text = extract_text(resume_file)

        # Extract skills
        resume_skills = extract_skills(resume_text, custom_skills)
        jd_skills = extract_skills(jd_text, custom_skills)
        missing_skills = skill_gap(resume_skills, jd_skills)

        # Compute semantic match score
        match_score = compute_match(resume_text, jd_text)

        # Generate GPT suggestions
        suggestions = generate_suggestions_llm(resume_text, missing_skills)

        # Save results to CSV
        df = pd.DataFrame([{
            "resume": resume_file.filename,
            "match_score": match_score,
            "matched_skills": ", ".join(resume_skills),
            "missing_skills": ", ".join(missing_skills),
            "suggestions": " | ".join(suggestions)
        }])
        df.to_csv("analysis_results.csv", mode="a", index=False, header=False)

        # Return JSON response
        return jsonify({
            "match_score": match_score,
            "resume_skills": resume_skills,
            "jd_skills": jd_skills,
            "missing_skills": missing_skills,
            "suggestions": suggestions
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
