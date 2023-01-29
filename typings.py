from typing import TypedDict

class Dragon(TypedDict):
    '''
    This class is supposed to match what the API returns.
    '''
    id: str
    name: str
    owner: str or None
    start: str
    hatch: str
    grow: str
    death: str
    views: int
    unique: int
    clicks: int
    gender:  str #"Male" or "Female" or ""
    hoursleft: int
    parent_f: str
    parent_m: str
