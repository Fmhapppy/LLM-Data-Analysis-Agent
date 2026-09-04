import os
import re
from openai import OpenAI


def clean_markdown(text: str) -> str:
    """
    清理 DeepSeek 返回结果中的 Markdown 符号，
    保留数字编号结构，方便前端直接展示。
    """

    if not text:
        return ""

    # 处理转义字符
    text = text.replace("\\#", "#")
    text = text.replace("\\*", "*")
    text = text.replace("\\`", "`")

    # 删除代码块
    text = re.sub(r"```.*?```", "", text, flags=re.S)

    # 删除 Markdown 标题符号，但保留标题文字
    text = re.sub(r"^#{1,6}\s*", "", text, flags=re.M)

    # 加粗
    text = re.sub(r"\*\*(.*?)\*\*", r"\1", text)

    # 下划线加粗
    text = re.sub(r"__(.*?)__", r"\1", text)

    # 行内代码
    text = re.sub(r"`([^`]*)`", r"\1", text)

    # Markdown 无序列表转换成普通项目符号
    text = re.sub(r"^\s*[-*]\s+", "• ", text, flags=re.M)

    # 清理连续空行
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()


def generate_ai_analysis(
    data_info,
    eda_result,
    machine_learning,
    cleaning_report=None
):
    """
    使用 DeepSeek 对数据分析结果进行智能总结。
    """

    api_key = os.getenv("DEEPSEEK_API_KEY")

    if not api_key:
        raise ValueError(
            "DEEPSEEK_API_KEY is not configured."
        )

    client = OpenAI(
        api_key=api_key,
        base_url="https://api.deepseek.com"
    )

    cleaning_report = cleaning_report or {}

    prompt = f"""
你是一名专业的数据分析师。

请根据下面的数据分析结果，生成一份中文数据分析报告。

【数据集信息】
{data_info}

【数据清洗结果】
{cleaning_report}

【探索性数据分析 EDA】
{eda_result}

【机器学习结果】
{machine_learning}

请按照以下结构输出：

1. 数据集概况
介绍数据规模、字段情况以及整体数据特征。

2. 数据质量
结合实际的数据清洗结果，说明：
- 是否存在重复数据
- 是否存在缺失值
- 数据清洗进行了什么处理
不要猜测没有提供的数据。

3. 关键发现
根据统计结果和相关性分析，总结数据中最值得关注的规律。

4. 关键影响因素
结合机器学习模型的 feature importance，分析哪些变量对目标变量影响最大。
必须结合实际数值进行说明。

5. 模型表现
说明 MAE、RMSE 等模型指标，并简单解释模型表现。

6. AI 建议
根据数据分析结果给出 3-5 条具有实际意义的建议。
建议必须基于当前数据，不要凭空编造业务背景。

【重要输出要求】

只输出普通中文文本。

不要使用 Markdown。

不要使用 #、##、### 等标题符号。

不要使用 ** 加粗符号。

不要使用反引号。

不要生成 Markdown 表格。

可以使用数字编号，例如：
1. 数据集概况
2. 数据质量

不要在报告开头添加“以下是分析报告”等无意义的介绍。

内容要专业、简洁、易读。
"""

    response = client.chat.completions.create(
        model="deepseek-v4-flash",
        messages=[
            {
                "role": "system",
                "content": "你是一名专业的数据分析师，擅长将统计分析和机器学习结果转化为清晰易懂的数据洞察。"
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.3
    )

    result = response.choices[0].message.content

    return clean_markdown(result)