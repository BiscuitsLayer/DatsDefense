import json
from src.models import Map, Base, EnemyBase, Vec2, Zombie, ZombieSpot
from src.war_utils import rank_zombies

dynamic_json = """
{
    "base": [
        {
            "id": "id1",
            "x": 2,
            "y": 2,
            "health": 100,
            "attack": 10,
            "range": 5,
            "lastAttack": null
        },
        {
            "id": "id2",
            "x": 3,
            "y": 2,
            "health": 100,
            "attack": 10,
            "range": 5,
            "lastAttack": null
        },
        {
            "id": "id3",
            "x": 4,
            "y": 2,
            "health": 100,
            "attack": 10,
            "range": 5,
            "lastAttack": null
        },
        {
            "id": "id4",
            "x": 5,
            "y": 2,
            "health": 100,
            "attack": 10,
            "range": 5,
            "lastAttack": null
        },
        {
            "id": "id5",
            "x": 6,
            "y": 2,
            "health": 100,
            "attack": 10,
            "range": 5,
            "lastAttack": null
        },
        {
            "id": "id6",
            "x": 7,
            "y": 2,
            "health": 100,
            "attack": 10,
            "range": 5,
            "lastAttack": null
        },
        {
            "id": "id7",
            "x": 8,
            "y": 2,
            "health": 100,
            "attack": 10,
            "range": 5,
            "lastAttack": null
        },
        {
            "id": "id8",
            "x": 9,
            "y": 2,
            "health": 100,
            "attack": 10,
            "range": 5,
            "lastAttack": null
        },
        {
            "id": "id9",
            "x": 10,
            "y": 2,
            "health": 100,
            "attack": 10,
            "range": 5,
            "lastAttack": null
        },
        {
            "id": "id10",
            "x": 2,
            "y": 3,
            "health": 100,
            "attack": 10,
            "range": 5,
            "lastAttack": null
        },
        {
            "id": "id11",
            "x": 3,
            "y": 3,
            "health": 100,
            "attack": 10,
            "range": 5,
            "lastAttack": null
        },
        {
            "id": "id12",
            "x": 4,
            "y": 3,
            "health": 100,
            "attack": 10,
            "range": 5,
            "lastAttack": null
        },
        {
            "id": "id13",
            "x": 5,
            "y": 3,
            "health": 100,
            "attack": 10,
            "range": 5,
            "lastAttack": null
        },
        {
            "id": "id14",
            "x": 6,
            "y": 3,
            "health": 100,
            "attack": 10,
            "range": 5,
            "lastAttack": null
        },
        {
            "id": "id15",
            "x": 7,
            "y": 3,
            "health": 100,
            "attack": 10,
            "range": 5,
            "lastAttack": null
        },
        {
            "id": "id16",
            "x": 8,
            "y": 3,
            "health": 100,
            "attack": 10,
            "range": 5,
            "lastAttack": null
        },
        {
            "id": "id17",
            "x": 9,
            "y": 3,
            "health": 100,
            "attack": 10,
            "range": 5,
            "lastAttack": null
        },
        {
            "id": "id18",
            "x": 10,
            "y": 3,
            "health": 100,
            "attack": 10,
            "range": 5,
            "lastAttack": null
        },
        {
            "id": "id19",
            "x": 2,
            "y": 4,
            "health": 100,
            "attack": 10,
            "range": 5,
            "lastAttack": null
        },
        {
            "id": "id20",
            "x": 3,
            "y": 4,
            "health": 100,
            "attack": 10,
            "range": 5,
            "lastAttack": null
        },
        {
            "id": "id21",
            "x": 4,
            "y": 4,
            "health": 100,
            "attack": 10,
            "range": 5,
            "lastAttack": null
        },
        {
            "id": "id22",
            "x": 5,
            "y": 4,
            "health": 100,
            "attack": 10,
            "range": 5,
            "lastAttack": null
        },
        {
            "id": "id23",
            "x": 6,
            "y": 4,
            "health": 100,
            "attack": 10,
            "range": 5,
            "lastAttack": null
        },
        {
            "id": "id24",
            "x": 7,
            "y": 4,
            "health": 100,
            "attack": 10,
            "range": 5,
            "lastAttack": null
        },
        {
            "id": "id25",
            "x": 8,
            "y": 4,
            "health": 100,
            "attack": 10,
            "range": 5,
            "lastAttack": null
        },
        {
            "id": "id26",
            "x": 9,
            "y": 4,
            "health": 100,
            "attack": 10,
            "range": 5,
            "lastAttack": null
        },
        {
            "id": "id27",
            "x": 10,
            "y": 4,
            "health": 100,
            "attack": 10,
            "range": 5,
            "lastAttack": null
        },
        {
            "id": "id28",
            "x": 2,
            "y": 5,
            "health": 100,
            "attack": 10,
            "range": 5,
            "lastAttack": null
        },
        {
            "id": "id29",
            "x": 3,
            "y": 5,
            "health": 100,
            "attack": 10,
            "range": 5,
            "lastAttack": null
        },
        {
            "id": "id30",
            "x": 4,
            "y": 5,
            "health": 100,
            "attack": 10,
            "range": 5,
            "lastAttack": null
        },
        {
            "id": "id31",
            "x": 5,
            "y": 5,
            "health": 100,
            "attack": 10,
            "range": 5,
            "lastAttack": null
        },
        {
            "id": "id32",
            "x": 6,
            "y": 5,
            "health": 100,
            "attack": 10,
            "range": 5,
            "lastAttack": null
        },
        {
            "id": "id33",
            "x": 7,
            "y": 5,
            "health": 100,
            "attack": 10,
            "range": 5,
            "lastAttack": null
        },
        {
            "id": "id34",
            "x": 8,
            "y": 5,
            "health": 100,
            "attack": 10,
            "range": 5,
            "lastAttack": null
        },
        {
            "id": "id35",
            "x": 9,
            "y": 5,
            "health": 100,
            "attack": 10,
            "range": 5,
            "lastAttack": null
        },
        {
            "id": "id36",
            "x": 10,
            "y": 5,
            "health": 100,
            "attack": 10,
            "range": 5,
            "lastAttack": null
        },
        {
            "id": "id37",
            "x": 2,
            "y": 6,
            "health": 100,
            "attack": 10,
            "range": 5,
            "lastAttack": null
        },
        {
            "id": "id38",
            "x": 3,
            "y": 6,
            "health": 100,
            "attack": 10,
            "range": 5,
            "lastAttack": null
        },
        {
            "id": "id39",
            "x": 4,
            "y": 6,
            "health": 100,
            "attack": 10,
            "range": 5,
            "lastAttack": null
        },
        {
            "id": "id40",
            "x": 5,
            "y": 6,
            "health": 100,
            "attack": 10,
            "range": 5,
            "lastAttack": null
        },
        {
            "id": "id41",
            "x": 6,
            "y": 6,
            "health": 100,
            "attack": 10,
            "range": 5,
            "lastAttack": null
        },
        {
            "id": "id42",
            "x": 7,
            "y": 6,
            "health": 100,
            "attack": 10,
            "range": 5,
            "lastAttack": null
        },
        {
            "id": "id43",
            "x": 8,
            "y": 6,
            "health": 100,
            "attack": 10,
            "range": 5,
            "lastAttack": null
        },
        {
            "id": "id44",
            "x": 9,
            "y": 6,
            "health": 100,
            "attack": 10,
            "range": 5,
            "lastAttack": null
        },
        {
            "id": "id45",
            "x": 10,
            "y": 6,
            "health": 100,
            "attack": 10,
            "range": 5,
            "lastAttack": null
        },
        {
            "id": "id46",
            "x": 2,
            "y": 7,
            "health": 100,
            "attack": 10,
            "range": 5,
            "lastAttack": null
        },
        {
            "id": "id47",
            "x": 3,
            "y": 7,
            "health": 100,
            "attack": 10,
            "range": 5,
            "lastAttack": null
        },
        {
            "id": "id48",
            "x": 4,
            "y": 7,
            "health": 100,
            "attack": 10,
            "range": 5,
            "lastAttack": null
        },
        {
            "id": "id49",
            "x": 5,
            "y": 7,
            "health": 100,
            "attack": 10,
            "range": 5,
            "lastAttack": null
        },
        {
            "id": "id50",
            "x": 6,
            "y": 7,
            "health": 100,
            "attack": 10,
            "range": 5,
            "lastAttack": null
        },
        {
            "id": "id51",
            "x": 7,
            "y": 7,
            "health": 100,
            "attack": 10,
            "range": 5,
            "lastAttack": null
        },
        {
            "id": "id52",
            "x": 8,
            "y": 7,
            "health": 100,
            "attack": 10,
            "range": 5,
            "lastAttack": null
        },
        {
            "id": "id53",
            "x": 9,
            "y": 7,
            "health": 100,
            "attack": 10,
            "range": 5,
            "lastAttack": null
        },
        {
            "id": "id54",
            "x": 10,
            "y": 7,
            "health": 100,
            "attack": 10,
            "range": 5,
            "lastAttack": null
        }
    ],
    "enemyBlocks": [],
    "zombies": [
        {
            "attack": 10,
            "direction": "up",
            "health": 100,
            "speed": 1,
            "type": normal,
            "waitTurns": 0,
            "id": "id1",
            "x": 6,
            "y": 10,
        }
    ]
}
"""

static_json = """
{
    "zpots": [
        {
            "x": 0,
            "y": 0,
            "type": "wall"
        },
        {
            "x": 12,
            "y": 0,
            "type": "wall"
        },
        {
            "x": 0,
            "y": 15,
            "type": "wall"
        },
        {
            "x": 12,
            "y": 15,
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
print(map)