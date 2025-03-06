from unittest.mock import patch

import pytest

from api import app
from routes import v1

app.register_blueprint(v1)


@pytest.fixture
def client():

    with app.test_client() as client:
        app.config.update(
            {
                "TESTING": True,
            }
        )
        yield client


@pytest.fixture
def mock_db_ops():
    with patch("routes.db_ops") as mock_db:
        yield mock_db


@pytest.fixture
def mock_geolocation_controller():
    with patch("routes.geolocation_controller") as mock_geo:
        yield mock_geo


def test_add_geolocation(client, mock_geolocation_controller, mock_db_ops):
    """Test the /geolocation/add route"""

    mock_geolocation_controller.batch_geolocate.return_value = {"status": "success", "data": []}
    request_data = {"ips": ["192.168.1.1", "10.0.0.1"], "domains": ["example.com", "anotherdomain.com"]}
    mock_db_ops.add_results_to_db.return_value = None
    response = client.post("/v1/geolocation/add", json=request_data)
    assert response.status_code == 200
    mock_db_ops.add_results_to_db.assert_called_once_with({"status": "success", "data": []})
    assert response.json == {"status": "success", "data": []}


def test_delete_geolocation(client, mock_db_ops):
    """Test the /geolocation/delete route"""
    mock_db_ops.delete_result_from_db.return_value = None
    request_data = {"ips": ["192.168.1.1", "10.0.0.1"]}
    response = client.delete("/v1/geolocation/delete", json=request_data)
    assert response.status_code == 200
    mock_db_ops.delete_result_from_db.assert_called_once_with(["192.168.1.1", "10.0.0.1"])
    assert response.json == {"status": "records removed"}


def test_get_geolocation_get(client, mock_db_ops):
    """Test the /geolocation/get route with GET method"""
    ip = "192.168.1.1"
    mock_db_ops.get_results_from_db.return_value = [{"ip": ip, "location": "USA"}]
    response = client.get("/v1/geolocation/get", query_string={"ip": ip})
    assert response.status_code == 200
    assert response.json == [{"ip": ip, "location": "USA"}]
    mock_db_ops.get_results_from_db.assert_called_once_with([ip])


def test_get_geolocation_post(client, mock_db_ops):
    """Test the /geolocation/get route with POST method"""
    request_data = {"ips": ["192.168.1.1", "10.0.0.1"]}
    mock_db_ops.get_results_from_db.return_value = [{"ip": "192.168.1.1", "location": "USA"}]
    response = client.post("/v1/geolocation/get", json=request_data)
    assert response.status_code == 200
    assert response.json == [{"ip": "192.168.1.1", "location": "USA"}]
    mock_db_ops.get_results_from_db.assert_called_once_with(["192.168.1.1", "10.0.0.1"])
