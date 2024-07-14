<<<<<<< HEAD
from DatsDefense.src.api import get_dynamic_objects, get_static_objects

=======
from src.api import get_dynamic_objects, get_static_objects
from src.build_utils import build_route_to_enemies
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
        self.bases: list[Base] = []
        self.enemy_bases: list[EnemyBase] = []
        self.zombies: list[Zombie] = []

        # No need to update zpots, because they are static (const)
        self.zpots: list[ZombieSpot] = get_static_objects()

        self.map: Map = Map(self.bases, self.enemy_bases, self.zombies, self.zpots)
        self.routes_to_enemies = []

    def update(self):
        self.bases, self.enemy_bases, self.zombies = get_dynamic_objects()
        self.map = Map(self.bases, self.enemy_bases, self.zombies, self.zpots)
        self.routes_to_enemies = build_route_to_enemies(
            n_to_build=5,
            enemy_bases_coords=[Vec2(x=base.x, y=base.y) for base in self.enemy_bases],
            bases_coords=[Vec2(x=base.x, y=base.y) for base in self.bases],
            zombies=self.zombies,
            map=self.map
        )

