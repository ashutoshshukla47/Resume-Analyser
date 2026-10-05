import os
import tempfile
from pathlib import Path

import pandas as pd
from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from pdfminer.high_level import extract_text as pdf_extract_text

from add_to_df import add_job_entry
from analyser import anaylse
from resume_parser import user_skill

BASE_DIR = Path(__file__).resolve().parent
JOB_DATA_PATH = BASE_DIR / "sample data" / "Job_description.csv"

app = FastAPI(title="Resume Analyzer API")


def read_uploaded_resume_text(file: UploadFile, data: bytes) -> str:
    file_extension = file.filename.rsplit(".", 1)[-1].lower() if file.filename else ""

    if file_extension == "txt":
        return data.decode("utf-8", errors="ignore")

    if file_extension == "docx":
        with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as temp_file:
            temp_file.write(data)
            temp_path = temp_file.name

        try:
            import docx2txt

            return docx2txt.process(temp_path) or ""
        finally:
            if os.path.exists(temp_path):
                os.unlink(temp_path)

    if file_extension == "pdf":
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
            temp_file.write(data)
            temp_path = temp_file.name

        try:
            return pdf_extract_text(temp_path) or ""
        finally:
            if os.path.exists(temp_path):
                os.unlink(temp_path)

    return ""


@app.get("/")
def health():
    return {"status": "ok", "service": "resume-analyzer-api"}


@app.post("/upload-resume")
async def upload_resume(file: UploadFile = File(...)):
    if not file.filename or file.filename.rsplit(".", 1)[-1].lower() not in {"pdf", "docx", "txt"}:
        raise HTTPException(status_code=400, detail="Unsupported file type. Use PDF, DOCX, or TXT.")

    data = await file.read()
    text = read_uploaded_resume_text(file, data)

    if not text or not text.strip():
        raise HTTPException(status_code=400, detail="Unable to read resume content.")

    skills = sorted(set(user_skill(text)))
    return {
        "status": "success",
        "file_name": file.filename,
        "skills": skills,
        "extracted_text_length": len(text)
    }


@app.post("/match-jobs")
async def match_jobs(file: UploadFile = File(...)):
    if not file.filename or file.filename.rsplit(".", 1)[-1].lower() not in {"pdf", "docx", "txt"}:
        raise HTTPException(status_code=400, detail="Unsupported file type. Use PDF, DOCX, or TXT.")

    data = await file.read()
    text = read_uploaded_resume_text(file, data)

    if not text or not text.strip():
        raise HTTPException(status_code=400, detail="Unable to read resume content.")

    user_skills = set(user_skill(text))
    if not JOB_DATA_PATH.exists():
        raise HTTPException(status_code=404, detail="Job dataset not found.")

    df = pd.read_csv(JOB_DATA_PATH)
    matches = anaylse(df, user_skills)

    formatted_matches = [
        {
            "score": round(float(match[0]), 2),
            "job_id": int(match[1]),
            "job_title": str(match[2]),
            "missing_skills": sorted([str(skill) for skill in match[3]])
        }
        for match in matches
    ]

    return {
        "status": "success",
        "file_name": file.filename,
        "detected_skills": sorted(user_skills),
        "matches": formatted_matches
    }


@app.post("/add-job")
async def add_job(job_title: str = Form(...), job_description: str = Form(...)):
    if not job_title.strip() or not job_description.strip():
        raise HTTPException(status_code=400, detail="Job title and description are required.")

    result = add_job_entry(job_title.strip(), job_description.strip())
    return {
        "status": "success" if result else "failed",
        "message": "Job added successfully." if result else "Could not add job.",
        "job_title": job_title.strip()
    }