import datetime
import os
import requests

from typing import Any, Dict, List, Optional, Tuple
from fastapi import Depends, Response, status

from src.const import MAX_ATTACKS_PER_ITER, MAX_BUILDS_PER_ITER
from src.planner import Planner
from src.models import Base, EnemyBase, Zombie, ZombieSpot
from src.logger import get_logger

from dotenv import load_dotenv
load_dotenv()

logger = get_logger("API")

servers = {
    "TEST": "https://games-test.datsteam.dev/",
    "MAIN": "https://games.datsteam.dev/"
}

def make_request(
        method: str, endpoint: str, body: Optional[Dict[str, Any]] = None, 
        params: Optional[Dict[str, Any]] = None
    ) -> Optional[Response]:
    headers = {
        "X-Auth-Token": os.getenv('TOKEN'),
    }
    api = servers[os.getenv('SERVER')]
    url = f"{api}{endpoint}"

    resp = requests.request(method, url, headers=headers, json=body, params=params)

    if resp.status_code == status.HTTP_200_OK:
        logger.debug(f"{datetime.datetime.now()}\n{method} Request for URL: {url} with body: {body}\nRequest success, body: {resp.text}\n")
        return resp
    else:
        logger.error(f"{datetime.datetime.now()}\n{method} Request for URL: {url} with body: {body}\nRequest failed with status: {resp.status_code}\nError text: {resp.text}")


def participate() -> Tuple[str, bool]:
    headers = {
        "X-Auth-Token": os.getenv('TOKEN'),
    }
    api = servers[os.getenv('SERVER')]
    url = f"{api}play/zombidef/participate"

    logger.info(datetime.datetime.now())
    logger.info(f"Attempt to participate in round")

    resp = requests.request("PUT", url, headers=headers)

    if resp.status_code == status.HTTP_200_OK:
        logger.info(f"Registered for round successfully\n")
        return f"ROUND STARTS IN {resp.json()['startsInSec']}", False
        
    if resp.status_code == status.HTTP_400_BAD_REQUEST:
        if "NOT" in resp.text:
            logger.info(f"Failed to register for round\n")
            return f"NOT PARTICIPATING IN THIS ROUND", False
        if "not" in  resp.text:
            logger.info(f"Rounds not found\n")
            return f"ROUNDS NOT FOUND", False
        else:
            logger.info(f"Round has already started\n")
            return "ROUND HAS ALREADY STARTED", True


def complete_action(planner: Planner):
    """
    POST request with all actions collected
    """
    body = {
        # NOTE: Generator expression inside list comprehension (WOW)
        # Do not touch this piece of code below is super cool
        # Written by Serega Vinogradov Inc. 2024
        "attack": [plan.model_dump() for plan in ((planner.get_next_attack_plan()) for _ in range(MAX_ATTACKS_PER_ITER)) if plan is not None],
        "build": [plan.model_dump() for plan in (planner.get_next_build_plan() for _ in range(MAX_BUILDS_PER_ITER)) if plan is not None],
        "moveBase": planner.get_next_move_base_plan(),
    }
    body = {k: v for k, v in body.items() if v is not None}
    resp = make_request("POST", f"play/zombidef/command", body=body)
    if resp:
        return resp.json()
    else:
        raise Exception("Request failed")


def get_rounds():
    game_name = "defense"

    resp = make_request("GET", f"rounds/{game_name}")
    if resp:
        return resp.json()
    else:
        raise Exception("Request failed")


def get_dynamic_objects():
    resp = make_request("GET", f"play/zombidef/units")
    if resp:
        resp_json = resp.json()
        bases = [Base(**base) for base in (resp_json['base'] or [])]
        enemy_bases = [EnemyBase(**enemy_base) for enemy_base in (resp_json['enemyBlocks'] or [])]
        zombies = [Zombie(**zombie) for zombie in (resp_json['zombies'] or [])]
        return bases, enemy_bases, zombies
    else:
        raise Exception("Request failed")
    

def get_static_objects():
    resp = make_request("GET", f"play/zombidef/world")
    if resp:
        resp_json = resp.json()
        zpots = [ZombieSpot(**zombie_spot) for zombie_spot in resp_json['zpots']]
        return zpots
    else:
        raise Exception("Request failed")
    
from src.context import Context
def collect_info(context: Context):
    context.update()