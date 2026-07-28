import json
from io import StringIO
from pathlib import Path
from uuid import uuid4

import pandas as pd
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from backend.csv_analyzer import analyze_dataframe
from backend.pipeline import clean_dataframe
from backend.session_store import SessionData, sessions


app = FastAPI(
    title="CSV Cleaning Agent API",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CleanRequest(BaseModel):
    session_id: str
    instruction: str


def create_preview(
    dataframe: pd.DataFrame,
    row_limit: int = 5,
) -> list[dict]:

    preview_json = dataframe.head(row_limit).to_json(
        orient="records",
        date_format="iso",
    )

    return json.loads(preview_json)


def create_dashboard_data(
    dataframe: pd.DataFrame,
) -> dict:

    analysis = analyze_dataframe(dataframe)

    total_missing = sum(
        analysis["missing_values"].values()
    )

    return {
        "stats": {
            "rows": analysis["row_count"],
            "columns": analysis["column_count"],
            "missing_values": total_missing,
            "duplicate_rows": analysis["duplicate_rows"],
        },
        "column_names": analysis["columns"],
        "missing_by_column": analysis["missing_values"],
        "preview": create_preview(dataframe),
    }


@app.get("/health")
def health_check():
    return {
        "status": "ok",
    }


@app.post("/upload")
def upload_csv(
    file: UploadFile = File(...),
):
    filename = file.filename or ""

    if Path(filename).suffix.lower() != ".csv":
        raise HTTPException(
            status_code=400,
            detail="Only CSV files are supported.",
        )

    try:
        dataframe = pd.read_csv(file.file)

    except pd.errors.EmptyDataError:
        raise HTTPException(
            status_code=400,
            detail="The CSV file is empty.",
        )

    except pd.errors.ParserError:
        raise HTTPException(
            status_code=400,
            detail="The CSV file could not be parsed.",
        )

    except UnicodeDecodeError:
        raise HTTPException(
            status_code=400,
            detail="The CSV file encoding is not supported.",
        )

    session_id = str(uuid4())

    sessions[session_id] = SessionData(
        dataframe=dataframe,
        filename=filename,
    )

    return {
        "session_id": session_id,
        "filename": filename,
        **create_dashboard_data(dataframe),
    }


@app.post("/clean")
def clean_csv(
    request: CleanRequest,
):
    session = sessions.get(request.session_id)

    if session is None:
        raise HTTPException(
            status_code=404,
            detail="Session not found.",
        )

    instruction = request.instruction.strip()

    if not instruction:
        raise HTTPException(
            status_code=400,
            detail="Cleaning instruction cannot be empty.",
        )

    try:
        (
            cleaned_dataframe,
            command,
            confidence,
            summary,
        ) = clean_dataframe(
            session.dataframe,
            instruction,
        )

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        )

    session.dataframe = cleaned_dataframe

    return {
        "session_id": request.session_id,
        "filename": session.filename,
        "command": command,
        "confidence": confidence,
        "summary": summary,
        **create_dashboard_data(cleaned_dataframe),
    }

@app.get("/download/{session_id}")
def download_csv(session_id: str):
    session = sessions.get(session_id)

    if session is None:
        raise HTTPException(
            status_code=404,
            detail="Session not found.",
        )

    csv_buffer = StringIO()

    session.dataframe.to_csv(
        csv_buffer,
        index=False,
    )

    csv_buffer.seek(0)

    original_name = Path(session.filename)

    download_name = (
        f"cleaned_{original_name.stem}.csv"
    )

    return StreamingResponse(
        csv_buffer,
        media_type="text/csv",
        headers={
            "Content-Disposition":
                f'attachment; filename="{download_name}"'
        },
    )