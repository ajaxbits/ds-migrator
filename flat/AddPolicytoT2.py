import sys
import os
import deepsecurity
from deepsecurity.rest import ApiException
import time
from time import sleep
import requests
import urllib3
import json

from api_config import PolicyApiInstance


def validate_create(all_old, api_instance, type):
    all_new = []
    id_dict = {}
    for count, dirlist in enumerate(all_old):
        namecheck = 1
        rename = 1
        oldjson = json.loads(dirlist)
        oldname = oldjson["name"]
        oldid = oldjson["ID"]
        print(oldid)
        while namecheck != -1:
            print(id_dict)
            if "parentID" in oldjson.keys():
                oldjson["parentID"] = id_dict[oldjson["parentID"]]
            try:
                newname = api_instance.create(oldjson)
                newid = api_instance.search(newname)
                print(newid)
                id_dict[oldid] = newid
                print(newname)
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
    return all_new


cert = False


def AddPolicy(allofpolicy):
    print("Creating Policy to Tenant 2 with new ID", flush=True)
    if allofpolicy:
        validate_create(allofpolicy, PolicyApiInstance(), "policy")
