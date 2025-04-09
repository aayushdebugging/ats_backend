# backend/main.py
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import FileResponse
from resume_parser import extract_resume_data
from scorer import get_resume_score
from emailer import send_invite_email
from dotenv import load_dotenv
import pandas as pd
import os, io, zipfile, json
from typing import List

load_dotenv()
app = FastAPI()

results = []  # Global list to store resume info


@app.post("/upload-resumes")
async def upload_zip_resumes(file: UploadFile = File(...)):
    global results
    results.clear()  # Clear previous entries
    contents = await file.read()

    with zipfile.ZipFile(io.BytesIO(contents)) as z:
        for filename in z.namelist():
            if filename.endswith(".pdf"):
                resume_file = z.read(filename)
                text, data = extract_resume_data(resume_file)
                result_entry = {
                    "filename": filename,
                    "text": text,
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
                    "work_experience": json.dumps(data.get("work_experience", []))
                }
                results.append(result_entry)

    return {"message": f"Uploaded and parsed {len(results)} resumes."}


@app.post("/score-resumes")
async def score_all(
    jd: str = Form(...),
    skills: str = Form(...),
    threshold: int = Form(...),
    meeting_link: str = Form(...)
):
    global results
    skill_list = [s.strip() for s in skills.split(",") if s.strip()]
    qualified = []

    for r in results:
        scoring = get_resume_score(r["text"], jd, skill_list)
        try:
            score = int(scoring.get("JD Match", "0%").replace("%", "").strip())
        except:
            score = 0

        r["JD Match"] = f"{score}%"
        r["MissingKeywords"] = ", ".join(scoring.get("MissingKeywords", []))
        r["Profile Summary"] = scoring.get("Profile Summary", "")
        r["Qualified"] = "Yes" if score >= threshold else "No"
        r["ScoreValue"] = score  # Temporary field for sorting

        # Add to email queue
        if score >= threshold and r.get("email") and "@" in r["email"]:
            qualified.append({
                "name": r.get("name", ""),
                "email": r.get("email"),
                "meeting_link": meeting_link
            })

    # Sort results by score
    sorted_results = sorted(results, key=lambda x: x["ScoreValue"], reverse=True)
    df = pd.DataFrame(sorted_results)
    df.drop(columns=["ScoreValue"], inplace=True)
    df.to_csv("../results/final_results.csv", index=False)

    # Send emails to qualified candidates
    success, failure = 0, 0
    for q in qualified:
        try:
            send_invite_email(q["name"], q["email"], q["meeting_link"])
            success += 1
        except Exception as e:
            print(f"❌ Failed to send to {q['email']}: {e}")
            failure += 1

    return {
        "message": f"Processed {len(results)} resumes.",
        "qualified_count": len(qualified),
        "emails_sent": success,
        "emails_failed": failure
    }


@app.get("/download-results")
def download():
    return FileResponse("../results/final_results.csv", media_type='text/csv', filename="results.csv")


@app.post("/send-invite")
async def send_invite(name: str = Form(...), email: str = Form(...), meeting_link: str = Form(...)):
    status = send_invite_email(name, email, meeting_link)
    return {"status": status}
