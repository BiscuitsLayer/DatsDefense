from api import get_dynamic_objects
from math import sqrt
from models import Location

def dist_sqr(p1: Location, p2: Location):
    return (p1-p2)**2 + (p1-p2)**2

def dist(p1: Location, p2: Location):
    return sqrt(dist_sqr(p1, p2))

def can_attack(bases, loc: Location):
    result = []
    for base in bases:
        if dist_sqr(loc, base.location) <= base.range:
            result.append(base)
    return result
