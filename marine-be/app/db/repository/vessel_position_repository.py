from decimal import Decimal

from sqlalchemy.orm import Session

from app.models.vessel_position import VesselPosition as VesselPositionDB
from app.schemas.vessel_position import VesselPosition as VesselPositionSchema


def create_new_vessel_position(vessel_position: VesselPositionSchema, db: Session) -> VesselPositionDB:
    vessel_position_db = VesselPositionDB(
        vessel_id=vessel_position.vessel_id,
        latitude=Decimal(vessel_position.latitude),
        longitude=Decimal(vessel_position.longitude),
        position_time=vessel_position.position_time,
    )
    db.add(vessel_position_db)
    db.commit()
    db.refresh(vessel_position_db)
    return vessel_position_db
