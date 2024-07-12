import os
from dotenv import load_dotenv

from src.planner import Planner
from src.models import Base, Location
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
    
    route = [
        Location(x=1, y=1),
        Location(x=1, y=2),
        Location(x=2, y=2),
        Location(x=2, y=3),
        Location(x=3, y=3),
    ]

    planner = Planner()
    for loc in route:
        planner.plan_attack(loc)

    while next_attack_plan := planner.get_next_attack_plan():
        print(next_attack_plan)
    
    
    # while True:
    #     dynamic_objects = get_dynamic_objects()
    #     static_object = get_static_objects()


if __name__ == "__main__":
    main()