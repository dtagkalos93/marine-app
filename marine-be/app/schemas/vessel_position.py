from datetime import datetime

from pydantic import BaseModel, validator

from app.exceptions import InvalidLatitude, InvalidLongitude


class VesselPosition(BaseModel):
    vessel_id: int
    latitude: float
    longitude: float
    position_time: datetime

    class Config:
        json_encoders = {
            # custom output conversion for datetime
            datetime: lambda v: v.strftime("%Y-%m-%d %H:%M:%S.%f")
        }
        orm_mode = True

    @validator("latitude", pre=True)
    def valid_latitude(cls, latitude: float) -> float:
        if not (-90.0 <= latitude <= 90.0):
            raise InvalidLatitude("The latitude must be a number between -90 and 90.")
        return latitude

    @validator("longitude", pre=True)
    def valid_longitude(cls, longitude: float) -> float:
        if not (-180.0 <= longitude <= 180.0):
            raise InvalidLongitude(
                "The longitude must be a number between -180 and 180."
            )
        return longitude
