""""
Dragcave API
"""
import json
from urllib.request import urlopen

class DragCaveAPI:
    """
    Provides methods for dealing with the dragcave API.
    """
    def __init__(self, api_key: str, api_url="https://dragcave.net/api"):
        self.url = f"{api_url}/{api_key}/json"
        print("Using API url: ", self.url)

    def call_api(self, endpoint: str):
        """
        generic method to call a provided API endpoint
        """
        full_url = self.url + endpoint
        print("Contacting endpoint: ", full_url)
        return urlopen(full_url)

    def get_children(self, code: str):
        """
        Calls the /children endpoint and returns progeny as a dict of
        [code]: { details }
        """
        with self.call_api("/children/" + code) as response:
            progeny = json.loads(response.read()).get('dragons')
            #print(progeny)
            return progeny.values()
