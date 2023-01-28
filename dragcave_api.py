""""
Dragcave API
"""
import json
from urllib import request, parse

class DragCaveAPI:
    """
    Provides methods for dealing with the dragcave API.
    """
    def __init__(self, api_key: str, api_url="https://dragcave.net/api"):
        self.url = f"{api_url}/{api_key}/json"
        print("Using API url: ", self.url)

    def call_api(self, endpoint: str, data: None or dict=None):
        """
        generic method to call a provided API endpoint
        """
        full_url = self.url + endpoint
        print("Contacting API endpoint: ", full_url)

        encoded_data = parse.urlencode(data).encode() if type(data) == dict else None

        with request.urlopen(request.Request(full_url, data=encoded_data)) as response:
            data = json.loads(response.read())

            # TODO handle errors from DC API
            if data.get('errors'):
                raise Exception(data.get('errors'))
            # Return dragon data
            else:
                return data.get('dragons')

    def get_children(self, code: str):
        """
        Calls the /children endpoint and returns progeny as a dict of
        [code]: { details }
        """
        return self.call_api("/children/" + code)

    def get_massview(self, codes: set):
        """
        Calls the /massview endpoint and returns API information for a list
        of dragons.
        """
        return self.call_api("/massview", data={"ids": ','.join(codes)})