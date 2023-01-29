from typing import Set

from typings import Dragon

class ProblemDragons:
    '''
    A class for handling problematic dragons.
    '''
    # Holds data for all problematic dragons
    problems: Set[Dragon] = []
    # A list of codes for problematic dragons we have specified
    codes: Set[str] = []

    def __init__(self, data: Set[Dragon]) -> None:
        self.problems = data
        self.codes = set(self.problems.keys())

    def filter_problems(self, code_list: set) -> Set[str]:
        '''
        Returns a filtered list of codes with problem codes removed.
        '''
        return set(filter(lambda code: code not in self.codes, code_list))

problem_dragons = ProblemDragons({
    # Replacement information
    "BOO": {
        "id": "BOO",
        "name": 'Jxuten Nucboh Thuwed',
        "owner": None,
        "start": 'Oct 31, 2011',
        "hatch": 'Oct 31, 2011',
        "grow": 'Nov 03, 2011',
        "death": "0",
        "views": 40346,
        "unique": 10707,
        "clicks": 5866,
        "gender": "Male",
        "hoursleft": -1,
        "parent_f": "",
        "parent_m": ""
    }
})
