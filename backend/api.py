import os
import shutil
from datetime import datetime

from fastapi import (
    FastAPI,
    File,
    Form,
    UploadFile,
    HTTPException,
)

from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from data_processor import load_data
from data_cleaner import clean_data
from eda import perform_eda
from ml_model import train_regression_model
from visualizations import generate_visualizations
from llm_analyzer import generate_ai_analysis
from analysis_agent import create_analysis_agent

from agent_evaluation import (
    build_evaluation_questions,
    evaluate_agent_response,
    summarize_evaluation,
)

from pdf_report import generate_pdf_report


# =========================================================
# FastAPI
# =========================================================

app = FastAPI(
    title="LLM Data Analysis Agent",
    description="AI-powered Data Science Platform",
    version="1.0.0",
)


# =========================================================
# CORS
# =========================================================

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


# =========================================================
# Directories
# =========================================================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

UPLOAD_DIR = os.path.join(
    BASE_DIR,
    "uploads",
)

OUTPUT_DIR = os.path.join(
    BASE_DIR,
    "outputs",
)


os.makedirs(
    UPLOAD_DIR,
    exist_ok=True,
)

os.makedirs(
    OUTPUT_DIR,
    exist_ok=True,
)


# =========================================================
# Static files
# =========================================================

app.mount(
    "/outputs",
    StaticFiles(
        directory=OUTPUT_DIR
    ),
    name="outputs",
)


# =========================================================
# Health Check
# =========================================================

@app.get("/")
def root():

    return {
        "success": True,
        "message": (
            "LLM Data Analysis Agent API "
            "is running."
        ),
    }


# =========================================================
# 自动识别字段
# =========================================================

@app.post("/inspect")
async def inspect_file(
    file: UploadFile = File(...)
):
    """
    上传数据文件后，仅进行字段识别。
    不进行完整的数据分析。
    """

    filename = file.filename or ""

    # -----------------------------------------------------
    # 检查文件格式
    # -----------------------------------------------------

    if not filename.lower().endswith(
        (
            ".csv",
            ".xlsx",
            ".xls",
        )
    ):

        raise HTTPException(
            status_code=400,
            detail=(
                "仅支持 CSV、XLSX、XLS 文件"
            ),
        )

    file_path = os.path.join(
        UPLOAD_DIR,
        filename,
    )

    try:

        # -------------------------------------------------
        # 保存文件
        # -------------------------------------------------

        with open(
            file_path,
            "wb",
        ) as buffer:

            shutil.copyfileobj(
                file.file,
                buffer,
            )

        # -------------------------------------------------
        # 读取数据
        # -------------------------------------------------

        df = load_data(
            file_path
        )

        # -------------------------------------------------
        # 获取字段
        # -------------------------------------------------

        columns = (
            df.columns.tolist()
        )

        numeric_columns = (
            df.select_dtypes(
                include=["number"]
            )
            .columns
            .tolist()
        )

        categorical_columns = (
            df.select_dtypes(
                exclude=["number"]
            )
            .columns
            .tolist()
        )

        # -------------------------------------------------
        # 自动推荐预测目标
        # -------------------------------------------------

        recommended_target = None

        target_keywords = [
            "target",
            "label",
            "score",
            "result",
            "outcome",
            "final",
            "price",
            "sales",
            "revenue",
            "y",
        ]

        # -------------------------------------------------
        # 优先匹配常见目标字段
        # -------------------------------------------------

        for column in numeric_columns:

            column_lower = (
                column.lower()
            )

            if any(
                keyword in column_lower
                for keyword in target_keywords
            ):

                recommended_target = (
                    column
                )

                break

        # -------------------------------------------------
        # 如果没有匹配
        # 使用最后一个数值字段
        # -------------------------------------------------

        if (
            recommended_target is None
            and numeric_columns
        ):

            recommended_target = (
                numeric_columns[-1]
            )

        return {

            "success": True,

            "filename": filename,

            "rows": int(
                len(df)
            ),

            "columns": columns,

            "numeric_columns": (
                numeric_columns
            ),

            "categorical_columns": (
                categorical_columns
            ),

            "recommended_target": (
                recommended_target
            ),
        }

    except HTTPException:

        raise

    except Exception as e:

        import traceback

        traceback.print_exc()

        raise HTTPException(
            status_code=500,
            detail=str(e),
        )


# =========================================================
# 完整数据分析
# =========================================================

