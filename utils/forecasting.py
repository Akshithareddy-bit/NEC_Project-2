import joblib
import numpy as np

from sklearn.model_selection import train_test_split

from sklearn.linear_model import LinearRegression

from sklearn.ensemble import RandomForestRegressor

from xgboost import XGBRegressor

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error
)


def train_linear_regression(X, y):

    model = LinearRegression()

    model.fit(X, y)

    return model


def train_random_forest(X, y):

    model = RandomForestRegressor(
        n_estimators=100,
        random_state=42
    )

    model.fit(X, y)

    return model


def train_xgboost(X, y):

    model = XGBRegressor(
        n_estimators=100,
        random_state=42
    )

    model.fit(X, y)

    return model


def evaluate_model(model, X_test, y_test):

    predictions = model.predict(X_test)

    mae = mean_absolute_error(
        y_test,
        predictions
    )

    rmse = np.sqrt(
        mean_squared_error(
            y_test,
            predictions
        )
    )

    mape = np.mean(
        np.abs(
            (y_test - predictions) / y_test
        )
    ) * 100

    accuracy = 100 - mape

    return {
        "MAE": round(mae, 2),
        "RMSE": round(rmse, 2),
        "MAPE": round(mape, 2),
        "Accuracy": round(accuracy, 2)
    }


def save_model(model, filename):

    joblib.dump(
        model,
        filename
    )