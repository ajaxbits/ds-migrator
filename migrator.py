from __future__ import print_function
import re
import requests
import urllib3
from time import sleep
import sys, warnings, os, time
import deepsecurity
from deepsecurity.rest import ApiException
import json
import csv
from datetime import date
from zeep.client import Client
from requests import Session
from zeep.transports import Transport
from datetime import datetime
from zeep import helpers
import os
import ip_rules
from api_config import RestApiConfiguration

# configuration
username = "admin"
password = "MwbdKr3NBwGKkeG5p8K7NdfToG"
hostname = "https://ajax-ds20-t-dsmelb-idi20586foba-797956631.us-east-2.elb.amazonaws.com/webservice/Manager?WSDL"
tenant = ""

# Setup
if not sys.warnoptions:
    warnings.simplefilter("ignore")


def to_snake(camel_case):
    pattern = re.compile(r"(?<!^)(?=[A-Z])")
    snake = pattern.sub("_", camel_case).lower()
    return snake


class PoliciesApiInstance(RestApiConfiguration):
    def __init__(self, overrides=False):
        super().__init__(overrides)
        self.api_instance = deepsecurity.PoliciesApi(self.api_client)

    def list(self):
        return self.api_instance.list_policies(
            self.api_version, overrides=self.overrides
        )

    def create(self, policy_object):
        policy = deepsecurity.Policy()
        for key in policy_object:
            setattr(policy, to_snake(key), policy_object[key])
        # TODO change
        # policy.name = "testing"
        return self.api_instance.create_policy(policy, self.api_version)


def gen_unique_dict(old_policies_list, new_policies_list):
    # generate a dict with unique policies in the old dsm
    unique = []
    duplicates = []
    if new_policies_list == []:
        unique = old_policies_list
    else:
        for old_policy in old_policies_list:
            for new_policy in new_policies_list:
                if (
                    old_policy.name == new_policy.name
                    and old_policy.description == new_policy.description
                ):
                    duplicates.append(old_policy)
                else:
                    unique.append(old_policy)
    return {"unique": unique, "duplicates": duplicates}


