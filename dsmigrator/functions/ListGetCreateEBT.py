import sys
import os
import time
from time import sleep
import requests
import urllib3
import json

cert = False


def ListEventTask(url_link_final, tenant1key):
    payload = {}
    url = url_link_final + "api/eventbasedtasks"
    headers = {
        "api-secret-key": tenant1key,
        "api-version": "v1",
        "Content-Type": "application/json",
    }
    response = requests.request("GET", url, headers=headers, data=payload, verify=cert)
    describe = str(response.text)
    index = 0
    oldetname = []
    oldetid = []
    namejson = json.loads(describe)
    for here in namejson["eventBasedTasks"]:
        oldetname.append(str(here["name"]))
        oldetid.append(str(here["ID"]))
    return enumerate(oldetname), oldetid


def GetEventTask(etIDs, url_link_final, tenant1key):
    allet = []
    nameet = []
    print("Getting Target Task...", flush=True)
    if etIDs:
        for part in etIDs:
            payload = {}
            url = url_link_final + "api/eventbasedtasks/" + str(part)
            headers = {
                "api-secret-key": tenant1key,
                "api-version": "v1",
                "Content-Type": "application/json",
            }
            response = requests.request(
                "GET", url, headers=headers, data=payload, verify=cert
            )

            describe = str(response.text)
            allet.append(describe)
            namejson = json.loads(describe)
            nameet.append(str(namejson["name"]))
    print(allet, flush=True)
    print(nameet, flush=True)
    return allet, nameet


def CreateEventTask(allet, nameet, url_link_final_2, tenant2key):
    print("Creating Task to target Account...", flush=True)
    if nameet:
        for count, dirlist in enumerate(nameet):
            payload = (
                '{"searchCriteria": [{"fieldName": "name","stringValue": "'
                + dirlist
                + '"}]}'
            )
            url = url_link_final_2 + "api/eventbasedtasks/search"
            headers = {
                "api-secret-key": tenant2key,
                "api-version": "v1",
                "Content-Type": "application/json",
            }
            response = requests.request(
                "POST", url, headers=headers, data=payload, verify=cert
            )
            describe = str(response.text)
            taskjson = json.loads(describe)
            if not "message" in taskjson:
                if taskjson["eventBasedTasks"]:
                    for here in taskjson["eventBasedTasks"]:
                        indexid = here["ID"]
                        payload = allet[count]
                        url = url_link_final_2 + "api/eventbasedtasks/" + str(indexid)
                        headers = {
                            "api-secret-key": tenant2key,
                            "api-version": "v1",
                            "Content-Type": "application/json",
                        }
                        response = requests.request(
                            "POST", url, headers=headers, data=payload, verify=cert
                        )
                        describe = str(response.text)
                        taskjson = json.loads(describe)
                        print(
                            "#"
                            + str(count)
                            + " Event Based Task name: "
                            + taskjson["name"],
                            flush=True,
                        )
                        print(
                            "#"
                            + str(count)
                            + " Event Based ID: "
                            + str(taskjson["ID"]),
                            flush=True,
                        )
                else:
                    payload = allet[count]
                    url = url_link_final_2 + "api/eventbasedtasks"
                    headers = {
                        "api-secret-key": tenant2key,
                        "api-version": "v1",
                        "Content-Type": "application/json",
                    }
                    response = requests.request(
                        "POST", url, headers=headers, data=payload, verify=cert
                    )
                    describe = str(response.text)
                    taskjson = json.loads(describe)
                    print(
                        "#"
                        + str(count)
                        + " Event Based Task name: "
                        + taskjson["name"],
                        flush=True,
                    )
                    print(
                        "#" + str(count) + " Event Based ID: " + str(taskjson["ID"]),
                        flush=True,
                    )
            else:
                print(describe, flush=True)
                print(payload, flush=True)
