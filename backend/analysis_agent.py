import json
import os

from dotenv import load_dotenv
from openai import OpenAI


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ENV_PATH = os.path.join(BASE_DIR, ".env")
load_dotenv(ENV_PATH)


def create_analysis_agent(
    columns,
    cleaning_report,
    eda_result,
    machine_learning
):
    api_key = os.getenv("DEEPSEEK_API_KEY")

    if not api_key:
        raise ValueError("DEEPSEEK_API_KEY is not configured")

    client = OpenAI(
        api_key=api_key,
        base_url="https://api.deepseek.com"
    )

    prompt = f"""
你是一名专业的数据科学家和 AI 数据分析 Agent。

请基于以下数据分析结果进行二次推理，生成结构化的深度分析。

【数据字段】
{json.dumps(columns, ensure_ascii=False)}

【数据清洗结果】
{json.dumps(cleaning_report, ensure_ascii=False)}

【EDA 结果】
{json.dumps(eda_result, ensure_ascii=False)}

【机器学习结果】
{json.dumps(machine_learning, ensure_ascii=False)}

请严格遵守以下分析原则：

1. 明确区分“相关性”和“因果关系”。
   - 相关系数只能说明变量之间存在统计关联。
   - 不得仅凭相关系数直接得出因果结论。
   - 如果提出可能的机制或解释，必须使用“可能”“暗示”“值得进一步验证”等谨慎表达。

2. 结合 EDA 和机器学习结果进行综合分析。
   不要只重复某一个指标。

3. 正确识别机器学习模型的预测目标。
   当前任务中：
   - 预测目标是 final_score
   - study_hours、sleep_hours、attendance、assignment_score 是预测变量

4. 分析特征重要性时，需要说明：
   - 特征重要性反映模型预测中的贡献程度
   - 不等同于现实世界中的因果影响

5. 如果目标变量存在明显的满分集中、上限效应或分布偏态，需要指出这一问题，并说明它可能对模型产生的影响。

6. 对模型评价必须使用实际提供的 MAE 和 RMSE。
   不允许输出“暂无模型评价”。

7. 下一步建议应该具有数据科学意义，例如：
   - 增加样本
   - 检查异常值
   - 尝试其他模型
   - 交叉验证
   - 特征工程
   - 处理目标变量分布
   - 分类模型或分位数回归
   等。

请严格返回 JSON，不要返回 Markdown，不要使用代码块。

JSON 格式必须严格为：

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
        }}
    ],
    "data_quality": [
        "数据质量分析1",
        "数据质量分析2"
    ],
    "relationships": [
        "变量关系分析1",
        "变量关系分析2"
    ],
    "model_evaluation": [
        "模型评价1",
        "模型评价2"
    ],
    "next_analysis": [
        "下一步分析建议1",
        "下一步分析建议2",
        "下一步分析建议3"
    ]
}}

注意：
- 所有分析必须基于提供的数据。
- 不要虚构数据。
- 不要把相关性写成因果关系。
- model_evaluation 必须包含实际的 MAE 和 RMSE。
"""

    response = client.chat.completions.create(
        model="deepseek-v4-flash",
        messages=[
            {
                "role": "system",
                "content": "You are an expert data scientist and AI data analysis agent."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2,
    )

    content = response.choices[0].message.content.strip()

    try:
        return json.loads(content)

    except json.JSONDecodeError:
        return {
            "raw_analysis": content
        }


if __name__ == "__main__":
    print("Analysis Agent module initialized.")