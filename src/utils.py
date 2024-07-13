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

def get_build_plan(bases: List[Base], enemy_bases: List[EnemyBase], map: Map, zombies: List[Zombie]):
    # bases, enemy_bases, zombies = ... #get_dynamic_objects()
    # world = ... #get_static_objects()
    if len(enemy_bases) > 0:
        enemy_coords = [Vec2(x=base.x, y=base.y) for base in enemy_bases]

    bases_coords = [Vec2(x=base.x, y=base.y) for base in bases]

    geom_center = Vec2(x=sum([point.x for point in bases_coords])/len(bases_coords),
                   y=sum([point.y for point in bases_coords])/len(bases_coords))
    closest_enemy_coords = sorted(enemy_coords, key=lambda x: dist(x, geom_center))[0]
    # dists_to_enemy = [dist(geom_center, enemy_coord) for enemy_coord in enemy_coords]
    # closest_enemy_coords = enemy_coords[min(range(len(dists_to_enemy)), key=dists_to_enemy.__getitem__)]
    # dists_to_closest_enemy = [dist(closest_enemy_coords, base_coord) for base_coord in bases_coords]
    sorted_closest_to_enemy_coords = sorted(bases_coords, key=lambda x: dist(x, closest_enemy_coords), reverse=True)
    # closest_to_enemy_coords = bases_coords[min(range(len(dists_to_closest_enemy)), key=dists_to_closest_enemy.__getitem__)]
    closest_to_enemy_ind = len(sorted_closest_to_enemy_coords)
    # build_direction = [build_direction.x, build_direction.y]
    build_coords_list = list()
    for _ in range(0, 3):
        add = False
        while add != True:
            closest_to_enemy_ind -= 1
            closest_to_enemy_coords = sorted_closest_to_enemy_coords[closest_to_enemy_ind]
            build_direction = closest_enemy_coords - closest_to_enemy_coords
            ax = (abs(build_direction.x) > abs(build_direction.y))*1
            dir_ = Vec2(x=sign(build_direction.x)*[1,0][ax], y=sign(build_direction.y)*[0,1][ax])
            closest_to_enemy_coords, add = check_build_dir(dir_, build_direction, closest_to_enemy_coords, build_coords_list, zombies)
            if add:
                sorted_closest_to_enemy_coords.append(closest_to_enemy_coords)
                closest_to_enemy_ind += 1
        # build_coords, build_direction, closest_to_enemy_coords, add, checked = check_build_ax_direction(ax=0, build_direction, closest_to_enemy_coords, zombies)
            

        # if abs(build_direction[0]) > abs(build_direction[1]):
        #     build_coords = [closest_to_enemy_coords[0] + sign(build_direction[0]),
        #                     closest_to_enemy_coords[1]]
        #     if can_build_here(Vec2(x=build_coords[0], y=build_coords[1]), map, zombies):
        #         build_coords_list.append(Vec2(x=build_coords[0], y=build_coords[1]))
        #         closest_to_enemy_coords = build_coords
        #         build_direction = [build_direction[0] - sign(build_direction[0]),
        #                            build_direction[1]]
        #         continue
        #     not_checked_go_x = False
        # else:
        #     build_coords = [closest_to_enemy_coords[0],
        #                     closest_to_enemy_coords[1]] + sign(build_coords[0]) 
        #     if can_build_here(Vec2(x=build_coords[0], y=build_coords[1]), map, zombies):
        #         build_coords_list.append(Vec2(x=build_coords[0], y=build_coords[1]))
        #         closest_to_enemy_coords = build_coords
        #         build_direction = [build_direction[0],
        #                            build_direction[1] - sign(build_direction[0])]
        #         continue
        #     if not_checked_go_x:
        #         build_coords = [closest_to_enemy_coords[0] + sign(build_direction[0]),
        #                         closest_to_enemy_coords[1]]
        #         if can_build_here(Vec2(x=build_coords[0], y=build_coords[1]), map, zombies):
        #             build_coords_list.append(Vec2(x=build_coords[0], y=build_coords[1]))
        #             closest_to_enemy_coords = build_coords
        #             build_direction = [build_direction[0] - sign(build_direction[0]),
        #                             build_direction[1]]
        #             continue
        #     closest_to_enemy_ind +=1
        #     if closest_to_enemy_ind == len(sorted_closest_to_enemy_coords):
        #         break
        #     closest_to_enemy_coords = sorted_closest_to_enemy_coords[closest_to_enemy_ind]
        #     build_direction = [(closest_enemy_coords[0] - closest_to_enemy_coords[0]),
        #                (closest_enemy_coords[0] - closest_to_enemy_coords[0])]

    return build_coords_list

        
