import sys
import os
import time
from time import sleep
import requests
import urllib3
import json
from .api_config import RestApiConfiguration, DirectoryListsApiInstance

cert = False


def DirListTenant2(alldirectory, url_link_final_2, tenant2key):

    alldirectorynew = []
    print("Creating list to tenant 2, if any", flush=True)
    if alldirectory:
        for count, dirlist in enumerate(alldirectory):
            rename = 1
            namecheck = 1
            oldjson = json.loads(dirlist)
            oldname = oldjson["name"]
            while namecheck != -1:
                payload = dirlist
                url = url_link_final_2 + "api/directorylists"
                headers = {
                    "api-secret-key": tenant2key,
                    "api-version": "v1",
                    "Content-Type": "application/json",
                }
                response = requests.request(
                    "POST", url, headers=headers, data=payload, verify=cert
                )
                describe = str(response.text)
                idjson = json.loads(describe)
                if not "message" in idjson:
                    print(
                        "#" + str(count) + " Directory List ID: " + str(idjson["ID"]),
                        flush=True,
                    )
                    alldirectorynew.append(str(idjson["ID"]))
                    namecheck = -1
                else:
                    if "name already exists" in idjson["message"]:
                        oldjson["name"] = oldname + " {" + str(rename) + "}"
                        dirlist = json.dumps(oldjson)
                        rename = rename + 1
                    else:
                        print(describe, flush=True)
                        namecheck = -1
    print("new directory list", flush=True)
    print(alldirectorynew, flush=True)

    return alldirectorynew


def FileExtensionListTenant2(allfileextention, url_link_final_2, tenant2key):
    allfileextentionnew = []
    if allfileextention:
        for count, dirlist in enumerate(allfileextention):
            rename = 1
            namecheck = 1
            oldjson = json.loads(dirlist)
            oldname = oldjson["name"]
            while namecheck != -1:
                payload = dirlist
                url = url_link_final_2 + "api/fileextensionlists"
                headers = {
                    "api-secret-key": tenant2key,
                    "api-version": "v1",
                    "Content-Type": "application/json",
                }
                response = requests.request(
                    "POST", url, headers=headers, data=payload, verify=cert
                )
                describe = str(response.text)
                idjson = json.loads(describe)
                if not "message" in idjson:
                    print(
                        "#"
                        + str(count)
                        + " File Extension List ID: "
                        + str(idjson["ID"]),
                        flush=True,
                    )
                    allfileextentionnew.append(str(idjson["ID"]))
                    namecheck = -1
                else:
                    if "name already exists" in idjson["message"]:
                        oldjson["name"] = oldname + " {" + str(rename) + "}"
                        dirlist = json.dumps(oldjson)
                        rename = rename + 1
                    else:
                        print(describe, flush=True)
                        namecheck = -1
    print("new file extention", flush=True)
    print(allfileextentionnew, flush=True)
    return allfileextentionnew


def FileListTenant2(allfilelist, url_link_final_2, tenant2key):
    allfilelistnew = []
    if allfilelist:
        for count, dirlist in enumerate(allfilelist):
            rename = 1
            namecheck = 1
            oldjson = json.loads(dirlist)
            oldname = oldjson["name"]
            while namecheck != -1:
                payload = dirlist
                url = url_link_final_2 + "api/filelists"
                headers = {
                    "api-secret-key": tenant2key,
                    "api-version": "v1",
                    "Content-Type": "application/json",
                }
                response = requests.request(
                    "POST", url, headers=headers, data=payload, verify=cert
                )
                describe = str(response.text)
                idjson = json.loads(describe)
                if not "message" in idjson:
                    print(
                        "#" + str(count) + " File List ID: " + str(idjson["ID"]),
                        flush=True,
                    )
                    allfilelistnew.append(str(idjson["ID"]))
                    namecheck = -1
                else:
                    if "name already exists" in idjson["message"]:
                        oldjson["name"] = oldname + " {" + str(rename) + "}"
                        dirlist = json.dumps(oldjson)
                        rename = rename + 1
                    else:
                        print(describe, flush=True)
                        namecheck = -1
    print("new file list", flush=True)
    print(allfilelistnew, flush=True)
    return allfilelistnew
