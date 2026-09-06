import os
import re

from dotenv import load_dotenv
from openai import OpenAI


# ============================================================
# 1. 加载 .env
# ============================================================

# 当前文件所在目录，也就是 backend 目录
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 明确指定 backend/.env
ENV_PATH = os.path.join(BASE_DIR, ".env")

# 加载环境变量
load_dotenv(ENV_PATH)


# ============================================================
# 2. 清理 Markdown
# ============================================================

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

    # 删除 Markdown 代码块
    text = re.sub(r"```.*?```", "", text, flags=re.S)

    # 删除 Markdown 标题符号，但保留标题文字
    text = re.sub(r"^#{1,6}\s*", "", text, flags=re.M)

    # 删除加粗
    text = re.sub(r"\*\*(.*?)\*\*", r"\1", text)

    # 删除下划线加粗
    text = re.sub(r"__(.*?)__", r"\1", text)

    # 删除行内代码
    text = re.sub(r"`([^`]*)`", r"\1", text)

    # Markdown 无序列表转换成普通项目符号
    text = re.sub(r"^\s*[-*]\s+", "• ", text, flags=re.M)

    # 清理连续空行
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()


# ============================================================
# 3. DeepSeek AI 数据分析
# ============================================================

def generate_ai_analysis(
    data_info,
    eda_result,
    machine_learning,
    cleaning_report=None
):
    """
    使用 DeepSeek 对数据分析结果进行智能总结。

    参数：
        data_info:
            数据集基本信息

        eda_result:
            EDA 探索性数据分析结果

        machine_learning:
            机器学习模型结果

        cleaning_report:
            数据清洗结果
    """

    # --------------------------------------------------------
    # 获取 API Key
    # --------------------------------------------------------

    api_key = os.getenv("DEEPSEEK_API_KEY")

    # API Key 不存在
    if not api_key:
        raise ValueError(
            "DEEPSEEK_API_KEY is not configured. "
            "Please add DEEPSEEK_API_KEY to backend/.env"
        )

    # --------------------------------------------------------
    # 创建 DeepSeek 客户端
    # --------------------------------------------------------

    client = OpenAI(
        api_key=api_key,
        base_url="https://api.deepseek.com"
    )

    # 如果没有传入 cleaning_report，则使用空字典
    cleaning_report = cleaning_report or {}

    # --------------------------------------------------------
    # 构建 Prompt
    # --------------------------------------------------------

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

需要结合实际的数据统计结果和相关性数值进行分析。


4. 关键影响因素

结合机器学习模型的 feature importance，
分析哪些变量对目标变量影响最大。

必须结合实际数值进行说明。

不要凭空添加不存在的变量。


5. 模型表现

说明：

- MAE
- RMSE

并简单解释模型表现。

解释必须基于实际模型结果。


6. AI 建议

根据数据分析结果给出 3-5 条具有实际意义的建议。

建议必须基于当前数据，
不要凭空编造业务背景。


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
3. 关键发现
4. 关键影响因素
5. 模型表现
6. AI 建议

不要在报告开头添加“以下是分析报告”等无意义的介绍。

内容要专业、简洁、易读。

不要虚构数据。

所有结论必须尽可能基于提供的数据分析结果。
"""

    # --------------------------------------------------------
    # 调用 DeepSeek
    # --------------------------------------------------------

    response = client.chat.completions.create(
        model="deepseek-v4-flash",
        messages=[
            {
                "role": "system",
                "content": (
                    "你是一名专业的数据分析师，"
                    "擅长将统计分析和机器学习结果"
                    "转化为清晰易懂的数据洞察。"
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.3
    )

    # --------------------------------------------------------
    # 获取 AI 返回结果
    # --------------------------------------------------------

    result = response.choices[0].message.content

    # 防止 AI 返回空内容
    if not result:
        raise ValueError(
            "DeepSeek returned an empty response."
        )

    # --------------------------------------------------------
    # 清理 Markdown 后返回
    # --------------------------------------------------------

    return clean_markdown(result)