# -----------------------------------
# CENTRAL SKILLS + JOB ROLES DATABASE
# -----------------------------------

SKILL_DB = [
    "python", "java", "c++", "c#",
    "html", "css", "javascript",
    "flask", "django", "fastapi",
    "sql", "mysql", "postgresql",
    "git", "github",
    "api", "rest api",
    "machine learning", "deep learning",
    "pandas", "numpy", "tensorflow",
    "keras", "docker", "aws",
    "linux"
]


# -----------------------------------
# JOB ROLE → REQUIRED SKILLS MAP
# -----------------------------------
JOB_ROLES = {
    "general": SKILL_DB,

    "web developer": [
        "html", "css", "javascript", "flask", "sql", "git"
    ],

    "frontend developer": [
        "html", "css", "javascript", "react", "git"
    ],

    "backend developer": [
        "python", "flask", "sql", "api", "git"
    ],

    "full stack developer": [
        "html", "css", "javascript", "python", "flask", "sql", "api", "git"
    ],

    "data analyst": [
        "python", "sql", "pandas", "numpy", "excel"
    ],

    "data scientist": [
        "python", "pandas", "numpy", "machine learning", "tensorflow"
    ],

    "machine learning engineer": [
        "python", "numpy", "pandas", "machine learning", "deep learning", "tensorflow"
    ],

    "devops engineer": [
        "linux", "docker", "aws", "git"
    ],
    "python developer": [
        "python", "flask", "django", "sql", "api", "git"
    ],

    "java developer": [
        "java", "spring", "hibernate", "sql", "git"
    ],

    "c++ developer": [
        "c++", "data structures", "algorithms", "oop"
    ],

    "ai engineer": [
        "python", "machine learning", "deep learning", "tensorflow"
    ],

    "android developer": [
        "java", "kotlin", "android studio", "xml"
    ]
}