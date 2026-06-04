from flask import Flask, render_template, request, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash
import os

from database import (
    create_tables,
    add_user,
    get_user_by_email,
    add_resume,
    add_analysis,
    get_history,
    get_user_count,
    get_resume_count,
    get_analysis_count,
    get_all_users
)

from ats import analyze_resume
from utils.file_parser import extract_resume_text

# ==========================
# APP CONFIG
# ==========================

app = Flask(__name__)
app.secret_key = "resume_analyzer_secret_key"

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Create database tables
create_tables()

# ==========================
# HOME PAGE
# ==========================

@app.route("/")
def home():
    return render_template("index.html")


# ==========================
# REGISTER
# ==========================

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form["username"].strip()
        email = request.form["email"].strip().lower()
        password = request.form["password"]

        existing_user = get_user_by_email(email)

        if existing_user:
            return "Email already registered!"

        hashed_password = generate_password_hash(password)

        add_user(
            username,
            email,
            hashed_password
        )

        return redirect("/login")

    return render_template("register.html")


# ==========================
# LOGIN
# ==========================

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"].strip().lower()
        password = request.form["password"]

        user = get_user_by_email(email)

        if user and check_password_hash(
            user["password"],
            password
        ):

            session["user_id"] = user["id"]
            session["username"] = user["username"]

            return redirect("/dashboard")

        return "Invalid Email or Password"

    return render_template("login.html")


# ==========================
# LOGOUT
# ==========================

@app.route("/logout")
def logout():

    session.clear()

    return redirect("/")


# ==========================
# USER DASHBOARD
# ==========================

@app.route("/dashboard")
def dashboard():

    if "user_id" not in session:
        return redirect("/login")

    return render_template(
        "dashboard.html",
        username=session["username"]
    )


# ==========================
# ADMIN DASHBOARD
# ==========================

@app.route("/admin")
def admin():

    if "user_id" not in session:
        return redirect("/login")

    return render_template(
        "admin.html",
        user_count=get_user_count(),
        resume_count=get_resume_count(),
        analysis_count=get_analysis_count(),
        users=get_all_users()
    )


# ==========================
# UPLOAD RESUME
# ==========================

@app.route("/upload", methods=["GET", "POST"])
def upload():

    if "user_id" not in session:
        return redirect("/login")

    if request.method == "POST":

        if "resume" not in request.files:
            return "No file uploaded"

        file = request.files["resume"]

        if file.filename == "":
            return "Please select a file"

        job_role = request.form["job_role"]

        filepath = os.path.join(
            UPLOAD_FOLDER,
            file.filename
        )

        file.save(filepath)

        # Extract text from PDF/DOCX
        resume_text = extract_resume_text(filepath)

        # ATS Analysis
        result = analyze_resume(
            resume_text,
            job_role
        )

        # Save resume
        resume_id = add_resume(
            session["user_id"],
            file.filename
        )

        # Save ATS analysis
        add_analysis(
            session["user_id"],
            resume_id,
            result["ats_score"],
            ",".join(result["matched_skills"]),
            ",".join(result["missing_skills"]),
            result["suggestions"],
            job_role
        )

        return render_template(
            "result.html",
            ats_score=result["ats_score"],
            matched_skills=result["matched_skills"],
            missing_skills=result["missing_skills"],
            suggestions=result["suggestions"]
        )

    return render_template("upload.html")


# ==========================
# HISTORY
# ==========================

@app.route("/history")
def history():

    if "user_id" not in session:
        return redirect("/login")

    history_data = get_history(
        session["user_id"]
    )

    return render_template(
        "history.html",
        history=history_data
    )


# ==========================
# RUN APP
# ==========================

if __name__ == "__main__":
    app.run(debug=True)