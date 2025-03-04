from geolocation.providers.ipstack import IPStackController


class GeolocationController:
    def __init__(self):
        self.providers = [IPStackController]

    def geolocate(self, ip_address):
        for provider in self.providers:
            provider().get_geolocation_for_ip(ip_address)
