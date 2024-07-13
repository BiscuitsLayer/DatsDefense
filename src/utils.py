import os
import logging
from src.models import Base, Vec2, NeighborType, Map, TileType, Zombie, EnemyBase
from typing import List
from war_utils import dist_sqr_casual as dist

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

def get_neighbor(loc: Vec2, type: NeighborType):
    match type:
        case NeighborType.TOP:
            return Vec2(x=loc.x, y=loc.y+1)
        case NeighborType.TOP_LEFT:
            return Vec2(x=loc.x-1, y=loc.y+1)
        case NeighborType.TOP_RIGHT:
            return Vec2(x=loc.x+1, y=loc.y+1)
        case NeighborType.LEFT:
            return Vec2(x=loc.x-1, y=loc.y)
        case NeighborType.RIGHT:
            return Vec2(x=loc.x+1, y=loc.y)
        case NeighborType.BOTTOM_LEFT:
            return Vec2(x=loc.x-1, y=loc.y-1)
        case NeighborType.BOTTOM_RIGHT:
            return Vec2(x=loc.x+1, y=loc.y-1)
        case NeighborType.BOTTOM:
            return Vec2(x=loc.x, y=loc.y-1)

def get_tile_type(loc: Vec2, map: Map):
    return map.tiles[loc.x][loc.y]

def can_build_here(loc: Vec2, map: Map, zombies: List[Zombie]):
    direct_neighbours = [get_tile_type(get_neighbor(loc, type_)) for type_ \
                         in [NeighborType.TOP, NeighborType.LEFT, NeighborType.RIGHT, NeighborType.BOTTOM]]
    no_bad_direct_neighbours = (TileType.ENEMY_BASE not in direct_neighbours) and (TileType.WALL not in direct_neighbours)
    if not no_bad_direct_neighbours:
        return False
    
    spot_free = (get_tile_type(loc) not in [TileType.BASE, TileType.ENEMY_BASE, TileType.WALL]) and (loc not in zombies)
    if not spot_free:
        return False
    
    diagonal_neighbours = [get_tile_type(get_neighbor(loc, type_)) for type_ \
                         in [NeighborType.TOP_RIGHT, NeighborType.TOP_LEFT, NeighborType.BOTTOM_RIGHT, NeighborType.BOTTOM_LEFT]]
    no_diagonal_enemy = TileType.ENEMY_BASE not in diagonal_neighbours
    if not no_diagonal_enemy:
        return False
    return True

def add_build_plan(loc: Vec2):
    pass

def sign(num):
    return -1 if num < 0 else 1

def get_build_plan(bases: List[Base], enemy_bases: List[EnemyBase], map: Map, zombies: List[Zombie]):
    # bases, enemy_bases, zombies = ... #get_dynamic_objects()
    # world = ... #get_static_objects()

    bases_coords = [[base.x, base.y] for base in bases]
    enemy_coords = [[base.x, base.y] for base in enemy_bases]

    geom_center = [sum([x[0] for x in bases_coords])/len(bases_coords),
                   sum([x[1] for x in bases_coords])/len(bases_coords)]
    closest_enemy_coords = sorted(enemy_coords, key=lambda x: dist(x, geom_center))[0]
    # dists_to_enemy = [dist(geom_center, enemy_coord) for enemy_coord in enemy_coords]
    # closest_enemy_coords = enemy_coords[min(range(len(dists_to_enemy)), key=dists_to_enemy.__getitem__)]
    # dists_to_closest_enemy = [dist(closest_enemy_coords, base_coord) for base_coord in bases_coords]
    sorted_closest_to_enemy_coords = sorted(bases_coords, key=lambda x: dist(x, closest_enemy_coords))
    # closest_to_enemy_coords = bases_coords[min(range(len(dists_to_closest_enemy)), key=dists_to_closest_enemy.__getitem__)]
    closest_to_enemy_ind = 0
    closest_to_enemy_coords = sorted_closest_to_enemy_coords[closest_to_enemy_ind]
    build_direction = [(closest_enemy_coords[0] - closest_to_enemy_coords[0]),
                       (closest_enemy_coords[0] - closest_to_enemy_coords[0])]
    build_coords_list = list()
    for _ in range(0, 3):
        not_checked_go_x = True
        if abs(build_direction[0]) > abs(build_direction[1]):
            build_coords = [closest_to_enemy_coords[0] + sign(build_direction[0]),
                            closest_to_enemy_coords[1]]
            if can_build_here(build_coords, map, zombies):
                build_coords_list.append(build_coords)
                continue
            not_checked_go_x = False
        else:
            build_coords = [closest_to_enemy_coords[0],
                            closest_to_enemy_coords[1]] + sign(build_coords[0]) 
            if can_build_here(build_coords, map, zombies):
                build_coords_list.append(build_coords)
                continue
            if not_checked_go_x:
                build_coords = [closest_to_enemy_coords[0] + sign(build_direction[0]),
                            closest_to_enemy_coords[1]]
                if can_build_here(build_coords, map, zombies):
                    build_coords_list.append(build_coords)
                    continue
            closest_to_enemy_ind +=1
            if closest_to_enemy_ind == len(sorted_closest_to_enemy_coords):
                break
            closest_to_enemy_coords = sorted_closest_to_enemy_coords[closest_to_enemy_ind]
            build_direction = [(closest_enemy_coords[0] - closest_to_enemy_coords[0]),
                       (closest_enemy_coords[0] - closest_to_enemy_coords[0])]

    return build_coords_list

        
