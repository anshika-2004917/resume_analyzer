import pdfplumber
import docx2txt
import os


# -----------------------
# EXTRACT TEXT FROM PDF
# -----------------------
def extract_text_from_pdf(file_path):
    text = ""

    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""

    return text


# -----------------------
# EXTRACT TEXT FROM DOCX
# -----------------------
def extract_text_from_docx(file_path):
    return docx2txt.process(file_path)


# -----------------------
# MAIN FUNCTION
# -----------------------
def extract_resume_text(file_path):
    
    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".pdf":
        return extract_text_from_pdf(file_path)

    elif ext == ".docx":
        return extract_text_from_docx(file_path)

    else:
        return ""