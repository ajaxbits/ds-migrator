import sys
import os
import time
from time import sleep
import requests
import urllib3
import json

import deepsecurity
import re


def to_snake(camel_case):
    pattern = re.compile(r"(?<!^)(?=[A-Z])")
    snake = pattern.sub("_", camel_case).lower()
    return snake


class RestApiConfiguration:
    def __init__(self, overrides=False):
        user_config = json.load(open("../config.json", "r"))
        self.configuration = deepsecurity.Configuration()
        self.api_client = deepsecurity.ApiClient(self.configuration)
        self.overrides = overrides
        self.configuration.host = (
            f"{user_config['new_hostname']}:{user_config['new_port']}/api"
        )
        self.configuration.api_key["api-secret-key"] = user_config["new_api_secret_key"]
        self.api_version = "v1"


class DirectoryListsApiInstance(RestApiConfiguration):
    def __init__(self, overrides=False):
        super().__init__(overrides)
        self.api_instance = deepsecurity.DirectoryListsApi(self.api_client)

    def create(self, json_dirlist):
        dirlist = deepsecurity.DirectoryList()
        for key in json_dirlist:
            if not key == "ID":
                setattr(dirlist, to_snake(key), json_dirlist[key])
        self.api_instance.create_directory_list(json_dirlist, self.api_version)
        return dirlist.name, dirlist.id


cert = False


def DirListTenant2(alldirectory, url_link_final_2, tenant2key):
    dirlist_api = DirectoryListsApiInstance()
    alldirectorynew = []
    print("Creating list to tenant 2, if any", flush=True)
    if alldirectory:
        for count, dirlist in enumerate(alldirectory):
            # rename = 1
            namecheck = 1
            oldjson = json.loads(dirlist)
            # oldname = oldjson["name"]
            while namecheck != -1:
                newname, newid = dirlist_api.create(oldjson)
                print(
                    "#"
                    + str(count)
                    + " Directory List ID: "
                    + str(newid)
                    + " Name: "
                    + newname,
                    flush=True,
                )
                alldirectorynew.append(str(newid))
                namecheck = -1
                # if "name already exists" in idjson["message"]:
                #         oldjson["name"] = oldname + " {" + str(rename) + "}"
                #         dirlist = json.dumps(oldjson)
                #         rename = rename + 1
                #     else:
                #         print(describe, flush=True)
                #         namecheck = -1
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
