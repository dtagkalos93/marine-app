from typing import Any

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.repository.vessel_position_repository import (
    create_new_vessel_position, get_multi_vessel_positions,
    get_total_of_vessel_positions)
from app.db.session import get_db
from app.schemas.vessel_position import VesselPosition as VesselPositionSchema
from app.schemas.vessel_position import VesselPositionResponse

router = APIRouter()


@router.post("/", status_code=201, response_model=VesselPositionSchema)
def create_vessel_position(
    vessel_position: VesselPositionSchema, db: Session = Depends(get_db)
) -> Any:
    vessel_position_entry = create_new_vessel_position(vessel_position, db)
    return vessel_position_entry


@router.get("/", response_model=VesselPositionResponse)
def get_vessel_positions(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    vessel_positions = get_multi_vessel_positions(db, skip=skip, limit=limit)
    total_vessel_position = get_total_of_vessel_positions(db)
    print(total_vessel_position)
    return {
        "data": vessel_positions,
        "number_of_pages": total_vessel_position / limit
        if total_vessel_position > limit
        else 1,
        "total_vessel_position": total_vessel_position,
    }
