import pytest
from starlette.testclient import TestClient

from app.data import VESSEL_POSITIONS
from app.main import app
from app.schemas.vessel_position import VesselPosition


@pytest.fixture(scope="session")
def client() -> TestClient:
    client = TestClient(app)
    return client


def test_vessel_position_have_been_added(client: TestClient) -> None:
    vessel_position = {
        "vessel_id": 23,
        "latitude": 10.3453,
        "longitude": -43.3432,
        "position_time": "2018-01-02 15:52:56.000000"
    }

    client.post("/vessel-position/", json=vessel_position)

    assert len(VESSEL_POSITIONS) == 1
    assert VESSEL_POSITIONS[0] == VesselPosition(**vessel_position)


def test_vessel_position_with_given_invalid_latitude(client: TestClient) -> None:
    vessel_position = {
        "vessel_id": 23,
        "latitude": 100.3453,
        "longitude": -43.3432,
        "position_time": "2018-01-02 15:52:56.000000"
    }

    response = client.post("/vessel-position/", json=vessel_position)

    assert response.status_code == 400
    assert response.json() == {
        "detail": "The latitude must be a number between -90 and 90."
    }


def test_vessel_position_with_given_invalid_longitude(client: TestClient) -> None:
    vessel_position = {
        "vessel_id": 23,
        "latitude": 10.3453,
        "longitude": -243.3432,
        "position_time": "2018-01-02 15:52:56.000000"
    }

    response = client.post("/vessel-position/", json=vessel_position)

    assert response.status_code == 400
    assert response.json() == {
        "detail": "The longitude must be a number between -180 and 180."
    }
