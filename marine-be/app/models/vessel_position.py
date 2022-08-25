from sqlalchemy import Column, DateTime, Float, Integer

from app.db.base_class import Base


class VesselPosition(Base):
    id = Column(Integer, primary_key=True, index=True)
    vessel_id = Column(Integer, index=True)
    latitude = Column(Float(precision=12))
    longitude = Column(Float(precision=12))
    position_time = Column(DateTime())
