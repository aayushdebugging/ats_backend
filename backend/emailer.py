# backend/emailer.py

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os

load_dotenv()

EMAIL = os.getenv("EMAIL_ADDRESS")
PASSWORD = os.getenv("EMAIL_PASSWORD")

def send_invite_email(name, recipient_email, meeting_link):
    subject = "Interview Invitation – AI Research Engineer Role"
    
    body = f"""
Hi {name},

Congratulations! Based on your resume evaluation, we are pleased to invite you to the next round of interviews for the AI Research Engineer position.

📅 Interview Link: {meeting_link}

Please confirm your availability by replying to this email.

Looking forward to speaking with you!

Best regards,  
Talent Acquisition Team
    """

    msg = MIMEMultipart()
    msg["From"] = EMAIL
    msg["To"] = recipient_email
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL, PASSWORD)
            server.sendmail(EMAIL, recipient_email, msg.as_string())
        print(f"✅ Email sent to {recipient_email}")
        return "Success"
    except Exception as e:
        print(f"❌ Failed to send email to {recipient_email}: {e}")
        return f"Failed: {e}"
