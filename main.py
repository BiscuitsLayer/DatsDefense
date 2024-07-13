import os
from dotenv import load_dotenv
load_dotenv()

from src.api import *
from src.const import ITER_TIME
from src.planner import IntervalRunner, Planner
from src.models import Build, Vec2, Attack

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
            for base in (context.bases or []):
                attack = Attack(target=Vec2(x=base.x+5, y=base.y+5), blockId=base.id)
                planner.plan_attack(attack)

            for base in (context.bases or []):
                build = Build(x=base.x+1, y=base.y+1)
                planner.plan_build(build)

        except KeyboardInterrupt:
            print("Shutting down...")
            post_runner.stop()
            get_runner.stop()
            break

if __name__ == "__main__":
    main()
