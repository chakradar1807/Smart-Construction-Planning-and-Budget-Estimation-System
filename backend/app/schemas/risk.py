from pydantic import BaseModel
from typing import List


class RiskWarning(BaseModel):
    level: str
    category: str
    message: str


class RiskResponse(BaseModel):
    overall_risk: str
    warnings: List[RiskWarning]