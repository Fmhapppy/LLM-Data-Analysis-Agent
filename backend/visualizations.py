import os

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd

from data_processor import load_data
from data_cleaner import clean_data
from ml_model import train_regression_model


def generate_visualizations(
    df: pd.DataFrame,
    ml_result: dict,
    output_dir: str = "outputs"
) -> dict:
    """
    Generate data analysis visualizations.

    Generated charts:
    1. Correlation heatmap
    2. Study hours vs final score scatter plot
    3. Random Forest feature importance
    """

    # Create output directory
    os.makedirs(output_dir, exist_ok=True)

    # ============================================================
    # 1. Correlation Heatmap
    # ============================================================

    correlation_path = os.path.join(
        output_dir,
        "correlation_heatmap.png"
    )

    numeric_df = df.select_dtypes(include=["number"])

    if numeric_df.shape[1] >= 2:

        correlation = numeric_df.corr()

        plt.figure(figsize=(8, 6))

        plt.imshow(
            correlation,
            cmap="coolwarm",
            vmin=-1,
            vmax=1
        )

        plt.colorbar(label="Correlation")

        plt.xticks(
            range(len(correlation.columns)),
            correlation.columns,
            rotation=45,
            ha="right"
        )

        plt.yticks(
            range(len(correlation.columns)),
            correlation.columns
        )

        # Display correlation values
        for i in range(len(correlation.columns)):
            for j in range(len(correlation.columns)):

                plt.text(
                    j,
                    i,
                    f"{correlation.iloc[i, j]:.2f}",
                    ha="center",
                    va="center"
                )

        plt.title("Correlation Heatmap")

        plt.tight_layout()

        plt.savefig(
            correlation_path,
            dpi=150,
            bbox_inches="tight"
        )

        plt.close()

    # ============================================================
    # 2. Study Hours vs Final Score
    # ============================================================

    scatter_path = os.path.join(
        output_dir,
        "study_hours_vs_final_score.png"
    )

    if (
        "study_hours" in df.columns
        and "final_score" in df.columns
    ):

        plt.figure(figsize=(8, 6))

        plt.scatter(
            df["study_hours"],
            df["final_score"],
            alpha=0.7
        )

        plt.xlabel("Study Hours")

        plt.ylabel("Final Score")

        plt.title(
            "Study Hours vs Final Score"
        )

        plt.grid(alpha=0.3)

        plt.tight_layout()

        plt.savefig(
            scatter_path,
            dpi=150,
            bbox_inches="tight"
        )

        plt.close()

    # ============================================================
    # 3. Random Forest Feature Importance
    # ============================================================

    feature_importance_path = os.path.join(
        output_dir,
        "feature_importance.png"
    )

    feature_importance = ml_result.get(
        "feature_importance",
        {}
    )

    if feature_importance:

        features = list(
            feature_importance.keys()
        )

        importance = list(
            feature_importance.values()
        )

        plt.figure(figsize=(8, 6))

        plt.barh(
            features,
            importance
        )

        plt.xlabel("Importance")

        plt.ylabel("Features")

        plt.title(
            "Random Forest Feature Importance"
        )

        plt.tight_layout()

        plt.savefig(
            feature_importance_path,
            dpi=150,
            bbox_inches="tight"
        )

        plt.close()

    # ============================================================
    # Return generated file paths
    # ============================================================

    return {
        "correlation_heatmap": correlation_path,
        "study_hours_vs_final_score": scatter_path,
        "feature_importance": feature_importance_path
    }


# ================================================================
# Standalone test
# ================================================================

if __name__ == "__main__":

    # The test CSV is stored in backend/uploads
    file_path = "uploads/student_learning_dataset.csv"

    print("Loading dataset...")

    df = load_data(file_path)

    print(
        f"Original dataset shape: {df.shape}"
    )

    print("Cleaning dataset...")

    cleaned_df = clean_data(df)

    print(
        f"Cleaned dataset shape: {cleaned_df.shape}"
    )

    print("Training machine learning model...")

    ml_result = train_regression_model(
        cleaned_df,
        "final_score"
    )

    print("Generating visualizations...")

    result = generate_visualizations(
        cleaned_df,
        ml_result
    )

    print("\nVisualization files generated:")

    for name, path in result.items():

        print(
            f"{name}: {path}"
        )

    print("\nAll visualization tasks completed successfully.")