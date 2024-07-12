import os
import requests
import logger

from dotenv import load_dotenv
load_dotenv()

servers = {
    "TEST": "https://games-test.datsteam.dev/",
    "MAIN": "https://games.datsteam.dev/"
}

def get_rounds():
    game_name = "game_name"
    resp = requests.get(f"{servers[os.getenv('SERVER')]}/rounds/{game_name}")
    print(resp)