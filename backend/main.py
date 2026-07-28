import json
from pathlib import Path
from uuid import uuid4

import pandas as pd
from fastapi import FastAPI, HTTPException, UploadFile

from backend.csv_analyzer import analyze_dataframe
from backend.session_store import SessionData, sessions


app = FastAPI(
    title="CSV Cleaning Agent API",
    version="1.0.0",
)


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
def upload_csv(file: UploadFile):
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