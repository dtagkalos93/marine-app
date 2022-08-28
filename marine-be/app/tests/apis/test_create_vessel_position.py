from starlette.testclient import TestClient

from app.db.repository.vessel_position_repository import \
    get_vessel_positions_by_vessel_id
from app.db.session import override_get_db


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
        vessel_id=vessel_position["vessel_id"], db=next(db)
    )
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


def test_vessel_positions_with_same_vessel_id_have_valid_travel_should_be_saved(
    client: TestClient,
) -> None:
    vessel_positions = [
        {
            "vessel_id": 23,
            "latitude": 25.768590,
            "longitude": -79.574440,
            "position_time": "2018-01-02 15:52:56.000000",
        },
        {
            "vessel_id": 24,
            "latitude": 15.432443,
            "longitude": -60.431343,
            "position_time": "2018-01-02 15:52:56.000000",
        },
    ]
    for vessel_position in vessel_positions:
        client.post("/vessel-position/", json=vessel_position)
    new_vessel_position = {
        "vessel_id": 23,
        "latitude": 25.778400,
        "longitude": -79.569710,
        "position_time": "2018-01-02 15:56:15.000000",
    }
    response = client.post("/vessel-position/", json=new_vessel_position)
    assert response.status_code == 201
    db = override_get_db()
    vessel_positions = get_vessel_positions_by_vessel_id(
        vessel_id=new_vessel_position["vessel_id"], db=next(db)
    )
    assert len(vessel_positions) == 2


def test_vessel_position_with_same_vessel_id_have_impossible_travel_should_return_error(
    client: TestClient,
) -> None:
    vessel_positions = [
        {
            "vessel_id": 23,
            "latitude": 25.768590,
            "longitude": -79.574440,
            "position_time": "2018-01-02 15:52:56.000000",
        },
        {
            "vessel_id": 24,
            "latitude": 15.432443,
            "longitude": -60.431343,
            "position_time": "2018-01-02 15:52:56.000000",
        },
    ]
    for vessel_position in vessel_positions:
        client.post("/vessel-position/", json=vessel_position)
    new_vessel_position = {
        "vessel_id": 23,
        "latitude": 25.778400,
        "longitude": -80.969710,
        "position_time": "2018-01-02 15:56:15.000000",
    }
    response = client.post("/vessel-position/", json=new_vessel_position)
    assert response.status_code == 400
    assert response.json() == {
        "detail": "The coordinates given define an "
        "impossible travel relative to the last coordinates"
    }
    db = override_get_db()
    vessel_positions = get_vessel_positions_by_vessel_id(
        vessel_id=new_vessel_position["vessel_id"], db=next(db)
    )
    assert len(vessel_positions) == 1
