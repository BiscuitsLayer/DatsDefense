import os
import logging
from src.models import Base, Location, NeighborType


def get_logger(name):
    """
    Get a logger with the given name
    """
    logger = logging.getLogger(name)
    ch = logging.StreamHandler()
    if os.environ.get("LOGFILE", None):
        filename = os.environ["LOGFILE"] 
        ch = logging.FileHandler(filename)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(ch)
    return logger


def can_attack(loc: Location, bases: list[Base]):
    possible_bases: list[Base] = []

    for base in bases:
        dist_sqr = (base.x - loc.x) ** 2 + (base.y - loc.y) ** 2
        if dist_sqr <= base.range ** 2:
            print(dist_sqr)
            possible_bases.append(base.id)

    return possible_bases



def get_neighbor(loc: Location, type: NeighborType):
    match type:
        case NeighborType.TOP:
            return Location(x=loc.x, y=loc.y+1)
        case NeighborType.TOP_LEFT:
            return Location(x=loc.x-1, y=loc.y+1)
        case NeighborType.TOP_RIGHT:
            return Location(x=loc.x+1, y=loc.y+1)
        case NeighborType.LEFT:
            return Location(x=loc.x-1, y=loc.y)
        case NeighborType.RIGHT:
            return Location(x=loc.x+1, y=loc.y)
        case NeighborType.BOTTOM_LEFT:
            return Location(x=loc.x-1, y=loc.y-1)
        case NeighborType.BOTTOM_RIGHT:
            return Location(x=loc.x+1, y=loc.y-1)
        case NeighborType.BOTTOM:
            return Location(x=loc.x, y=loc.y-1)


def add_build_plan(loc: Location):
    pass