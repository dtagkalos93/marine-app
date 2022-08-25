from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.repository.vessel_position_repository import \
    create_new_vessel_position
from app.db.session import get_db
from app.models.vessel_position import VesselPosition as VesselPositionDB
from app.schemas.vessel_position import VesselPosition as VesselPositionSchema

router = APIRouter()


@router.post("/", status_code=201, response_model=VesselPositionSchema)
def create_vessel_position(
    vessel_position: VesselPositionSchema, db: Session = Depends(get_db)
) -> VesselPositionDB:
    vessel_position_entry = create_new_vessel_position(vessel_position, db)
    return vessel_position_entry
