import os
import sys
import logging
from src.bfs import build_route
from src.models import Base, EnemyBase, Map, TileType, Vec2, NeighborType, Zombie, Attack
from src.utils import get_neighbor
from src.war_utils import dist, zombie_order

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
        # build_coords_list = enemies_n_build_plan(n_to_build, closest_enemy_coords, sorted_closest_to_enemy_base_coords, zombies)
        # return build_coords_list
    
    else: # no enemies
        # build_coords_list = no_enemies_n_build_plan(n_to_build, zombies)
        # return build_coords_list
        pass
    
def build_route_to_enemies(n_to_build: int, enemy_bases_coords: list[Vec2], bases_coords: list[Vec2], map: Map, zombies: list[Zombie]):
    dest_locations = set()
    for enemy_base_coords in enemy_bases_coords:
        neighbor_locs = set(get_neighbor(Vec2(x=enemy_base_coords.x, y=enemy_base_coords.y), neighbor_type, delta=2) for neighbor_type in NeighborType)
        dest_locations |= neighbor_locs

    routes = []
    for dest_location in dest_locations:
        routes += [route for route in (build_route(base_coords, dest_location, map, zombies) for base_coords in bases_coords) if route is not None]

    routes = [route for route in routes if None not in route][:n_to_build]
    return routes

def attack_enemies(n_to_attack: int, enemy_bases_coords: list[Vec2], bases: list[Base]):
    attacks = []
    for enemy_base_coords in enemy_bases_coords:
        for base in bases:
            if dist(enemy_base_coords, Vec2(x=base.x, y=base.y)) < base.range:
                attacks.append(Attack(blockId=base.id, target=enemy_base_coords))
                break

    return attacks

def heal_zombies(bases: list[Base], zombies: list[Zombie], map: Map):
    order = zombie_order(map, zombies, bases, 8)
    heals = []
    busy_bases_ids = []
    for item in order:
        heals.append(Attack(blockId=item[0], target=item[1]))
        busy_bases_ids.append(item[0])
    return heals, busy_bases_ids
