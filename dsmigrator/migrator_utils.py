import os
import json
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
                    + " List ID: "
                    + str(newid)
                    + ", Name: "
                    + newname,
                    flush=True,
                )
                all_new.append(str(newid))
                namecheck = -1
            except ApiException as e:
                print(e)
                error_json = json.loads(e.body)
                if (
                    "name already exists"
                    or "Name must be unique" in error_json["message"]
                ):
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
        oldname = oldjson["name"]
        oldid = oldjson["ID"]
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
