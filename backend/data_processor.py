import pandas as pd


def load_data(file_path: str) -> pd.DataFrame:
    """Load CSV or Excel data."""
    if file_path.endswith(".csv"):
        return pd.read_csv(file_path)

    if file_path.endswith((".xlsx", ".xls")):
        return pd.read_excel(file_path)

    raise ValueError("Unsupported file format")


def get_data_summary(df: pd.DataFrame) -> dict:
    """Generate a basic dataset summary."""
    return {
        "rows": len(df),
        "columns": len(df.columns),
        "column_names": list(df.columns),
        "missing_values": df.isnull().sum().to_dict(),
        "data_types": df.dtypes.astype(str).to_dict(),
    }
