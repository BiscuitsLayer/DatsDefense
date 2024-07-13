from api import get_dynamic_objects
from math import sqrt
from typing import List
from models import Vec2, Base, Zombie, Map
from utils import get_direction

def dist_sqr(p1: Vec2, p2: Vec2):
    return (p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2

def dist(p1: Vec2, p2: Vec2):
    return sqrt(dist_sqr(p1, p2))

def can_attack(bases: List[Base], loc: Vec2) -> List[str]:
    result = []
    for base in bases:
        if dist_sqr(loc, Vec2(base.x, base.y)) <= base.range ** 2:
            result.append(base.id)
    return result

def rank_normal_zombie(map: Map, zombie: Zombie, depth: int) -> float:
    curr_coord = Vec2(x=zombie.x, y=zombie.y)

    for _ in range(depth):
        curr_coord += get_direction(zombie.direction)


def rank_zombies(map: Map, zombies: List[Zombie], depth: int) -> List[Zombie]:
    result = []
    

def zombie_order() -> List[str]:
    pass