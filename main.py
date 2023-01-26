""""
Main program
"""
from config import get_config
from thuwed_stalker import ThuwedStalker
from dragcave_api import DragCaveAPI

def main(cfg):
    """
    program entry
    """
    dc_api = DragCaveAPI(cfg.get("APIKey"))
    grabber = ThuwedStalker(dc_api)
    grabber.find_pairs()

    # TODO automate script to grab codes, for testing purposes we use these.
    #grabber.findPairs()
    # codes = ["ZTJsh"]
    # for code in codes:
    #     grabber.examineProgeny(code)

main(get_config())
