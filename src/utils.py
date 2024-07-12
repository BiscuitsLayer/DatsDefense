import os
import logging
from src.models import Base, Vec2


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


def can_attack(loc: Vec2, bases: list[Base]):
    possible_bases: list[Base] = []

    for base in bases:
        dist_sqr = (base.x - loc.x) ** 2 + (base.y - loc.y) ** 2
        if dist_sqr <= base.range ** 2:
            print(dist_sqr)
            possible_bases.append(base.id)

    return possible_bases


def add_build_plan(loc: Vec2):
    pass