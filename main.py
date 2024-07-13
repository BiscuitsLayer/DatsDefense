import os
import time
from dotenv import load_dotenv

from src.bfs import build_route, can_build_here
from src.build_utils import attack_enemies, build_route_to_enemies
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
        time.sleep(2)
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

            map = map(context.bases, context.enemy_bases, context.zombies, context.zpots)

            routes_to_enemies = build_route_to_enemies(
                n_to_build=5,
                enemy_bases_coords=[Vec2(x=base.x, y=base.y) for base in context.enemy_bases],
                bases_coords=[Vec2(x=base.x, y=base.y) for base in context.bases],
                zombies=context.zombies,
                map=map
            )
            if routes_to_enemies:
                best_route = routes_to_enemies[0]
                for loc in best_route:
                    build = Build(x=loc.x+1, y=loc.y+1)
                    planner.plan_build(build)
            else:
                for base in context.bases:
                    for loc in (get_neighbor(Vec2(x=base.x, y=base.y), neighbor_type) for neighbor_type in NeighborType):
                        if can_build_here(loc, map, context.zombies):
                            build = Build(x=loc.x, y=loc.y)
                            planner.plan_build(build)

            attacks = attack_enemies(
                n_to_attack=5,
                enemy_bases_coords=[Vec2(x=base.x, y=base.y) for base in context.enemy_bases],
                bases=context.bases,
            )

            # Sample logic can be done like that
            for base in (context.bases or []):
                attack = Attack(target=Vec2(x=base.x+5, y=base.y+5), blockId=base.id)
                planner.plan_attack(attack)
            if attacks:
                for attack in attacks:
                    planner.plan_attack(attack)
                
        except KeyboardInterrupt:
            print("Shutting down...")
            post_runner.stop()
            get_runner.stop()
            break

if __name__ == "__main__":
    main()
