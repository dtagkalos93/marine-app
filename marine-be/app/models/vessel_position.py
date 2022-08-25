from sqlalchemy import Column, DateTime, Float, Integer

from app.db.base_class import Base


class VesselPosition(Base):
    id = Column(Integer, primary_key=True, index=True)
    vessel_id = Column(Integer, index=True, nullable=False)
    latitude = Column(Float(precision=12), nullable=False)
    longitude = Column(Float(precision=12), nullable=False)
    position_time = Column(DateTime(), nullable=False)
