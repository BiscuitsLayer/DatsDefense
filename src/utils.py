import os
import sys
import logging
from src.models import Base, EnemyBase, Map, TileType, Vec2, NeighborType, Zombie


def can_attack(loc: Vec2, bases: list[Base]):
    possible_bases: list[Base] = []

    for base in bases:
        dist_sqr = (base.x - loc.x) ** 2 + (base.y - loc.y) ** 2
        if dist_sqr <= base.range ** 2:
            print(dist_sqr)
            possible_bases.append(base.id)

    return possible_bases


def get_neighbor(loc: Vec2, type: NeighborType, delta: int = 1):
    match type:
        case NeighborType.TOP:
            return Vec2(x=loc.x, y=loc.y-delta)
        case NeighborType.TOP_LEFT:
            return Vec2(x=loc.x-delta, y=loc.y-delta)
        case NeighborType.TOP_RIGHT:
            return Vec2(x=loc.x+delta, y=loc.y-delta)
        case NeighborType.LEFT:
            return Vec2(x=loc.x-delta, y=loc.y)
        case NeighborType.RIGHT:
            return Vec2(x=loc.x+delta, y=loc.y)
        case NeighborType.BOTTOM_LEFT:
            return Vec2(x=loc.x-delta, y=loc.y+delta)
        case NeighborType.BOTTOM_RIGHT:
            return Vec2(x=loc.x+delta, y=loc.y+delta)
        case NeighborType.BOTTOM:
            return Vec2(x=loc.x, y=loc.y+delta)
        
def get_direction(dir: str) -> Vec2:
    if dir == "up":
        return Vec2(x=0, y=-1)
    if dir == "down":
        return Vec2(x=0, y=1)
    if dir == "left":
        return Vec2(x=-1, y=0)
    if dir == "right":
        return Vec2(x=1, y=0)
    
    raise ValueError("wrong direction name: must be up, down, left or right")
