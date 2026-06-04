import re
from skills_data import SKILL_DB, JOB_ROLES


# -------------------------
# CLEAN TEXT
# -------------------------
def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9+.# ]', ' ', text)
    return text


# -------------------------
# EXTRACT SKILLS FROM RESUME
# -------------------------
def extract_skills(resume_text):
    text = clean_text(resume_text)

    found_skills = []

    for skill in SKILL_DB:
        if skill in text:
            found_skills.append(skill)

    return list(set(found_skills))


# -------------------------
# FIND MISSING SKILLS
# -------------------------
def find_missing_skills(found_skills, required_skills):
    missing = []

    for skill in required_skills:
        if skill not in found_skills:
            missing.append(skill)

    return missing


# -------------------------
# ATS SCORE CALCULATION
# -------------------------
def calculate_ats_score(found_skills, required_skills):
    if not required_skills:
        return 0

    match_count = len(found_skills)
    total_required = len(required_skills)

    score = (match_count / total_required) * 100
    return round(score, 2)


# -------------------------
# GENERATE SUGGESTIONS
# -------------------------
def generate_suggestions(missing_skills):
    if not missing_skills:
        return "Excellent! Your resume matches all required skills."

    return "Improve your profile by adding: " + ", ".join(missing_skills)


# -------------------------
# MAIN FUNCTION (USED IN app.py)
# -------------------------
def analyze_resume(resume_text, job_role="general"):

    job_role = job_role.lower().strip()

    # GET SKILLS FROM skills_data.py
    required_skills = JOB_ROLES.get(job_role, SKILL_DB)

    found_skills = extract_skills(resume_text)

    missing_skills = find_missing_skills(found_skills, required_skills)

    score = calculate_ats_score(found_skills, required_skills)

    suggestions = generate_suggestions(missing_skills)

    return {
        "ats_score": score,
        "matched_skills": found_skills,
        "missing_skills": missing_skills,
        "suggestions": suggestions,
        "job_role": job_role
    }