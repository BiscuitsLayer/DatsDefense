import json

<<<<<<< HEAD
from DatsDefense.src.api import get_dynamic_objects
=======
from src.api import get_dynamic_objects
>>>>>>> 9053c0fcef3ad36df4080c1a7d783cb13c933e75
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