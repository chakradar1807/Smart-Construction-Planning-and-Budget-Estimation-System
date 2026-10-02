import joblib
import pandas as pd
from fastapi import APIRouter

from app.schemas.concrete import ConcreteMixInput, ConcreteStrengthResponse

router = APIRouter(prefix="/concrete", tags=["Concrete Mix Advisor"])

model_data = joblib.load("app/ml/concrete_strength_model.joblib")
model = model_data["model"]
FEATURES = model_data["feature_names"]

GRADES = [10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60]


def nearest_grade(mpa: float) -> str:
    grade = min(GRADES, key=lambda g: abs(g - mpa))
    return f"M{grade}"


@router.post("/predict-strength", response_model=ConcreteStrengthResponse)
def predict_strength(mix: ConcreteMixInput):
    input_df = pd.DataFrame([{
        "cement_kg": mix.cement_kg,
        "blast_furnace_slag_kg": mix.blast_furnace_slag_kg,
        "fly_ash_kg": mix.fly_ash_kg,
        "water_kg": mix.water_kg,
        "superplasticizer_kg": mix.superplasticizer_kg,
        "coarse_aggregate_kg": mix.coarse_aggregate_kg,
        "fine_aggregate_kg": mix.fine_aggregate_kg,
        "age_days": mix.age_days,
    }])[FEATURES]

    predicted = float(model.predict(input_df)[0])
    wc_ratio = round(mix.water_kg / mix.cement_kg, 3) if mix.cement_kg else 0

    return {
        "predicted_strength_mpa": round(predicted, 2),
        "nearest_grade": nearest_grade(predicted),
        "water_cement_ratio": wc_ratio,
    }