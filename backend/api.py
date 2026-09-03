import os
import shutil

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from data_processor import load_data
from data_cleaner import clean_data
from eda import perform_eda
from ml_model import train_regression_model
from llm_analyzer import generate_ai_analysis
from visualizations import generate_visualizations


# ==========================================
# FastAPI 应用
# ==========================================

app = FastAPI(
    title="LLM Data Analysis Agent",
    description="AI-powered data analysis API",
    version="1.0.0"
)


# ==========================================
# CORS 跨域配置
# ==========================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==========================================
# 文件目录
# ==========================================

UPLOAD_DIR = "uploads"
OUTPUT_DIR = "outputs"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)


# ==========================================
# 静态文件访问
# ==========================================
# 例如：
# http://127.0.0.1:8000/outputs/correlation_heatmap.png

app.mount(
    "/outputs",
    StaticFiles(directory=OUTPUT_DIR),
    name="outputs"
)


# ==========================================
# 根路径
# ==========================================

@app.get("/")
def root():
    return {
        "message": "LLM Data Analysis Agent is running."
    }


# ==========================================
# 上传文件接口
# ==========================================

@app.post("/upload")
async def upload_file(
    file: UploadFile = File(...)
):
    try:

        file_path = os.path.join(
            UPLOAD_DIR,
            file.filename
        )

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(
                file.file,
                buffer
            )

        return {
            "filename": file.filename,
            "file_path": file_path
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# ==========================================
# 数据分析接口
# ==========================================

@app.post("/analyze")
async def analyze_file(
    file: UploadFile = File(...),
    target_column: str = "final_score"
):

    try:

        # --------------------------------------
        # 1. 保存上传文件
        # --------------------------------------

        file_path = os.path.join(
            UPLOAD_DIR,
            file.filename
        )

        with open(file_path, "wb") as buffer:

            shutil.copyfileobj(
                file.file,
                buffer
            )


        # --------------------------------------
        # 2. 读取数据
        # --------------------------------------

        df = load_data(
            file_path
        )


        # --------------------------------------
        # 3. 数据清洗
        # --------------------------------------

        cleaned_df = clean_data(
            df
        )


        # --------------------------------------
        # 4. EDA
        # --------------------------------------

        eda_result = perform_eda(
            cleaned_df
        )


        # --------------------------------------
        # 5. 机器学习
        # --------------------------------------

        ml_result = train_regression_model(
            cleaned_df,
            target_column
        )


        # --------------------------------------
        # 6. 数据基本信息
        # --------------------------------------

        data_info = {

            "original_rows": int(
                df.shape[0]
            ),

            "original_columns": int(
                df.shape[1]
            ),

            "cleaned_rows": int(
                cleaned_df.shape[0]
            ),

            "cleaned_columns": int(
                cleaned_df.shape[1]
            ),

            "columns": (
                cleaned_df
                .columns
                .tolist()
            )
        }


        # --------------------------------------
        # 7. 生成可视化图表
        # --------------------------------------

        visualization_result = (
            generate_visualizations(
                cleaned_df,
                ml_result,
                OUTPUT_DIR
            )
        )


        # --------------------------------------
        # 8. 转换图片路径为 HTTP 地址
        # --------------------------------------

        visualization_urls = {}

        for key, path in visualization_result.items():

            filename = os.path.basename(
                path
            )

            visualization_urls[key] = (
                f"/outputs/{filename}"
            )


        # --------------------------------------
        # 9. DeepSeek AI 分析
        # --------------------------------------

        ai_analysis = generate_ai_analysis(
            data_info,
            eda_result,
            ml_result
        )


        # --------------------------------------
        # 10. 返回完整结果
        # --------------------------------------

        return {

            "filename": file.filename,

            "data_info": data_info,

            "eda": eda_result,

            "machine_learning": ml_result,

            "visualizations": visualization_urls,

            "ai_analysis": ai_analysis

        }


    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )