from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from app.database import Base


class StageName(str, enum.Enum):
    layout = "layout"
    foundation = "foundation"
    superstructure = "superstructure"
    finishes = "finishes"
    closing = "closing"


class StageStatus(str, enum.Enum):
    not_started = "not_started"
    in_progress = "in_progress"
    completed = "completed"


class InspectionCategory(str, enum.Enum):
    layout = "layout"
    foundation = "foundation"
    frame_masonry = "frame_masonry"


class InspectionStatus(str, enum.Enum):
    pending = "pending"
    pass_ = "pass"
    fail = "fail"
    na = "na"


class ConstructionStage(Base):
    __tablename__ = "construction_stages"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    stage_name = Column(Enum(StageName), nullable=False)
    status = Column(Enum(StageStatus), default=StageStatus.not_started)
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)

    inspections = relationship("InspectionItem", back_populates="stage", cascade="all, delete-orphan")


class InspectionItem(Base):
    __tablename__ = "inspection_items"

    id = Column(Integer, primary_key=True, index=True)
    stage_id = Column(Integer, ForeignKey("construction_stages.id"), nullable=False)
    category = Column(Enum(InspectionCategory), nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    status = Column(Enum(InspectionStatus), default=InspectionStatus.pending)
    inspector_name = Column(String, nullable=True)
    inspected_at = Column(DateTime, nullable=True)
    notes = Column(Text, nullable=True)

    stage = relationship("ConstructionStage", back_populates="inspections")
    photos = relationship("InspectionPhoto", back_populates="inspection_item", cascade="all, delete-orphan")


class InspectionPhoto(Base):
    __tablename__ = "inspection_photos"

    id = Column(Integer, primary_key=True, index=True)
    inspection_item_id = Column(Integer, ForeignKey("inspection_items.id"), nullable=False)
    file_path = Column(String, nullable=False)
    uploaded_at = Column(DateTime, default=datetime.utcnow)

    inspection_item = relationship("InspectionItem", back_populates="photos")