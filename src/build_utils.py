import os
import sys
import logging
from src.bfs import build_route
from src.models import Base, EnemyBase, Map, TileType, Vec2, NeighborType, Zombie
from src.utils import get_neighbor
from src.war_utils import dist

def sign(num):
    return -1 if num < 0 else 1

def get_tile_type(loc: Vec2, map: Map):
    return map.tiles[loc.y][loc.x]


def can_build_here(loc: Vec2, map: Map, zombies: list[Zombie], build_coords_list: list[Vec2]) -> bool:
    print(loc)
    print(build_coords_list)
    if not (loc.x > 0 and loc.y > 0 and loc.x < map.bounds.size.x and loc.y < map.bounds.size.y):
        print('out of bounds')
        return False
    
    spot_free = (get_tile_type(loc, map) not in [TileType.BASE, TileType.ENEMY_BASE, TileType.WALL, TileType.ZOMBIE_GTOR]) and (loc not in zombies)
    if not spot_free:
        print('spot not free')
        return False
    
    direct_neighbors_types = [get_tile_type(get_neighbor(loc, type_), map) for type_ in [NeighborType.TOP, NeighborType.LEFT, NeighborType.RIGHT, NeighborType.BOTTOM]]

    bad_direct_neighbors = any([type_ in [TileType.ZOMBIE_GTOR, TileType.WALL, TileType.ENEMY_BASE] for type_ in (direct_neighbors_types or [])])
    if bad_direct_neighbors:
        print("bad_direct_neighbors")
        return False

    diagonal_neighbors = [get_tile_type(get_neighbor(loc, type_), map) for type_ in [NeighborType.TOP_RIGHT, NeighborType.TOP_LEFT, NeighborType.BOTTOM_RIGHT, NeighborType.BOTTOM_LEFT]]
    no_diagonal_enemy = TileType.ENEMY_BASE not in diagonal_neighbors
    if not no_diagonal_enemy:
        print("diagonal enemy")
        return False

    return True

## BUILD PLAN PART ##

def get_build_plan(n_to_build, bases: list[Base], enemy_bases: list[EnemyBase], map: Map, zombies: list[Zombie]):
    if len(enemy_bases) > 0:
        enemy_coords = [Vec2(x=base.x, y=base.y) for base in enemy_bases]
        bases_coords = [Vec2(x=base.x, y=base.y) for base in bases]
        geom_center = Vec2(
            x=sum([point.x for point in bases_coords])/len(bases_coords),
            y=sum([point.y for point in bases_coords])/len(bases_coords)
        )
        closest_enemy_coords = sorted(enemy_coords, key=lambda x: dist(x, geom_center))[0] # closest enemy to geom center
        sorted_closest_to_enemy_base_coords = sorted(bases_coords, key=lambda x: dist(x, closest_enemy_coords), reverse=True) # closest are in the end
        build_coords_list = enemies_n_build_plan(n_to_build, closest_enemy_coords, sorted_closest_to_enemy_base_coords, zombies)
        return build_coords_list
    
    else: # no enemies
        # build_coords_list = no_enemies_n_build_plan(n_to_build, zombies)
        # return build_coords_list
        pass
    
def enemies_n_build_plan(n_to_build: int, closest_enemy_coords: Vec2, sorted_closest_to_enemy_base_coords: list[Vec2],  map: Map, zombies: list[Zombie]):
    routes = [build_route(base_coords, closest_enemy_coords, map, zombies) for base_coords in sorted_closest_to_enemy_base_coords]
    routes = [route for route in routes if route is not None][:n_to_build]
    return routes

    # return build_route(sorted_closest_to_enemy_base_coords[0], closest_enemy_coords, map, zombies)

def enemies_n_build_plan_old(n_to_build: int, closest_enemy_coords: Vec2, sorted_closest_to_enemy_base_coords: list[Vec2], zombies: list[Zombie], map: Map):
    build_coords_list = list()
    closest_to_enemy_ind = len(sorted_closest_to_enemy_base_coords)
    for _ in range(0, n_to_build):
        is_built = False
        if closest_to_enemy_ind < 0:
            break

        while is_built == False and closest_to_enemy_ind >= 0:
            closest_to_enemy_ind -= 1
            closest_to_enemy_coords = sorted_closest_to_enemy_base_coords[closest_to_enemy_ind]
            print(f"closest_to_enemy_coords {closest_to_enemy_coords}")

            build_direction = closest_enemy_coords - closest_to_enemy_coords
            print(f"build_direction {build_direction}")

            ax = int(abs(build_direction.x) > abs(build_direction.y))
            axis_unit = Vec2(
                x=sign(build_direction.x)*[1, 0][ax], 
                y=sign(build_direction.y)*[0, 1][ax]
            )
            print(f"axis_unit {axis_unit}")

            closest_to_enemy_coords, is_built = check_build_direction(axis_unit, build_direction, closest_to_enemy_coords, build_coords_list, zombies, map)
            if is_built:
                sorted_closest_to_enemy_base_coords.append(closest_to_enemy_coords)
                closest_to_enemy_ind += 1
    
    return build_coords_list


def check_build_direction(axis_unit: Vec2, build_direction: Vec2, closest_to_enemy_coords: Vec2, build_coords_list: list[Vec2], zombies: list[Zombie], map: Map): # 0 / 1
    add = False
    potential_build_coords = closest_to_enemy_coords + axis_unit
    print(f'potential coords: {potential_build_coords} result {can_build_here(potential_build_coords, map, zombies, build_coords_list)}')
    if can_build_here(potential_build_coords, map, zombies, build_coords_list):
        add = True
        build_coords_list.append(potential_build_coords)
        build_direction -= axis_unit
    else:
        axis_unit = Vec2(x=axis_unit.y, y=axis_unit.x)
        potential_build_coords = closest_to_enemy_coords+axis_unit
        print(f'potential coords: {potential_build_coords} result {can_build_here(potential_build_coords, map, zombies, build_coords_list)}')
        if can_build_here(potential_build_coords, map, zombies, build_coords_list):
            add = True
            build_coords_list.append(potential_build_coords)
            build_direction -= axis_unit
    if add == True:
        closest_to_enemy_coords = potential_build_coords
    return closest_to_enemy_coords, add