if __name__ == "__main__":
    # create SOAP session
    session = Session()
    session.verify = False
    url = hostname
    transport = Transport(session=session, timeout=1800)
    client = Client(url, transport=transport)
    factory = client.type_factory("ns0")
    sID = client.service.authenticate(username=username, password=password)

    # get policies and dedupe
    old_policies_list = client.service.securityProfileRetrieveAll(sID)
    new_policies_list = PoliciesApiInstance("new").list().policies
    policies_dict = gen_unique_dict(old_policies_list, new_policies_list)
    # print(policies_dict)

    ###############################PH#####################################

    cert = False

    policyIDs = []
    for i in policies_dict["unique"]:
        policyIDs.append(i.ID)

    def RestHttpGetPolicy(policyIDs, url_link_final, tenant1key):
        antimalwareconfig = []
        allofpolicy = []
        i = 0
        print("Getting Policy from Tenant 1", flush=True)
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
                    if (
                        startIndex != -1 and endIndex != -1
                    ):  # i.e. both quotes were found
                        rtid = rtpart[startIndex + 1 : endIndex]
                        antimalwareconfig.append(str(rtid))

            mscan = describe.find("manualScanConfigurationID")
            if mscan != -1:
                mpart = describe[mscan + 26 :]
                startIndex = mpart.find(":")
                if startIndex != -1:  # i.e. if the first quote was found
                    endIndex = mpart.find(",", startIndex + 1)
                    if (
                        startIndex != -1 and endIndex != -1
                    ):  # i.e. both quotes were found
                        mid = mpart[startIndex + 1 : endIndex]
                        antimalwareconfig.append(str(mid))

            sscan = describe.find("scheduledScanConfigurationID")
            if sscan != -1:
                spart = describe[sscan + 29 :]
                startIndex = spart.find(":")
                if startIndex != -1:  # i.e. if the first quote was found
                    endIndex = spart.find("}", startIndex + 1)
                    if (
                        startIndex != -1 and endIndex != -1
                    ):  # i.e. both quotes were found
                        ssid = spart[startIndex + 1 : endIndex]
                        antimalwareconfig.append(str(ssid))
        antimalwareconfig = list(dict.fromkeys(antimalwareconfig))
        return antimalwareconfig, allofpolicy

    full_script = RestHttpGetPolicy(
        policyIDs,
        "https://ajax-ds20-t-dsmelb-idi20586foba-797956631.us-east-2.elb.amazonaws.com/",
        "3177CE32-B1C7-EF55-112E-5FD7E8425F8B:nqdzbK24j6zuj89djtY+UTpDw1TtesuJVcbYWEY5d7w=",
    )

    first_policy = full_script[1][0]

    first_policy_dict = json.loads(first_policy)

    def RenamePolicy(allofpolicy):
        if allofpolicy:
            for count, describe in enumerate(allofpolicy):
                policyjson = json.loads(describe)
                policyjson["name"] = policyjson["name"] + " - Migrated"
                policyjson["parentID"] = "1"
                allofpolicy[count] = json.dumps(policyjson)

    policy_json_list = []

    RenamePolicy(full_script[1])

    print(full_script[1][0])

    for i in full_script[1]:
        policy_json_list.append(json.loads(i))

    rest = PoliciesApiInstance()

    def create(policy_object):
        policy = deepsecurity.Policy()
        for key in policy_object:
            new_key = to_snake(key)
            setattr(policy, new_key, policy_object[key])
        rest.api_instance.create_policy(policy, rest.api_version)

    for i in policy_json_list:
        create(i)

    # rest.create(first_policy)

    ###############################PH#####################################
    allofpolicy = full_script[1]

    def IPSGet(allofpolicy):
        ipsruleid = []
        print("IPS rules in Tenant 1", flush=True)
        for describe in allofpolicy:
            namejson = json.loads(describe)
            if "ruleIDs" in namejson["intrusionPrevention"]:
                for count, here2 in enumerate(
                    namejson["intrusionPrevention"]["ruleIDs"]
                ):
                    ipsruleid.append(str(here2))
        ipsruleid = list(dict.fromkeys(ipsruleid))
        print(ipsruleid, flush=True)
        return ipsruleid

    ipsruleid = IPSGet(allofpolicy)

    def IPSDescribe(
        ipsruleid,
        ipsappid,
        allipsappidnew1,
        allipsappidnew2,
        allipsappidold,
        allipscustomapp,
        url_link_final,
        tenant1key,
        url_link_final_2,
        tenant2key,
    ):
        allipsrule = []
        allipsrulename = []
        allipsruleidnew1 = []
        allipsruleidold = []
        allipscustomrule = []
        print("Searching IPS rules in Tenant 1...", flush=True)
        if ipsruleid:
            for count, dirlist in enumerate(ipsruleid):
                payload = {}
                url = url_link_final + "api/intrusionpreventionrules/" + str(dirlist)
                headers = {
                    "api-secret-key": tenant1key,
                    "api-version": "v1",
                    "Content-Type": "application/json",
                }
                response = requests.request(
                    "GET", url, headers=headers, data=payload, verify=cert
                )
                describe = str(response.text)
                allipsrule.append(describe)
                ipsjson = json.loads(describe)
                allipsrulename.append(str(ipsjson["name"]))
                print(
                    "#" + str(count) + " IPS rule name: " + str(ipsjson["name"]),
                    flush=True,
                )
                index3 = describe.find("applicationTypeID")
                if index3 != -1:
                    indexpart = describe[index3 + 17 :]
                    startIndex = indexpart.find(":")
                    if startIndex != -1:  # i.e. if the first quote was found
                        endIndex3 = indexpart.find(",", startIndex + 1)
                        if (
                            startIndex != -1 and endIndex3 != -1
                        ):  # i.e. both quotes were found
                            indexid1 = indexpart[startIndex + 1 : endIndex3]
                            checkindex = ipsappid.index(indexid1)
                            if checkindex in allipsappidold:
                                checkindex1 = allipsappidold.index(checkindex)
                                replaceid = allipsappidnew1[checkindex1]
                            elif checkindex in allipscustomapp:
                                checkindex1 = allipscustomapp.index(checkindex)
                                replaceid = allipsappidnew2[checkindex1]
                            indexid5 = describe[index3 : index3 + 17 + endIndex3]
                            listpart = indexid5.replace(indexid1, replaceid)
                            allipsrule[count] = describe.replace(indexid5, listpart)
                print("#" + str(count) + " IPS rule ID: " + dirlist, flush=True)
        print("Done!", flush=True)
        print("Searching and Modifying IPS rule in Tenant 2...", flush=True)
        for count, dirlist in enumerate(allipsrulename):
            payload = (
                '{"searchCriteria": [{"fieldName": "name","stringValue": "'
                + dirlist
                + '"}]}'
            )
            url = url_link_final_2 + "api/intrusionpreventionrules/search"
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
                index = describe.find(dirlist)
                if index != -1:
                    index = describe.find('"ID"')
                    if index != -1:
                        indexpart = describe[index + 4 :]
                        startIndex = indexpart.find(":")
                        if startIndex != -1:  # i.e. if the first quote was found
                            endIndex = indexpart.find(",", startIndex + 1)
                            if (
                                startIndex != -1 and endIndex != -1
                            ):  # i.e. both quotes were found
                                indexid = indexpart[startIndex + 1 : endIndex]
                                allipsruleidnew1.append(str(indexid))
                                allipsruleidold.append(count)
                                print(
                                    "#" + str(count) + " IPS rule ID: " + str(indexid),
                                    flush=True,
                                )
                            else:
                                endIndex = indexpart.find("}", startIndex + 1)
                                if (
                                    startIndex != -1 and endIndex != -1
                                ):  # i.e. both quotes were found
                                    indexid = indexpart[startIndex + 1 : endIndex]
                                    allipsruleidnew1.append(str(indexid))
                                    allipsruleidold.append(count)
                                    print(
                                        "#"
                                        + str(count)
                                        + " IPS rule ID: "
                                        + str(indexid),
                                        flush=True,
                                    )
                    else:
                        print(describe, flush=True)
                        print(payload, flush=True)
                else:
                    allipscustomrule.append(count)
            else:
                print(describe, flush=True)
                print(payload, flush=True)
        print("Done!", flush=True)
        return allipsrule, allipsruleidnew1, allipsruleidold, allipscustomrule

    def IPSCustom(allipsrule, allipscustomrule, url_link_final_2, tenant2key):
        allipsruleidnew2 = []
        if allipscustomrule:
            print("Creating new custom IPS rule in Tenant 2...", flush=True)
            for count, indexnum in enumerate(allipscustomrule):
                payload = allipsrule[indexnum]
                url = url_link_final_2 + "api/intrusionpreventionrules"
                headers = {
                    "api-secret-key": tenant2key,
                    "api-version": "v1",
                    "Content-Type": "application/json",
                }
                response = requests.request(
                    "POST", url, headers=headers, data=payload, verify=cert
                )
                describe = str(response.text)
                index = describe.find('"ID"')
                if index != -1:
                    indexpart = describe[index + 4 :]
                    startIndex = indexpart.find(":")
                    if startIndex != -1:  # i.e. if the first quote was found
                        endIndex = indexpart.find(",", startIndex + 1)
                        if (
                            startIndex != -1 and endIndex != -1
                        ):  # i.e. both quotes were found
                            indexid = indexpart[startIndex + 1 : endIndex]
                            allipsruleidnew2.append(str(indexid))
                            print(
                                "#" + str(count) + " IPS rule ID: " + str(indexid),
                                flush=True,
                            )
                        else:
                            endIndex = indexpart.find("}", startIndex + 1)
                            if (
                                startIndex != -1 and endIndex != -1
                            ):  # i.e. both quotes were found
                                indexid = indexpart[startIndex + 1 : endIndex]
                                allipsruleidnew2.append(str(indexid))
                                print(
                                    "#" + str(count) + " IPS rule ID: " + str(indexid),
                                    flush=True,
                                )
                else:
                    print(describe, flush=True)
                    print(payload, flush=True)
            print("Done!", flush=True)
        # print("all new IPS rule custom rule", flush=True)
        # print(allipsruleidnew2, flush=True)
        return allipsruleidnew2

    def IPSReplace(
        allofpolicy,
        allipsruleidnew1,
        allipsruleidnew2,
        ipsruleid,
        allipsruleidold,
        allipscustomrule,
    ):
        for count, describe in enumerate(allofpolicy):
            index = describe.find('"intrusionPrevention"')
            if index != -1:
                indexpart = describe[index + 20 :]
                startIndex = indexpart.find("}")
                if startIndex != -1:  # i.e. if the first quote was found
                    endIndex = indexpart.find("}", startIndex + 1)
                    if (
                        startIndex != -1 and endIndex != -1
                    ):  # i.e. both quotes were found
                        indexid = indexpart[startIndex + 1 : endIndex]
                        index2 = indexid.find("ruleIDs")
                        if index2 != -1:
                            indexpart2 = indexid[index2 + 9 :]
                            startIndex2 = indexpart2.find("[")
                            if startIndex2 != -1:  # i.e. if the first quote was found
                                endIndex2 = indexpart2.find("]", startIndex2 + 1)
                                if (
                                    startIndex2 != -1 and endIndex2 != -1
                                ):  # i.e. both quotes were found
                                    indexid2 = indexpart2[startIndex2 + 1 : endIndex2]
                                    indexid3 = indexpart2[startIndex2 + 1 : endIndex2]
                                    indexid4 = indexid2.split(", ")
                                    if allipsruleidnew1 or allipsruleidnew2:
                                        for count1, this in enumerate(indexid4):
                                            checkindex = ipsruleid.index(this)
                                            if checkindex in allipsruleidold:
                                                checkindex1 = allipsruleidold.index(
                                                    checkindex
                                                )
                                                indexid4[count1] = allipsruleidnew1[
                                                    checkindex1
                                                ]
                                            elif checkindex in allipscustomrule:
                                                checkindex1 = allipscustomrule.index(
                                                    checkindex
                                                )
                                                indexid4[count1] = allipsruleidnew2[
                                                    checkindex1
                                                ]
                                        indexid2 = ",".join(indexid4)
                                    modulepart = describe[index : index + 20 + endIndex]
                                    modulepart2 = modulepart.replace(indexid3, indexid2)
                                    allofpolicy[count] = describe.replace(
                                        modulepart, modulepart2
                                    )
        return allofpolicy

    # IMPORTANT! close the session, so there's not a session pileup
    client.service.endSession(sID)
