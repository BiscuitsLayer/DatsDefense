import json
from src.models import Map, Base, EnemyBase, Vec2, Zombie, ZombieSpot
from src.build_utils import build_route_to_enemies

dynamic_json = """
{
    "base": [
        {
            "id": "id1",
            "x": 218,
            "y": 203,
            "health": 100,
            "attack": 10,
            "range": 5,
            "lastAttack": null
        },
        {
            "id": "id2",
            "x": 218,
            "y": 202,
            "health": 100,
            "attack": 10,
            "range": 5,
            "lastAttack": null
        },
        {
            "id": "id3",
            "x": 217,
            "y": 203,
            "health": 100,
            "attack": 10,
            "range": 5,
            "lastAttack": null
        },
        {
            "id": "id4",
            "x": 217,
            "y": 202,
            "health": 100,
            "attack": 10,
            "range": 5,
            "lastAttack": null
        }
    ],
    "enemyBlocks": [
        {
            "id": "enemy-id1",
            "x": 213,
            "y": 203,
            "health": 100,
            "attack": 10,
            "range": 5,
            "lastAttack": null
        },
        {
            "id": "enemy-id2",
            "x": 213,
            "y": 202,
            "health": 100,
            "attack": 10,
            "range": 5,
            "lastAttack": null
        },
        {
            "id": "enemy-id3",
            "x": 212,
            "y": 203,
            "health": 100,
            "attack": 10,
            "range": 5,
            "lastAttack": null
        },
        {
            "id": "enemy-id4",
            "x": 212,
            "y": 202,
            "health": 100,
            "attack": 10,
            "range": 5,
            "lastAttack": null
        }
    ],
    "zombies": []
}
"""

static_json = """
{
    "zpots": [
        {
            "x": 215,
            "y": 200,
            "type": "wall"
        },
        {
            "x": 215,
            "y": 201,
            "type": "wall"
        },
        {
            "x": 215,
            "y": 202,
            "type": "wall"
        },
        {
            "x": 215,
            "y": 203,
            "type": "wall"
        },
        {
            "x": 215,
            "y": 205,
            "type": "wall"
        },
        {
            "x": 215,
            "y": 206,
            "type": "wall"
        }
    ]
}
"""

resp_dynamic_json = json.loads(dynamic_json)
resp_static_json = json.loads(static_json)

bases = [Base(**base) for base in resp_dynamic_json['base']]
enemy_bases = [EnemyBase(**enemy_base) for enemy_base in (resp_dynamic_json['enemyBlocks'] or [])]
zombies = [Zombie(**zombie) for zombie in (resp_dynamic_json['zombies'] or [])]
zpots = [ZombieSpot(**zombie_spot) for zombie_spot in resp_static_json['zpots']]

map = Map(bases, enemy_bases, zombies, zpots)

build_coords_list = build_route_to_enemies(
    n_to_build=5,
    enemy_bases_coords=[Vec2(x=base.x, y=base.y) for base in enemy_bases],
    bases_coords=[Vec2(x=base.x, y=base.y) for base in bases],
    zombies=[],
    map=map
)

print(build_coords_list)