import json
import typing
import os
import sys
from types import SimpleNamespace

import deepsecurity
import requests
import urllib3
from deepsecurity.rest import ApiException
from rich.progress import Progress

from dsmigrator.api_config import PolicyApiInstance
from dsmigrator.migrator_utils import safe_request
from dsmigrator.logging import console, log

cert = False


def delete_cloud_one_policies(CLOUD_ONE_API_KEY: str):
    console.log("Deleting Policies from Cloud One...")

    host = "https://cloudone.trendmicro.com/api/policies"
    message = requests.get(
        host,
        verify=False,
        headers={"api-secret-key": CLOUD_ONE_API_KEY, "api-version": "v1"},
    )
    parsed = message.text
    x = json.loads(parsed, object_hook=lambda d: SimpleNamespace(**d))
    policyNumbers = []
    for key in x.policies:
        policyNumbers.append(key.ID)
    if policyNumbers:
        for policyID in policyNumbers:
            console.log(f"Deleting policy #{policyID}")
            policyHost = f"https://cloudone.trendmicro.com/api/policies/{policyID}"
            requests.delete(
                policyHost,
                verify=False,
                headers={"api-secret-key": CLOUD_ONE_API_KEY, "api-version": "v1"},
            )
    else:
        console.log("No policies detected in Cloud One. Skipping.")


def ListAllPolicy(url_link_final, tenant1key):
    payload = {}
    url = url_link_final + "api/policies"
    response = safe_request(tenant1key, "GET", url, payload=payload, cert=cert)
    describe = str(response.text)
    oldpolicyname = []
    oldpolicyid = []
    namejson = json.loads(describe)
    for policy in namejson["policies"]:
        oldpolicyname.append(str(policy["name"]))
        oldpolicyid.append(str(policy["ID"]))
    return oldpolicyid


def GetPolicy(policyIDs, url_link_final, tenant1key):
    antimalwareconfig = []
    allofpolicy = []
    i = 0
    console.log("Getting Policy from Deep Security")
    for count, part in enumerate(policyIDs):
        payload = {}
        url = url_link_final + "api/policies/" + str(part)
        response = safe_request(tenant1key, "GET", url, payload=payload, cert=cert)
        policy_string = str(response.text)
        i = i + 1
        allofpolicy.append(policy_string)
        console.log("#" + str(count) + " Policy ID: " + str(part))
        rtscan = policy_string.find("realTimeScanConfigurationID")
        if rtscan != -1:
            rtpart = policy_string[rtscan + 28 :]
            startIndex = rtpart.find(":")
            if startIndex != -1:  # i.e. if the first quote was found
                endIndex = rtpart.find(",", startIndex + 1)
                if startIndex != -1 and endIndex != -1:  # i.e. both quotes were found
                    rtid = rtpart[startIndex + 1 : endIndex]
                    antimalwareconfig.append(str(rtid))

        mscan = policy_string.find("manualScanConfigurationID")
        if mscan != -1:
            mpart = policy_string[mscan + 26 :]
            startIndex = mpart.find(":")
            if startIndex != -1:  # i.e. if the first quote was found
                endIndex = mpart.find(",", startIndex + 1)
                if startIndex != -1 and endIndex != -1:  # i.e. both quotes were found
                    mid = mpart[startIndex + 1 : endIndex]
                    antimalwareconfig.append(str(mid))

        sscan = policy_string.find("scheduledScanConfigurationID")
        if sscan != -1:
            spart = policy_string[sscan + 29 :]
            startIndex = spart.find(":")
            if startIndex != -1:  # i.e. if the first quote was found
                endIndex = spart.find("}", startIndex + 1)
                if startIndex != -1 and endIndex != -1:  # i.e. both quotes were found
                    ssid = spart[startIndex + 1 : endIndex]
                    antimalwareconfig.append(str(ssid))
    antimalwareconfig = list(dict.fromkeys(antimalwareconfig))
    return antimalwareconfig, allofpolicy


def policy_validate_create(
    all_old: typing.List[str], api_instance: PolicyApiInstance, type: str
) -> typing.Dict[int, int]:
    """
    Takes in a list of json strings that represent policies, sets some key
    settings, assigns the proper parent ID to each, creates each policy,
    renames if necessary, and outputs a dictionary of form
    {oldid: newid, ...} for future use.

    Args:
        all_old (typing.List[str]): A list containing strings of json data
                                    representing policies
        api_instance (PolicyApiInstance): From api_config, a wrapper SDK class
        type (str): The type of output for printing purposes

    Returns:
        typing.Dict[int, int]: dict of form {oldid:newid, ...}
    """
    all_new = []
    id_dict = {}
    for count, dirlist in enumerate(all_old):
        namecheck = 1
        rename = 1
        oldjson = json.loads(dirlist)
        oldname = oldjson["name"]
        oldid = oldjson["ID"]
        # cleanup input
        if "policySettings" in oldjson.keys():
            oldjson["policySettings"]["platformSettingAgentCommunicationsDirection"] = {
                "value": "Agent/Appliance Initiated"
            }
        # Modify parent ID. If errors, to prevent wasted time, create policy at base level.
        try:
            if "parentID" in oldjson.keys():
                oldjson["parentID"] = id_dict[oldjson["parentID"]]
        except Exception as e:
            log.exception(e)
            log.error(
                "ParentID error. Creating policy at base level, please set inheritance manually."
            )
            del oldjson["parentID"]
            pass
        while namecheck != -1:
            try:
                newname = api_instance.create(oldjson)
                newid = api_instance.search(newname).id
                id_dict[oldid] = newid
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
                all_new.append(str(newid))
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
                    log.exception(e)
                    log.error(
                        f"{oldname} could not be transferred. Please transfer manually."
                    )
                    namecheck = -1
    id_dict[0] = 0
    return id_dict


cert = False


def AddPolicy(allofpolicy: typing.List[str], NEW_API_KEY: str) -> typing.Dict[int, int]:
    console.log("Creating Policy to Tenant 2 with new ID")
    if allofpolicy:
        return policy_validate_create(
            allofpolicy, PolicyApiInstance(NEW_API_KEY), "policy"
        )
