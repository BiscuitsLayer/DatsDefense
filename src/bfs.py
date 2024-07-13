from collections import deque, defaultdict
from dataclasses import dataclass

from src.const import FURTHEST_DIST
from src.models import *
from src.utils import get_neighbor

def is_out_of_map(loc: Vec2):
    return loc.x < 0 or loc.y < 0

@dataclass
class BFSMapElement:
    loc: Vec2
    where_came_from: Vec2
    distance: int


def bfs(furthest_dist: int, init_loc: Vec2, map: Map, zombies: list[Zombie]) -> dict[Vec2, BFSMapElement]:
    q: deque[BFSMapElement] = deque()
    visited = defaultdict(bool) # returns False if value is not present in dict
    bfs_map: dict[Vec2, BFSMapElement] = {} 

    start_element = BFSMapElement(
        loc=init_loc,
        where_came_from=Vec2(x=init_loc.x, y=init_loc.y),
        distance=0,
    )
    bfs_map[init_loc] = start_element
    q.append(start_element)

    while q:
        cur = q.popleft()
        visited[cur.loc] = True

        if cur.loc not in bfs_map or (cur.loc in bfs_map and bfs_map[cur.loc].distance > cur.distance):
            bfs_map[cur.loc] = cur
        
        if cur.distance >= furthest_dist:
            continue

        for neighbor_type in NeighborType:
            neighbor_loc = get_neighbor(cur.loc, neighbor_type)

            # FIXME: add check that can step here
            if not is_out_of_map(neighbor_loc) and \
                    (not visited[neighbor_loc] or visited[neighbor_loc] and bfs_map[neighbor_loc].distance >= cur.distance + 1) and \
                    can_build_here(neighbor_loc, map, zombies):
                q.append(
                    BFSMapElement(
                        loc=neighbor_loc,
                        where_came_from=cur.loc,
                        distance=cur.distance + 1,
                    )
                )

    return bfs_map


def build_route(init_loc: Vec2, dest_loc: Vec2, map: Map, zombies: list[Zombie]) -> list[Vec2]:
    bfs_map: dict[Vec2, BFSMapElement] = bfs(FURTHEST_DIST, init_loc, map, zombies)

    if not dest_loc in bfs_map:
        print(bfs_map.keys())
        print(f"UNREACHABLE from {init_loc}")
        # Cannot reach
        return None
    
    cur_pos = dest_loc
    route: list[Vec2] = []
    while cur_pos != init_loc:
        route.append(cur_pos)
        # print(f"Came to {cur_pos} from {bfs_map[cur_pos].where_came_from} with distance {bfs_map[cur_pos].distance}")
        cur_pos = bfs_map[cur_pos].where_came_from

    route.append(init_loc)
    return route[::-1]


def get_tile_type(loc: Vec2, map: map):
    return map.tiles[loc.y][loc.x]


def can_build_here(loc: Vec2, map: Map, zombies: list[Zombie]) -> bool:
    if not (loc.x > 0 and loc.y > 0 and loc.x < map.bounds.size.x and loc.y < map.bounds.size.y):
        return False
    
    spot_free = (get_tile_type(loc, map) not in [TileType.BASE, TileType.ENEMY_BASE, TileType.WALL, TileType.ZOMBIE_GTOR]) and (loc not in zombies)
    if not spot_free:
        return False
    
    direct_neighbors_types = [get_tile_type(get_neighbor(loc, type_), map) for type_ in [NeighborType.TOP, NeighborType.LEFT, NeighborType.RIGHT, NeighborType.BOTTOM]]
    bad_direct_neighbors = any([type_ in [TileType.ZOMBIE_GTOR, TileType.WALL, TileType.ENEMY_BASE] for type_ in (direct_neighbors_types or [])])
    if bad_direct_neighbors:
        return False

    diagonal_neighbors = [get_tile_type(get_neighbor(loc, type_), map) for type_ in [NeighborType.TOP_RIGHT, NeighborType.TOP_LEFT, NeighborType.BOTTOM_RIGHT, NeighborType.BOTTOM_LEFT]]
    no_diagonal_enemy = TileType.ENEMY_BASE not in diagonal_neighbors
    if not no_diagonal_enemy:
        return False

    return True
