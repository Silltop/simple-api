from typing import Optional
from flask import abort
from geolocation.providers.ipstack import IPStackController


class GeolocationApiFactory:
    def __init__(self):
        self.providers = {"ipstack": IPStackController}

    def geolocate(self, ip_address: str, provider: str = "ipstack") -> list:
        if provider not in self.providers:
            raise ValueError(f"Configured provider - {provider} not found.")
        else:
            return [self.providers[provider]().get_geolocation_for_ip(ip_address)]

    def batch_geolocate(self, ip_addresses: list, provider: str = "ipstack") -> list:
        if provider not in self.providers:
            raise ValueError(f"Configured provider - {provider} not found.")
        # current provider only requires comma separated list of IPs
        ip_list = ",".join(ip_addresses)
        response_data = self.providers[provider]().get_geolocation_for_ip(ip_list)
        if isinstance(response_data, dict):
            return [response_data]
        return response_data
