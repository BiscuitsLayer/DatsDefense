from src.models import Base, Location

def can_attack(loc: Location, bases: list[Base]):
    possible_bases: list[Base] = []

    for base in bases:
        dist_sqr = (base.x - loc.x) ** 2 + (base.y - loc.y) ** 2
        if dist_sqr <= base.range ** 2:
            print(dist_sqr)
            possible_bases.append(base.id)

    return possible_bases
