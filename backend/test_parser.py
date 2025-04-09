from resume_parser import extract_resume_data

with open("Nandini_Bhalla_22cs22002_IDD (1) (1).pdf", "rb") as f:
    text, data = extract_resume_data(f.read())

    print("✅ Extracted Resume Data:")
    print("Name:", data.get("name", "Not found"))
    print("Email:", data.get("email", "Not found"))
    print("Phone:", data.get("phone", "Not found"))
    print("LinkedIn:", data.get("linkedin", "Not found"))
    print("Experience:", data.get("total_experience", "Not found"))

    print("\nSkills:", data.get("skills", []))
    print("Technical Skills:", data.get("technical_skills", []))
    print("Certifications:", data.get("certifications", []))
    print("Projects:", data.get("projects", []))
