import os
from typing import Any, Dict, Optional
import requests
from fastapi import Depends, Response, status
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
    url = f"{api}a{endpoint}"

    logger.info(f"Request for URL: {url} with body: {body}")
    resp = requests.request(method, url, headers=headers, json=body, params=params)

    if resp.status_code == status.HTTP_200_OK:
        logger.debug("Request success\n")
        return resp
    else:
        logger.error(f"Request failed with status: {resp.status_code}")
        logger.error(f"Error text: {resp.text}")


def get_rounds():
    game_name = "game_name"

    resp = make_request("GET", f"rounds/{game_name}")

    if resp:
        return resp.json()
    else:
        raise Exception("Request failed")