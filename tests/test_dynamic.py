import json

from api import get_dynamic_objects
from src.models import Base, EnemyBase, Vec2, Zombie, ZombieSpot, Map
from src.utils import can_attack, get_build_plan, can_build_here, get_tile_type, get_neighbor

sample_json = """
{
  "base": [
    {
      "attack": 10,
      "health": 100,
      "id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
      "isHead": true,
      "lastAttack": {
        "x": 1,
        "y": 1
      },
      "range": 5,
      "x": 1,
      "y": 1
    },
    {
      "attack": 10,
      "health": 100,
      "id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
      "isHead": true,
      "lastAttack": {
        "x": 1,
        "y": 1
      },
      "range": 5,
      "x": 7,
      "y": 6
    }
  ],
  "enemyBlocks": [
    {
      "attack": 10,
      "health": 100,
      "isHead": true,
      "lastAttack": {
        "x": 1,
        "y": 1
      },
      "name": "player-test",
      "x": 1,
      "y": 1
    }
  ],
  "player": {
    "enemyBlockKills": 100,
    "gameEndedAt": "2021-10-10T10:00:00Z",
    "gold": 100,
    "name": "player-test",
    "points": 100,
    "zombieKills": 100
  },
  "realmName": "map1",
  "turn": 1,
  "turnEndsInMs": 1000,
  "zombies": [
    {
      "attack": 10,
      "direction": "up",
      "health": 100,
      "id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
      "speed": 10,
      "type": "normal",
      "waitTurns": 1,
      "x": 1,
      "y": 1
    }
  ]
}
"""

resp_json = json.loads(sample_json)

bases = [Base(**base) for base in resp_json['base']]
enemy_bases = [EnemyBase(**enemy_base) for enemy_base in resp_json['enemyBlocks']]
zombies = [Zombie(**zombie) for zombie in resp_json['zombies']]

print(bases)
print(enemy_bases)
print(zombies)

possible_bases = can_attack(Vec2(x=10, y=10), bases)

print(possible_bases)

zpots = [ZombieSpot(**zombie_spot) for zombie_spot in resp_json['zpots']]
map = Map(bases, enemy_bases, zombies, zpots)
print(get_build_plan())