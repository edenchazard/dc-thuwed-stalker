""""
Thuwed Stalker
"""
from urllib.request import urlopen
from datetime import datetime
from bs4 import BeautifulSoup
from dragcave_api import DragCaveAPI

class ThuwedScraper:
    """
        Provides methods for dealing with Thuweds.
    """
    def __init__(self, api: DragCaveAPI) -> None:
        self.api = api

    def find_pairs(self, thuwed_page_url="https://dragcave.net/thuwed"):
        """ Returns a list of pairs of Thuweds in the format [male, female]
        from the /thuwed page
        Each pair is in the format of [m code, f code]"""

        # Gets the code for each dragon from a href attribute
        def get_code(element):
            href = element['href']
            return href[href.rindex('/') + 1:]

        # from https://www.geeksforgeeks.org/break-list-chunks-size-n-python/
        def divide_chunks(l, n):
            # looping till length l
            for i in range(0, len(l), n):
                yield l[i:i + n]

        with urlopen(thuwed_page_url) as response:
            soup = BeautifulSoup(response.read(), 'html.parser')

            # Soup will return these in order of left to right, top to bottom
            # so we then need to split them into sets of 2 codes (the male
            # and the female)
            pairings = soup.select("a[href^='/view/']")

            # Make into a list of codes
            codes = [get_code(code) for code in pairings]

            pairs = divide_chunks(codes, 2)
            return list(pairs)

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

                bred_dates = [date_to_timestamp(child) for child in progeny_list]
                earliest = max(bred_dates)
                return datetime.fromtimestamp(earliest).strftime(dragcave_date_format)

            # creates a filter function that asserts whether a dragon
            # matches:
            # 1) our start date
            # 2) is a qualified child of our parent
            # 3) the bred date matches our most recent date
            def is_qualified_child(parent_code: str, start_date: str):
                def filter_function(child):
                    parents = [child.get("parent_m"), child.get("parent_f")]
                    return parent_code in parents and child.get("start") == start_date
                return filter_function

            earliest_date = most_recent_date(progeny_list)
            #print("MAX:", earliest_date)

            return [child for child in progeny_list if is_qualified_child(child, earliest_date)]

        recent = get_most_recent(self.api.get_children(code))
        print(recent)
