import sqlite3
from datetime import datetime

DB_NAME = "resume.db"


# -------------------------
# DATABASE CONNECTION
# -------------------------
def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


# -------------------------
# CREATE TABLES
# -------------------------
def create_tables():

    conn = get_connection()
    cursor = conn.cursor()

    # USERS TABLE
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        created_at TEXT
    )
    """)

    # RESUMES TABLE
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS resumes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        filename TEXT NOT NULL,
        uploaded_at TEXT,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
    """)

    # ANALYSIS TABLE
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS analysis (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        resume_id INTEGER,
        ats_score REAL,
        matched_skills TEXT,
        missing_skills TEXT,
        suggestions TEXT,
        job_role TEXT,
        created_at TEXT,
        FOREIGN KEY (user_id) REFERENCES users(id),
        FOREIGN KEY (resume_id) REFERENCES resumes(id)
    )
    """)

    conn.commit()
    conn.close()


# -------------------------
# USER FUNCTIONS
# -------------------------
def add_user(username, email, password):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO users
    (username, email, password, created_at)
    VALUES (?, ?, ?, ?)
    """, (
        username,
        email,
        password,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    conn.commit()
    conn.close()


def get_user_by_email(email):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE email = ?",
        (email,)
    )

    user = cursor.fetchone()

    conn.close()

    return user


# -------------------------
# RESUME FUNCTIONS
# -------------------------
def add_resume(user_id, filename):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO resumes
    (user_id, filename, uploaded_at)
    VALUES (?, ?, ?)
    """, (
        user_id,
        filename,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    resume_id = cursor.lastrowid

    conn.commit()
    conn.close()

    return resume_id


# -------------------------
# ANALYSIS FUNCTIONS
# -------------------------
def add_analysis(
    user_id,
    resume_id,
    ats_score,
    matched_skills,
    missing_skills,
    suggestions,
    job_role
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO analysis (
        user_id,
        resume_id,
        ats_score,
        matched_skills,
        missing_skills,
        suggestions,
        job_role,
        created_at
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        user_id,
        resume_id,
        ats_score,
        matched_skills,
        missing_skills,
        suggestions,
        job_role,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    conn.commit()
    conn.close()


# -------------------------
# USER HISTORY
# -------------------------
def get_history(user_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT *
    FROM analysis
    WHERE user_id = ?
    ORDER BY id DESC
    """, (user_id,))

    history = cursor.fetchall()

    conn.close()

    return history


# -------------------------
# ADMIN DASHBOARD
# -------------------------
def get_user_count():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM users")

    count = cursor.fetchone()[0]

    conn.close()

    return count


def get_resume_count():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM resumes")

    count = cursor.fetchone()[0]

    conn.close()

    return count


def get_analysis_count():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM analysis")

    count = cursor.fetchone()[0]

    conn.close()

    return count


def get_all_users():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT
        id,
        username,
        email,
        created_at
    FROM users
    ORDER BY id DESC
    """)

    users = cursor.fetchall()

    conn.close()

    return users


# -------------------------
# TEST DATABASE
# -------------------------
if __name__ == "__main__":

    create_tables()

    print("Database created successfully!")
    print("Database file:", DB_NAME)