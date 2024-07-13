import os
from dotenv import load_dotenv

from src.const import ITER_TIME
from src.planner import IntervalRunner, Planner
from src.models import Vec2, DirectionType
load_dotenv()

from api import *
from src.drawer import draw_map

def main():
    # Verify token and register for a round
    # print(f"Token is {os.getenv('TOKEN')}")
    # msg, participating = participate()
    # print(msg)
    # if not participating:
    #     print("Exiting")
    #     return None

    test_dir = "right"
    if test_dir == DirectionType.RIGHT.value:
        print("yes")
    
    # Create context to avoid doing many requests for a single iteration
    context = Context()

    # Create task planner and interval_runner that runs POST request every ITER_TIME seconds
    planner = Planner()
    get_runner = IntervalRunner(ITER_TIME, collect_info, args=[context])
    # post_runner = IntervalRunner(ITER_TIME, complete_action, args=[planner])
    get_runner.start()
    # post_runner.start()

    while True:
        try:  
            ###
            # ADD ALL LOGIC HERE
            ###

            # Sample logic can be done like that
            route = [
                Vec2(x=1, y=1),
                Vec2(x=1, y=2),
                Vec2(x=2, y=2),
                Vec2(x=2, y=3),
                Vec2(x=3, y=3),
            ]

            for loc in route:
                planner.plan_attack(loc)

        except KeyboardInterrupt:
            print("Shutting down...")
            # post_runner.stop()
            get_runner.stop()
            break

if __name__ == "__main__":
    main()