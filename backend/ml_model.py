"""
Machine Learning Module - V2

This module provides a reproducible regression pipeline for the
LLM-Based Intelligent Data Analysis Agent.

V2 improvements:
1. Linear Regression baseline
2. Random Forest regression
3. Train/Test evaluation
4. R² metric
5. K-Fold Cross Validation
6. Model comparison
7. Feature importance
8. Prediction / residual analysis
9. Backward-compatible output fields

The module is intentionally designed to keep compatibility with
the existing API:

    train_regression_model(df, target_column)
"""

from typing import Dict, Any, Tuple

import numpy as np
import pandas as pd

from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score,
)
from sklearn.model_selection import (
    train_test_split,
    KFold,
    cross_validate,
)


# ============================================================
# Configuration
# ============================================================

RANDOM_STATE = 42

TEST_SIZE = 0.2

DEFAULT_CV_FOLDS = 5

RANDOM_FOREST_ESTIMATORS = 100


# ============================================================
# Utility Functions
# ============================================================

def _calculate_regression_metrics(
    y_true: pd.Series,
    y_pred: np.ndarray,
) -> Dict[str, float]:
    """
    Calculate standard regression metrics.

    Returns:
        mae
        rmse
        r2
    """

    mae = mean_absolute_error(
        y_true,
        y_pred
    )

    rmse = np.sqrt(
        mean_squared_error(
            y_true,
            y_pred
        )
    )

    r2 = r2_score(
        y_true,
        y_pred
    )

    return {
        "mae": float(mae),
        "rmse": float(rmse),
        "r2": float(r2),
    }


def _build_random_forest() -> RandomForestRegressor:
    """
    Create a reproducible Random Forest regressor.
    """

    return RandomForestRegressor(
        n_estimators=RANDOM_FOREST_ESTIMATORS,
        random_state=RANDOM_STATE,
        n_jobs=-1,
    )


def _prepare_numeric_data(
    df: pd.DataFrame,
    target_column: str,
) -> Tuple[pd.DataFrame, pd.Series]:
    """
    Select numerical features and validate the target column.
    """

    if target_column not in df.columns:
        raise ValueError(
            f"Target column '{target_column}' "
            f"does not exist in the dataset."
        )

    numeric_df = (
        df
        .select_dtypes(include=["number"])
        .copy()
    )

    if target_column not in numeric_df.columns:
        raise ValueError(
            f"Target column '{target_column}' "
            f"must be numeric."
        )

    X = (
        numeric_df
        .drop(columns=[target_column])
        .copy()
    )

    y = (
        numeric_df[target_column]
        .copy()
    )

    if X.empty:
        raise ValueError(
            "At least one numerical feature "
            "is required for regression."
        )

    # --------------------------------------------------------
    # Remove rows containing NaN / infinite values.
    #
    # Normally data_cleaner.py should already handle this,
    # but this safeguard prevents ML failure if dirty data
    # reaches this module.
    # --------------------------------------------------------

    X = X.replace(
        [np.inf, -np.inf],
        np.nan
    )

    y = y.replace(
        [np.inf, -np.inf],
        np.nan
    )

    valid_mask = (
        X.notna().all(axis=1)
        & y.notna()
    )

    X = X.loc[valid_mask]
    y = y.loc[valid_mask]

    if len(X) < 10:
        raise ValueError(
            "Not enough valid observations for "
            "reliable regression analysis. "
            f"Only {len(X)} valid rows remain."
        )

    return X, y


# ============================================================
# Cross Validation
# ============================================================

def _cross_validate_model(
    model,
    X: pd.DataFrame,
    y: pd.Series,
    n_splits: int = DEFAULT_CV_FOLDS,
) -> Dict[str, Any]:
    """
    Perform K-Fold Cross Validation.

    Uses negative MAE / negative MSE because that is the
    convention used by sklearn's scoring API.
    """

    # --------------------------------------------------------
    # Prevent invalid CV configuration for small datasets.
    # --------------------------------------------------------

    actual_splits = min(
        n_splits,
        len(X)
    )

    if actual_splits < 2:
        return {
            "folds": 0,
            "mae_mean": None,
            "mae_std": None,
            "rmse_mean": None,
            "rmse_std": None,
            "r2_mean": None,
            "r2_std": None,
        }

    kfold = KFold(
        n_splits=actual_splits,
        shuffle=True,
        random_state=RANDOM_STATE,
    )

    scores = cross_validate(
        model,
        X,
        y,
        cv=kfold,
        scoring={
            "mae": "neg_mean_absolute_error",
            "mse": "neg_mean_squared_error",
            "r2": "r2",
        },
        n_jobs=-1,
        return_train_score=False,
    )

    mae_scores = -scores["test_mae"]

    rmse_scores = np.sqrt(
        -scores["test_mse"]
    )

    r2_scores = scores["test_r2"]

    return {
        "folds": int(actual_splits),

        "mae_mean": float(
            np.mean(mae_scores)
        ),

        "mae_std": float(
            np.std(
                mae_scores,
                ddof=1
            )
        ) if len(mae_scores) > 1 else 0.0,

        "rmse_mean": float(
            np.mean(rmse_scores)
        ),

        "rmse_std": float(
            np.std(
                rmse_scores,
                ddof=1
            )
        ) if len(rmse_scores) > 1 else 0.0,

        "r2_mean": float(
            np.mean(r2_scores)
        ),

        "r2_std": float(
            np.std(
                r2_scores,
                ddof=1
            )
        ) if len(r2_scores) > 1 else 0.0,
    }


