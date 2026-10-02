from pydantic import BaseModel


class PredictionResponse(BaseModel):
    predicted_cost: float
    cost_range_low: float
    cost_range_high: float
    predicted_duration_weeks: float