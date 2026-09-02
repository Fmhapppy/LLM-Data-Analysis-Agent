import pandas as pd


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Basic data cleaning:
    - Remove duplicate rows
    - Remove completely empty columns
    - Fill missing numeric values with the median
    - Fill missing text values with the mode
    """

    df = df.copy()

    # Remove duplicate rows
    df = df.drop_duplicates()

    # Remove completely empty columns
    df = df.dropna(axis=1, how="all")

    # Handle missing values
    for column in df.columns:
        if df[column].isnull().any():

            if pd.api.types.is_numeric_dtype(df[column]):
                df[column] = df[column].fillna(df[column].median())

            else:
                mode = df[column].mode()

                if not mode.empty:
                    df[column] = df[column].fillna(mode.iloc[0])

    return df
