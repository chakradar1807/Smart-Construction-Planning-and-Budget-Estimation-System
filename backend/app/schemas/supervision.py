from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from app.models.supervision import StageName, StageStatus, InspectionCategory, InspectionStatus


class InspectionPhotoResponse(BaseModel):
    id: int
    file_path: str
    uploaded_at: datetime

    class Config:
        from_attributes = True


class InspectionItemCreate(BaseModel):
    category: InspectionCategory
    title: str
    description: Optional[str] = None


class InspectionItemUpdate(BaseModel):
    status: Optional[InspectionStatus] = None
    inspector_name: Optional[str] = None
    notes: Optional[str] = None


class InspectionItemResponse(BaseModel):
    id: int
    stage_id: int
    category: InspectionCategory
    title: str
    description: Optional[str] = None
    status: InspectionStatus
    inspector_name: Optional[str] = None
    inspected_at: Optional[datetime] = None
    notes: Optional[str] = None
    photos: List[InspectionPhotoResponse] = []

    class Config:
        from_attributes = True


class ConstructionStageResponse(BaseModel):
    id: int
    project_id: int
    stage_name: StageName
    status: StageStatus
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    inspections: List[InspectionItemResponse] = []

    class Config:
        from_attributes = True