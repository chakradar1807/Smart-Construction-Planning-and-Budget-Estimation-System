import os
import shutil
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session, joinedload

from app.database import get_db
from app.models.project import Project
from app.models.supervision import (
    ConstructionStage, InspectionItem, InspectionPhoto,
    StageName, StageStatus, InspectionStatus, InspectionCategory
)
from app.schemas.supervision import (
    ConstructionStageResponse, InspectionItemUpdate, InspectionItemResponse
)

router = APIRouter(prefix="/projects", tags=["Construction Supervision"])

UPLOAD_DIR = "app/uploads/inspections"
os.makedirs(UPLOAD_DIR, exist_ok=True)

DEFAULT_CHECKLIST = {
    StageName.layout: [
        (InspectionCategory.layout, "Excavation markings match approved layout"),
        (InspectionCategory.layout, "Plot boundary verified on-site"),
    ],
    StageName.foundation: [
        (InspectionCategory.foundation, "Excavation depth as per drawing"),
        (InspectionCategory.foundation, "Reinforcement steel placement checked"),
        (InspectionCategory.foundation, "Cover blocks placed correctly"),
    ],
    StageName.superstructure: [
        (InspectionCategory.frame_masonry, "Column alignment verified"),
        (InspectionCategory.frame_masonry, "Beam and lintel levels checked"),
        (InspectionCategory.frame_masonry, "Brickwork alignment and bonding reviewed"),
    ],
}


@router.get("/{project_id}/stages", response_model=list[ConstructionStageResponse])
def get_stages(project_id: int, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    stages = (
        db.query(ConstructionStage)
        .options(joinedload(ConstructionStage.inspections).joinedload(InspectionItem.photos))
        .filter(ConstructionStage.project_id == project_id)
        .all()
    )

    if not stages:
        for stage_name in StageName:
            new_stage = ConstructionStage(project_id=project_id, stage_name=stage_name)
            db.add(new_stage)
        db.commit()
        stages = (
            db.query(ConstructionStage)
            .options(joinedload(ConstructionStage.inspections).joinedload(InspectionItem.photos))
            .filter(ConstructionStage.project_id == project_id)
            .all()
        )

    return stages


@router.patch("/{project_id}/stages/{stage_id}/start", response_model=ConstructionStageResponse)
def start_stage(project_id: int, stage_id: int, db: Session = Depends(get_db)):
    stage = db.query(ConstructionStage).filter(ConstructionStage.id == stage_id).first()
    if not stage:
        raise HTTPException(status_code=404, detail="Stage not found")

    if stage.status == StageStatus.not_started:
        stage.status = StageStatus.in_progress
        stage.started_at = datetime.utcnow()

        existing = db.query(InspectionItem).filter(InspectionItem.stage_id == stage_id).count()
        if existing == 0:
            for category, title in DEFAULT_CHECKLIST.get(stage.stage_name, []):
                db.add(InspectionItem(stage_id=stage_id, category=category, title=title))

        db.commit()
        db.refresh(stage)

    return stage


@router.patch("/inspections/{inspection_id}", response_model=InspectionItemResponse)
def update_inspection(inspection_id: int, update: InspectionItemUpdate, db: Session = Depends(get_db)):
    item = db.query(InspectionItem).filter(InspectionItem.id == inspection_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Inspection item not found")

    if update.status is not None:
        item.status = update.status
        item.inspected_at = datetime.utcnow()
    if update.inspector_name is not None:
        item.inspector_name = update.inspector_name
    if update.notes is not None:
        item.notes = update.notes

    db.commit()
    db.refresh(item)

    stage = db.query(ConstructionStage).filter(ConstructionStage.id == item.stage_id).first()
    all_items = db.query(InspectionItem).filter(InspectionItem.stage_id == stage.id).all()
    if all_items and all(i.status in [InspectionStatus.pass_, InspectionStatus.na] for i in all_items):
        stage.status = StageStatus.completed
        stage.completed_at = datetime.utcnow()
        db.commit()

    return item


@router.post("/inspections/{inspection_id}/photos")
def upload_inspection_photo(inspection_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):
    item = db.query(InspectionItem).filter(InspectionItem.id == inspection_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Inspection item not found")

    filename = f"{inspection_id}_{datetime.utcnow().timestamp()}_{file.filename}"
    file_path = os.path.join(UPLOAD_DIR, filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    photo = InspectionPhoto(inspection_item_id=inspection_id, file_path=file_path)
    db.add(photo)
    db.commit()
    db.refresh(photo)

    return {"id": photo.id, "file_path": photo.file_path}