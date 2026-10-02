from pydantic import BaseModel


class ConcreteMixInput(BaseModel):
    cement_kg: float
    blast_furnace_slag_kg: float = 0
    fly_ash_kg: float = 0
    water_kg: float
    superplasticizer_kg: float = 0
    coarse_aggregate_kg: float
    fine_aggregate_kg: float
    age_days: int = 28


class ConcreteStrengthResponse(BaseModel):
    predicted_strength_mpa: float
    nearest_grade: str
    water_cement_ratio: float