import sys
import os
import time
from time import sleep
import requests
import urllib3
import json

cert = False


def AddPolicy(allofpolicy, url_link_final_2, tenant2key):
    print("Creating Policy to Tenant 2 with new ID", flush=True)
    for count, dirlist in enumerate(allofpolicy):
        rename = 1
        namecheck = 1
        oldpolicyjson = json.loads(dirlist)
        oldname = oldpolicyjson["name"]
        while namecheck != -1:
            payload = dirlist
            url = url_link_final_2 + "api/policies"
            headers = {
                "api-secret-key": tenant2key,
                "api-version": "v1",
                "Content-Type": "application/json",
            }
            response = requests.request(
                "POST", url, headers=headers, data=payload, verify=cert
            )
            describe = str(response.text)
            policyjson = json.loads(describe)
            if not "message" in policyjson:
                print(
                    "#" + str(count) + " Policy name: " + policyjson["name"], flush=True
                )
                print(
                    "#" + str(count) + " Policy ID: " + str(policyjson["ID"]),
                    flush=True,
                )
                namecheck = -1
            else:
                if "name already exists" in policyjson["message"]:
                    oldpolicyjson["name"] = oldname + " {" + str(rename) + "}"
                    dirlist = json.dumps(oldpolicyjson)
                    rename = rename + 1
                else:
                    print(describe, flush=True)
                    namecheck = -1
