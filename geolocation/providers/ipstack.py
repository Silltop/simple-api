import json
import logging
import os
from typing import Union, Dict, List
from flask import abort
import requests


class IPStackController:
    def __init__(self):
        self.url = "http://api.ipstack.com/"
        self.apikey = os.getenv("IPSTACK_API_KEY", None)

        if self.apikey is None:
            raise ValueError("IPSTACK_API_KEY is not set in environment variables.")
        self.params = {"access_key": self.apikey, "hostname": 1}

    def get_geolocation_for_ip(self, ip_address: str) -> Union[Dict, List]:
        try:
            response = requests.get(f"{self.url}{ip_address}", params=self.params)
            if response.status_code != 200:
                logging.info(f"Failed to get geolocation for IP: {ip_address}, status code: {response.status_code}")
            return response.json()
        except json.JSONDecodeError as e:
            logging.error(f"Malformed JSON response for IP: {ip_address}, error: {e}")
            abort(500, description="Unable to proceed with request, Malformed JSON response from Geolocation provider")
        except requests.exceptions.RequestException as e:
            logging.error(f"Failed to get geolocation for IP: {ip_address}, details: {e}")
            abort(500, description="Unable to proceed with request, Request Exception occurred")
        except Exception as e:
            logging.error(f"Unexpected Error occurred: {e}")
            abort(500, description="Internal server error")
