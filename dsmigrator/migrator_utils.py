import json
import logging
import os
import sys
from typing import List, Tuple, Union

import requests
import urllib3
from deepsecurity.rest import ApiException

from dsmigrator.logging import console, error_console, filename, log


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
        log.error(
            "Having trouble connecting to the old DSM. Please ensure the url and routes are correct."
        )
        log.error("Aborting...")
        with open(filename, "a") as logfile:
            logfile.write(f"{error_console.export_text(clear=False)}\n")
            logfile.close()
        sys.exit(0)


def validate_create(all_old: List[str], api_instance, type: str) -> List[str]:
    """
    Takes in old json objects, creates them in Cloud one, and returns a list of
    the new object IDs in Cloud One

    Args:
        all_old (List[str]): list of string-formatted json objects from DS
        api_instance (RestApiConfiguration): SDK module wrapper object configured from api_config
        type (str): what to display during printing (e.g. 'Antimalware Configuration')

    Returns:
        List[str]: A list of all the objects' new IDs in Cloud One (as strings)
    """
    all_new = []
    for count, dirlist in enumerate(all_old):
        namecheck = 1
        rename = 1
        oldjson = json.loads(dirlist)
        oldname = oldjson["name"]
        while namecheck != -1:
            try:
                newname = api_instance.create(oldjson)
                newid = api_instance.search(newname)
                log.info(
                    "#"
                    + str(count)
                    + " "
                    + type.capitalize()
                    + " ID: "
                    + str(newid)
                    + ", Name: "
                    + newname,
                )
                all_new.append(str(newid))
                namecheck = -1
            except ApiException as e:
                error_json = json.loads(e.body)
                if "name already exists" in error_json["message"]:
                    oldjson["name"] = oldname + " {" + str(rename) + "}"
                    rename = rename + 1
                elif "Name must be unique" in error_json["message"]:
                    log.info(
                        f"{oldjson['name']} already exists in new tenant, renaming...",
                    )
                    oldjson["name"] = oldname + " {" + str(rename) + "}"
                    rename = rename + 1
                else:
                    log.info(e.body)
                    namecheck = -1
    return all_new


def validate_create_dict(all_old: list, api_instance, type: str) -> dict:
    """Take in a list of old objects, create the objects in Cloud One, then make a mapping of oldids to new ids for use later

    Args:
        all_old (list): a list of json strings that are provided as output of other functions
        api_instance (RestApiConfiguration): an sdk configuration from api_config
        type (str): The type of operation being performed, for log.infoing (e.g. "Intrusion Prevention Rule")

    Returns:
        dict: A dict of form {oldid1:newid1, oldid2:newid2, ...}
    """
    new_dict = {}
    for count, dirlist in enumerate(all_old):
        namecheck = 1
        rename = 1
        oldjson = json.loads(dirlist)
        oldname = oldjson.get("name")
        oldid = oldjson.get("ID")
        if (oldname is not None) and (oldid is not None):
            while namecheck != -1:
                try:
                    newname = api_instance.create(oldjson)
                    newid = api_instance.search(newname)
                    log.info(
                        "#"
                        + str(count)
                        + " "
                        + type.capitalize()
                        + " List ID: "
                        + str(newid)
                        + ", Name: "
                        + newname,
                    )
                    new_dict[oldid] = newid
                    namecheck = -1
                except ApiException as e:
                    error_json = json.loads(e.body)
                    if "name already exists" in error_json["message"]:
                        log.info(
                            f"{oldjson['name']} already exists in new tenant, renaming..."
                        )
                        oldjson["name"] = oldname + " {" + str(rename) + "}"
                        rename = rename + 1
                    else:
                        log.info(e.body)
                        namecheck = -1
    return new_dict


def validate_create_dict_custom(
    all_old: list, skeleton_dict: dict, api_instance, type: str
) -> Tuple[dict, list]:
    """Transforms a list of pre-defined DS objects in json into a id mapping dict and a list of custom items

    Args:
        all_old (list): list of pre-defined objects as json strings
        skeleton_dict (dict): A skeleton of the final ID mapping of form {oldid1: None, oldid2: None,...}
        api_instance (ApiInstance): The requisite ApiInstance object defined in api_config
        type (str): The type of operation being performed, for log.infoing (e.g. "Intrusion Prevention Rule")

    Returns:
        Tuple[(dict, list)]: A dict of form {oldid:newid,...} for all common pre-defined objects, and a list of custom objects as strings of json
    """
    custom_list = []
    for (count, json_string) in enumerate(all_old):
        namecheck = 1
        rename = 1
        item_json = json.loads(json_string)
        old_id = item_json["ID"]
        old_name = item_json["name"]
        while namecheck != -1:
            try:
                new_id = api_instance.search(old_name)
                if new_id is not None:
                    skeleton_dict[old_id] = new_id
                    log.info(
                        f"#{str(count)} {type}: {old_name}",
                    )
                elif "template" in item_json:
                    custom_list.append(json.dumps(item_json))
                else:
                    log.warning(
                        f"{old_name} is not valid in Workload Security and will not be transferred."
                    )
                    log.warning(
                        f"Consider transferring {old_name} manually using the xml export feature in the GUI."
                    )
                    with open(filename, "a") as logfile:
                        logfile.write(f"{error_console.export_text(clear=False)}\n")
                        logfile.close()
                namecheck = -1
            except ApiException as e:
                if "already exists" in e.body:
                    log.info(f"{old_name} already exists in new tenant, renaming...")
                    item_json["name"] = old_name + " {" + str(rename) + "}"
                    rename = rename + 1
                else:
                    log.error(e.body)
                    pass
    log.info("Done!")
    return skeleton_dict, custom_list
