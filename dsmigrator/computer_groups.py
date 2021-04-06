import sys
import os
import requests
import urllib3
import json
from dsmigrator.api_config import ComputerGroupsApiInstance
from dsmigrator.migrator_utils import validate_create_dict, value_exists, rename_json
from deepsecurity.rest import ApiException

cert = False


def computer_group_listmaker(OLD_HOST, OLD_API_KEY, NEW_HOST, NEW_API_KEY):
    computer_group_dict = {}
    enum_oldetname, groupIDs = ListGroup(OLD_HOST, OLD_API_KEY)
    if groupIDs:
        allgroup, namegroup = GetGroup(groupIDs, OLD_HOST, OLD_API_KEY)
        computer_group_dict = CreateGroup(allgroup, namegroup, NEW_HOST, NEW_API_KEY)
    computer_group_dict[0] = 0
    return computer_group_dict


def ListGroup(url_link_final, tenant1key):
    payload = {}
    url = url_link_final + "api/computergroups"
    headers = {
        "api-secret-key": tenant1key,
        "api-version": "v1",
        "Content-Type": "application/json",
    }
    response = requests.request("GET", url, headers=headers, data=payload, verify=cert)
    describe = str(response.text)
    oldetname = []
    oldetid = []
    ebt_json = json.loads(describe).get("computerGroups")
    if ebt_json is not None:
        for here in ebt_json:
            oldetname.append(str(here["name"]))
            oldetid.append(str(here["ID"]))
    return enumerate(oldetname), oldetid


def GetGroup(etIDs, url_link_final, tenant1key):
    allet = []
    nameet = []
    print("Getting Target Task...", flush=True)
    if etIDs:
        for part in etIDs:
            payload = {}
            url = url_link_final + "api/computergroups/" + str(part)
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
        return allet, nameet


def CreateGroup(allet, nameet, url_link_final_2, tenant2key):
    print("Creating group to target Account...", flush=True)
    if nameet:
        modet = []
        for task in allet:
            task_json = rename_json(json.loads(task))
            modet.append(json.dumps(task_json))
        return validate_create_dict(
            modet, ComputerGroupsApiInstance(tenant2key), "Computer Group"
        )
