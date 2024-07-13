from pydantic.dataclasses import dataclass
from enum import Enum, auto
from typing import Any, Optional, List
from pydantic import BaseModel

INT_INFTY = 10 ** 10


class NeighborType(Enum):
    TOP = auto(),
    TOP_LEFT = auto(),
    TOP_RIGHT = auto(),
    LEFT = auto(),
    RIGHT = auto(),
    BOTTOM_LEFT = auto(),
    BOTTOM_RIGHT = auto(),
    BOTTOM = auto()

class DirectionType(Enum):
    UP = "up"
    DOWN = "down"
    LEFT = "left"
    RIGHT = "right"

class Vec2(BaseModel):
    x: int
    y: int

    def __hash__(self):
        return hash(str(self))
    
    def __add__(self, other):
        if not isinstance(other, Vec2):
            raise ValueError("Operand must be instance of Vec2")
        return Vec2(self.x + other.x, self.y + other.y)
    
    def __mul__(self, scalar):
        if not isinstance(scalar, int):
            raise ValueError("Operand must be a numeric value")
        return Vec2(self.x * scalar, self.y * scalar)

class Rect:
    top_left: Vec2
    size: Vec2

    def __init__(self, top_left: Vec2, size: Vec2):
        self.top_left = top_left
        self.size = size

    def is_point_inside(self, point: Vec2) -> bool:
        return (
            point.x >= self.top_left.x and point.x < self.top_left.x + self.size.x and
            point.y >= self.top_left.y and point.y < self.top_left.y + self.size.y
        )

class Attack(BaseModel):
    blockId: str
    target: Vec2

class Build(Vec2):
    pass

class MoveBase(Vec2):
    pass

class Base(BaseModel):
    attack: int # сколько урона даёт
    health: int
    id: str
    isHead: bool
    lastAttack: Vec2
    range: int # насколько далеко
    x: int
    y: int

class EnemyBase(BaseModel):
    attack: int # сколько урона даёт
    health: int
    isHead: bool
    lastAttack: Vec2
    name: str
    x: int
    y: int

class Zombie(BaseModel):
    attack: int
    direction: str
    health: int
    id: str
    speed: int
    type: str
    waitTurns: int
    x: int
    y: int

class ZombieSpot(Vec2):
    type: str

class ZombieType(Enum):
    NORMAL = "normal" # атакует одну клетку. Самоуничтожается после атаки.
    FAST = "fast" # атакует одну клетку. Самоуничтожается после атаки. Имеет повышенную скорость 2.
    BOMBER = "bomber" # атакует все клетки в радиусе 1 от себя. Самоуничтожается после атаки.
    LINER = "liner" # атакует все клетки базы расположенные рядом друг с другом вне зависимости от их количества. Самоуничтожается после атаки.
    JUGGERNAUT = "juggernaut" # уничтожает все клетки базы на которых окажется. В отличие от своих собратьев он не самоуничтожается, а всегда будет идти напролом, пока его не остановит игрок или специальные клетки.
    CHAOS_KNIGHT = "chaos_knight" # атакует клетку в которой оказался. Двигается в соответствии с правилами движения коня в шахматах. Движение происходит всегда на 3 клетки вперед и одну клетку в сторону, сторона и поворот Г определяется рандомно каждый ход. После атаки не самоуничтожается.

class TileType(Enum):
    DEFAULT = auto()
    BASE = auto()
    CONTROL_CENTER = auto()
    ENEMY_BASE = auto()
    WALL = auto()
    ZOMBIE_GTOR = auto()


class Map:
    """
        Хранит тайлы карты

        tiles - список тайлов
        адресация: tiles[y][x]

        зомби при хранении тайлов не учитываются, т.к. считаются динамическими игровыми объектами,
        не представляющими из себя постройку, поверхность, препятствие etc

        control_center - доступ к координатам центра управления. Опционален (тк нас могли УБИТЬ АХАХАХАХАХАХАХААХАХАХАХАХ)
        base_entrance - координаты некой (любой) клетки базы. Опционально (если нас ПОЛНОСТЬЮ СНЕСЛИ АХАХАХАХАХАХАХААХАХАХАХАХ)
        может быть полезно для каких-либо обходов в стиле dfs/bfs
    """

    tiles: List[List[TileType]]
    control_center: Optional[Vec2] = None
    base_entrance: Optional[Vec2] = None
    bounds: Rect = Rect(top_left=Vec2(x=0, y=0), size=Vec2(x=0, y=0))

    def __init__(self, bases: List[Base], enemy_bases: List[EnemyBase], zombies: List[Zombie], zpots: List[ZombieSpot]):
        self._calc_bounds(bases, enemy_bases, zombies, zpots)

        self.tiles = [[TileType.DEFAULT for _ in range(self.bounds.size.x)] for _ in range(self.bounds.size.y)]

        for base in bases:
            base_entrance = Vec2(x=base.x, y=base.y)
            if (base.isHead):
                control_center = Vec2(x=base.x, y=base.y)
            self.tiles[base.y][base.x] = TileType.BASE
        for enemy_base in enemy_bases:
            self.tiles[base.y][base.x] = TileType.ENEMY_BASE
        for zpot in zpots:
            if zpot.type == "wall":
                self.tiles[base.y][base.x] = TileType.WALL
            if zpot.type == "default":
                self.tiles[base.y][base.x] = TileType.ZOMBIE_GTOR

    def _calc_bounds(self, bases, enemy_bases, zombies, zpots):
        top_left = Vec2(x=0, y=0)
        down_right = Vec2(x=-INT_INFTY, y=-INT_INFTY)

        for base in bases:
            self._update_bounds_by_point(top_left, down_right, Vec2(x=base.x, y=base.y))

        for enemy_base in enemy_bases:
            self._update_bounds_by_point(top_left, down_right, Vec2(x=enemy_base.x, y=enemy_base.y))

        for zombie in zombies:
            self._update_bounds_by_point(top_left, down_right, Vec2(x=zombie.x, y=zombie.y))

        self.bounds.top_left = top_left
        self.bounds.size.x = down_right.x - top_left.x + 1
        self.bounds.size.y = down_right.y - top_left.y + 1

    def _update_bounds_by_point(self, top_left: Vec2, down_right: Vec2, new_point: Vec2):
        top_left.x = min(top_left.x, new_point.x)
        top_left.y = min(top_left.y, new_point.y)

        down_right.x = max(down_right.x, new_point.x)
        down_right.y = max(down_right.y, new_point.y)
        