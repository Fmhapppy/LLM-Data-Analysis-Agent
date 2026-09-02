import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error


def train_regression_model(
    df: pd.DataFrame,
    target_column: str
) -> dict:
    """
    Train a Random Forest regression model
    for numerical prediction.
    """

    numeric_df = df.select_dtypes(include=["number"]).copy()

    if target_column not in numeric_df.columns:
        raise ValueError(
            f"Target column '{target_column}' must be numeric."
        )

    X = numeric_df.drop(columns=[target_column])
    y = numeric_df[target_column]

    if X.empty:
        raise ValueError(
            "At least one numerical feature is required."
        )

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42
    )

    model = RandomForestRegressor(
        n_estimators=100,
        random_state=42
    )

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    mae = mean_absolute_error(y_test, predictions)
    rmse = mean_squared_error(
        y_test,
        predictions
    ) ** 0.5

    feature_importance = dict(
        zip(
            X.columns,
            model.feature_importances_
        )
    )

    return {
        "mae": float(mae),
        "rmse": float(rmse),
        "feature_importance": feature_importance
    }
