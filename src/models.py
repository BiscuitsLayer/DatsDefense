from enum import Enum

class Location:
    x: int
    y: int

class CommandType(Enum):
    ATTACK = 0
    BUILD = 1
    MOVE_BASE = 2

class Command:
    type: CommandType
    loc: Location