# ============================================================
# Prediction / Error Analysis
# ============================================================

def _build_error_analysis(
    y_true: pd.Series,
    y_pred: np.ndarray,
) -> Dict[str, Any]:
    """
    Build prediction and residual analysis.

    This information can later be used by the LLM Agent
    to reason about model weaknesses.
    """

    actual = np.asarray(
        y_true,
        dtype=float
    )

    predicted = np.asarray(
        y_pred,
        dtype=float
    )

    residuals = (
        actual - predicted
    )

    absolute_errors = np.abs(
        residuals
    )

    if len(actual) == 0:
        return {
            "sample_count": 0,
            "mean_residual": None,
            "mean_absolute_error": None,
            "max_absolute_error": None,
            "max_absolute_error_index": None,
            "over_prediction_count": 0,
            "under_prediction_count": 0,
            "predictions": [],
        }

    worst_index = int(
        np.argmax(
            absolute_errors
        )
    )

    prediction_rows = []

    for i in range(len(actual)):
        prediction_rows.append(
            {
                "index": int(i),
                "actual": float(
                    actual[i]
                ),
                "predicted": float(
                    predicted[i]
                ),
                "residual": float(
                    residuals[i]
                ),
                "absolute_error": float(
                    absolute_errors[i]
                ),
            }
        )

    return {
        "sample_count": int(
            len(actual)
        ),

        "mean_residual": float(
            np.mean(residuals)
        ),

        "mean_absolute_error": float(
            np.mean(absolute_errors)
        ),

        "max_absolute_error": float(
            np.max(absolute_errors)
        ),

        "max_absolute_error_index": (
            worst_index
        ),

        "over_prediction_count": int(
            np.sum(residuals < 0)
        ),

        "under_prediction_count": int(
            np.sum(residuals > 0)
        ),

        "predictions": prediction_rows,
    }


# ============================================================
# Main Regression Pipeline
# ============================================================

