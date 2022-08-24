from fastapi import APIRouter

from app.data import VESSEL_POSITIONS
from app.schemas.vessel_position import VesselPosition

router = APIRouter()


@router.post("/", status_code=201, response_model=VesselPosition)
def create_vessel_position(vessel_position: VesselPosition) -> VesselPosition:

    vessel_position_entry = VesselPosition(
        vessel_id=vessel_position.vessel_id,
        latitude=vessel_position.latitude,
        longitude=vessel_position.longitude,
        position_time=vessel_position.position_time,
    )
    VESSEL_POSITIONS.append(vessel_position_entry.dict())

    return vessel_position_entry
