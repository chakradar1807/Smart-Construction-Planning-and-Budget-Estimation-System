from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.project import Project
from app.schemas.risk import RiskResponse
from app.engine.risk_engine import calculate_risks

router = APIRouter(prefix="/projects", tags=["Risk & Safety"])


@router.get("/{project_id}/risks", response_model=RiskResponse)
def get_risks(project_id: int, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    return calculate_risks(
        construction_area=project.construction_area,
        number_of_floors=project.number_of_floors,
        basement=project.basement,
        parking_cars=project.parking_cars,
    )