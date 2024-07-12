from api import get_dynamic_objects
from models import Location

def can_attack(loc: Location):
    bases_loc = [Location(base['x'], base['y']) for base in get_dynamic_objects()['base']]
    for base_loc in bases_loc:
        dist_sqr = (base_loc.x - loc.x) ** 2 + (base_loc.y - loc.y) ** 2
        if dist_sqr >= base.range ** 2:
            possible_bases.append(base.id)