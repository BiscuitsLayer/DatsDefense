import datetime
import os
import requests

from typing import Any, Dict, List, Optional, Tuple
from fastapi import Depends, Response, status

from src.models import Command
from src.utils import get_logger

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

    logger.info(datetime.datetime.now())
    logger.info(f"Request for URL: {url} with body: {body}")
    resp = requests.request(method, url, headers=headers, json=body, params=params)

    if resp.status_code == status.HTTP_200_OK:
        logger.debug("Request success\n")
        return resp
    else:
        logger.error(f"Request failed with status: {resp.status_code}")
        logger.error(f"Error text: {resp.text}")


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


def complete_action(commands: List[Command]):
    resp = make_request("POST", f"play/zombidef/command")
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
        return resp.json()
    else:
        raise Exception("Request failed")
    

def get_static_objects():
    resp = make_request("GET", f"play/zombidef/world")
    if resp:
        return resp.json()
    else:
        raise Exception("Request failed")
    
