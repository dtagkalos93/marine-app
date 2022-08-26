from typing import Any, List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.repository.vessel_position_repository import (
    create_new_vessel_position, get_multi_vessel_positions)
from app.db.session import get_db
from app.schemas.vessel_position import VesselPosition as VesselPositionSchema

router = APIRouter()


@router.post("/", status_code=201, response_model=VesselPositionSchema)
def create_vessel_position(
    vessel_position: VesselPositionSchema, db: Session = Depends(get_db)
) -> Any:
    vessel_position_entry = create_new_vessel_position(vessel_position, db)
    return vessel_position_entry


@router.get("/", response_model=List[VesselPositionSchema])
def get_vessel_positions(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    vessel_positions = get_multi_vessel_positions(db, skip=skip, limit=limit)
    return vessel_positions
