from models import Vec2
from typing import List
import json

def load_knight_offsets() -> List[List[Vec2]]:
    with open('knight_offsets.json', 'r') as json_file:
        data_dict = json.load(json_file)

    return [[Vec2(x=vec['x'], y=vec['y']) for vec in row] for row in data_dict]

KNIGHT_OFFSETS = load_knight_offsets()