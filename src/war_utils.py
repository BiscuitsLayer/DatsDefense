from src.api import get_dynamic_objects
from math import sqrt
from typing import List
from models import Vec2, Base, Zombie, Map, TileType
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
    curr_point = Vec2(x=zombie.x, y=zombie.y)
    direction = get_direction(zombie.direction)

    curr_score = 10.0
    linear_coeff = 0.1
    delta = curr_score * linear_coeff

    for _ in range(depth):
        for _ in range(zombie.speed):
            if not map.bounds.is_point_inside(curr_point):
                return 0.0
            if map.tiles[curr_point.y][curr_point.x] == TileType.BASE:
                return curr_score
            curr_point += direction
        curr_score -= delta
        if curr_score <= 0.0:
            return 0.0
        
    raise RuntimeError("should have returned the value already")

def rank_bomber_zombie(map: Map, zombie: Zombie, depth: int) -> float:
    curr_point = Vec2(x=zombie.x, y=zombie.y)
    direction = get_direction(zombie.direction)

    res_score = 0.0
    curr_score = 10.0
    linear_coeff = 0.1
    delta = curr_score * linear_coeff

    for _ in range(depth):
        for _ in range(zombie.speed):
            if not map.bounds.is_point_inside(curr_point):
                return 0.0
            if map.tiles[curr_point.y][curr_point.x] == TileType.BASE:
                for dy in range(-1, 2):
                    for dx in range (-1, 2):
                        check_point = Vec2(x=curr_point.x+dx, y=curr_point.y+dy)
                        if not map.bounds.is_point_inside(check_point):
                            continue
                        if map.tiles[check_point.y][check_point.x] == TileType.BASE:
                            res_score += curr_score
                return res_score
            curr_point += direction
        curr_score -= delta
        if curr_score <= 0.0:
            return 0.0

    raise RuntimeError("should have returned the value already")


def rank_zombies(map: Map, zombies: List[Zombie], depth: int) -> List[Zombie]:
    result = []
    

def zombie_order() -> List[str]:
    pass
