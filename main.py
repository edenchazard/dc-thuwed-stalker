""""
Main program
"""
from config import get_config
from problem_dragons import problem_dragons
from thuwed_scraper import ThuwedScraper
from dragcave_api import DragCaveAPI
from program_utils import flatten_pairs

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
    #thuweds = dc_api.get_massview(set(["mdCF", "HAEc", "pf13", "9tfz"]))

    # Unfortunately TJ has some codes that actually fail the API
    # so we have to filter them from the massview and manually
    # add their data
    thuweds = dc_api.get_massview(problem_dragons.filter_problems(flatten_pairs(pairs_as_codes)))

    def assign_dragon_data(code):
        """
        Here, we'll search our thuweds data for a matching code
        and assign the data from it to our array
        """
        if thuweds.get(code):
            return thuweds.get(code)

        if code in problem_dragons.codes:
            # Not in list? It's probably a 'problem dragon' we have to
            # add manually
            return problem_dragons.problems.get(code)

        raise Exception("UNRECOGNISED DRAGON: " + code)

    # Loop through every pair and assign data to each
    pairs = list(map(lambda pair: {
        "m": assign_dragon_data(pair[0]),
        "f": assign_dragon_data(pair[1])
    }, pairs_as_codes))

    print(pairs)

    # for pair in pairs:
    #   for code in pair:
    #     grabber.examine_progeny(code)

main(get_config())
