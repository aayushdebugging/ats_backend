# backend/scorer.py
import google.generativeai as genai
from dotenv import load_dotenv
import os
import json
import re

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_resume_score(resume_text: str, jd: str, skills: list):
    prompt = f"""
You are an experienced AI resume evaluator for an Applicant Tracking System (ATS).

Evaluate the following resume text for its match with the provided Job Description and Required Skills.

Resume:
{resume_text}

Job Description:
{jd}

Required Skills:
{', '.join(skills)}

You must return a valid JSON like:
{{
  "JD Match": "85%",  // Match percentage with the JD
  "MissingKeywords": ["list", "of", "missing", "skills"],
  "Profile Summary": "A brief summary of the candidate's background and suitability for the role"
}}

Only return valid JSON. Do not include any additional explanation or formatting.
"""

    model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")
    response = model.generate_content(prompt)
    text_response = response.text.strip()

    try:
        if text_response.startswith("```json"):
            text_response = text_response[7:-3].strip()

        match = re.search(r'\{.*\}', text_response, re.DOTALL)
        if match:
            return json.loads(match.group())
        else:
            raise ValueError("Could not parse valid JSON.")
    except Exception as e:
        print("Scoring error:", e)
        print("Gemini response:", text_response)
        return {
            "JD Match": "0%",
            "MissingKeywords": skills,
            "Profile Summary": "Could not evaluate this resume properly."
        }
