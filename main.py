""""
Main program
"""
from config import get_config
from thuwed_scraper import ThuwedScraper
from dragcave_api import DragCaveAPI

def main(cfg):
    """
    program entry
    """
    dc_api = DragCaveAPI(cfg.get("APIKey"))
    grabber = ThuwedScraper(dc_api)

    # For this to work, we need two sets of data
    # 1 - A list of thuwed pairs
    # 2 - A massview return of thuwed codes
    pairs_as_codes = grabber.find_pairs()

    # TODO for testing purposes, we're only going to fetch data for a set list
    # of codes for now.
    thuweds = dc_api.get_massview(set(["mdCF", "HAEc", "pf13", "9tfz"]))

    def assign_dragon_data(code):
        """
        Here, we'll search our thuweds data for a matching code
        and assign the data from it to our array
        """
        if thuweds.get(code):
            return thuweds.get(code)
        else:
            return ''

    # Loop through every pair and assign data from thuweds to each dragon
    pairs = list(map(lambda pair: {
        "m": assign_dragon_data(pair[0]),
        "f": assign_dragon_data(pair[1])
    }, pairs_as_codes))

    print(pairs)

    # codes = ["ZTJsh"]
    # for code in codes:
    #     grabber.examineProgeny(code)

main(get_config())
