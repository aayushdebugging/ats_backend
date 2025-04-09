from scorer import get_resume_score

dummy_resume = "Experienced Python developer with 2 years of experience in data analytics and machine learning using Pandas, NumPy, and Scikit-learn. Built dashboards with Power BI."
jd = "Looking for a Data Analyst with experience in Python, SQL, Power BI, and strong communication skills."
skills = ["Python", "SQL", "Power BI", "Communication", "Tableau"]

result = get_resume_score(dummy_resume, jd, skills)
print(result)
