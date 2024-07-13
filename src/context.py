from DatsDefense.src.api import get_dynamic_objects, get_static_objects


class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
 

class Context(metaclass=Singleton):
    def __init__(self):
        self.bases = None
        self.enemy_bases = None
        self.zombies = None

        # No need to update zpots, because they are static (const)
        # self.zpots = get_static_objects()

    def update(self):
        print("Context updated")
        # self.bases, self.enemy_bases, self.zombies = get_dynamic_objects()
