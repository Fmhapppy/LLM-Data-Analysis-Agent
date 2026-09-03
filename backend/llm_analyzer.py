import os
from openai import OpenAI


def generate_ai_analysis(
    data_info: dict,
    eda_result: dict,
    machine_learning: dict
) -> str:

    api_key = os.getenv("DEEPSEEK_API_KEY")

    if not api_key:
        raise ValueError("DEEPSEEK_API_KEY is not set.")

    client = OpenAI(
        api_key=api_key,
        base_url="https://api.deepseek.com"
    )

    prompt = f"""
你是一名专业的数据科学分析师。

请根据下面提供的完整数据分析结果，生成一份专业、客观、容易理解的 AI 数据分析报告。

【一、数据集基本信息】
{data_info}

【二、探索性数据分析（EDA）】
{eda_result}

【三、机器学习结果】
{machine_learning}

请按照以下结构进行分析：

## 1. 数据集概况
介绍数据规模、字段以及数据类型。

## 2. 数据质量
分析缺失值、重复数据以及其他值得注意的数据质量问题。

## 3. 探索性数据分析
重点分析：
- 数值变量的基本统计情况
- 各变量之间的相关性
- 是否存在明显的数据分布问题
- 是否存在异常现象，例如天花板效应或数据偏斜

## 4. 机器学习结果
解释：
- MAE
- RMSE
- 特征重要性

说明这些指标对模型预测效果意味着什么。

## 5. 关键发现
总结从 EDA 和机器学习中发现的最重要规律。

## 6. 实际建议
根据数据分析结果给出 2-3 条合理建议。

要求：
- 使用中文
- 不要编造数据
- 所有数字必须来自输入数据
- 区分“相关性”和“因果关系”，不要把相关性直接说成因果关系
- 如果发现数据质量问题，必须指出
- 如果发现数据分布异常，必须指出
- 不要过度解读样本量较小的数据
- 语言专业但容易理解
- 控制在 800 字以内
"""

    response = client.chat.completions.create(
        model="deepseek-v4-flash",
        messages=[
            {
                "role": "system",
                "content": "You are a professional data science analyst."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.3
    )

    return response.choices[0].message.content


if __name__ == "__main__":

    test_data_info = {
        "original_rows": 122,
        "original_columns": 5,
        "cleaned_rows": 120,
        "cleaned_columns": 5,
        "columns": [
            "study_hours",
            "sleep_hours",
            "attendance",
            "assignment_score",
            "final_score"
        ]
    }

    test_eda = {
        "missing_values": {
            "study_hours": 0,
            "sleep_hours": 3,
            "attendance": 0,
            "assignment_score": 2,
            "final_score": 0
        },
        "correlation": {
            "study_hours": {
                "final_score": 0.684
            },
            "sleep_hours": {
                "final_score": -0.118
            },
            "attendance": {
                "final_score": 0.216
            },
            "assignment_score": {
                "final_score": 0.2
            }
        }
    }

    test_machine_learning = {
        "mae": 2.6367,
        "rmse": 4.2828,
        "feature_importance": {
            "study_hours": 0.7103,
            "sleep_hours": 0.0509,
            "attendance": 0.1452,
            "assignment_score": 0.0935
        }
    }

    print("Generating AI analysis...")

    result = generate_ai_analysis(
        test_data_info,
        test_eda,
        test_machine_learning
    )

    print("\n===== AI Analysis Report =====\n")
    print(result)