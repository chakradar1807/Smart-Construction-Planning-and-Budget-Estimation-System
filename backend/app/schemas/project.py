from pydantic import BaseModel
from typing import Optional


class ProjectCreate(BaseModel):
    project_name: str
    location: Optional[str] = None
    total_land_area: float
    construction_area: float
    open_area: Optional[float] = None
    number_of_floors: int = 1
    basement: bool = False
    parking_cars: int = 0


class ProjectResponse(ProjectCreate):
    id: int

    class Config:
        from_attributes = True