# backend/test_single_resume.py

from resume_parser import extract_resume_data
from scorer import get_resume_score
from emailer import send_invite_email
import os
import json
import pandas as pd

# ------------ USER INPUTS ------------

pdf_path = "Nandini_Bhalla_22cs22002_IDD (1).pdf"  # Replace with your file
job_description = """
We are seeking an AI Research Engineer to join our team to work on cutting-edge problems in machine learning, deep learning, and generative AI. 
The ideal candidate will have experience in developing and optimizing models, conducting experiments, and publishing research. 
Strong knowledge of Python, PyTorch or TensorFlow, and transformer-based architectures is essential. 
Familiarity with tools such as Hugging Face, LangChain, and experience with LLM fine-tuning and model deployment is a plus.
"""
required_skills = [
    "Python", "PyTorch", "TensorFlow", "Transformers", "Hugging Face",
    "LangChain", "LLM Fine-Tuning", "Model Deployment", "Deep Learning", "Machine Learning Research"
]
threshold = 70  # Minimum score to qualify
meeting_link = "https://meet.example.com/interview-link"

# ------------ PROCESS SINGLE FILE ------------

with open(pdf_path, "rb") as f:
    file_bytes = f.read()

# Extract structured info
text, data = extract_resume_data(file_bytes)
print("\n👤 Extracted:")
print("Name:", data.get("name"))
print("Email:", data.get("email"))

# Score resume
scoring = get_resume_score(text, job_description, required_skills)
score = int(scoring.get("JD Match", "0%").replace("%", "").strip())

result = {
    "filename": os.path.basename(pdf_path),
    "name": data.get("name", "Not found"),
    "email": data.get("email", "Not found"),
    "phone": data.get("phone", ""),
    "linkedin": data.get("linkedin", ""),
    "total_experience": data.get("total_experience", ""),
    "skills": ", ".join(data.get("skills", [])),
    "technical_skills": ", ".join(data.get("technical_skills", [])),
    "certifications": ", ".join(data.get("certifications", [])),
    "projects": json.dumps(data.get("projects", [])),
    "education": json.dumps(data.get("education", [])),
    "work_experience": json.dumps(data.get("work_experience", [])),
    "JD Match": f"{score}%",
    "MissingKeywords": ", ".join(scoring.get("MissingKeywords", [])),
    "Profile Summary": scoring.get("Profile Summary", ""),
    "Qualified": "Yes" if score >= threshold else "No"
}

# Send interview invite if qualified
if result["Qualified"] == "Yes" and "@" in result["email"]:
    try:
        send_invite_email(result["name"], result["email"], meeting_link)
        print(f"✅ Email sent to: {result['email']}")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")
else:
    print("❌ Candidate did not qualify. No email sent.")

# Save to CSV
df = pd.DataFrame([result])
os.makedirs("../results", exist_ok=True)
df.to_csv("../results/final_results.csv", index=False)

print(f"\n📄 Saved result to ../results/final_results.csv")
