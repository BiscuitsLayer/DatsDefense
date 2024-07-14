import os
import time
from dotenv import load_dotenv

from src.bfs import build_route, can_build_here
from src.build_utils import attack_enemies, build_route_to_enemies, heal_zombies
from src.utils import get_neighbor
load_dotenv()

from src.api import *
from src.const import ITER_TIME
from src.planner import IntervalRunner, Planner

from src.models import *

def main():
    # Verify token and register for a round
    print(f"Token is {os.getenv('TOKEN')}")
    msg, participating = participate()
    print(msg)

    while not participating:
        msg, participating = participate()
        print(msg)
        time.sleep(5)
        # print("Exiting")
        # return None
    
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
            
            if context.routes_to_enemies:
                best_route = context.routes_to_enemies[0]
                planner.clear_build_plan()
                for loc in best_route:
                    build = Build(x=loc.x, y=loc.y)
                    planner.plan_build(build)
            else:
                for base in context.bases:
                    for loc in (get_neighbor(Vec2(x=base.x, y=base.y), neighbor_type) for neighbor_type in NeighborType):
                        if can_build_here(loc, context.map, context.zombies):
                            build = Build(x=loc.x, y=loc.y)
                            planner.plan_build(build)

            attacks, busy_bases_ids = heal_zombies(
                bases=context.bases,
                zombies=context.zombies,
                map=context.map
            )
            attacks += attack_enemies(
                n_to_attack=5,
                enemy_bases_coords=[Vec2(x=base.x, y=base.y) for base in context.enemy_bases],
                bases=[base for base in context.bases if not base.id in busy_bases_ids],
            )
            if attacks:
                planner.clear_attack_plan()
                for attack in attacks:
                    planner.plan_attack(attack)

        except KeyboardInterrupt:
            print("Shutting down...")
            post_runner.stop()
            get_runner.stop()
            break

if __name__ == "__main__":
    main()
