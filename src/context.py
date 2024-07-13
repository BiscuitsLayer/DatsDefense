<<<<<<< HEAD
from DatsDefense.src.api import get_dynamic_objects, get_static_objects

=======
from src.api import get_dynamic_objects, get_static_objects
from src.models import *
>>>>>>> 9053c0fcef3ad36df4080c1a7d783cb13c933e75

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
 

class Context(metaclass=Singleton):
    def __init__(self):
        self.bases: list[Base] = None
        self.enemy_bases: list[EnemyBase] = None
        self.zombies: list[Zombie] = None

        # No need to update zpots, because they are static (const)
        self.zpots: list[ZombieSpot] = get_static_objects()

    def update(self):
        self.bases, self.enemy_bases, self.zombies = get_dynamic_objects()
