import unittest
from unittest.mock import MagicMock, patch

from geolocation.geolocation_factory import GeolocationApiFactory


@patch("path_to_your_module.IPStackController")
def test_geolocate_success(self, MockIPStackController):
    # Arrange
    mock_ipstack_controller = MagicMock()
    mock_ipstack_controller().get_geolocation_for_ip.return_value = {"country": "US", "city": "New York"}
    MockIPStackController.return_value = mock_ipstack_controller

    factory = GeolocationApiFactory()

    # Act
    result = factory.geolocate("192.168.1.1")

    # Assert
    self.assertEqual(len(result), 1)
    self.assertEqual(result[0], {"country": "US", "city": "New York"})


@patch("path_to_your_module.IPStackController")
def test_batch_geolocate_success(self, MockIPStackController):
    # Arrange
    mock_ipstack_controller = MagicMock()
    mock_ipstack_controller().get_geolocation_for_ip.return_value = [
        {"country": "US", "city": "Los Angeles"},
        {"country": "IN", "city": "Mumbai"},
    ]
    MockIPStackController.return_value = mock_ipstack_controller

    factory = GeolocationApiFactory()

    # Act
    result = factory.batch_geolocate(["192.168.1.1", "8.8.8.8"])

    # Assert
    self.assertEqual(len(result), 2)
    self.assertEqual(result[0], {"country": "US", "city": "Los Angeles"})
    self.assertEqual(result[1], {"country": "IN", "city": "Mumbai"})


def test_geolocate_invalid_provider(self):
    # Arrange
    factory = GeolocationApiFactory()

    # Act & Assert
    with self.assertRaises(ValueError) as context:
        factory.geolocate("192.168.1.1", provider="nonexistent_provider")

    self.assertEqual(str(context.exception), "Configured provider - nonexistent_provider not found.")


def test_batch_geolocate_invalid_provider(self):
    # Arrange
    factory = GeolocationApiFactory()

    # Act & Assert
    with self.assertRaises(ValueError) as context:
        factory.batch_geolocate(["192.168.1.1", "8.8.8.8"], provider="nonexistent_provider")

    self.assertEqual(str(context.exception), "Configured provider - nonexistent_provider not found.")


@patch("path_to_your_module.IPStackController")
def test_batch_geolocate_single_response(self, MockIPStackController):
    # Arrange
    mock_ipstack_controller = MagicMock()
    mock_ipstack_controller().get_geolocation_for_ip.return_value = {"country": "US", "city": "Chicago"}
    MockIPStackController.return_value = mock_ipstack_controller

    factory = GeolocationApiFactory()

    # Act
    result = factory.batch_geolocate(["192.168.1.1"])

    # Assert
    self.assertEqual(len(result), 1)
    self.assertEqual(result[0], {"country": "US", "city": "Chicago"})


@patch("path_to_your_module.IPStackController")
def test_batch_geolocate_non_dict_response(self, MockIPStackController):
    # Arrange
    mock_ipstack_controller = MagicMock()
    mock_ipstack_controller().get_geolocation_for_ip.return_value = ["country", "city"]
    MockIPStackController.return_value = mock_ipstack_controller

    factory = GeolocationApiFactory()

    # Act
    result = factory.batch_geolocate(["192.168.1.1"])

    # Assert
    self.assertEqual(result, ["country", "city"])
