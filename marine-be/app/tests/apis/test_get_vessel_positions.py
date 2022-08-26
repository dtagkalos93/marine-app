import json

from starlette.testclient import TestClient


def test_should_return_empty_list_if_no_data_in_db(client: TestClient):
    response = client.get("/vessel-position/")
    assert response.status_code == 200
    assert json.loads(response.text) == []


def test_should_return_first_element_if_limit_is_one(client: TestClient):
    vessel_positions = [
        {
            "vessel_id": 23,
            "latitude": 10.3453,
            "longitude": -43.3432,
            "position_time": "2018-01-02 15:52:56.000000",
        },
        {
            "vessel_id": 23,
            "latitude": 15.432443,
            "longitude": -60.431343,
            "position_time": "2018-01-02 15:52:56.000000",
        },
    ]
    for vessel_position in vessel_positions:
        client.post("/vessel-position/", json=vessel_position)

    response = client.get("/vessel-position?limit=1")
    vessel_positions_resp = json.loads(response.text)
    assert response.status_code == 200
    assert len(vessel_positions_resp) == 1
    assert vessel_positions_resp[0] == vessel_positions[0]


def test_should_return_second_element_if_limit_is_one(client: TestClient):
    vessel_positions = [
        {
            "vessel_id": 23,
            "latitude": 10.3453,
            "longitude": -43.3432,
            "position_time": "2018-01-02 15:52:56.000000",
        },
        {
            "vessel_id": 23,
            "latitude": 15.432443,
            "longitude": -60.431343,
            "position_time": "2018-01-03 15:52:56.000000",
        },
    ]
    for vessel_position in vessel_positions:
        client.post("/vessel-position/", json=vessel_position)

    response = client.get("/vessel-position?limit=1&skip=1")
    vessel_positions_resp = json.loads(response.text)
    assert response.status_code == 200
    print(response.text)
    assert len(vessel_positions_resp) == 1
    assert vessel_positions_resp[0] == vessel_positions[1]


def test_should_return_all_elements_with_default_offset(client: TestClient):
    vessel_positions = [
        {
            "vessel_id": 23,
            "latitude": 10.3453,
            "longitude": -43.3432,
            "position_time": "2018-01-02 15:52:56.000000",
        },
        {
            "vessel_id": 23,
            "latitude": 15.432443,
            "longitude": -60.431343,
            "position_time": "2018-01-03 15:52:56.000000",
        },
    ]
    for vessel_position in vessel_positions:
        client.post("/vessel-position/", json=vessel_position)

    response = client.get("/vessel-position")
    vessel_positions_resp = json.loads(response.text)
    assert response.status_code == 200
    assert len(vessel_positions_resp) == 2
    assert vessel_positions_resp[0] == vessel_positions[0]
    assert vessel_positions_resp[1] == vessel_positions[1]
