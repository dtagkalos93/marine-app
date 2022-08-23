from pydantic import BaseModel


class VesselPosition(BaseModel):
    vessel_id: int
    latitude: float
    longitude: float
    position_time: str
