import os
import shutil
from pathlib import Path

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from data_processor import load_data
from data_cleaner import clean_data
from eda import perform_eda
from ml_model import train_regression_model
from visualizations import generate_visualizations
from llm_analyzer import generate_ai_analysis


# =========================
# 基础配置
# =========================

BASE_DIR = Path(__file__).resolve().parent
UPLOAD_DIR = BASE_DIR / "uploads"
OUTPUT_DIR = BASE_DIR / "outputs"

UPLOAD_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)


# =========================
# FastAPI
# =========================

app = FastAPI(
    title="LLM Data Analysis Agent",
    description="AI-powered data analysis and visualization system",
    version="1.0.0"
)


# =========================
# CORS
# =========================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================
# 静态文件
# =========================

app.mount(
    "/outputs",
    StaticFiles(directory=str(OUTPUT_DIR)),
    name="outputs"
)


# =========================
# 根路径
# =========================

@app.get("/")
def root():
    return {
        "message": "LLM Data Analysis Agent API is running.",
        "version": "1.0.0"
    }


# =========================
# 上传文件
# =========================

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """
    上传 CSV / Excel 数据文件
    """

    allowed_extensions = {
        ".csv",
        ".xlsx",
        ".xls"
    }

    file_extension = Path(file.filename).suffix.lower()

    if file_extension not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail="只支持 CSV、XLSX、XLS 文件。"
        )

    file_path = UPLOAD_DIR / file.filename

    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        return {
            "success": True,
            "filename": file.filename,
            "file_path": str(file_path)
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"文件上传失败：{str(e)}"
        )


# =========================
# 数据分析
# =========================

@app.post("/analyze")
async def analyze_file(
    file: UploadFile = File(...),
    target_column: str = "final_score"
):
    """
    完整数据分析流程：

    1. 保存数据
    2. 加载数据
    3. 数据清洗
    4. EDA
    5. 机器学习
    6. 生成可视化
    7. DeepSeek AI 分析
    8. 返回完整分析结果
    """

    allowed_extensions = {
        ".csv",
        ".xlsx",
        ".xls"
    }

    file_extension = Path(file.filename).suffix.lower()

    if file_extension not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail="只支持 CSV、XLSX、XLS 文件。"
        )

    # =========================
    # 1. 保存上传文件
    # =========================

    file_path = UPLOAD_DIR / file.filename

    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"文件保存失败：{str(e)}"
        )

    try:

        # =========================
        # 2. 加载数据
        # =========================

        df = load_data(str(file_path))

        if df.empty:
            raise ValueError("上传的数据集为空。")

        original_shape = df.shape

        # =========================
        # 3. 数据清洗
        # =========================

        cleaned_df, cleaning_report = clean_data(
            df,
            return_report=True
        )

        if cleaned_df.empty:
            raise ValueError("数据清洗后没有剩余有效数据。")

        cleaned_shape = cleaned_df.shape

        # =========================
        # 4. EDA
        # =========================

        eda_result = perform_eda(cleaned_df)

        # =========================
        # 5. 机器学习
        # =========================

        ml_result = train_regression_model(
            cleaned_df,
            target_column
        )

        # =========================
        # 6. 数据集基本信息
        # =========================

        data_info = {
            "filename": file.filename,

            "original_rows": int(original_shape[0]),
            "original_columns": int(original_shape[1]),

            "cleaned_rows": int(cleaned_shape[0]),
            "cleaned_columns": int(cleaned_shape[1]),

            "columns": list(cleaned_df.columns),

            "target_column": target_column,

            "data_types": {
                column: str(dtype)
                for column, dtype in cleaned_df.dtypes.items()
            }
        }

        # =========================
        # 7. 生成可视化
        # =========================

        visualization_result = generate_visualizations(
            cleaned_df,
            ml_result,
            output_dir=str(OUTPUT_DIR)
        )

        # =========================
        # 8. 转换图片路径
        # =========================

        visualization_urls = {}

        for key, path in visualization_result.items():

            filename = Path(path).name

            visualization_urls[key] = (
                f"/outputs/{filename}"
            )

        # =========================
        # 9. DeepSeek AI 分析
        # =========================

        ai_analysis = generate_ai_analysis(
            data_info,
            eda_result,
            ml_result,
            cleaning_report
        )

        # =========================
        # 10. 返回结果
        # =========================

        return {
            "success": True,

            "filename": file.filename,

            "data_shape": {
                "original": list(original_shape),
                "cleaned": list(cleaned_shape)
            },

            "columns": list(cleaned_df.columns),

            "target_column": target_column,

            "cleaning_report": cleaning_report,

            "eda": eda_result,

            "machine_learning": ml_result,

            "visualizations": visualization_urls,

            "ai_analysis": ai_analysis
        }

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"数据分析失败：{str(e)}"
        )


# =========================
# 本地运行
# =========================

if __name__ == "__main__":

    import uvicorn

    uvicorn.run(
        "api:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )