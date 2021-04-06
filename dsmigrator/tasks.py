import sys
import os
import requests
import urllib3
import json
from nested_lookup import nested_lookup, nested_update
from dsmigrator.api_config import ScheduledTasksApiInstance, EventBasedTasksApiInstance
from dsmigrator.migrator_utils import validate_create, value_exists, rename_json

cert = False


def ebt_listmaker(
    policy_dict, computer_group_dict, OLD_HOST, OLD_API_KEY, NEW_HOST, NEW_API_KEY
):
    enum_oldetname, etIDs = ListEventTask(OLD_HOST, OLD_API_KEY)
    if etIDs:
        allet, nameet = GetEventTask(etIDs, OLD_HOST, OLD_API_KEY)
        CreateEventTask(
            allet, nameet, policy_dict, computer_group_dict, NEW_HOST, NEW_API_KEY
        )


def st_listmaker(
    policy_dict, computer_group_dict, OLD_HOST, OLD_API_KEY, NEW_HOST, NEW_API_KEY
):
    enum_oldstname, stIDs = ListScheduledTask(OLD_HOST, OLD_API_KEY)
    if stIDs:
        allst, namest = GetScheduledTask(stIDs, OLD_HOST, OLD_API_KEY)
        CreateScheduledTask(
            allst, namest, policy_dict, computer_group_dict, NEW_HOST, NEW_API_KEY
        )


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
    oldetname = []
    oldetid = []
    ebt_json = json.loads(describe).get("eventBasedTasks")
    if ebt_json is not None:
        for here in ebt_json:
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
        return allet, nameet


def CreateEventTask(
    allet, nameet, policy_dict, computer_group_dict, url_link_final_2, tenant2key
):
    print("Creating Task to target Account...", flush=True)
    if nameet:
        modet = []
        for task in allet:
            task_json = rename_json(json.loads(task))
            oldname = task_json.get("name")
            actions_list = task_json.get("actions")
            if actions_list is not None:
                for action in actions_list:
                    oldid = action.get("parameterValue")
                    if oldid is not None:
                        if (computer_group_dict.get(oldid) is not None) and (action["type"] == "assign-group"):
                            action["parameterValue"] = computer_group_dict[oldid]
                        elif computer_group_dict.get(oldid) is None:
                            print(
                                f"WARNING: THE COMPUTER GROUP ASSIGNED IN {oldname} DOES NOT EXIST. TASK WILL NOT BE MIGRATED"
                            )
                            task_json = {}
                        if (policy_dict.get(oldid) is not None) and (action["type"] == "assign-policy"):
                            action["parameterValue"] = policy_dict[oldid]
                        elif policy_dict.get(oldid) is None:
                            print(
                                f"WARNING: THE POLICY ASSIGNED IN {oldname} DOES NOT EXIST. TASK WILL NOT BE MIGRATED"
                            )
                            task_json = {}
            if task_json:
                modet.append(json.dumps(task_json))

        validate_create(modet, EventBasedTasksApiInstance(tenant2key), "Event Based")


def ListScheduledTask(url_link_final, tenant1key):
    payload = {}
    url = url_link_final + "api/scheduledtasks"
    headers = {
        "api-secret-key": tenant1key,
        "api-version": "v1",
        "Content-Type": "application/json",
    }
    response = requests.request("GET", url, headers=headers, data=payload, verify=cert)
    oldstname = []
    oldstid = []
    st_json = json.loads(str(response.text)).get("scheduledTasks")
    if st_json is not None:
        for here in st_json:
            oldstname.append(str(here["name"]))
            oldstid.append(str(here["ID"]))
    return enumerate(oldstname), oldstid


def GetScheduledTask(stIDs, url_link_final, tenant1key):
    allst = []
    namest = []
    print("Getting Target Task...", flush=True)
    if stIDs:
        for part in stIDs:
            payload = {}
            url = url_link_final + "api/scheduledtasks/" + str(part)
            headers = {
                "api-secret-key": tenant1key,
                "api-version": "v1",
                "Content-Type": "application/json",
            }
            response = requests.request(
                "GET", url, headers=headers, data=payload, verify=cert
            )
            describe = str(response.text)
            allst.append(describe)
            namejson = json.loads(describe)
            namest.append(str(namejson["name"]))
    return allst, namest


def CreateScheduledTask(
    allst, namest, policy_dict, computer_group_dict, url_link_final_2, tenant2key
):
    print("Creating Task to target Account...", flush=True)
    if namest:
        modst = []
        for task in allst:
            task_json = rename_json(json.loads(task))
            oldname = task_json.get("name")
            oldcomputergroup = nested_lookup("computerGroupID", task_json)
            oldpolicy = nested_lookup("policyID", task_json)
            has_smartfolder = bool(nested_lookup("smartFolderID", task_json))
            if oldcomputergroup:
                oldid = oldcomputergroup[0]
                if computer_group_dict.get(oldid) is not None:
                    task_json = nested_update(
                        task_json,
                        "computerGroupID",
                        computer_group_dict[oldid],
                    )
                else:
                    print(
                        f"WARNING: THE COMPUTER GROUP ASSIGNED IN {oldname} DOES NOT EXIST. TASK WILL NOT BE MIGRATED"
                    )
                    task_json = {}
            if oldpolicy:
                oldid = oldpolicy[0]
                if computer_group_dict.get(oldid) is not None:
                    task_json = nested_update(task_json, "policyID", policy_dict[oldid])
                else:
                    print(
                        f"WARNING: THE POLICY ASSIGNED IN {oldname} DOES NOT EXIST. TASK WILL NOT BE MIGRATED"
                    )
                    task_json = {}
            if has_smartfolder:
                print(f"WARNING: THE SMART FOLDER ASSIGNED IN {oldname} CANNOT BE MIGRATED.")
                task_json = {}
            if task_json:
                modst.append(json.dumps(task_json))

        validate_create(modst, ScheduledTasksApiInstance(tenant2key), "Scheduled")
