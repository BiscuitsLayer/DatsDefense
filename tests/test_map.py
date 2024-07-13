import json
from src.models import Map, Base, EnemyBase, Vec2, Zombie, ZombieSpot

dynamic_json = """
{
    "realmName": "test-day2-4",
    "player": {
        "gold": 10,
        "points": 0,
        "name": "long_live_breaking",
        "zombieKills": 0,
        "enemyBlockKills": 0,
        "gameEndedAt": null
    },
    "base": [
        {
            "id": "0190ab1f-b459-7564-963f-8f4783003709",
            "x": 218,
            "y": 203,
            "health": 100,
            "attack": 10,
            "range": 5,
            "lastAttack": null
        },
        {
            "id": "0190ab1f-b459-7557-b326-8ec8fe26efb3",
            "x": 217,
            "y": 202,
            "health": 287,
            "attack": 40,
            "range": 8,
            "isHead": true,
            "lastAttack": null
        },
        {
            "id": "0190ab1f-b459-755b-9a6b-772cf5712844",
            "x": 218,
            "y": 202,
            "health": 100,
            "attack": 10,
            "range": 5,
            "lastAttack": null
        },
        {
            "id": "0190ab1f-b459-755f-b277-d826d89b00b0",
            "x": 217,
            "y": 203,
            "health": 100,
            "attack": 10,
            "range": 5,
            "lastAttack": null
        }
    ],
    "zombies": [
        {
            "x": 216,
            "y": 208,
            "id": "d233dbae-58e7-45e4-b5c9-70102134044c",
            "type": "liner",
            "health": 7,
            "attack": 7,
            "speed": 1,
            "waitTurns": 1,
            "direction": "left"
        },
        {
            "x": 216,
            "y": 208,
            "id": "34c16b09-8afc-43b2-acf1-171e9f8cd09a",
            "type": "bomber",
            "health": 9,
            "attack": 13,
            "speed": 1,
            "waitTurns": 1,
            "direction": "down"
        },
        {
            "x": 212,
            "y": 212,
            "id": "d0a55093-40d8-4dc7-ac59-2de86d62b9dd",
            "type": "bomber",
            "health": 7,
            "attack": 7,
            "speed": 1,
            "waitTurns": 1,
            "direction": "down"
        },
        {
            "x": 211,
            "y": 193,
            "id": "89aa1e12-efef-48ae-8346-fd46061cb14e",
            "type": "juggernaut",
            "health": 5,
            "attack": 999999,
            "speed": 1,
            "waitTurns": 2,
            "direction": "right"
        },
        {
            "x": 228,
            "y": 213,
            "id": "5d33feea-c797-4dd6-959e-db7a62a8d6e1",
            "type": "liner",
            "health": 9,
            "attack": 13,
            "speed": 1,
            "waitTurns": 1,
            "direction": "down"
        },
        {
            "x": 207,
            "y": 206,
            "id": "e19ec9f9-48a6-4b6f-a148-5cfc5d597ccc",
            "type": "normal",
            "health": 9,
            "attack": 13,
            "speed": 1,
            "waitTurns": 1,
            "direction": "left"
        },
        {
            "x": 210,
            "y": 198,
            "id": "0064a8d2-cc86-4d15-a4b7-a0e85b6c58d3",
            "type": "bomber",
            "health": 7,
            "attack": 7,
            "speed": 1,
            "waitTurns": 1,
            "direction": "left"
        },
        {
            "x": 217,
            "y": 196,
            "id": "3ca397cb-038d-4f7e-ad22-3d26df4339a4",
            "type": "juggernaut",
            "health": 11,
            "attack": 999999,
            "speed": 1,
            "waitTurns": 1,
            "direction": "down"
        },
        {
            "x": 215,
            "y": 207,
            "id": "823b6d30-3f3d-4660-97d3-cfafc965272b",
            "type": "bomber",
            "health": 5,
            "attack": 1,
            "speed": 1,
            "waitTurns": 1,
            "direction": "left"
        },
        {
            "x": 215,
            "y": 207,
            "id": "83f029b9-6327-476a-b314-dac43e549fc8",
            "type": "bomber",
            "health": 9,
            "attack": 13,
            "speed": 1,
            "waitTurns": 1,
            "direction": "right"
        },
        {
            "x": 226,
            "y": 195,
            "id": "7441b82b-f1a6-4765-b389-58ba29f2258b",
            "type": "liner",
            "health": 7,
            "attack": 7,
            "speed": 1,
            "waitTurns": 1,
            "direction": "up"
        },
        {
            "x": 226,
            "y": 195,
            "id": "959d4b33-09fe-4349-a0a5-915cd4051599",
            "type": "chaos_knight",
            "health": 11,
            "attack": 19,
            "speed": 3,
            "waitTurns": 1,
            "direction": "right"
        },
        {
            "x": 219,
            "y": 212,
            "id": "087a6257-136c-4d28-955c-133f064dd127",
            "type": "fast",
            "health": 9,
            "attack": 13,
            "speed": 2,
            "waitTurns": 1,
            "direction": "left"
        },
        {
            "x": 223,
            "y": 198,
            "id": "531b2c41-7d92-483d-afbc-4c5d091cb2dd",
            "type": "normal",
            "health": 11,
            "attack": 19,
            "speed": 1,
            "waitTurns": 1,
            "direction": "left"
        },
        {
            "x": 217,
            "y": 207,
            "id": "6fc18ffd-0093-4846-ac01-bd6a3db88459",
            "type": "bomber",
            "health": 7,
            "attack": 7,
            "speed": 1,
            "waitTurns": 1,
            "direction": "left"
        },
        {
            "x": 224,
            "y": 209,
            "id": "2e5f278e-3f36-4b7f-b228-cbc80e6d1fb2",
            "type": "liner",
            "health": 7,
            "attack": 7,
            "speed": 1,
            "waitTurns": 1,
            "direction": "left"
        },
        {
            "x": 227,
            "y": 209,
            "id": "ec5a9300-85ab-4d29-84d0-26bf4c7bd605",
            "type": "normal",
            "health": 9,
            "attack": 13,
            "speed": 1,
            "waitTurns": 1,
            "direction": "left"
        },
        {
            "x": 227,
            "y": 209,
            "id": "10ef9947-13fa-4c28-b932-5dfb1f049214",
            "type": "bomber",
            "health": 11,
            "attack": 19,
            "speed": 1,
            "waitTurns": 1,
            "direction": "up"
        },
        {
            "x": 226,
            "y": 207,
            "id": "4e5817e1-c1f1-4767-8810-a945a0dbdc86",
            "type": "juggernaut",
            "health": 9,
            "attack": 999999,
            "speed": 1,
            "waitTurns": 1,
            "direction": "up"
        },
        {
            "x": 219,
            "y": 209,
            "id": "cc92ce49-68c2-49f2-8d4c-574f59bdebb4",
            "type": "chaos_knight",
            "health": 9,
            "attack": 13,
            "speed": 3,
            "waitTurns": 1,
            "direction": "left"
        },
        {
            "x": 224,
            "y": 193,
            "id": "5e096a18-3f62-4b8e-ba3b-034773a6aa12",
            "type": "juggernaut",
            "health": 11,
            "attack": 999999,
            "speed": 1,
            "waitTurns": 2,
            "direction": "left"
        },
        {
            "x": 207,
            "y": 194,
            "id": "2386ec1a-647b-4f1e-a952-18a590736305",
            "type": "chaos_knight",
            "health": 9,
            "attack": 13,
            "speed": 3,
            "waitTurns": 1,
            "direction": "up"
        },
        {
            "x": 218,
            "y": 200,
            "id": "70f452ce-356b-456f-8486-ba1e073dac94",
            "type": "bomber",
            "health": 9,
            "attack": 13,
            "speed": 1,
            "waitTurns": 1,
            "direction": "left"
        },
        {
            "x": 226,
            "y": 203,
            "id": "6a7d16aa-60a9-431c-84ec-e5e3347ba13b",
            "type": "normal",
            "health": 9,
            "attack": 13,
            "speed": 1,
            "waitTurns": 1,
            "direction": "up"
        },
        {
            "x": 227,
            "y": 199,
            "id": "5e858e39-bad8-4a82-89b3-aabb310ab259",
            "type": "bomber",
            "health": 11,
            "attack": 19,
            "speed": 1,
            "waitTurns": 1,
            "direction": "right"
        },
        {
            "x": 227,
            "y": 205,
            "id": "736b4aa0-3e4c-4fba-bde8-7fbb5e00f777",
            "type": "fast",
            "health": 9,
            "attack": 13,
            "speed": 2,
            "waitTurns": 1,
            "direction": "up"
        },
        {
            "x": 211,
            "y": 200,
            "id": "7e77205a-297d-4c03-b7b5-7b22882cb614",
            "type": "bomber",
            "health": 9,
            "attack": 13,
            "speed": 1,
            "waitTurns": 1,
            "direction": "down"
        },
        {
            "x": 226,
            "y": 197,
            "id": "11f178cd-a916-4959-aa05-66586fbb0833",
            "type": "liner",
            "health": 9,
            "attack": 13,
            "speed": 1,
            "waitTurns": 1,
            "direction": "up"
        },
        {
            "x": 226,
            "y": 212,
            "id": "63833198-3140-4098-a3b9-a2a75fab5aa4",
            "type": "bomber",
            "health": 11,
            "attack": 19,
            "speed": 1,
            "waitTurns": 1,
            "direction": "down"
        },
        {
            "x": 228,
            "y": 196,
            "id": "623c4e7f-410d-413b-8bc9-7491bc901908",
            "type": "juggernaut",
            "health": 9,
            "attack": 999999,
            "speed": 1,
            "waitTurns": 2,
            "direction": "right"
        },
        {
            "x": 213,
            "y": 199,
            "id": "3b55bba6-5d27-4750-8973-ba8636862f31",
            "type": "bomber",
            "health": 9,
            "attack": 13,
            "speed": 1,
            "waitTurns": 1,
            "direction": "left"
        },
        {
            "x": 225,
            "y": 203,
            "id": "db7ba82f-e717-4000-9d52-1977a7ed6475",
            "type": "juggernaut",
            "health": 7,
            "attack": 999999,
            "speed": 1,
            "waitTurns": 1,
            "direction": "up"
        },
        {
            "x": 225,
            "y": 203,
            "id": "a68ba08f-fe88-4c0d-9252-357c85aecb7d",
            "type": "fast",
            "health": 11,
            "attack": 19,
            "speed": 2,
            "waitTurns": 1,
            "direction": "down"
        },
        {
            "x": 210,
            "y": 192,
            "id": "30917fc3-2c5a-4848-8e6d-9cc21be52317",
            "type": "fast",
            "health": 11,
            "attack": 19,
            "speed": 2,
            "waitTurns": 1,
            "direction": "up"
        },
        {
            "x": 215,
            "y": 208,
            "id": "a20f7520-48b8-4a77-bad3-bc3d9070e895",
            "type": "bomber",
            "health": 9,
            "attack": 13,
            "speed": 1,
            "waitTurns": 1,
            "direction": "right"
        },
        {
            "x": 213,
            "y": 205,
            "id": "03b8b474-3b22-4f3a-aa19-e46b2bb4c54a",
            "type": "juggernaut",
            "health": 7,
            "attack": 999999,
            "speed": 1,
            "waitTurns": 2,
            "direction": "down"
        }
    ],
    "enemyBlocks": null,
    "turnEndsInMs": 685,
    "turn": 35
}
"""

