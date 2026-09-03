import pandas as pd


def perform_eda(df: pd.DataFrame) -> dict:
    """
    Perform basic Exploratory Data Analysis (EDA).
    """

    # 1. 基本统计信息
    numeric_df = df.select_dtypes(include=["number"])

    statistics = {}

    if not numeric_df.empty:
        statistics = numeric_df.describe().round(2).to_dict()

    # 2. 缺失值统计
    missing_values = df.isnull().sum().to_dict()

    # 3. 数据类型
    data_types = {
        column: str(dtype)
        for column, dtype in df.dtypes.items()
    }

    # 4. 相关性分析
    correlation = {}

    if numeric_df.shape[1] >= 2:
        correlation = (
            numeric_df
            .corr()
            .round(3)
            .to_dict()
        )

    return {
        "statistics": statistics,
        "missing_values": missing_values,
        "data_types": data_types,
        "correlation": correlation
    }


if __name__ == "__main__":
    print("EDA module initialized.")