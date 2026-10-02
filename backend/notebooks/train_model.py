"""
Trains ML models to predict construction cost and duration from project features.
Compares Linear Regression vs Random Forest, picks the best performer, and saves it.
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib

# --- Load data ---
df = pd.read_csv("notebooks/training_data.csv")

FEATURES = [
    "construction_area", "number_of_floors", "basement",
    "location", "category", "parking_cars", "total_built_up_area"
]
CATEGORICAL = ["location", "category"]
NUMERIC = [f for f in FEATURES if f not in CATEGORICAL]

X = df[FEATURES]
y_cost = df["total_cost"]
y_duration = df["duration_weeks"]

# --- Preprocessing: one-hot encode categorical columns ---
preprocessor = ColumnTransformer(
    transformers=[
        ("cat", OneHotEncoder(handle_unknown="ignore"), CATEGORICAL),
    ],
    remainder="passthrough"  # keep numeric columns as-is
)


def train_and_evaluate(X, y, target_name):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    models = {
        "LinearRegression": LinearRegression(),
        "RandomForest": RandomForestRegressor(n_estimators=200, random_state=42),
    }

    best_model = None
    best_score = -np.inf
    best_name = None

    print(f"\n=== Training models for: {target_name} ===")
    for name, model in models.items():
        pipeline = Pipeline([
            ("preprocess", preprocessor),
            ("model", model),
        ])
        pipeline.fit(X_train, y_train)
        preds = pipeline.predict(X_test)

        mae = mean_absolute_error(y_test, preds)
        rmse = np.sqrt(mean_squared_error(y_test, preds))
        r2 = r2_score(y_test, preds)

        print(f"{name}: MAE={mae:.2f}  RMSE={rmse:.2f}  R2={r2:.4f}")

        if r2 > best_score:
            best_score = r2
            best_model = pipeline
            best_name = name

    print(f"Best model for {target_name}: {best_name} (R2={best_score:.4f})")
    return best_model


# --- Train cost prediction model ---
cost_model = train_and_evaluate(X, y_cost, "Total Cost")
joblib.dump(cost_model, "app/ml/cost_model.joblib")

# --- Train duration prediction model ---
duration_model = train_and_evaluate(X, y_duration, "Duration (weeks)")
joblib.dump(duration_model, "app/ml/duration_model.joblib")

print("\nModels saved to app/ml/")