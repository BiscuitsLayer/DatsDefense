import os
import logging
from src.models import Base, Vec2, NeighborType, Map, TileType, Zombie, EnemyBase
from typing import List
from war_utils import dist_sqr as dist

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

def check_build_dir(dir_: Vec2, build_direction: Vec2, closest_to_enemy_coords: Vec2, build_coords_list: List[Vec2], zombies: List[Zombie]): # 0 / 1
    add = False
    potential_build_coords = closest_to_enemy_coords+dir_
    if can_build_here(potential_build_coords, map, zombies):
        add = True
        build_coords_list.append(potential_build_coords)
        build_direction -= dir_
    else:
        dir_ = Vec2(x=dir_.y, y=dir_.x)
        potential_build_coords = closest_to_enemy_coords+dir_
        if can_build_here(potential_build_coords, map, zombies):
            add = True
            build_coords_list.append(potential_build_coords)
            build_direction -= dir_
    if add == True:
        closest_to_enemy_coords = potential_build_coords
    return closest_to_enemy_coords, add

def enemies_n_build_plan(n: int, closest_enemy_coords: Vec2, sorted_closest_to_enemy_coords: List[Vec2], zombies: List[Zombie]):
    build_coords_list = list()
    closest_to_enemy_ind = len(sorted_closest_to_enemy_coords)
    build_coords_list = list()
    for _ in range(0, n):
        add = False
        if closest_to_enemy_ind <= 0:
            break
        while add != True or closest_to_enemy_ind >= 0:
            closest_to_enemy_ind -= 1
            closest_to_enemy_coords = sorted_closest_to_enemy_coords[closest_to_enemy_ind]
            build_direction = closest_enemy_coords - closest_to_enemy_coords
            ax = (abs(build_direction.x) > abs(build_direction.y))*1
            dir_ = Vec2(x=sign(build_direction.x)*[1,0][ax], y=sign(build_direction.y)*[0,1][ax])
            closest_to_enemy_coords, add = check_build_dir(dir_, build_direction, closest_to_enemy_coords, build_coords_list, zombies)
            if add:
                sorted_closest_to_enemy_coords.append(closest_to_enemy_coords)
                closest_to_enemy_ind += 1
    return build_coords_list

def no_enemies_n_build_plan(n: int, closest_enemy_coords: Vec2, sorted_closest_to_enemy_coords: List[Vec2], zombies: List[Zombie]):
    build_coords_list = list()
    closest_to_enemy_ind = len(sorted_closest_to_enemy_coords)
    build_coords_list = list()
    for _ in range(0, n):
        add = False
        if closest_to_enemy_ind <= 0:
            break
        while add != True or closest_to_enemy_ind >= 0:
            closest_to_enemy_ind -= 1
            closest_to_enemy_coords = sorted_closest_to_enemy_coords[closest_to_enemy_ind]
            build_direction = closest_enemy_coords - closest_to_enemy_coords
            ax = (abs(build_direction.x) > abs(build_direction.y))*1
            dir_ = Vec2(x=sign(build_direction.x)*[1,0][ax], y=sign(build_direction.y)*[0,1][ax])
            closest_to_enemy_coords, add = check_build_dir(dir_, build_direction, closest_to_enemy_coords, build_coords_list, zombies)
            if add:
                sorted_closest_to_enemy_coords.append(closest_to_enemy_coords)
                closest_to_enemy_ind += 1
    return build_coords_list

def get_build_plan(n_bases, bases: List[Base], enemy_bases: List[EnemyBase], map: Map, zombies: List[Zombie]):
    if len(enemy_bases) > 0:
        enemy_coords = [Vec2(x=base.x, y=base.y) for base in enemy_bases]
        bases_coords = [Vec2(x=base.x, y=base.y) for base in bases]
        geom_center = Vec2(x=sum([point.x for point in bases_coords])/len(bases_coords),
                    y=sum([point.y for point in bases_coords])/len(bases_coords))
        closest_enemy_coords = sorted(enemy_coords, key=lambda x: dist(x, geom_center))[0]
        sorted_closest_to_enemy_coords = sorted(bases_coords, key=lambda x: dist(x, closest_enemy_coords), reverse=True)
        build_coords_list = enemies_n_build_plan(n_bases, closest_enemy_coords, sorted_closest_to_enemy_coords, zombies)

        return build_coords_list
    build_coords_list = no_enemies_n_build_plan(n_bases, zombies)

    return build_coords_list

        
