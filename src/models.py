from enum import Enum
from pydantic import BaseModel

class Location(BaseModel):
    x: int
    y: int

class Base(BaseModel):
    attack: int # сколько урона даёт
    range: int # насколько далеко
    health: int
    loc: Location
    isHead: bool
    lastAttack: Location

    def __init__(self, **kwargs):
        self.loc = Location(x=kwargs.get('x'), y=kwargs.get('y'))

        super.__init__()

class CommandType(Enum):
    ATTACK = 0
    BUILD = 1
    MOVE_BASE = 2

class Command:
    type: CommandType
    loc: Location

class ZombieType(Enum):
    NORMAL = "normal" # атакует одну клетку. Самоуничтожается после атаки.
    FAST = "fast" # атакует одну клетку. Самоуничтожается после атаки. Имеет повышенную скорость 2.
    BOMBER = "bomber" # атакует все клетки в радиусе 1 от себя. Самоуничтожается после атаки.
    LINER = "liner" # атакует все клетки базы расположенные рядом друг с другом вне зависимости от их количества. Самоуничтожается после атаки.
    JUGGERNAUT = "juggernaut" # уничтожает все клетки базы на которых окажется. В отличие от своих собратьев он не самоуничтожается, а всегда будет идти напролом, пока его не остановит игрок или специальные клетки.
    CHAOS_KNIGHT = "chaos_knight" # атакует клетку в которой оказался. Двигается в соответствии с правилами движения коня в шахматах. Движение происходит всегда на 3 клетки вперед и одну клетку в сторону, сторона и поворот Г определяется рандомно каждый ход. После атаки не самоуничтожается.
