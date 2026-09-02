import pandas as pd

from data_processor import load_data
from data_cleaner import clean_data
from eda import perform_eda
from ml_model import train_regression_model


def run_analysis(file_path: str, target_column: str):
    # 1. Load data
    df = load_data(file_path)

    # 2. Clean data
    cleaned_df = clean_data(df)

    # 3. Exploratory Data Analysis
    eda_result = perform_eda(cleaned_df)

    # 4. Machine Learning
    ml_result = train_regression_model(
        cleaned_df,
        target_column
    )

    return {
        "data_shape": cleaned_df.shape,
        "eda": eda_result,
        "machine_learning": ml_result
    }


if __name__ == "__main__":
    print("LLM Data Analysis Agent")
    print("Analysis pipeline initialized.")
