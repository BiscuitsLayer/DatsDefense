from dataclasses import dataclass
import multiprocessing
from queue import Queue

from src.models import Location

@dataclass
class Planner:
    def __init__(self):
        self.attack_queue = Queue()
        self.build_queue = Queue()
        self.move_base_queue = Queue()

    ## ATTACK ##

    def plan_attack(self, loc: Location):
        self.attack_queue.put(loc)

    def get_next_attack_plan(self):
        return self.attack_queue.get()

    def clear_attack(self):
        try:
            while True:
                self.attack_queue.get_nowait()
        except multiprocessing.queues.Empty:
            pass  # reached before the producer process deserialises the Process

    ## BUILD ##

    def plan_build(self, loc: Location):
        self.build_queue.put(loc)

    ## MOVE BASE ##

    def plan_move_base(self, loc: Location):
        self.move_base_queue.put(loc)