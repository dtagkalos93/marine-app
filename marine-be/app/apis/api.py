from fastapi import APIRouter

from app.apis.endpoints import vessel_position

api_router = APIRouter()
api_router.include_router(vessel_position.router, prefix="/vessel-position")
