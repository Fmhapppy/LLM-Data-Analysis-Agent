from fastapi import FastAPI, UploadFile, File
import os
import tempfile

from data_processor import load_data
from data_cleaner import clean_data
from ml_model import train_regression_model


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


@app.post("/analyze")
async def analyze_file(
    file: UploadFile = File(...),
    target_column: str = "final_score"
):
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
        # 1. Load data
        df = load_data(temp_path)

        # 2. Clean data
        cleaned_df = clean_data(df)

        # 3. Basic data information
        data_info = {
            "original_rows": len(df),
            "original_columns": len(df.columns),
            "cleaned_rows": len(cleaned_df),
            "cleaned_columns": len(cleaned_df.columns),
            "columns": cleaned_df.columns.tolist()
        }

        # 4. Machine Learning
        ml_result = train_regression_model(
            cleaned_df,
            target_column
        )

        # 5. Return analysis result
        return {
            "filename": file.filename,
            "data_info": data_info,
            "machine_learning": ml_result
        }

    finally:
        # Delete temporary file
        if os.path.exists(temp_path):
            os.remove(temp_path)
