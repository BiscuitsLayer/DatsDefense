import os
from dotenv import load_dotenv

from src.const import ITER_TIME
from src.planner import IntervalRunner, Planner
from src.models import Build, Vec2, Attack
load_dotenv()

from src.api import *
from src.drawer import draw_map

def main():
    # Verify token and register for a round
    print(f"Token is {os.getenv('TOKEN')}")
    msg, participating = participate()
    print(msg)
    if not participating:
        print("Exiting")
        return None
    
    # Create context to avoid doing many requests for a single iteration
    context = Context()

    # Create task planner and interval_runner that runs POST request every ITER_TIME seconds
    planner = Planner()
    get_runner = IntervalRunner(ITER_TIME, collect_info, args=[context])
    post_runner = IntervalRunner(ITER_TIME, complete_action, args=[planner])
    get_runner.start()
    post_runner.start()

    while True:
        try:  
            ###
            # ADD ALL LOGIC HERE
            ###

            # Sample logic can be done like that
            pts = [
                Attack(target=Vec2(x=1, y=1), blockId="test"),
                Attack(target=Vec2(x=1, y=2), blockId="test"),
                Attack(target=Vec2(x=2, y=2), blockId="test"),
                Attack(target=Vec2(x=2, y=3), blockId="test"),
                Attack(target=Vec2(x=3, y=3), blockId="test"),
            ]

            for pt in pts:
                planner.plan_attack(pt)
                planner.plan_build(Build(x=pt.target.x, y=pt.target.y))

        except KeyboardInterrupt:
            print("Shutting down...")
            post_runner.stop()
            get_runner.stop()
            break

if __name__ == "__main__":
    main()