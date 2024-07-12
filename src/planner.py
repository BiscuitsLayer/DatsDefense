from dataclasses import dataclass
import multiprocessing
from queue import Queue

from src.models import Vec2

@dataclass
class Planner:
    def __init__(self):
        self.attack_queue = Queue()
        self.build_queue = Queue()
        self.move_base_queue = Queue()

    ## ATTACK ##

    def plan_attack(self, loc: Vec2):
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

    def plan_build(self, loc: Vec2):
        self.build_queue.put(loc)

    ## MOVE BASE ##

    def plan_move_base(self, loc: Vec2):
        self.move_base_queue.put(loc)