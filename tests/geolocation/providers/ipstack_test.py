import json
from unittest.mock import patch

import pytest
import requests

from geolocation.providers.ipstack import IPStackController


@patch("os.getenv")
@patch("geolocation.providers.ipstack.requests.get")
def test_successful_response(mock_get, mock_getenv):
    mock_getenv.return_value = "test"
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"country": "US", "city": "New York"}
    controller = IPStackController()
    result = controller.get_geolocation_for_ip("some_ip")
    assert result == {"country": "US", "city": "New York"}


@patch("os.getenv")
@patch("geolocation.providers.ipstack.requests.get")
def test_malformed_json_response(mock_get, mock_getenv):
    mock_getenv.return_value = "test"
    mock_get.side_effect = json.JSONDecodeError
    controller = IPStackController()
    with pytest.raises(Exception) as context:
        controller.get_geolocation_for_ip("some_ip")
    assert "Internal server error" in str(context.value)


@patch("os.getenv")
@patch("geolocation.providers.ipstack.requests.get")
def test_request_exception(mock_get, mock_getenv):
    mock_getenv.return_value = "test"
    mock_get.side_effect = requests.exceptions.RequestException
    controller = IPStackController()
    with pytest.raises(Exception) as context:
        controller.get_geolocation_for_ip("some_ip")
    assert "500 Internal Server Error: Unable to proceed with request" in str(context.value)


@patch("os.getenv")
@patch("geolocation.providers.ipstack.requests.get")
def test_unexpected_error(mock_get, mock_getenv):
    mock_getenv.return_value = "test"
    mock_get.side_effect = ConnectionRefusedError
    controller = IPStackController()
    with pytest.raises(Exception) as context:
        controller.get_geolocation_for_ip("some_ip")
    assert "500 Internal Server Error" in str(context.value)
