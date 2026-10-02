from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.project import Project
from app.schemas.cost import CostResponse
from app.engine.quantity_engine import calculate_quantities
from app.engine.cost_engine import calculate_cost

router = APIRouter(prefix="/projects", tags=["Cost"])


@router.get("/{project_id}/cost", response_model=CostResponse)
def get_cost(
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

    return calculate_cost(
        total_built_up_area=quantities["total_built_up_area"],
        category=category,
    )