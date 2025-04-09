import zipfile
import io
import os
from resume_parser import extract_resume_data
from scorer import get_resume_score
import pandas as pd

# 👇 Path to a single PDF file to test
pdf_path = "Nandini_Bhalla_22cs22002_IDD (1) (1).pdf"

# 👇 Simulated Job Description and Skills input
job_description = """
We are seeking an AI Research Engineer to join our team to work on cutting-edge problems in machine learning, deep learning, and generative AI. 
The ideal candidate will have experience in developing and optimizing models, conducting experiments, and publishing research. 
Strong knowledge of Python, PyTorch or TensorFlow, and transformer-based architectures is essential. 
Familiarity with tools such as Hugging Face, LangChain, and experience with LLM fine-tuning and model deployment is a plus.
"""

required_skills = [
    "Python",
    "PyTorch",
    "TensorFlow",
    "Transformers",
    "Hugging Face",
    "LangChain",
    "LLM Fine-Tuning",
    "Model Deployment",
    "Deep Learning",
    "Machine Learning Research"
]

# Step 1: Read the PDF
with open(pdf_path, "rb") as f:
    file_bytes = f.read()

# Step 2: Extract resume info
resume_text, data = extract_resume_data(file_bytes)

print("\n✅ Parsed Resume Info:")
print("Name:", data.get("name"))
print("Email:", data.get("email"))
print("Phone:", data.get("phone"))
print("Skills:", data.get("skills"))

# Step 3: Score with JD and Skills
scoring = get_resume_score(resume_text, job_description, required_skills)

print("\n🧠 Gemini Scoring Result:")
print("JD Match:", scoring.get("JD Match"))
print("Missing Keywords:", scoring.get("MissingKeywords"))
print("Summary:", scoring.get("Profile Summary"))

# Step 4: Combine all into a result row
result = {
    "name": data.get("name"),
    "email": data.get("email"),
    "phone": data.get("phone"),
    "linkedin": data.get("linkedin"),
    "total_experience": data.get("total_experience"),
    "skills": ", ".join(data.get("skills", [])),
    "technical_skills": ", ".join(data.get("technical_skills", [])),
    "certifications": ", ".join(data.get("certifications", [])),
    "projects": str(data.get("projects", [])),
    "education": str(data.get("education", [])),
    "work_experience": str(data.get("work_experience", [])),
    "JD Match": scoring.get("JD Match", "0%"),
    "MissingKeywords": ", ".join(scoring.get("MissingKeywords", [])),
    "Profile Summary": scoring.get("Profile Summary", "")
}

# Step 5: Save to CSV
df = pd.DataFrame([result])
os.makedirs("../results", exist_ok=True)
df.to_csv("../results/test_result.csv", index=False)
print("\n📁 Saved to results/test_result.csv")
