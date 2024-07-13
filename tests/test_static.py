import json

from src.api import get_dynamic_objects
from src.models import ZombieSpot

sample_json = """
{
    "realmName": "map1",
    "zpots": [
        {
            "x": 1,
            "y": 1,
            "type": "default"
        }
    ]
}
"""

resp_json = json.loads(sample_json)

zpots = [ZombieSpot(**zombie_spot) for zombie_spot in resp_json['zpots']]

print(zpots)