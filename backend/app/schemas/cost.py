from pydantic import BaseModel


class CostResponse(BaseModel):
    category: str
    rate_range_low: float
    rate_range_high: float
    material_cost: float
    labour_cost: float
    contingency: float
    other_cost: float
    total_cost: float
    cost_per_sqft: float