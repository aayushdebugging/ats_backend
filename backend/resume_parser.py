# backend/resume_parser.py
import google.generativeai as genai
from dotenv import load_dotenv
import os
import io
import PyPDF2
import json
import re

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def extract_resume_data(file_bytes: bytes):
    file = {
        "mime_type": "application/pdf",
        "data": file_bytes
    }

    prompt = """
    You are an intelligent resume parsing AI designed to support Applicant Tracking Systems (ATS).

    Your task is to extract all relevant candidate information from a resume document.

    Return the extracted data in the **exact JSON format** shown below:

    {
      "name": "Full Name",
      "email": "Email Address",
      "phone": "Phone Number",
      "linkedin": "LinkedIn URL (if present)",
      "total_experience": "Total years of experience (e.g., '3.5 years')",
      "education": [
        {
          "degree": "Degree Name",
          "institution": "University or College Name",
          "year": "Graduation Year or Duration"
        }
      ],
      "work_experience": [
        {
          "job_title": "Job Title",
          "company": "Company Name",
          "duration": "e.g., Jan 2020 - Dec 2022",
          "description": "Short summary of responsibilities and achievements"
        }
      ],
      "skills": [
        "List", "of", "soft", "and", "domain", "skills"
      ],
      "technical_skills": [
        "List", "of", "technical", "tools", "languages", "frameworks"
      ],
      "certifications": [
        "AWS Certified Solutions Architect", "Scrum Master", ...
      ],
      "projects": [
        {
          "title": "Project Title",
          "description": "Brief project summary (tech stack, outcome, etc.)"
        }
      ]
    }

    Only extract information **if available** in the resume. Do not hallucinate or fabricate data.
    Keep the JSON valid and return nothing else besides the JSON.
    """

    model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")
    response = model.generate_content([prompt, file])
    text_response = response.text.strip()

    try:
        # Handle markdown formatting if present
        if text_response.startswith("```json"):
            text_response = text_response[7:-3].strip()

        match = re.search(r'\{.*\}', text_response, re.DOTALL)
        if match:
            result = json.loads(match.group())
        else:
            raise ValueError("Could not find valid JSON structure.")

        return extract_text_from_pdf(file_bytes), result
    except Exception as e:
        print("Parsing error:", e)
        print("Gemini raw response:", text_response)
        return extract_text_from_pdf(file_bytes), {
            "name": "Not found",
            "email": "Not found"
        }

def extract_text_from_pdf(file_bytes: bytes):
    reader = PyPDF2.PdfReader(io.BytesIO(file_bytes))
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text
