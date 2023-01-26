"""
Program config
"""
import json

def get_config():
    """
    Returns program configuration as a dict.
    """
    with open("./config.json", "r", encoding="utf8") as config_file:
        return json.load(config_file)
