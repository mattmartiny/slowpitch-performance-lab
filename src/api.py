import os
import tempfile
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware

from src.analyzer import analyze_team

app = FastAPI(title="Slowpitch Performance Lab API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://slowpitchlab.mattmartiny.com",
    ],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def health_check():
    return {"status": "ok"}


@app.post("/analyze")
async def analyze_csv(
    file: UploadFile = File(...),
    league_name: str = Form("Uploaded Team"),
    league_code: str = Form("UPL"),
):
    suffix = os.path.splitext(file.filename or "")[1] or ".csv"

    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp:
        temp.write(await file.read())
        temp_path = temp.name

    try:
        result = analyze_team(temp_path, league_name, league_code)
        return result
    finally:
        os.remove(temp_path)