def train_regression_model(
    df: pd.DataFrame,
    target_column: str,
) -> Dict[str, Any]:
    """
    Train and evaluate regression models.

    V2 pipeline:

        Data
          ↓
        Numeric Feature Selection
          ↓
        Train/Test Split
          ↓
        ┌─────────────────────┐
        │ Linear Regression   │
        │ Random Forest       │
        └─────────────────────┘
          ↓
        Test Set Evaluation
          ↓
        5-Fold Cross Validation
          ↓
        Model Comparison
          ↓
        Feature Importance
          ↓
        Error Analysis

    Args:
        df:
            Cleaned input DataFrame.

        target_column:
            Name of the numerical target variable.

    Returns:
        Dictionary containing:
            - mae
            - rmse
            - r2
            - feature_importance
            - models
            - model_comparison
            - cross_validation
            - error_analysis
            - metadata
    """

    # ========================================================
    # 1. Prepare data
    # ========================================================

    X, y = _prepare_numeric_data(
        df,
        target_column,
    )

    # ========================================================
    # 2. Train/Test Split
    # ========================================================

    X_train, X_test, y_train, y_test = (
        train_test_split(
            X,
            y,
            test_size=TEST_SIZE,
            random_state=RANDOM_STATE,
        )
    )

    # ========================================================
    # 3. Define models
    # ========================================================

    linear_model = (
        LinearRegression()
    )

    random_forest_model = (
        _build_random_forest()
    )

    # ========================================================
    # 4. Train Linear Regression
    # ========================================================

    linear_model.fit(
        X_train,
        y_train,
    )

    linear_predictions = (
        linear_model.predict(
            X_test
        )
    )

    linear_metrics = (
        _calculate_regression_metrics(
            y_test,
            linear_predictions,
        )
    )

    # ========================================================
    # 5. Train Random Forest
    # ========================================================

    random_forest_model.fit(
        X_train,
        y_train,
    )

    rf_predictions = (
        random_forest_model.predict(
            X_test
        )
    )

    rf_metrics = (
        _calculate_regression_metrics(
            y_test,
            rf_predictions,
        )
    )

    # ========================================================
    # 6. Cross Validation
    # ========================================================

    linear_cv = (
        _cross_validate_model(
            LinearRegression(),
            X,
            y,
            DEFAULT_CV_FOLDS,
        )
    )

    rf_cv = (
        _cross_validate_model(
            _build_random_forest(),
            X,
            y,
            DEFAULT_CV_FOLDS,
        )
    )

    # ========================================================
    # 7. Model Comparison
    # ========================================================

    model_comparison = {
        "linear_regression": {
            "test": linear_metrics,
            "cross_validation": linear_cv,
        },

        "random_forest": {
            "test": rf_metrics,
            "cross_validation": rf_cv,
        },
    }

    # ========================================================
    # 8. Determine best model
    #
    # Primary criterion:
    # Cross-validation MAE
    #
    # Lower MAE is better.
    # ========================================================

    if (
        linear_cv["mae_mean"] is not None
        and rf_cv["mae_mean"] is not None
    ):

        if (
            linear_cv["mae_mean"]
            <= rf_cv["mae_mean"]
        ):
            best_model = (
                "linear_regression"
            )
        else:
            best_model = (
                "random_forest"
            )

    else:

        if (
            linear_metrics["mae"]
            <= rf_metrics["mae"]
        ):
            best_model = (
                "linear_regression"
            )
        else:
            best_model = (
                "random_forest"
            )

    # ========================================================
    # 9. Feature Importance
    #
    # Keep Random Forest importance because this was already
    # part of V1 and is useful for the existing frontend/report.
    # ========================================================

    feature_importance = dict(
        zip(
            X.columns.tolist(),
            random_forest_model.feature_importances_,
        )
    )

    # Sort descending.
    feature_importance = dict(
        sorted(
            feature_importance.items(),
            key=lambda item: item[1],
            reverse=True,
        )
    )

    # ========================================================
    # 10. Error Analysis
    #
    # Analyze the Random Forest test predictions because RF
    # is the primary model in the existing project.
    # ========================================================

    error_analysis = (
        _build_error_analysis(
            y_test,
            rf_predictions,
        )
    )

    # ========================================================
    # 11. Feature metadata
    # ========================================================

    feature_count = len(
        X.columns
    )

    sample_count = len(X)

    train_sample_count = len(
        X_train
    )

    test_sample_count = len(
        X_test
    )

    # ========================================================
    # 12. Backward-compatible result
    # ========================================================

    return {

        # ----------------------------------------------------
        # Existing V1 fields
        # ----------------------------------------------------

        "mae": float(
            rf_metrics["mae"]
        ),

        "rmse": float(
            rf_metrics["rmse"]
        ),

        "feature_importance": {
            key: float(value)
            for key, value
            in feature_importance.items()
        },

        # ----------------------------------------------------
        # New V2 metrics
        # ----------------------------------------------------

        "r2": float(
            rf_metrics["r2"]
        ),

        "model_name": (
            "Random Forest"
        ),

        "best_model": (
            best_model
        ),

        # ----------------------------------------------------
        # Individual model results
        # ----------------------------------------------------

        "models": {

            "linear_regression": {
                "mae": float(
                    linear_metrics["mae"]
                ),

                "rmse": float(
                    linear_metrics["rmse"]
                ),

                "r2": float(
                    linear_metrics["r2"]
                ),
            },

            "random_forest": {
                "mae": float(
                    rf_metrics["mae"]
                ),

                "rmse": float(
                    rf_metrics["rmse"]
                ),

                "r2": float(
                    rf_metrics["r2"]
                ),
            },
        },

        # ----------------------------------------------------
        # Model comparison
        # ----------------------------------------------------

        "model_comparison": (
            model_comparison
        ),

        # ----------------------------------------------------
        # Cross Validation
        # ----------------------------------------------------

        "cross_validation": {

            "linear_regression": (
                linear_cv
            ),

            "random_forest": (
                rf_cv
            ),
        },

        # ----------------------------------------------------
        # Error Analysis
        # ----------------------------------------------------

        "error_analysis": (
            error_analysis
        ),

        # ----------------------------------------------------
        # Dataset metadata
        # ----------------------------------------------------

        "metadata": {

            "target_column": (
                target_column
            ),

            "feature_columns": (
                X.columns.tolist()
            ),

            "feature_count": (
                feature_count
            ),

            "sample_count": (
                sample_count
            ),

            "train_sample_count": (
                train_sample_count
            ),

            "test_sample_count": (
                test_sample_count
            ),

            "test_size": (
                TEST_SIZE
            ),

            "random_state": (
                RANDOM_STATE
            ),

            "cv_folds": (
                DEFAULT_CV_FOLDS
            ),
        },
    }