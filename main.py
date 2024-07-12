import os
from dotenv import load_dotenv

from src.planner import Planner
from src.models import *
load_dotenv()

from api import *
from src.drawer import draw_map

def main():
    # print(f"Token is {os.getenv('TOKEN')}")
    # msg, participating = participate()
    # print(msg)
    # if not participating:
    #     print("Exiting")
    #     return None
    
    # route = [
    #     Location(x=1, y=1),
    #     Location(x=1, y=2),
    #     Location(x=2, y=2),
    #     Location(x=2, y=3),
    #     Location(x=3, y=3),
    # ]

    # planner = Planner()
    # for loc in route:
    #     planner.plan_attack(loc)

    # while next_attack_plan := planner.get_next_attack_plan():
    #     print(next_attack_plan)
    
    
    # while True:
    #     dynamic_objects = get_dynamic_objects()
    #     static_object = get_static_objects()

    # class Base(BaseModel):
    #     attack: int # сколько урона даёт
    #     health: int
    #     id: str
    #     isHead: bool
    #     lastAttack: Vec2
    #     range: int # насколько далеко
    #     x: int
    #     y: int


    map = Map(bases=[Base(attack=0, health=0, id="HAHAHAHAH", isHead=True, lastAttack=Vec2(x=0, y=0), range=10, x=0, y=0),
                     Base(attack=0, health=0, id="HAHAHAHAH", isHead=True, lastAttack=Vec2(x=0, y=0), range=10, x=10, y=20),
                     Base(attack=0, health=0, id="HAHAHAHAH", isHead=True, lastAttack=Vec2(x=0, y=0), range=10, x=10, y=30),
                     Base(attack=0, health=0, id="HAHAHAHAH", isHead=True, lastAttack=Vec2(x=0, y=0), range=10, x=50, y=5)],
                     enemy_bases=[], zombies=[], zpots=[])
    
    print(map.bounds.size.x)
    print(map.bounds.size.y)

    for rows in map.tiles:
        for col in rows:
            if col == TileType.BASE:
                print('#', end='')
            else:
                print('_', end='')
        print()


if __name__ == "__main__":
    main()