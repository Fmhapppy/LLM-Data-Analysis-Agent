import json
import os
import re

from dotenv import load_dotenv
from openai import OpenAI


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ENV_PATH = os.path.join(BASE_DIR, ".env")
load_dotenv(ENV_PATH)


def _safe_float(value, digits=4):
    """
    将数值安全转换为 float，并保留指定小数位。
    """
    try:
        return round(float(value), digits)
    except (TypeError, ValueError):
        return None


def _build_fact_sheet(
    columns,
    cleaning_report,
    eda_result,
    machine_learning
):
    """
    从已有分析结果中提取关键事实。
    这些事实会作为 Agent 的“不可修改事实层”。
    """

    fact_sheet = {
        "columns": columns,
        "sample_count": None,
        "duplicate_removed": None,
        "missing_values_after_cleaning": None,
        "target_column": None,
        "mae": None,
        "rmse": None,
        "r2": None,
        "model_name": None,
        "feature_importance": {},
    }

    # =========================
    # 数据清洗事实
    # =========================

    if isinstance(cleaning_report, dict):
        for key in [
            "duplicate_removed",
            "duplicates_removed",
            "removed_duplicates"
        ]:
            if key in cleaning_report:
                fact_sheet["duplicate_removed"] = cleaning_report[key]
                break

        for key in [
            "remaining_rows",
            "cleaned_rows",
            "rows_after_cleaning",
            "sample_count"
        ]:
            if key in cleaning_report:
                fact_sheet["sample_count"] = cleaning_report[key]
                break

        for key in [
            "missing_after",
            "missing_values_after",
            "remaining_missing_values"
        ]:
            if key in cleaning_report:
                fact_sheet["missing_values_after_cleaning"] = cleaning_report[key]
                break

    # =========================
    # 机器学习事实
    # =========================

    if isinstance(machine_learning, dict):

        metadata = machine_learning.get("metadata", {})

        if isinstance(metadata, dict):
            fact_sheet["target_column"] = metadata.get("target_column")

        # 兼容当前 V1/V2 结构
        fact_sheet["mae"] = _safe_float(
            machine_learning.get("mae")
        )

        fact_sheet["rmse"] = _safe_float(
            machine_learning.get("rmse")
        )

        fact_sheet["r2"] = _safe_float(
            machine_learning.get("r2")
        )

        fact_sheet["model_name"] = (
            machine_learning.get("model_name")
            or machine_learning.get("best_model")
        )

        feature_importance = machine_learning.get(
            "feature_importance",
            {}
        )

        if isinstance(feature_importance, dict):
            fact_sheet["feature_importance"] = {
                str(k): _safe_float(v, 4)
                for k, v in feature_importance.items()
                if _safe_float(v, 4) is not None
            }

        # 如果 metadata 中没有 target_column，
        # 尝试从其他位置获取
        if not fact_sheet["target_column"]:
            fact_sheet["target_column"] = (
                machine_learning.get("target_column")
            )

    return fact_sheet


def _validate_analysis_result(result, fact_sheet):
    """
    对 LLM 输出进行基础事实一致性检查。

    这里不修改 LLM 原文，只负责检测明显的问题。
    """

    warnings = []

    if not isinstance(result, dict):
        return ["Agent output is not a JSON object."]

    text = json.dumps(
        result,
        ensure_ascii=False
    )

    # =========================
    # 样本数量检查
    # =========================

    sample_count = fact_sheet.get("sample_count")

    if isinstance(sample_count, (int, float)):
        sample_count = int(sample_count)

        numbers = [
            int(x)
            for x in re.findall(r"(?<![\d.])\d+(?![\d.])", text)
        ]

        suspicious_counts = [
            n for n in numbers
            if 50 <= n <= 1000 and n != sample_count
        ]

        # 这里只作为提醒，不直接判定错误
        if suspicious_counts:
            warnings.append(
                f"Please verify sample count references. "
                f"Actual cleaned sample count is {sample_count}."
            )

    # =========================
    # MAE 检查
    # =========================

    mae = fact_sheet.get("mae")

    if mae is not None:
        mae_text = f"{mae:.3f}"

        if "MAE" in text.upper():
            if mae_text not in text:
                warnings.append(
                    f"Verify MAE. Actual MAE is {mae}."
                )

    # =========================
    # RMSE 检查
    # =========================

    rmse = fact_sheet.get("rmse")

    if rmse is not None:
        rmse_text = f"{rmse:.3f}"

        if "RMSE" in text.upper():
            if rmse_text not in text:
                warnings.append(
                    f"Verify RMSE. Actual RMSE is {rmse}."
                )

    return warnings


