from typing import Any

import geopy.distance
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.repository.vessel_position_repository import (
    create_new_vessel_position, get_latest_vessel_position_by_vessel_id,
    get_multi_vessel_positions, get_total_of_vessel_positions)
from app.db.session import get_db
from app.exceptions import InvalidTravel
from app.schemas.vessel_position import VesselPosition as VesselPositionSchema
from app.schemas.vessel_position import VesselPositionResponse

router = APIRouter()
MAXIMUM_KM_PER_MIN = 0.5


def valid_travel(db: Session, new_vessel_position: VesselPositionSchema) -> bool:
    """
    This function is responsibly to valid that the new coordinates is not
    impossible travel.We assume that a vessel can travel up to 0.5 kilometers
    per minute, so we make proper calculations and validation. If that is correct
    will return True else it will an impossible travel, so it will return False.
    :param db:
    :param new_vessel_position:
    :return:
    """
    latest_vessel_position = get_latest_vessel_position_by_vessel_id(
        db, new_vessel_position.vessel_id
    )
    if latest_vessel_position:
        latest_coordinates = (
            latest_vessel_position.latitude,
            latest_vessel_position.longitude,
        )
        new_coordinates = (new_vessel_position.latitude, new_vessel_position.longitude)
        distance = geopy.distance.distance(latest_coordinates, new_coordinates).km

        time_diff = (
            new_vessel_position.position_time - latest_vessel_position.position_time
        ).total_seconds() / 60.0

        distance_tolerant = time_diff * MAXIMUM_KM_PER_MIN
        if distance > distance_tolerant:
            return False
    return True


@router.post("/", status_code=201, response_model=VesselPositionSchema)
def create_vessel_position(
    vessel_position: VesselPositionSchema, db: Session = Depends(get_db)
) -> Any:
    if not valid_travel(db, vessel_position):
        raise InvalidTravel(
            "The coordinates given define an impossible "
            "travel relative to the last coordinates"
        )
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
