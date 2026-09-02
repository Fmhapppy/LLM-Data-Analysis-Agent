import pandas as pd
import matplotlib.pyplot as plt


def analyze_data(df: pd.DataFrame) -> dict:
    """
    Perform basic exploratory data analysis.
    """

    numeric_columns = df.select_dtypes(
        include=["number"]
    ).columns.tolist()

    categorical_columns = df.select_dtypes(
        include=["object", "category", "bool"]
    ).columns.tolist()

    analysis = {
        "shape": {
            "rows": len(df),
            "columns": len(df.columns)
        },
        "numeric_columns": numeric_columns,
        "categorical_columns": categorical_columns,
        "statistics": df[numeric_columns].describe().to_dict()
        if numeric_columns else {},
    }

    return analysis


def create_histograms(
    df: pd.DataFrame,
    output_dir: str = "outputs"
):
    """
    Generate histograms for numeric columns.
    """

    import os

    os.makedirs(output_dir, exist_ok=True)

    numeric_columns = df.select_dtypes(
        include=["number"]
    ).columns

    for column in numeric_columns:
        plt.figure(figsize=(8, 5))
        df[column].hist()
        plt.title(f"Distribution of {column}")
        plt.xlabel(column)
        plt.ylabel("Frequency")

        output_path = os.path.join(
            output_dir,
            f"{column}_distribution.png"
        )

        plt.savefig(output_path)
        plt.close()
