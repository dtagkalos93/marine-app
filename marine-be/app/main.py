from typing import Dict

from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import JSONResponse

from app.apis.api import api_router
from app.exceptions import InvalidLatitude, InvalidLongitude

app = FastAPI()

app.include_router(api_router)


@app.exception_handler(InvalidLatitude)
@app.exception_handler(InvalidLongitude)
def validation_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    return JSONResponse({"detail": str(exc)}, status_code=422)


@app.get("/")
def root() -> Dict[str, str]:
    return {"message": "Hello World"}
