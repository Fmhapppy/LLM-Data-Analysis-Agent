import os
from datetime import datetime

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Image,
    PageBreak,
)


# ============================================================
# 1. 基础路径
# ============================================================

# 当前文件所在目录
# 也就是你的 backend 文件夹
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


# ============================================================
# 2. 中文字体
# ============================================================

def register_chinese_font():
    """
    注册 Windows 中文字体。
    优先使用微软雅黑。
    """

    possible_fonts = [
        r"C:\Windows\Fonts\msyh.ttc",
        r"C:\Windows\Fonts\msyh.ttf",
        r"C:\Windows\Fonts\simhei.ttf",
        r"C:\Windows\Fonts\simsun.ttc",
    ]

    for font_path in possible_fonts:

        if os.path.exists(font_path):

            try:
                pdfmetrics.registerFont(
                    TTFont(
                        "ChineseFont",
                        font_path,
                    )
                )

                return "ChineseFont"

            except Exception:
                continue

    # 如果没有找到中文字体
    # 使用 Helvetica
    return "Helvetica"


FONT_NAME = register_chinese_font()


# ============================================================
# 3. 工具函数
# ============================================================

def safe_text(value):
    """
    安全转换文本。
    """

    if value is None:
        return ""

    return str(value)


def format_number(value):
    """
    格式化数字。
    """

    if value is None:
        return ""

    try:

        value = float(value)

        if value.is_integer():
            return str(int(value))

        return f"{value:.3f}"

    except (ValueError, TypeError):

        return str(value)


def create_table(data, col_widths=None):
    """
    创建统一风格的数据表格。
    """

    table = Table(
        data,
        colWidths=col_widths,
        repeatRows=1,
    )

    table.setStyle(
        TableStyle(
            [
                # 表头
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.HexColor("#E9EEF5"),
                ),

                (
                    "TEXTCOLOR",
                    (0, 0),
                    (-1, 0),
                    colors.HexColor("#1F2937"),
                ),

                (
                    "FONTNAME",
                    (0, 0),
                    (-1, -1),
                    FONT_NAME,
                ),

                (
                    "FONTNAME",
                    (0, 0),
                    (-1, 0),
                    FONT_NAME,
                ),

                (
                    "FONTSIZE",
                    (0, 0),
                    (-1, -1),
                    8,
                ),

                (
                    "LEADING",
                    (0, 0),
                    (-1, -1),
                    12,
                ),

                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.HexColor("#D1D5DB"),
                ),

                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "MIDDLE",
                ),

                (
                    "LEFTPADDING",
                    (0, 0),
                    (-1, -1),
                    6,
                ),

                (
                    "RIGHTPADDING",
                    (0, 0),
                    (-1, -1),
                    6,
                ),

                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    6,
                ),

                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    6,
                ),
            ]
        )
    )

    return table


# ============================================================
# 4. 生成 PDF
# ============================================================

