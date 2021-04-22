import sys
import os
import deepsecurity
from deepsecurity.rest import ApiException
import requests
import urllib3
import json
from types import SimpleNamespace
from dsmigrator.api_config import PolicyApiInstance
from rich.progress import Progress

cert = False


def delete_cloud_one_policies(CLOUD_ONE_API_KEY: str):
    print("Deleting Policies from Cloud One...")

    host = "https://cloudone.trendmicro.com/api/policies"
    message = requests.get(
        host,
        verify=False,
        headers={"api-secret-key": CLOUD_ONE_API_KEY, "api-version": "v1"},
    )
    parsed = message.text
    x = json.loads(parsed, object_hook=lambda d: SimpleNamespace(**d))
    policyNumbers = []
    for key in x.policies:  # ERRORS here
        policyNumbers.append(key.ID)
    if policyNumbers:
        for policyID in policyNumbers:
            print(f"Deleting policy #{policyID}")
            policyHost = f"https://cloudone.trendmicro.com/api/policies/{policyID}"
            requests.delete(
                policyHost,
                verify=False,
                headers={"api-secret-key": CLOUD_ONE_API_KEY, "api-version": "v1"},
            )
    else:
        print("No policies detected in Cloud One. Skipping.")


def ListAllPolicy(url_link_final, tenant1key):
    payload = {}
    url = url_link_final + "api/policies"
    headers = {
        "api-secret-key": tenant1key,
        "api-version": "v1",
        "Content-Type": "application/json",
    }
    response = requests.request("GET", url, headers=headers, data=payload, verify=cert)
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
    print("Getting Policy from Deep Security", flush=True)
    for count, part in enumerate(policyIDs):

        payload = {}
        url = url_link_final + "api/policies/" + str(part)
        headers = {
            "api-secret-key": tenant1key,
            "api-version": "v1",
            "Content-Type": "application/json",
        }
        response = requests.request(
            "GET", url, headers=headers, data=payload, verify=cert
        )

        describe = str(response.text)
        i = i + 1
        allofpolicy.append(describe)
        print("#" + str(count) + " Policy ID: " + str(part), flush=True)
        rtscan = describe.find("realTimeScanConfigurationID")
        if rtscan != -1:
            rtpart = describe[rtscan + 28 :]
            startIndex = rtpart.find(":")
            if startIndex != -1:  # i.e. if the first quote was found
                endIndex = rtpart.find(",", startIndex + 1)
                if startIndex != -1 and endIndex != -1:  # i.e. both quotes were found
                    rtid = rtpart[startIndex + 1 : endIndex]
                    antimalwareconfig.append(str(rtid))

        mscan = describe.find("manualScanConfigurationID")
        if mscan != -1:
            mpart = describe[mscan + 26 :]
            startIndex = mpart.find(":")
            if startIndex != -1:  # i.e. if the first quote was found
                endIndex = mpart.find(",", startIndex + 1)
                if startIndex != -1 and endIndex != -1:  # i.e. both quotes were found
                    mid = mpart[startIndex + 1 : endIndex]
                    antimalwareconfig.append(str(mid))

        sscan = describe.find("scheduledScanConfigurationID")
        if sscan != -1:
            spart = describe[sscan + 29 :]
            startIndex = spart.find(":")
            if startIndex != -1:  # i.e. if the first quote was found
                endIndex = spart.find("}", startIndex + 1)
                if startIndex != -1 and endIndex != -1:  # i.e. both quotes were found
                    ssid = spart[startIndex + 1 : endIndex]
                    antimalwareconfig.append(str(ssid))
    antimalwareconfig = list(dict.fromkeys(antimalwareconfig))
    return antimalwareconfig, allofpolicy


def validate_create(all_old, api_instance, type):
    all_new = []
    id_dict = {}
    for count, dirlist in enumerate(all_old):
        namecheck = 1
        rename = 1
        oldjson = json.loads(dirlist)
        oldname = oldjson["name"]
        oldid = oldjson["ID"]
        policysettings = oldjson.get("policySettings")
        if policysettings is not None:
            policysettings["platformSettingAgentCommunicationsDirection"] = {
                "value": "Agent/Appliance Initiated"
            }
        while namecheck != -1:
            if "parentID" in oldjson.keys():
                newparentid = id_dict[oldjson["parentID"]]
            try:
                newname = api_instance.create(oldjson)
                newid = api_instance.search(newname).id
                id_dict[oldid] = newid
                if "parentID" in oldjson.keys():
                    api_instance.modify_parent(newid, newparentid)
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
                    print(e.body)
                    print(
                        f"[bold bright_red]WARNING[/bold bright_red]: {oldname} could not be transferred. Please transfer manually."
                    )
                    print(
                        "[i]NOTE: This is under construction and will work soon. :)[/i]"
                    )
                    namecheck = -1
    id_dict[0] = 0
    return id_dict


cert = False


def AddPolicy(allofpolicy, NEW_API_KEY):
    print("Creating Policy to Tenant 2 with new ID", flush=True)
    if allofpolicy:
        return validate_create(allofpolicy, PolicyApiInstance(NEW_API_KEY), "policy")
