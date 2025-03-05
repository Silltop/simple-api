import unittest
from unittest.mock import MagicMock, patch

import pytest

from geolocation.geolocation_factory import GeolocationApiFactory


@patch("os.getenv")
@patch("geolocation.providers.ipstack.IPStackController.get_geolocation_for_ip")
def test_geolocate_success(mock_get_geolocation_for_ip, mock_getenv):
    mock_getenv.return_value = "test"
    mock_get_geolocation_for_ip.return_value = {"country": "US", "city": "New York"}
    factory = GeolocationApiFactory()
    result = factory.geolocate("192.168.1.1")
    assert result == [{"country": "US", "city": "New York"}]


def test_geolocate_invalid_provider():
    factory = GeolocationApiFactory()
    with pytest.raises(Exception) as context:
        factory.geolocate("192.168.1.1", provider="nonexistent_provider")
    assert str(context.value) == "Configured provider - nonexistent_provider not found."


@patch("os.getenv")
@patch("geolocation.providers.ipstack.IPStackController.get_geolocation_for_ip")
def test_batch_geolocate_non_dict_response(mock_get_geolocation_for_ip, mock_getenv):
    mock_getenv.return_value = "test"
    mock_get_geolocation_for_ip.return_value = ["country", "city"]
    factory = GeolocationApiFactory()
    result = factory.batch_geolocate(["192.168.1.1"])
    assert result == ["country", "city"]
