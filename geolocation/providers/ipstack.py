import json
import logging
import os
from typing import Dict, List, Union

import requests
from flask import abort


class APIError(Exception):
    pass


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
                logging.error(f"Failed to get geolocation for IP/s: {ip_address}, status code: {response.status_code}")
            json_data = response.json()
            if json_data.get("success", True) is False:
                logging.error(f"Failed to get geolocation for IP: {ip_address}, details: {json_data}")
                raise APIError("Provider error occurred, unable to get proper response with geolocation")
            else:
                return json_data
        except json.JSONDecodeError as e:
            logging.error(f"Malformed JSON response for IP: {ip_address}, error: {e}")
            abort(500, description="Unable to proceed with request, Malformed JSON response from Geolocation provider")
        except requests.exceptions.RequestException as e:
            logging.error(f"Failed to get geolocation for IP: {ip_address}, details: {e}")
            abort(500, description="Unable to proceed with request, Request Exception occurred")
        except APIError as e:
            abort(424, description=str(e))
        except Exception as e:
            logging.error(f"Unexpected Error occurred: {e}")
            abort(500, description="Internal server error")
