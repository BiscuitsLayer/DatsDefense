import os
import logging
from src.models import Base, Location, NeighborType
from api import get_dynamic_objects, get_static_objects
from vlad import dist

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

def can_build_here(loc: Location): 
    pass


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
def sign(num):
    return -1 if num < 0 else 1

def add_build_plan():
    units = get_dynamic_objects()
    world = get_static_objects()

    bases_coords = [[base.x, base.y] for base in units.bases]
    enemy_coords = [[base.x, base.y] for base in units.enemy_bases]

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
    for _ in range(1, 4):
        not_checked_go_x = True
        if abs(build_direction[0]) > abs(build_direction[1]):
            build_coords = [closest_to_enemy_coords[0] + sign(build_direction[0]),
                            closest_to_enemy_coords[1]]
            if can_build_here(build_coords):
                build_coords_list.append(build_coords)
                continue
            not_checked_go_x = False
        else:
            build_coords = [closest_to_enemy_coords[0],
                            closest_to_enemy_coords[1]] + sign(build_coords[0]) 
            if can_build_here(build_coords):
                build_coords_list.append(build_coords)
                continue
            if not_checked_go_x:
                build_coords = [closest_to_enemy_coords[0] + sign(build_direction[0]),
                            closest_to_enemy_coords[1]]
                if can_build_here(build_coords):
                    build_coords_list.append(build_coords)
                    continue
            closest_to_enemy_ind +=1
            closest_to_enemy_coords = sorted_closest_to_enemy_coords[closest_to_enemy_ind]
            build_direction = [(closest_enemy_coords[0] - closest_to_enemy_coords[0]),
                       (closest_enemy_coords[0] - closest_to_enemy_coords[0])]

    return build_coords_list

        
