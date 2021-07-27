import json
import os
import datetime
import sys
from typing import List, Tuple, Union

import requests

from dsmigrator.logging import log

policy_mapping = None
suffix = f" - migrated ({datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat()})"


def safe_list_get(l: list, idx: int):
    try:
        return l[idx]
    except IndexError:
        return None


def rename_json(json: dict) -> dict:
    """
    Adds 'Migrated' to the end of items

    Args:
        json (dict): dict of some kind from json

    Returns:
        dict: same dict with different 'name' key
    """
    if json["name"]:
        json["name"] = f"{json['name']} - Migrated"
    return json


def to_title(snake_case: str) -> str:
    """
    Takes a snake case string and turns it into a title case string

    Args:
        snake_case (str): snake case string

    Returns:
        str: title case string
    """
    temp = str(snake_case).split("_")
    title = " ".join(ele.title() for ele in temp)
    return title


def safe_request(
    old_api_key: str, http_method: str, url: str, payload: dict, cert: Union[str, bool]
) -> requests.models.Response:
    """
    Makes a request through the requests module, and handles errors through rich

    Args:
        old_api_key (str): self-explanatory
        http_method (str): "GET", "POST", etc
        url (str): of form "https://www.google.com/"
        payload (dict): Dict version of json payload
        cert (Union[str, bool]): if using a cert, pass string file path here. If not, pass False.

    Returns:
        requests.models.Response: Response object from Requests
    """
    headers = {
        "api-secret-key": old_api_key,
        "api-version": "v1",
        "Content-Type": "application/json",
    }
    try:
        return requests.request(
            http_method,
            url,
            headers=headers,
            data=payload,
            verify=cert,
        )
    except Exception as e:
        log.exception(e)
        log.critical(
            "Having trouble connecting to the old DSM. Please ensure the url and routes are correct."
        )
        log.critical("Aborting...")
        sys.exit(0)

def _load_policy_mapping(migration_task_response: dict):
    global policy_mapping
    policy_mapping = {}
    for map in migration_task_response["policyMappings"]:
        dsm_id = map["migrateFrom"]["policyID"]
        c1ws_id = map["migrateTo"]["policyID"]
        policy_mapping[dsm_id] = c1ws_id
        log.info(f"Policy ID mapping: {dsm_id} -> {c1ws_id}")


def get_c1ws_policy_id(dsm_policy_id: int, migration_task_response) -> int:
    if policy_mapping is None:
        _load_policy_mapping(migration_task_response)
    return policy_mapping[dsm_policy_id]


def get_suffix() -> str:
    return suffix

