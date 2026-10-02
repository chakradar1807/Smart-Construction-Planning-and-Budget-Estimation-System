from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.project import Project
from app.schemas.quantity import QuantityResponse
from app.engine.quantity_engine import calculate_quantities

router = APIRouter(prefix="/projects", tags=["Quantities"])


@router.get("/{project_id}/quantities", response_model=QuantityResponse)
def get_quantities(project_id: int, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    return calculate_quantities(
        construction_area=project.construction_area,
        number_of_floors=project.number_of_floors,
        basement=project.basement,
    )