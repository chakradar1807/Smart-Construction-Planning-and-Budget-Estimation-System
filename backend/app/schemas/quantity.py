from pydantic import BaseModel


class QuantityResponse(BaseModel):
    total_built_up_area: float
    cement_bags: float
    steel_kg: float
    sand_cft: float
    aggregate_cft: float
    bricks_units: float