import json
import sys
from dsmigrator.logging import console, error_console, filename, log
import logging
import os
from typing import Union

import requests
import urllib3
from deepsecurity.rest import ApiException


def safe_list_get(l: list, idx: int):
    try:
        return l[idx]
    except IndexError:
        return None


def value_exists(some_json, key):
    value = some_json.get(key)
    if value is not None:
        return value
    else:
        return False


def rename_json(json):
    if json["name"]:
        json["name"] = f"{json['name']} - Migrated"
    return json


def to_json_name(snake_case):
    temp = str(snake_case).split("_")
    json_name = temp[0] + "".join(ele.title() for ele in temp[1:])
    return json_name


def to_api_endpoint(snake_case):
    temp = str(snake_case).split("_")
    endpoint_name = "".join(ele for ele in temp)
    return endpoint_name


def to_title(snake_case):
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


def http_list_get(type, OLD_HOST, OLD_API_KEY, cert=False):
    """
    Takes in a string type in snake case, outputs a list of string json (for now)
    """
    list_all = []
    list_name = []
    list_id = []
    endpoint = f"{OLD_HOST}api/{to_api_endpoint(type)}"
    headers = {
        "api-secret-key": OLD_API_KEY,
        "api-version": "v1",
        "Content-Type": "application/json",
    }
    response = requests.request("GET", endpoint, headers=headers, data={}, verify=cert)
    describe = str(response.text)
    response_json = json.loads(describe).get(to_json_name(type))
    if response_json is not None:
        for count, item in enumerate(response_json):
            list_all.append(str(json.dumps(item)))
            list_id.append(str(item["ID"]))
            console.log(f"#{str(count)} {to_title(type)} name: {str(item['name'])}")
            console.log(f"#{str(count)} {to_title(type)} ID: {str(item['ID'])}")
        console.log("Done!")
    return list_all, list_name, list_id


def http_search(
    type,
    list_name,
    OLD_HOST,
    OLD_API_KEY,
    cert=False,
    search_type="name",
):
    # returns a list of items
    all_results = []
    if not isinstance(list_name, list):
        list_name = [list_name]
    for item in list_name:
        payload = (
            '{"searchCriteria": [{"fieldName": "'
            + str(search_type)
            + '","stringValue": "'
            + str(item)
            + '"}]}'
        )
        endpoint = f"{OLD_HOST}api/{to_api_endpoint(type)}/search"
        headers = {
            "api-secret-key": OLD_API_KEY,
            "api-version": "v1",
            "Content-Type": "application/json",
        }
        response = requests.request(
            "POST",
            endpoint,
            headers=headers,
            data=payload,
            verify=cert,
        )
        describe = str(response.text)
        all_results.append(describe)
    return all_results


def validate_create(all_old, api_instance, type):
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
                console.log(
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
                    console.log(
                        f"{oldjson['name']} already exists in new tenant, renaming...",
                    )
                    oldjson["name"] = oldname + " {" + str(rename) + "}"
                    rename = rename + 1
                else:
                    console.log(e.body)
                    namecheck = -1
    return all_new


def validate_create_dict(all_old: list, api_instance, type: str):
    """Take in a list of old objects, create the objects in Cloud One, then make a mapping of oldids to new ids for use later

    Args:
        all_old (list): a list of json strings that are provided as output of other functions
        api_instance (api_instance type found in api_config): configure in api_config
        type (str): The type of operation being performed, for console.loging (e.g. "Intrusion Prevention Rule")

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
                    console.log(
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
                        console.log(
                            f"{oldjson['name']} already exists in new tenant, renaming..."
                        )
                        oldjson["name"] = oldname + " {" + str(rename) + "}"
                        rename = rename + 1
                    else:
                        console.log(e.body)
                        namecheck = -1
    return new_dict


def validate_create_dict_custom(
    all_old: list, skeleton_dict: dict, api_instance, type: str
):
    """Transforms a list of pre-defined DS objects in json into a id mapping dict and a list of custom items

    Args:
        all_old (list): list of pre-defined objects as json strings
        skeleton_dict (dict): A skeleton of the final ID mapping of form {oldid1: None, oldid2: None,...}
        api_instance (ApiInstance): The requisite ApiInstance object defined in api_config
        type (str): The type of operation being performed, for console.loging (e.g. "Intrusion Prevention Rule")

    Returns:
        (dict, list): A dict of form {oldid:newid,...} for all common pre-defined objects, and a list of custom objects as strings of json
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
                    console.log(
                        f"#{str(count)} {type}: {old_name}",
                    )
                elif "template" in item_json:
                    custom_list.append(json.dumps(item_json))
                namecheck = -1
            except ApiException as e:
                if "already exists" in e.body:
                    console.log(f"{old_name} already exists in new tenant, renaming...")
                    item_json["name"] = old_name + " {" + str(rename) + "}"
                    rename = rename + 1
                else:
                    console.log(e.body)
                    pass
    console.log("Done!")
    return skeleton_dict, custom_list
