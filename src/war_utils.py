from api import get_dynamic_objects
from models import Location

def can_attack(loc: Location):
    bases_coords = [Location(base['x'], base['y']) for base in get_dynamic_objects()['base']]
    dist <= sqrt(abs(x1-x2)^2 + abs(y1-y2)^2)