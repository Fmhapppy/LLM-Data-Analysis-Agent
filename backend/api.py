from fastapi import FastAPI, UploadFile, File
import pandas as pd
import os
import tempfile

from data_processor import load_data


app = FastAPI(
    title="LLM Data Analysis Agent",
    description="An intelligent data analysis backend.",
    version="1.0.0"
)


@app.get("/")
def root():
    return {
        "message": "LLM Data Analysis Agent is running."
    }


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    # Create a temporary file
    suffix = os.path.splitext(file.filename)[1]

    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=suffix
    ) as temp_file:

        contents = await file.read()
        temp_file.write(contents)
        temp_path = temp_file.name

    try:
        # Load the uploaded dataset
        df = load_data(temp_path)

        return {
            "filename": file.filename,
            "rows": len(df),
            "columns": len(df.columns),
            "column_names": df.columns.tolist()
        }

    finally:
        # Delete temporary file
        if os.path.exists(temp_path):
            os.remove(temp_path)