def generate_pdf_report(
    output_path,
    filename,
    data_shape,
    columns,
    cleaning_report,
    eda_result,
    machine_learning,
    visualizations,
    ai_analysis,
):
    """
    生成完整 AI 数据分析 PDF 报告。

    参数：
        output_path:
            PDF 输出路径

        filename:
            原始数据文件名

        data_shape:
            数据规模

        columns:
            数据字段

        cleaning_report:
            数据清洗结果

        eda_result:
            EDA 分析结果

        machine_learning:
            机器学习结果

        visualizations:
            可视化图片路径

        ai_analysis:
            DeepSeek AI 分析报告
    """

    # ========================================================
    # 1. 创建输出目录
    # ========================================================

    output_dir = os.path.dirname(
        os.path.abspath(output_path)
    )

    os.makedirs(
        output_dir,
        exist_ok=True,
    )

    # ========================================================
    # 2. 创建 PDF
    # ========================================================

    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,

        rightMargin=18 * mm,
        leftMargin=18 * mm,
        topMargin=18 * mm,
        bottomMargin=18 * mm,

        title="AI Data Analysis Report",
        author="LLM Data Analysis Agent",
    )

    # ========================================================
    # 3. 样式
    # ========================================================

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "ReportTitle",
        parent=styles["Title"],

        fontName=FONT_NAME,
        fontSize=24,
        leading=30,

        alignment=TA_CENTER,

        spaceAfter=15,
    )

    cover_subtitle_style = ParagraphStyle(
        "CoverSubtitle",
        parent=styles["Normal"],

        fontName=FONT_NAME,
        fontSize=15,
        leading=22,

        alignment=TA_CENTER,

        textColor=colors.HexColor("#555555"),

        spaceAfter=10,
    )

    section_style = ParagraphStyle(
        "SectionTitle",
        parent=styles["Heading2"],

        fontName=FONT_NAME,
        fontSize=16,
        leading=22,

        textColor=colors.HexColor("#111827"),

        spaceBefore=10,
        spaceAfter=10,
    )

    subsection_style = ParagraphStyle(
        "SubSectionTitle",
        parent=styles["Heading3"],

        fontName=FONT_NAME,
        fontSize=12,
        leading=18,

        textColor=colors.HexColor("#374151"),

        spaceBefore=8,
        spaceAfter=6,
    )

    body_style = ParagraphStyle(
        "BodyTextCustom",
        parent=styles["BodyText"],

        fontName=FONT_NAME,
        fontSize=9.5,
        leading=16,

        textColor=colors.HexColor("#374151"),

        spaceAfter=7,
    )

    small_style = ParagraphStyle(
        "SmallText",
        parent=styles["BodyText"],

        fontName=FONT_NAME,
        fontSize=8,
        leading=12,

        textColor=colors.HexColor("#6B7280"),
    )

    # ========================================================
    # 4. PDF 内容
    # ========================================================

    story = []

    # ========================================================
    # 封面
    # ========================================================

    story.append(
        Spacer(
            1,
            35 * mm,
        )
    )

    story.append(
        Paragraph(
            "AI Data Analysis Report",
            title_style,
        )
    )

    story.append(
        Paragraph(
            "智能数据分析报告",
            cover_subtitle_style,
        )
    )

    story.append(
        Spacer(
            1,
            10 * mm,
        )
    )

    story.append(
        Paragraph(
            f"数据文件：{safe_text(filename)}",
            cover_subtitle_style,
        )
    )

    story.append(
        Paragraph(
            "LLM Data Analysis Agent",
            cover_subtitle_style,
        )
    )

    story.append(
        Paragraph(
            f"生成时间："
            f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            cover_subtitle_style,
        )
    )

    story.append(
        Spacer(
            1,
            35 * mm,
        )
    )

    story.append(
        Paragraph(
            "Generated by LLM Data Analysis Agent",
            small_style,
        )
    )

    story.append(
        PageBreak()
    )

    # ========================================================
    # 1. 数据集概况
    # ========================================================

    story.append(
        Paragraph(
            "1. 数据集概况",
            section_style,
        )
    )

    original_shape = data_shape.get(
        "original",
        [0, 0],
    )

    cleaned_shape = data_shape.get(
        "cleaned",
        [0, 0],
    )

    overview_data = [
        [
            "指标",
            "结果",
        ],

        [
            "原始数据行数",
            str(original_shape[0]),
        ],

        [
            "原始字段数量",
            str(original_shape[1]),
        ],

        [
            "清洗后数据行数",
            str(cleaned_shape[0]),
        ],

        [
            "清洗后字段数量",
            str(cleaned_shape[1]),
        ],

        [
            "分析字段数量",
            str(len(columns)),
        ],
    ]

    story.append(
        create_table(
            overview_data,
            col_widths=[
                65 * mm,
                90 * mm,
            ],
        )
    )

    story.append(
        Spacer(
            1,
            8 * mm,
        )
    )

    story.append(
        Paragraph(
            "数据字段",
            subsection_style,
        )
    )

    field_text = "、".join(
        [
            safe_text(column)
            for column in columns
        ]
    )

    story.append(
        Paragraph(
            field_text,
            body_style,
        )
    )

    # ========================================================
    # 2. 数据质量
    # ========================================================

    story.append(
        Paragraph(
            "2. 数据质量与数据清洗",
            section_style,
        )
    )

    original_rows = cleaning_report.get(
        "original_rows",
        0,
    )

    cleaned_rows = cleaning_report.get(
        "cleaned_rows",
        0,
    )

    duplicate_removed = cleaning_report.get(
        "duplicate_rows_removed",
        0,
    )

    original_missing = cleaning_report.get(
        "original_missing_values",
        0,
    )

    remaining_missing = cleaning_report.get(
        "remaining_missing_values",
        0,
    )

    numeric_filled = cleaning_report.get(
        "numeric_missing_values_filled",
        0,
    )

    categorical_filled = cleaning_report.get(
        "categorical_missing_values_filled",
        0,
    )

    quality_data = [
        [
            "数据质量指标",
            "结果",
        ],

        [
            "原始数据行数",
            str(original_rows),
        ],

        [
            "清洗后数据行数",
            str(cleaned_rows),
        ],

        [
            "删除重复记录",
            str(duplicate_removed),
        ],

        [
            "原始缺失值",
            str(original_missing),
        ],

        [
            "数值型缺失值填充",
            str(numeric_filled),
        ],

        [
            "类别型缺失值填充",
            str(categorical_filled),
        ],

        [
            "剩余缺失值",
            str(remaining_missing),
        ],
    ]

    story.append(
        create_table(
            quality_data,
            col_widths=[
                65 * mm,
                90 * mm,
            ],
        )
    )

    story.append(
        Spacer(
            1,
            6 * mm,
        )
    )

    story.append(
        Paragraph(
            "数据清洗步骤",
            subsection_style,
        )
    )

    cleaning_steps = cleaning_report.get(
        "cleaning_steps",
        [],
    )

    if cleaning_steps:

        for step in cleaning_steps:

            story.append(
                Paragraph(
                    f"• {safe_text(step)}",
                    body_style,
                )
            )

    else:

        story.append(
            Paragraph(
                "未检测到需要额外处理的数据质量问题。",
                body_style,
            )
        )

    # ========================================================
    # 3. EDA
    # ========================================================

    story.append(
        Paragraph(
            "3. 探索性数据分析（EDA）",
            section_style,
        )
    )

    statistics = eda_result.get(
        "statistics",
        {},
    )

    if statistics:

        story.append(
            Paragraph(
                "数值字段统计信息",
                subsection_style,
            )
        )

        stat_columns = list(
            statistics.keys()
        )

        stat_table = [
            ["统计指标"] + stat_columns
        ]

        metrics = [
            "count",
            "mean",
            "std",
            "min",
            "25%",
            "50%",
            "75%",
            "max",
        ]

        for metric in metrics:

            row = [metric]

            for column in stat_columns:

                value = (
                    statistics
                    .get(column, {})
                    .get(metric, "")
                )

                row.append(
                    format_number(value)
                )

            stat_table.append(row)

        total_width = 155 * mm

        first_width = 25 * mm

        other_width = (
            total_width - first_width
        ) / max(
            len(stat_columns),
            1,
        )

        widths = [
            first_width
        ] + [
            other_width
            for _ in stat_columns
        ]

        story.append(
            create_table(
                stat_table,
                col_widths=widths,
            )
        )

    else:

        story.append(
            Paragraph(
                "暂无数值统计信息。",
                body_style,
            )
        )

    # ========================================================
    # 4. 相关性分析
    # ========================================================

    story.append(
        Spacer(
            1,
            8 * mm,
        )
    )

    story.append(
        Paragraph(
            "相关性分析",
            subsection_style,
        )
    )

    correlation = eda_result.get(
        "correlation",
        {},
    )

    if correlation:

        correlation_columns = list(
            correlation.keys()
        )

        correlation_table = [
            ["变量"] + correlation_columns
        ]

        for column in correlation_columns:

            row = [column]

            for target in correlation_columns:

                value = (
                    correlation
                    .get(column, {})
                    .get(target, "")
                )

                row.append(
                    format_number(value)
                )

            correlation_table.append(row)

        total_width = 155 * mm

        column_width = (
            total_width
            / (len(correlation_columns) + 1)
        )

        story.append(
            create_table(
                correlation_table,
                col_widths=[
                    column_width
                    for _ in correlation_table[0]
                ],
            )
        )

    else:

        story.append(
            Paragraph(
                "暂无相关性分析结果。",
                body_style,
            )
        )

    # ========================================================
    # 5. 数据可视化
    # ========================================================

    story.append(
        PageBreak()
    )

    story.append(
        Paragraph(
            "4. 数据可视化",
            section_style,
        )
    )

    visualization_order = [
        (
            "correlation_heatmap",
            "相关性热力图",
        ),

        (
            "study_hours_vs_final_score",
            "特征与目标变量关系",
        ),

        (
            "feature_importance",
            "机器学习特征重要性",
        ),
    ]

    for key, title in visualization_order:

        image_path = visualizations.get(
            key
        )

        if not image_path:
            continue

        # API 可能返回：
        #
        # /outputs/xxx.png
        #
        # 或：
        #
        # outputs/xxx.png
        #
        # 统一转换成 backend 实际路径。

        image_path = safe_text(
            image_path
        ).replace(
            "/",
            os.sep,
        )

        if image_path.startswith(
            os.sep
        ):
            image_path = image_path[
                len(os.sep):
            ]

        if not os.path.isabs(
            image_path
        ):

            image_path = os.path.join(
                BASE_DIR,
                image_path,
            )

        if os.path.exists(
            image_path
        ):

            story.append(
                Paragraph(
                    title,
                    subsection_style,
                )
            )

            image = Image(
                image_path,
                width=160 * mm,
                height=90 * mm,
                kind="proportional",
            )

            story.append(image)

            story.append(
                Spacer(
                    1,
                    8 * mm,
                )
            )

        else:

            story.append(
                Paragraph(
                    f"图表文件不存在："
                    f"{safe_text(image_path)}",
                    small_style,
                )
            )

    # ========================================================
    # 6. 机器学习
    # ========================================================

    story.append(
        PageBreak()
    )

    story.append(
        Paragraph(
            "5. 机器学习模型表现",
            section_style,
        )
    )

    mae = machine_learning.get(
        "mae",
        0,
    )

    rmse = machine_learning.get(
        "rmse",
        0,
    )

    model_data = [
        [
            "模型指标",
            "结果",
        ],

        [
            "MAE",
            f"{float(mae):.4f}",
        ],

        [
            "RMSE",
            f"{float(rmse):.4f}",
        ],
    ]

    story.append(
        create_table(
            model_data,
            col_widths=[
                65 * mm,
                90 * mm,
            ],
        )
    )

    # ========================================================
    # 特征重要性
    # ========================================================

    story.append(
        Spacer(
            1,
            8 * mm,
        )
    )

    story.append(
        Paragraph(
            "特征重要性",
            subsection_style,
        )
    )

    feature_importance = machine_learning.get(
        "feature_importance",
        {},
    )

    if feature_importance:

        importance_data = [
            [
                "特征",
                "重要性",
            ]
        ]

        sorted_features = sorted(
            feature_importance.items(),
            key=lambda item: item[1],
            reverse=True,
        )

        for feature, importance in sorted_features:

            importance_data.append(
                [
                    safe_text(feature),
                    f"{float(importance):.4f}",
                ]
            )

        story.append(
            create_table(
                importance_data,
                col_widths=[
                    65 * mm,
                    90 * mm,
                ],
            )
        )

    else:

        story.append(
            Paragraph(
                "暂无特征重要性数据。",
                body_style,
            )
        )

    # ========================================================
    # 7. AI 分析
    # ========================================================

    story.append(
        PageBreak()
    )

    story.append(
        Paragraph(
            "6. AI 数据分析报告",
            section_style,
        )
    )

    if ai_analysis:

        paragraphs = safe_text(
            ai_analysis
        ).split("\n")

        for paragraph in paragraphs:

            paragraph = paragraph.strip()

            if not paragraph:
                story.append(
                    Spacer(
                        1,
                        3 * mm,
                    )
                )

                continue

            story.append(
                Paragraph(
                    paragraph,
                    body_style,
                )
            )

    else:

        story.append(
            Paragraph(
                "暂无 AI 分析结果。",
                body_style,
            )
        )

    # ========================================================
    # 8. 报告结尾
    # ========================================================

    story.append(
        Spacer(
            1,
            15 * mm,
        )
    )

    story.append(
        Paragraph(
            "本报告由 LLM Data Analysis Agent 自动生成。",
            small_style,
        )
    )

    # ========================================================
    # 9. 生成 PDF
    # ========================================================

    doc.build(story)

    return output_path


# ============================================================
# 10. 单独运行测试
# ============================================================

if __name__ == "__main__":

    print(
        "PDF Report module initialized."
    )

    print(
        f"BASE_DIR: {BASE_DIR}"
    )

    print(
        f"Chinese font: {FONT_NAME}"
    )

    print(
        "Use generate_pdf_report() "
        "to create a PDF report."
    )