from urllib.request import urlopen
from datetime import datetime
import json
from bs4 import BeautifulSoup
from config import get_config

class DragCaveAPI:
    def __init__(self, APIKey: str, APIUrl="https://dragcave.net/api"):
        self.url = "{url}/{key}/json".format(url=APIUrl, key=APIKey)
        print("Using API url: ", self.url)

    def callAPI(self, endpoint: str):
        fullUrl = self.url + endpoint
        print("Contacting endpoint: ", fullUrl)
        return urlopen(fullUrl)

    def getChildren(self, code: str):
        with self.callAPI("/children/" + code) as response:
            progeny = json.loads(response.read()).get('dragons')
            #print(progeny)
            return progeny.values()

class ThuwedGrabber:
    def __init__(self, API: DragCaveAPI) -> None:
        self.API = API

    """ Returns a list of pairs of Thuweds in the format [male, female]
        from the /thuwed page """
    def findPairs(self, thuwedPageUrl="https://dragcave.net/thuwed"):
        with urlopen(thuwedPageUrl) as response:
            html = response.read()
            soup = BeautifulSoup(html, 'html.parser')

            pairings = soup.find_all("img", class_="spr")
            print(pairings)

    """Examines a dragon's progeny"""
    def examineProgeny(self, code: str, dragCaveDateFormat='%b %d, %Y'):
        def getMostRecentOffsprings(progenyList):
            """
            ALGORITHM:
            We find the most recent date dragons were produced in the progeny
            by
            1. iterating through the list of children
            2. fetching their bred dates (aka 'start')
            3. converting each date to a timestamp (for easier ordering)
            4. finally, selecting the most recent date
            """
            def mostRecentProduce(progenyList):
                def convertDateToTimestamp(child):
                    date = datetime.strptime(child.get("start"), dragCaveDateFormat)
                    return date.timestamp()

                bredDates = list(map(convertDateToTimestamp, progenyList))
                earliest = max(bredDates)
                return datetime.fromtimestamp(earliest).strftime(dragCaveDateFormat)

            """ creates a filter function that asserts whether a dragon
            matches our start date and is a qualified child of our parent
            dragons """
            def makeFilter(parentCode: str, startDate: str):
                def filterFunction(child):
                    parents = [child.get("parent_m"), child.get("parent_f")]
                    return parentCode in parents and child.get("start") == startDate
                return filterFunction

            earliestDate = mostRecentProduce(progenyList)
            print("MAX:", earliestDate)
    
            return list(filter(makeFilter(code, earliestDate), progenyList))

        recent = getMostRecentOffsprings(self.API.getChildren(code))
        print(recent)

def main(cfg):
    dCAPI = DragCaveAPI(cfg.get("APIKey"))
    grabber = ThuwedGrabber(dCAPI)

    # TODO automate script to grab codes, for testing purposes we use these.
    grabber.findPairs()
    """  codes = ["ZTJsh"]
    for code in codes:
        grabber.examineProgeny(code) """

main(get_config())