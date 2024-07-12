from api import get_dynamic_objects
from math import sqrt
from typing import List
from models import Location, Base, Zombie

def dist_sqr(p1: Location, p2: Location):
    return (p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2

def dist(p1: Location, p2: Location):
    return sqrt(dist_sqr(p1, p2))

def can_attack(bases: List[Base], loc: Location) -> List[str]:
    result = []
    for base in bases:
        if dist_sqr(loc, Location(base.x, base.y)) <= base.range ** 2:
            result.append(base.id)
    return result

def rank_zombies(zombies: List[Zombie]) -> List[Zombie]:
    result = []

def zombie_order() -> List[str]:
    pass