@app.post("/analyze")
async def analyze(

    file: UploadFile = File(...),

    target_column: str = Form(...),

):

    filename = file.filename or ""

    # -----------------------------------------------------
    # 检查文件格式
    # -----------------------------------------------------

    if not filename.lower().endswith(
        (
            ".csv",
            ".xlsx",
            ".xls",
        )
    ):

        raise HTTPException(
            status_code=400,
            detail=(
                "仅支持 CSV、XLSX、XLS 文件"
            ),
        )

    file_path = os.path.join(
        UPLOAD_DIR,
        filename,
    )

    try:

        # =================================================
        # 1. 保存上传文件
        # =================================================

        with open(
            file_path,
            "wb",
        ) as buffer:

            shutil.copyfileobj(
                file.file,
                buffer,
            )

        print(
            "\n" + "=" * 70
        )

        print(
            "LLM DATA ANALYSIS AGENT"
        )

        print(
            "=" * 70
        )

        print(
            f"文件：{filename}"
        )

        # =================================================
        # 2. 加载数据
        # =================================================

        print(
            "\n[1/10] 正在读取数据..."
        )

        df = load_data(
            file_path
        )

        original_rows = len(df)

        original_columns = len(
            df.columns
        )

        original_columns_list = (
            df.columns.tolist()
        )

        print(
            f"原始数据："
            f"{original_rows} 行 × "
            f"{original_columns} 列"
        )

        # =================================================
        # 3. 检查目标字段
        # =================================================

        print(
            "\n[2/10] 检查预测目标..."
        )

        if target_column not in df.columns:

            raise HTTPException(
                status_code=400,
                detail=(
                    f"预测目标字段 "
                    f"'{target_column}' "
                    f"不存在。"
                    f"当前字段："
                    f"{', '.join(df.columns.tolist())}"
                ),
            )

        print(
            f"预测目标："
            f"{target_column}"
        )

        # =================================================
        # 4. 数据清洗
        # =================================================

        print(
            "\n[3/10] 正在进行数据清洗..."
        )

        (
            cleaned_df,
            cleaning_report,
        ) = clean_data(
            df,
            return_report=True,
        )

        print(
            f"清洗后数据："
            f"{len(cleaned_df)} 行 × "
            f"{len(cleaned_df.columns)} 列"
        )

        print(
            f"删除重复记录："
            f"{cleaning_report.get('duplicate_rows_removed', 0)}"
        )

        print(
            f"原始缺失值："
            f"{cleaning_report.get('original_missing_values', 0)}"
        )

        print(
            f"剩余缺失值："
            f"{cleaning_report.get('remaining_missing_values', 0)}"
        )

        # =================================================
        # 5. EDA
        # =================================================

        print(
            "\n[4/10] 正在进行 EDA..."
        )

        eda_result = perform_eda(
            cleaned_df
        )

        print(
            "EDA 完成"
        )

        # =================================================
        # 6. Machine Learning
        # =================================================

        print(
            "\n[5/10] 正在训练机器学习模型..."
        )

        ml_result = (
            train_regression_model(
                cleaned_df,
                target_column,
            )
        )

        print(
            "机器学习模型训练完成"
        )

        print(
            f"MAE: "
            f"{ml_result.get('mae', 0):.4f}"
        )

        print(
            f"RMSE: "
            f"{ml_result.get('rmse', 0):.4f}"
        )

        if ml_result.get("r2") is not None:

            print(
                f"R²: "
                f"{ml_result.get('r2', 0):.4f}"
            )

        if ml_result.get("best_model"):

            print(
                f"最佳模型："
                f"{ml_result.get('best_model')}"
            )

        # =================================================
        # 7. Visualization
        # =================================================

        print(
            "\n[6/10] 正在生成可视化..."
        )

        visualization_result = (
            generate_visualizations(
                cleaned_df,
                ml_result,
                OUTPUT_DIR,
            )
        )

        print(
            "可视化生成完成"
        )

        print(
            visualization_result
        )

        # =================================================
        # 8. AI Analysis
        # =================================================

        print(
            "\n[7/10] 正在生成 AI 分析报告..."
        )

        data_info = {

            "filename": filename,

            "original_rows": (
                original_rows
            ),

            "cleaned_rows": (
                len(cleaned_df)
            ),

            "original_columns": (
                original_columns
            ),

            "cleaned_columns": (
                len(cleaned_df.columns)
            ),

            "columns": (
                cleaned_df.columns.tolist()
            ),

            "target_column": (
                target_column
            ),
        }

        ai_analysis = (
            generate_ai_analysis(
                data_info=data_info,
                eda_result=eda_result,
                machine_learning=ml_result,
                cleaning_report=cleaning_report,
            )
        )

        print(
            "普通 AI 分析报告生成完成"
        )

        # =================================================
        # 8.5 Analysis Agent
        # =================================================

        print(
            "\n[8/10] 正在启动 Analysis Agent..."
        )

        print(
            "Agent 正在综合："
            "数据质量 + EDA + 特征关系 + ML 模型"
        )

        analysis_agent_result = (
            create_analysis_agent(
                columns=(
                    cleaned_df.columns.tolist()
                ),

                cleaning_report=(
                    cleaning_report
                ),

                eda_result=(
                    eda_result
                ),

                machine_learning=(
                    ml_result
                ),
            )
        )

        print(
            "Analysis Agent 分析完成"
        )

        print(
            "----------------------------------------"
        )

        print(
            "Agent 分析结果："
        )

        print(
            analysis_agent_result
        )

        print(
            "----------------------------------------"
        )

        # =================================================
        # 8.6 Agent Evaluation
        # =================================================

        print(
            "\n[9/10] 正在进行 Agent Evaluation..."
        )

        # -------------------------------------------------
        # 构建 Evaluation 测试题
        # -------------------------------------------------

        evaluation_input = {

            "machine_learning": (
                ml_result
            ),

            "eda": (
                eda_result
            ),

            "cleaning_report": (
                cleaning_report
            ),

            "target_column": (
                target_column
            ),

            "sample_count": (
                len(cleaned_df)
            ),
        }

        evaluation_questions = (
            build_evaluation_questions(
                evaluation_input
            )
        )

        print(
            f"Evaluation 测试题数量："
            f"{len(evaluation_questions)}"
        )

        # -------------------------------------------------
        # 将 Agent 输出转换成文本
        # -------------------------------------------------

        agent_answer_text = str(
            analysis_agent_result
        )

        # -------------------------------------------------
        # 逐题进行 Evaluation
        # -------------------------------------------------

        evaluation_results = []

        for question in evaluation_questions:

            evaluation_result = (
                evaluate_agent_response(
                    question,
                    agent_answer_text,
                )
            )

            evaluation_results.append(
                evaluation_result
            )

        # -------------------------------------------------
        # 汇总 Evaluation 指标
        # -------------------------------------------------

        evaluation_summary = (
            summarize_evaluation(
                evaluation_results
            )
        )

        # -------------------------------------------------
        # 打印 Evaluation Summary
        # -------------------------------------------------

        print(
            "----------------------------------------"
        )

        print(
            "Agent Evaluation Results"
        )

        print(
            "----------------------------------------"
        )

        print(
            f"总体准确率："
            f"{evaluation_summary['overall_accuracy']}%"
        )

        print(
            f"事实准确率："
            f"{evaluation_summary['fact_accuracy']}%"
        )

        print(
            f"数值准确率："
            f"{evaluation_summary['numerical_accuracy']}%"
        )

        print(
            f"因果推理准确率："
            f"{evaluation_summary['causal_reasoning_accuracy']}%"
        )

        print(
            f"潜在幻觉率："
            f"{evaluation_summary['hallucination_rate']}%"
        )

        print(
            f"正确题数："
            f"{evaluation_summary['correct_questions']}/"
            f"{evaluation_summary['total_questions']}"
        )

        print(
            "----------------------------------------"
        )

        # -------------------------------------------------
        # 打印每道题
        # -------------------------------------------------

        for item in evaluation_results:

            status = (
                "✓"
                if item.get("correct")
                else "✗"
            )

            print(
                f"[{status}] "
                f"Q{item.get('question_id')}: "
                f"{item.get('question')}"
            )

        print(
            "----------------------------------------"
        )

        # =================================================
        # 10. 生成 PDF
        # =================================================

        print(
            "\n[10/10] 正在生成 PDF 报告..."
        )

        # -------------------------------------------------
        # 当前时间
        # -------------------------------------------------

        timestamp = (
            datetime.now()
            .strftime(
                "%Y%m%d_%H%M%S"
            )
        )

        # -------------------------------------------------
        # 原始文件名去掉扩展名
        # -------------------------------------------------

        base_filename = (
            os.path.splitext(
                filename
            )[0]
        )

        # -------------------------------------------------
        # 防止文件名包含特殊字符
        # -------------------------------------------------

        safe_filename = "".join(
            char
            for char in base_filename
            if char.isalnum()
            or char in (
                "_",
                "-",
            )
        )

        if not safe_filename:

            safe_filename = (
                "data_analysis"
            )

        # -------------------------------------------------
        # PDF 文件名
        # -------------------------------------------------

        pdf_filename = (
            f"{safe_filename}_analysis_"
            f"{timestamp}.pdf"
        )

        # -------------------------------------------------
        # PDF 实际保存路径
        # -------------------------------------------------

        pdf_path = os.path.join(
            OUTPUT_DIR,
            pdf_filename,
        )

        # -------------------------------------------------
        # 生成 PDF
        # -------------------------------------------------

        try:

            generate_pdf_report(

                output_path=pdf_path,

                filename=filename,

                data_shape={
                    "original": [
                        original_rows,
                        original_columns,
                    ],

                    "cleaned": [
                        len(cleaned_df),
                        len(
                            cleaned_df.columns
                        ),
                    ],
                },

                columns=(
                    original_columns_list
                ),

                cleaning_report=(
                    cleaning_report
                ),

                eda_result=(
                    eda_result
                ),

                machine_learning=(
                    ml_result
                ),

                visualizations=(
                    visualization_result
                ),

                ai_analysis=(
                    ai_analysis
                ),
            )

        except Exception as pdf_error:

            import traceback

            print(
                "\n" + "=" * 70
            )

            print(
                "PDF 生成失败"
            )

            print(
                "=" * 70
            )

            traceback.print_exc()

            print(
                "=" * 70 + "\n"
            )

            raise HTTPException(
                status_code=500,
                detail=(
                    "数据分析成功，但 PDF "
                    "报告生成失败："
                    f"{str(pdf_error)}"
                ),
            )

        # =================================================
        # PDF URL
        # =================================================

        pdf_url = (
            f"/outputs/{pdf_filename}"
        )

        print(
            f"PDF 报告生成完成："
            f"{pdf_filename}"
        )

        print(
            f"PDF 地址："
            f"{pdf_url}"
        )

        # =================================================
        # 最终结果
        # =================================================

        result = {

            "success": True,

            "filename": filename,

            # -------------------------------------------------
            # 数据基本信息
            # -------------------------------------------------

            "data_info": data_info,

            "data_shape": {

                "original": [
                    original_rows,
                    original_columns,
                ],

                "cleaned": [
                    len(cleaned_df),
                    len(
                        cleaned_df.columns
                    ),
                ],
            },

            "columns": (
                original_columns_list
            ),

            "target_column": (
                target_column
            ),

            # -------------------------------------------------
            # 数据清洗
            # -------------------------------------------------

            "cleaning_report": (
                cleaning_report
            ),

            # -------------------------------------------------
            # EDA
            # -------------------------------------------------

            "eda": (
                eda_result
            ),

            # -------------------------------------------------
            # Machine Learning
            # -------------------------------------------------

            "machine_learning": (
                ml_result
            ),

            # -------------------------------------------------
            # Visualization
            # -------------------------------------------------

            "visualizations": (
                visualization_result
            ),

            # -------------------------------------------------
            # 普通 AI 分析
            # -------------------------------------------------

            "ai_analysis": (
                ai_analysis
            ),

            # -------------------------------------------------
            # Analysis Agent
            # -------------------------------------------------

            "analysis_agent": (
                analysis_agent_result
            ),

            # -------------------------------------------------
            # Agent Evaluation
            # -------------------------------------------------

            "agent_evaluation": {

                "total_questions": (
                    len(evaluation_questions)
                ),

                "questions": (
                    evaluation_questions
                ),

                "results": (
                    evaluation_results
                ),

                "summary": (
                    evaluation_summary
                ),
            },

            # -------------------------------------------------
            # PDF
            # -------------------------------------------------

            "pdf_report": pdf_url,

            "pdf_filename": pdf_filename,
        }

        # =================================================
        # 完成
        # =================================================

        print(
            "\n" + "=" * 70
        )

        print(
            "数据分析全部完成"
        )

        print(
            "=" * 70
        )

        print(
            f"文件：{filename}"
        )

        print(
            f"目标字段：{target_column}"
        )

        print(
            f"数据："
            f"{len(cleaned_df)} 行 × "
            f"{len(cleaned_df.columns)} 列"
        )

        print(
            f"PDF：{pdf_filename}"
        )

        print(
            "Analysis Agent：完成"
        )

        print(
            f"Agent Evaluation："
            f"{len(evaluation_questions)} 道题"
        )

        print(
            f"Evaluation Accuracy："
            f"{evaluation_summary['overall_accuracy']}%"
        )

        print(
            "=" * 70 + "\n"
        )

        return result

    except HTTPException:

        # FastAPI 主动抛出的错误
        # 直接继续抛出

        raise

    except Exception as e:

        import traceback

        print(
            "\n" + "=" * 70
        )

        print(
            "数据分析失败"
        )

        print(
            "=" * 70
        )

        traceback.print_exc()

        print(
            "=" * 70 + "\n"
        )

        raise HTTPException(
            status_code=500,
            detail=str(e),
        )