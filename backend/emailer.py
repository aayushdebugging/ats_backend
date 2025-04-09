# backend/emailer.py

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os
import google.generativeai as genai

load_dotenv()

EMAIL = os.getenv("EMAIL_ADDRESS")
PASSWORD = os.getenv("EMAIL_PASSWORD")
API_KEY = os.getenv("GOOGLE_API_KEY")

# Configure Gemini with your API key.
genai.configure(api_key=API_KEY)

def generate_email_content(name, jd, meeting_link):
    """
    Use Gemini Generative AI to create a personalized email invitation based on the job description.
    """
    prompt = f"""
You are an AI email generator. Write a professional and personalized interview invitation email for an AI Research Engineer candidate.
Use the following job description to tailor the email:
Job Description: {jd}

Candidate's Name: {name}
Meeting Link: {meeting_link}

Write an email in plain text that invites the candidate to an interview, emphasizing key points from the job description.
Return only the email content as plain text.
"""
    model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")
    response = model.generate_content(prompt)
    email_text = response.text.strip()
    
    # Optional: Remove markdown code blocks if present.
    if email_text.startswith("```") and email_text.endswith("```"):
        email_text = email_text[3:-3].strip()
    
    return email_text

def send_invite_email(name, recipient_email, meeting_link, jd):
    """
    Generate an email using the job description and send the invitation email.
    """
    subject = "Interview Invitation – AI Research Engineer Role"
    
    # Generate dynamic email content based on the candidate's name, job description, and meeting link.
    email_body = generate_email_content(name, jd, meeting_link)
    
    msg = MIMEMultipart()
    msg["From"] = EMAIL
    msg["To"] = recipient_email
    msg["Subject"] = subject
    
    msg.attach(MIMEText(email_body, "plain"))
    
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL, PASSWORD)
            server.sendmail(EMAIL, recipient_email, msg.as_string())
        print(f"✅ Email sent to {recipient_email}")
        return "Success"
    except Exception as e:
        print(f"❌ Failed to send email to {recipient_email}: {e}")
        return f"Failed: {e}"
