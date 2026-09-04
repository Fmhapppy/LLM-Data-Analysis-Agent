import pandas as pd


def clean_data(df: pd.DataFrame, return_report: bool = False):
    """
    Data cleaning pipeline.

    Cleaning steps:
    1. Remove duplicate rows
    2. Remove completely empty columns
    3. Fill missing numeric values with the median
    4. Fill missing text values with the mode

    Parameters
    ----------
    df : pd.DataFrame
        Original dataset.

    return_report : bool
        If True, return both cleaned dataframe and cleaning report.
        If False, only return cleaned dataframe.

    Returns
    -------
    pd.DataFrame
        Cleaned dataframe.

    OR

    tuple[pd.DataFrame, dict]
        Cleaned dataframe and cleaning report.
    """

    # Make a copy so the original dataframe is not modified
    df = df.copy()

    # ==============================
    # Basic information
    # ==============================

    original_rows = len(df)
    original_columns = len(df.columns)

    # Count missing values before cleaning
    original_missing_values = int(df.isnull().sum().sum())

    # ==============================
    # 1. Remove duplicate rows
    # ==============================

    duplicate_rows = int(df.duplicated().sum())

    df = df.drop_duplicates()

    # ==============================
    # 2. Remove completely empty columns
    # ==============================

    empty_columns = [
        column
        for column in df.columns
        if df[column].isnull().all()
    ]

    df = df.dropna(axis=1, how="all")

    # ==============================
    # 3. Handle missing values
    # ==============================

    numeric_filled = 0
    categorical_filled = 0

    cleaning_steps = []

    if duplicate_rows > 0:
        cleaning_steps.append(
            f"删除 {duplicate_rows} 条重复记录"
        )

    if empty_columns:
        cleaning_steps.append(
            f"删除 {len(empty_columns)} 个完全为空的字段"
        )

    # Process remaining columns
    for column in df.columns:

        missing_count = int(df[column].isnull().sum())

        if missing_count == 0:
            continue

        # Numeric columns
        if pd.api.types.is_numeric_dtype(df[column]):

            median_value = df[column].median()

            df[column] = df[column].fillna(median_value)

            numeric_filled += missing_count

            cleaning_steps.append(
                f"字段 {column} 的 {missing_count} 个缺失值使用中位数填充"
            )

        # Text / categorical columns
        else:

            mode = df[column].mode()

            if not mode.empty:

                mode_value = mode.iloc[0]

                df[column] = df[column].fillna(mode_value)

                categorical_filled += missing_count

                cleaning_steps.append(
                    f"字段 {column} 的 {missing_count} 个缺失值使用众数填充"
                )

    # ==============================
    # Final information
    # ==============================

    cleaned_rows = len(df)
    cleaned_columns = len(df.columns)

    remaining_missing_values = int(
        df.isnull().sum().sum()
    )

    # ==============================
    # Cleaning report
    # ==============================

    cleaning_report = {
        "original_rows": original_rows,
        "cleaned_rows": cleaned_rows,

        "original_columns": original_columns,
        "cleaned_columns": cleaned_columns,

        "duplicate_rows_removed": duplicate_rows,

        "empty_columns_removed": len(empty_columns),

        "empty_column_names": empty_columns,

        "original_missing_values": original_missing_values,

        "numeric_missing_values_filled": numeric_filled,

        "categorical_missing_values_filled": categorical_filled,

        "remaining_missing_values": remaining_missing_values,

        "cleaning_steps": cleaning_steps,
    }

    # ==============================
    # Return result
    # ==============================

    if return_report:
        return df, cleaning_report

    return df