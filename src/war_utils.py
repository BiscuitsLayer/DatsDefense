from math import sqrt
from typing import List, Tuple

from src.api import get_dynamic_objects
from src.models import Vec2, Base, Zombie, Map, TileType
from src.utils import get_direction
from src.knight_offsets import KNIGHT_OFFSETS

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

    curr_score = zombie.attack
    linear_coeff = 1 / depth
    delta = curr_score * linear_coeff

    for _ in range(depth):
        for _ in range(zombie.speed):
            if not map.bounds.is_point_inside(curr_point):
                return 0.0
            if map.tiles[curr_point.y][curr_point.x] == TileType.BASE:
                return curr_score
            curr_point += direction
        curr_score -= delta

    return 0.0  

def rank_bomber_zombie(map: Map, zombie: Zombie, depth: int) -> float:
    curr_point = Vec2(x=zombie.x, y=zombie.y)
    direction = get_direction(zombie.direction)

    res_score = 0.0
    curr_score = zombie.attack
    linear_coeff = 1 / depth
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

    return res_score


def rank_liner_zombie(map: Map, zombie: Zombie, depth: int) -> float:
    curr_point = Vec2(x=zombie.x, y=zombie.y)
    direction = get_direction(zombie.direction)

    res_score = 0.0
    curr_score = zombie.attack
    linear_coeff = 1 / depth
    delta = curr_score * linear_coeff

    faced_base = False

    last_depth_remain = zombie.speed
    depth_remain = depth

    for i in range(depth):
        for j in range(zombie.speed):
            if not map.bounds.is_point_inside(curr_point):
                return 0.0
            if map.tiles[curr_point.y][curr_point.x] == TileType.BASE:
                faced_base = True
                depth_remain -= i + 1
                last_depth_remain -= j + 1
                break
            curr_point += direction
        if faced_base:
            break
        curr_score -= delta
    
    if not faced_base:
        return 0.0
    
    for _ in range(last_depth_remain):
        if (not map.bounds.is_point_inside(curr_point) or
            map.tiles[curr_point.y][curr_point.x] != TileType.BASE):
            return res_score
        res_score += curr_score
        curr_point += direction
    curr_score -= delta
    
    for _ in range(depth_remain):
        for _ in range(zombie.speed):
            if (not map.bounds.is_point_inside(curr_point) or
                map.tiles[curr_point.y][curr_point.x] != TileType.BASE):
                return res_score
            res_score += curr_score
            curr_point += direction
        curr_score -= delta
    
    return res_score

def rank_juggernaut_zombie(map: Map, zombie: Zombie, depth: int) -> float:
    curr_point = Vec2(x=zombie.x, y=zombie.y)
    direction = get_direction(zombie.direction)

    res_score = 0.0
    curr_score = zombie.attack
    linear_coeff = 1 / depth
    delta = curr_score * linear_coeff

    faced_base = False

    last_depth_remain = zombie.speed
    depth_remain = depth

    for i in range(depth):
        for j in range(zombie.speed):
            if not map.bounds.is_point_inside(curr_point):
                return 0.0
            if map.tiles[curr_point.y][curr_point.x] == TileType.BASE:
                faced_base = True
                depth_remain -= i + 1
                last_depth_remain -= j + 1
                break
            curr_point += direction
        if faced_base:
            break
        curr_score -= delta
    
    if not faced_base:
        return 0.0
    
    for _ in range(last_depth_remain):
        if not map.bounds.is_point_inside(curr_point):
            return res_score
        if map.tiles[curr_point.y][curr_point.x] == TileType.BASE:
            res_score += curr_score
        curr_point += direction
    curr_score -= delta
    
    for _ in range(depth_remain):
        for _ in range(zombie.speed):
            if not map.bounds.is_point_inside(curr_point):
                return res_score
            if map.tiles[curr_point.y][curr_point.x] == TileType.BASE:
                res_score += curr_score
            curr_point += direction
        curr_score -= delta
    
    return res_score


def rank_knight_zombie(map: Map, zombie: Zombie, depth: int) -> float:
    depth = min(depth, 5)

    n_strikes = 0
    res_score = 0
    cur_score = zombie.attack
    for offset in KNIGHT_OFFSETS[depth - 1]:
        to = Vec2(x=zombie.x + offset.x, y=zombie.y + offset.y)
        if not map.bounds.is_point_inside(to):
            continue
        if map.tiles[to.y][to.x] == TileType.BASE:
            n_strikes += 1
            res_score += cur_score
            cur_score *= 0.5

    return 0.5 * res_score

def rank_zombie(map: Map, zombie: Zombie, depth: int) -> float:
    match zombie.type:
        case "normal":
            return rank_normal_zombie(map, zombie, depth)
        case "fast":
            return rank_normal_zombie(map, zombie, depth)
        case "bomber":
            return rank_bomber_zombie(map, zombie, depth)
        case "liner":
            return rank_liner_zombie(map, zombie, depth)
        case "juggernaut":
            return rank_juggernaut_zombie(map, zombie, depth)
        case "chaos_knight":
            return rank_knight_zombie(map, zombie, depth)
        case _:
            raise ValueError("Unknown zombie type: " + zombie.type)

def rank_zombies(map: Map, zombies: List[Zombie], depth: int) -> List[Tuple[float, str]]:
    zombie_score_id = [(rank_zombie(map, zombie, depth), zombie.id) for zombie in zombies]
    sorted(zombie_score_id, key=lambda pair: pair[0], reverse=True)
    return zombie_score_id

def zombie_order() -> List[str]:
    pass
