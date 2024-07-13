from src.bfs import bfs, build_route, is_out_of_map
from src.models import Vec2

pts = [
    Vec2(x=1, y=1),
    Vec2(x=-1, y=1),
    Vec2(x=1, y=-1),
    Vec2(x=-1, y=-1)
]

for pt in pts:
    print(is_out_of_map(pt))

# bfs_map = bfs(
#     furthest_dist=5,
#     init_loc=Vec2(x=3, y=3),
# )
# print(bfs_map)

route = build_route(
    init_loc=Vec2(x=3, y=3),
    dest_loc=Vec2(x=8, y=2),
)
print(route)