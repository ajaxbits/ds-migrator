import os
import json
import requests
import urllib3
from deepsecurity.rest import ApiException


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
            print(
                f"#{str(count)} {to_title(type)} name: {str(item['name'])}", flush=True
            )
            print(f"#{str(count)} {to_title(type)} ID: {str(item['ID'])}", flush=True)
        print("Done!", flush=True)
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
            "POST", endpoint, headers=headers, data=payload, verify=cert
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
                print(
                    "#"
                    + str(count)
                    + " "
                    + type.capitalize()
                    + " ID: "
                    + str(newid)
                    + ", Name: "
                    + newname,
                    flush=True,
                )
                all_new.append(str(newid))
                namecheck = -1
            except ApiException as e:
                error_json = json.loads(e.body)
                if "name already exists" in error_json["message"]:
                    oldjson["name"] = oldname + " {" + str(rename) + "}"
                    rename = rename + 1
                elif "Name must be unique" in error_json["message"]:
                    print(
                        f"{oldjson['name']} already exists in new tenant, renaming...",
                        flush=True,
                    )
                    oldjson["name"] = oldname + " {" + str(rename) + "}"
                    rename = rename + 1
                else:
                    print(e.body, flush=True)
                    namecheck = -1
    return all_new


def validate_create_dict(all_old, api_instance, type):
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
                    print(
                        "#"
                        + str(count)
                        + " "
                        + type.capitalize()
                        + " List ID: "
                        + str(newid)
                        + ", Name: "
                        + newname,
                        flush=True,
                    )
                    new_dict[oldid] = newid
                    namecheck = -1
                except ApiException as e:
                    error_json = json.loads(e.body)
                    if "name already exists" in error_json["message"]:
                        print(
                            f"{oldjson['name']} already exists in new tenant, renaming..."
                        )
                        oldjson["name"] = oldname + " {" + str(rename) + "}"
                        rename = rename + 1
                    else:
                        print(e.body, flush=True)
                        namecheck = -1
    return new_dict


def validate_create_dict_custom(all_old, skeleton_dict, api_instance, type):
    # add printing to this
    custom_list = []
    for (count, object) in enumerate(all_old):
        namecheck = 1
        rename = 1
        object_json = json.loads(object)
        old_id = object_json["ID"]
        old_name = object_json["name"]
        while namecheck != -1:
            try:
                new_id = api_instance.search(old_name)
                if new_id is not None:
                    skeleton_dict[old_id] = new_id
                    print(
                        f"#{str(count)} {type}: {old_name}",
                        flush=True,
                    )
                elif "template" in object_json:
                    custom_list.append(json.dumps(object_json))
                namecheck = -1
            except ApiException as e:
                if "already exists" in e.body:
                    print(f"{old_name} already exists in new tenant, renaming...")
                    object_json["name"] = old_name + " {" + str(rename) + "}"
                    rename = rename + 1
                else:
                    print(e.body, flush=True)
                    pass
    print("Done!", flush=True)
    return skeleton_dict, custom_list