static_json = """
{
    "realmName": "test-day2-5",
    "zpots": [
        {
            "x": 48,
            "y": 104,
            "type": "default"
        },
        {
            "x": 48,
            "y": 116,
            "type": "default"
        },
        {
            "x": 48,
            "y": 117,
            "type": "default"
        },
        {
            "x": 48,
            "y": 100,
            "type": "default"
        },
        {
            "x": 48,
            "y": 101,
            "type": "default"
        },
        {
            "x": 48,
            "y": 105,
            "type": "wall"
        },
        {
            "x": 48,
            "y": 102,
            "type": "default"
        },
        {
            "x": 48,
            "y": 112,
            "type": "wall"
        },
        {
            "x": 48,
            "y": 119,
            "type": "default"
        },
        {
            "x": 48,
            "y": 113,
            "type": "default"
        },
        {
            "x": 48,
            "y": 103,
            "type": "default"
        },
        {
            "x": 48,
            "y": 98,
            "type": "default"
        },
        {
            "x": 48,
            "y": 118,
            "type": "default"
        },
        {
            "x": 48,
            "y": 114,
            "type": "default"
        },
        {
            "x": 48,
            "y": 99,
            "type": "default"
        },
        {
            "x": 48,
            "y": 115,
            "type": "default"
        }
    ]
}
"""

resp_dynamic_json = json.loads(dynamic_json)
resp_static_json = json.loads(static_json)

bases = [Base(**base) for base in resp_dynamic_json['base']]
enemy_bases = [EnemyBase(**enemy_base) for enemy_base in (resp_dynamic_json['enemyBlocks'] or [])]
zombies = [Zombie(**zombie) for zombie in resp_dynamic_json['zombies']]
zpots = [ZombieSpot(**zombie_spot) for zombie_spot in resp_static_json['zpots']]

map = Map(bases, enemy_bases, zombies, zpots)
print(map.tiles)