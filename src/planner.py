from dataclasses import dataclass
from collections import deque

from src.models import Attack, Build, MoveBase

from threading import Timer
from functools import partial
from threading import Thread, Lock

class IntervalRunner(object):
    def __init__(self, interval, function, args=[], kwargs={}):
        """
        Runs the function at a specified interval with given arguments.
        """
        self.interval = interval
        self.function = partial(function, *args, **kwargs)
        self.running  = False 
        self._timer   = None 

    def __call__(self):
        """
        Handler function for calling the partial and continue. 
        """
        self.running = False  # mark not running
        self.start()          # reset the timer for the next go 
        self.function()       # call the partial function 

    def start(self):
        """
        Starts the interval and lets it run. 
        """
        if self.running:
            # Don't start if we're running! 
            return 
            
        # Create the timer object, start and set state. 
        self._timer = Timer(self.interval, self)
        self._timer.start() 
        self.running = True

    def stop(self):
        """
        Cancel the interval (no more function calls).
        """
        if self._timer:
            self._timer.cancel() 
        self.running = False 
        self._timer  = None


class Planner:
    def __init__(self):
        self.attack_queue: deque = deque()
        self.attack_queue_mutex = Lock()

        self.build_queue: deque = deque()
        self.build_queue_mutex = Lock()

        self.move_base_queue: deque = deque()
        self.move_base_queue_mutex = Lock()

    ## ATTACK ##

    def plan_attack(self, loc: Attack):
        with self.attack_queue_mutex:
            self.attack_queue.append(loc)

    def get_next_attack_plan(self):
        with self.attack_queue_mutex:
            if self.attack_queue:
                return self.attack_queue.popleft()

    def clear_attack_plan(self):
        with self.attack_queue_mutex:
            self.attack_queue.clear()

    ## BUILD ##

    def plan_build(self, loc: Build):
        with self.build_queue_mutex:
            self.build_queue.append(loc)

    def get_next_build_plan(self):
        with self.build_queue_mutex:
            if self.build_queue:
                return self.build_queue.popleft()

    def clear_build_plan(self):
        with self.build_queue_mutex:
            self.build_queue.clear()

    ## MOVE BASE ##

    def plan_move_base(self, loc: MoveBase):
        with self.move_base_queue_mutex:
            self.move_base_queue.append(loc)

    def get_next_move_base_plan(self):
        with self.move_base_queue_mutex:
            if self.move_base_queue:
                return self.move_base_queue.popleft()

    def clear_move_base_plan(self):
        with self.move_base_queue_mutex:
            self.move_base_queue.clear()
