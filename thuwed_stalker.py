""""
Thuwed Stalker
"""
from urllib.request import urlopen
from datetime import datetime
from bs4 import BeautifulSoup
from dragcave_api import DragCaveAPI

class ThuwedStalker:
    """
        Provides methods for dealing with Thuweds.
    """
    def __init__(self, api: DragCaveAPI) -> None:
        self.api = api

    def find_pairs(self, thuwed_page_url="https://dragcave.net/thuwed"):
        """ Returns a list of pairs of Thuweds in the format [male, female]
        from the /thuwed page """

        with urlopen(thuwed_page_url) as response:
            html = response.read()
            soup = BeautifulSoup(html, 'html.parser')

            pairings = soup.find_all("img", class_="spr")
            print(pairings)

    def examine_clutch(self, code: str, dragcave_date_format='%b %d, %Y'):
        """Examines a dragon's progeny"""
        def get_most_recent(progeny_list):
            # ALGORITHM:
            # We find the most recent date dragons were produced in the progeny
            # by
            # 1. iterating through the list of children
            # 2. fetching their bred dates (aka 'start')
            # 3. converting each date to a timestamp (for easier ordering)
            # 4. finally, selecting the most recent date

            def most_recent_date(progeny_list):
                def date_to_timestamp(child):
                    date = datetime.strptime(child.get("start"), dragcave_date_format)
                    return date.timestamp()

                bred_dates = list(map(date_to_timestamp, progeny_list))
                earliest = max(bred_dates)
                return datetime.fromtimestamp(earliest).strftime(dragcave_date_format)

            # creates a filter function that asserts whether a dragon
            # matches our start date and is a qualified child of our parent
            # dragons
            def make_filter(parent_code: str, start_date: str):
                def filter_function(child):
                    parents = [child.get("parent_m"), child.get("parent_f")]
                    return parent_code in parents and child.get("start") == start_date
                return filter_function

            earliest_date = most_recent_date(progeny_list)
            print("MAX:", earliest_date)

            return list(filter(make_filter(code, earliest_date), progeny_list))

        recent = get_most_recent(self.api.get_children(code))
        print(recent)