from collections import deque, defaultdict
from dataclasses import dataclass

from src.const import FURTHEST_DIST
from src.models import NeighborType, Vec2
from src.utils import get_neighbor

def is_out_of_map(loc: Vec2):
    return loc.x < 0 or loc.y < 0

@dataclass
class BFSMapElement:
    loc: Vec2
    where_came_from: Vec2
    distance: int


def bfs(furthest_dist: int, init_loc: Vec2):
    q: deque[BFSMapElement] = deque()
    visited = defaultdict(bool) # returns False if value is not present in dict
    bfs_map: dict[Vec2, BFSMapElement] = {} 

    start_element = BFSMapElement(
        loc=init_loc,
        where_came_from=Vec2(x=0, y=0),
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
            if not is_out_of_map(neighbor_loc) and (not visited[neighbor_loc] or visited[neighbor_loc] and bfs_map[neighbor_loc].distance >= cur.distance + 1):
                q.append(
                    BFSMapElement(
                        loc=neighbor_loc,
                        where_came_from=cur.loc,
                        distance=cur.distance + 1,
                    )
                )

    return bfs_map


def build_route(init_loc: Vec2, dest_loc: Vec2):
    bfs_map = bfs(FURTHEST_DIST, init_loc)

    if not dest_loc in bfs_map:
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