def create_analysis_agent(
    columns,
    cleaning_report,
    eda_result,
    machine_learning
):
    api_key = os.getenv("DEEPSEEK_API_KEY")

    if not api_key:
        raise ValueError(
            "DEEPSEEK_API_KEY is not configured"
        )

    client = OpenAI(
        api_key=api_key,
        base_url="https://api.deepseek.com"
    )

    # =====================================================
    # 1. 建立事实层
    # =====================================================

    fact_sheet = _build_fact_sheet(
        columns,
        cleaning_report,
        eda_result,
        machine_learning
    )

    # =====================================================
    # 2. 构建 Agent Prompt
    # =====================================================

    prompt = f"""
你是一名专业的数据科学家和 AI 数据分析 Agent。

你的任务不是重新计算模型，而是基于已经完成的数据分析结果进行二次推理。

==================================================
【最重要原则：事实优先】
==================================================

以下 FACT SHEET 是系统从真实程序结果中提取的关键事实。

你必须以 FACT SHEET 为最高优先级。

不要修改、猜测、补充或创造 FACT SHEET 中不存在的数值。

【FACT SHEET】
{json.dumps(fact_sheet, ensure_ascii=False, indent=2)}

==================================================
【原始分析结果】
==================================================

【数据字段】
{json.dumps(columns, ensure_ascii=False)}

【数据清洗结果】
{json.dumps(cleaning_report, ensure_ascii=False)}

【EDA 结果】
{json.dumps(eda_result, ensure_ascii=False)}

【机器学习结果】
{json.dumps(machine_learning, ensure_ascii=False)}

==================================================
【当前分析任务】
==================================================

预测目标：

final_score

预测变量：

study_hours
sleep_hours
attendance
assignment_score

必须围绕 final_score 进行分析。

==================================================
【分析原则】
==================================================

1. 相关性 ≠ 因果关系

Pearson correlation 只能描述统计关联。

不得把：

“相关”

写成：

“导致”
“造成”
“决定”
“影响了多少百分比”

如果提出可能机制，必须使用：

“可能”
“暗示”
“值得进一步验证”

等谨慎表达。

--------------------------------------------------

2. Feature Importance ≠ Causal Importance

Random Forest feature importance：

只表示模型预测过程中对该特征的依赖程度。

例如：

study_hours = 0.71

不能写成：

“study_hours 对成绩有 71% 的影响”。

应该写成：

“study_hours 在当前随机森林模型中的特征重要性为 0.71，是模型最依赖的预测变量之一。”

--------------------------------------------------

3. 必须正确识别目标变量

当前预测目标：

final_score

如果机器学习结果中的 target_column 不是 final_score：

必须明确指出：

“当前机器学习实验的目标变量与任务要求不一致。”

不得假装模型是在预测 final_score。

--------------------------------------------------

4. 模型评价必须使用真实指标

如果 FACT SHEET 中存在：

MAE
RMSE
R²

必须直接使用这些实际结果。

不得虚构其他数值。

--------------------------------------------------

5. 数据量必须保持一致

如果清洗后的样本数量为：

120

任何地方都不能写成：

125
122
121
119

除非是在明确描述：

“原始数据为122条，清洗后为120条”。

--------------------------------------------------

6. 注意目标变量的分布

如果 final_score 存在：

满分集中
天花板效应
偏态
低分样本不足

必须指出。

同时解释这些问题可能如何影响：

模型预测
R²
MAE
低分样本预测
模型泛化能力

--------------------------------------------------

7. 不要过度解读模型

尤其注意：

样本量较小。

5-fold cross-validation 可以帮助估计模型稳定性，

但不能证明模型具有很强的真实世界泛化能力。

==================================================
【输出要求】
==================================================

严格返回 JSON。

不要返回 Markdown。

不要使用代码块。

JSON 格式：

{{
    "core_findings": [
        "核心发现1",
        "核心发现2",
        "核心发现3"
    ],
    "key_factors": [
        {{
            "feature": "study_hours",
            "reason": "原因"
        }},
        {{
            "feature": "attendance",
            "reason": "原因"
        }},
        {{
            "feature": "assignment_score",
            "reason": "原因"
        }},
        {{
            "feature": "sleep_hours",
            "reason": "原因"
        }}
    ],
    "data_quality": [
        "数据质量分析1",
        "数据质量分析2",
        "数据质量分析3"
    ],
    "relationships": [
        "变量关系分析1",
        "变量关系分析2",
        "变量关系分析3"
    ],
    "model_evaluation": [
        "模型评价1",
        "模型评价2",
        "模型评价3"
    ],
    "next_analysis": [
        "下一步分析建议1",
        "下一步分析建议2",
        "下一步分析建议3"
    ]
}}

==================================================
【最终检查】
==================================================

生成 JSON 前必须自行检查：

1. 有没有虚构数据？
2. 样本数量是否与 FACT SHEET 一致？
3. MAE 是否与 FACT SHEET 一致？
4. RMSE 是否与 FACT SHEET 一致？
5. R² 是否与 FACT SHEET 一致？
6. target 是否为 final_score？
7. 有没有把 correlation 写成 causation？
8. 有没有把 feature importance 写成 causal importance？
9. 有没有把“模型重要性71%”写成“学习时间影响成绩71%”？
10. 是否指出了 final_score 的天花板效应？
11. 是否考虑了小样本问题？

只输出 JSON。
"""

    # =====================================================
    # 3. 调用 DeepSeek
    # =====================================================

    response = client.chat.completions.create(
        model="deepseek-v4-flash",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an expert data scientist "
                    "and AI data analysis agent. "
                    "Always prioritize structured facts "
                    "over generated assumptions."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.1,
    )

    content = response.choices[0].message.content.strip()

    # =====================================================
    # 4. JSON 解析
    # =====================================================

    try:
        result = json.loads(content)

    except json.JSONDecodeError:

        # 尝试提取 ```json ... ``` 中的 JSON
        match = re.search(
            r"```(?:json)?\s*(.*?)\s*```",
            content,
            re.DOTALL
        )

        if match:
            try:
                result = json.loads(
                    match.group(1)
                )
            except json.JSONDecodeError:
                return {
                    "raw_analysis": content,
                    "validation_warnings": [
                        "LLM returned invalid JSON."
                    ]
                }

        else:
            return {
                "raw_analysis": content,
                "validation_warnings": [
                    "LLM returned invalid JSON."
                ]
            }

    # =====================================================
    # 5. 自动事实校验
    # =====================================================

    validation_warnings = _validate_analysis_result(
        result,
        fact_sheet
    )

    # =====================================================
    # 6. 将验证信息一起返回
    # =====================================================

    if isinstance(result, dict):

        result["_agent_metadata"] = {
            "fact_sheet": fact_sheet,
            "validation_warnings": validation_warnings,
            "validation_passed": len(validation_warnings) == 0
        }

    return result


if __name__ == "__main__":
    print("Analysis Agent V2 initialized.")