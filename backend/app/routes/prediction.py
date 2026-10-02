
import joblib
import pandas as pd
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.project import Project
from app.schemas.prediction import PredictionResponse
from app.engine.quantity_engine import calculate_quantities

router = APIRouter(prefix="/projects", tags=["ML Prediction"])

cost_model = joblib.load("app/ml/cost_model.joblib")
duration_model = joblib.load("app/ml/duration_model.joblib")


@router.get("/{project_id}/predict", response_model=PredictionResponse)
def predict_cost_duration(
    project_id: int,
    category: str = Query("Standard", enum=["Economy", "Standard", "Premium", "Luxury"]),
    db: Session = Depends(get_db),
):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    quantities = calculate_quantities(
        construction_area=project.construction_area,
        number_of_floors=project.number_of_floors,
        basement=project.basement,
    )

    input_df = pd.DataFrame([{
        "construction_area": project.construction_area,
        "number_of_floors": project.number_of_floors,
        "basement": int(project.basement),
        "location": project.location or "Chennai",
        "category": category,
        "parking_cars": project.parking_cars,
        "total_built_up_area": quantities["total_built_up_area"],
    }])

    predicted_cost = float(cost_model.predict(input_df)[0])
    predicted_duration = float(duration_model.predict(input_df)[0])

    return {
        "predicted_cost": round(predicted_cost, 2),
        "cost_range_low": round(predicted_cost * 0.9, 2),
        "cost_range_high": round(predicted_cost * 1.1, 2),
        "predicted_duration_weeks": round(predicted_duration, 1),
    }