from sqlalchemy import Column, Integer, String, Float, Boolean
from app.database import Base


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    project_name = Column(String, nullable=False)
    location = Column(String, nullable=True)

    total_land_area = Column(Float, nullable=False)
    construction_area = Column(Float, nullable=False)
    open_area = Column(Float, nullable=True)

    number_of_floors = Column(Integer, nullable=False, default=1)
    basement = Column(Boolean, default=False)
    parking_cars = Column(Integer, default=0)