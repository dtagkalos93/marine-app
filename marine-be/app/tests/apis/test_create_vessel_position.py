import pytest
from starlette.testclient import TestClient

from app.db.repository.vessel_position_repository import \
    get_vessel_positions_by_vessel_id
from app.db.session import get_db, override_get_db
from app.main import app


@pytest.fixture(scope="session")
def client() -> TestClient:
    app.dependency_overrides[get_db] = override_get_db
    client = TestClient(app)
    return client


def test_vessel_position_have_been_added(client: TestClient) -> None:
    vessel_position = {
        "vessel_id": 23,
        "latitude": 10.3453,
        "longitude": -43.3432,
        "position_time": "2018-01-02 15:52:56.000000",
    }

    response = client.post("/vessel-position/", json=vessel_position)
    assert response.status_code == 201
    db = override_get_db()
    vessel_positions = get_vessel_positions_by_vessel_id(
        vessel_id=vessel_position["vessel_id"], db=db
    )
    print(vessel_positions)
    assert len(vessel_positions) == 1
    assert vessel_positions[0].vessel_id == vessel_position["vessel_id"]
    assert vessel_positions[0].latitude == vessel_position["latitude"]
    assert vessel_positions[0].longitude == vessel_position["longitude"]
    assert (
        vessel_positions[0].position_time.strftime("%Y-%m-%d %H:%M:%S.%f")
        == vessel_position["position_time"]
    )


def test_vessel_position_with_given_invalid_latitude(client: TestClient) -> None:
    vessel_position = {
        "vessel_id": 23,
        "latitude": 100.3453,
        "longitude": -43.3432,
        "position_time": "2018-01-02 15:52:56.000000",
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
        "position_time": "2018-01-02 15:52:56.000000",
    }

    response = client.post("/vessel-position/", json=vessel_position)

    assert response.status_code == 400
    assert response.json() == {
        "detail": "The longitude must be a number between -180 and 180."
    }
