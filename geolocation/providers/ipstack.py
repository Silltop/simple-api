import os


class IPStackController:
    def __init__(self):
        self.url = "http://api.ipstack.com/"
        self.apikey = os.getenv("IPSTACK_API_KEY", None)
        if self.apikey is None:
            raise ValueError("IPSTACK_API_KEY is not set in environment variables.")

    def get_geolocation_for_ip(self, ip_address):
        pass

    def get_geolocation_for_url(self, url):
        pass
