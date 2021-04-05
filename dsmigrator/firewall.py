import sys
import os
import time
from time import sleep
import requests
import urllib3
import json

cert = False


def firewall_config_transform(
    allofpolicy,
    t1iplistid,
    t2iplistid,
    t1maclistid,
    t2maclistid,
    t1portlistid,
    t2portlistid,
    t1statefulid,
    t2statefulid,
    t1scheduleid,
    t2scheduleid,
    t1contextid,
    t2contextid,
    OLD_HOST,
    OLD_API_KEY,
    NEW_HOST,
    NEW_API_KEY,
):
    firewallruleid, policystateful = FirewallGet(allofpolicy)
    (
        allfirewallrule,
        allfirewallruleidnew1,
        allfirewallruleidold,
        allfirewallcustomrule,
    ) = FirewallDescribe(
        firewallruleid,
        t1iplistid,
        t2iplistid,
        t1maclistid,
        t2maclistid,
        t1portlistid,
        t2portlistid,
        t1scheduleid,
        t2scheduleid,
        t1contextid,
        t2contextid,
        OLD_HOST,
        OLD_API_KEY,
        NEW_HOST,
        NEW_API_KEY,
    )
    allfirewallruleidnew2 = FirewallCustom(
        allfirewallrule, allfirewallcustomrule, NEW_HOST, NEW_API_KEY
    )

    new_allofpolicy = FirewallReplace(
        allofpolicy,
        allfirewallruleidnew1,
        allfirewallruleidnew2,
        firewallruleid,
        allfirewallruleidold,
        allfirewallcustomrule,
        t1statefulid,
        t2statefulid,
    )
    return new_allofpolicy


def FirewallGet(allofpolicy):
    firewallruleid = []
    policystateful = []
    # find all Firewall rules
    print("Firewall rules in Tenant 1", flush=True)
    for describe in allofpolicy:
        namejson = json.loads(describe)
        if "globalStatefulConfigurationID" in namejson["firewall"]:
            policystateful.append(
                str(namejson["firewall"]["globalStatefulConfigurationID"])
            )
        if "ruleIDs" in namejson["firewall"]:
            for count, here2 in enumerate(namejson["firewall"]["ruleIDs"]):
                firewallruleid.append(str(here2))
    firewallruleid = list(dict.fromkeys(firewallruleid))
    print(firewallruleid, flush=True)
    return firewallruleid, policystateful


def FirewallDescribe(
    firewallruleid,
    t1iplistid,
    t2iplistid,
    t1maclistid,
    t2maclistid,
    t1portlistid,
    t2portlistid,
    t1scheduleid,
    t2scheduleid,
    t1contextid,
    t2contextid,
    url_link_final,
    tenant1key,
    url_link_final_2,
    tenant2key,
):
    allfirewallrule = []
    allfirewallrulename = []
    allfirewallruleidnew1 = []
    allfirewallruleidold = []
    allfirewallcustomrule = []
    # describe Firewall rules
    print("Searching and Modifying Firewall rules in Tenant 1...", flush=True)
    if firewallruleid:
        for count, dirlist in enumerate(firewallruleid):
            payload = {}
            url = url_link_final + "api/firewallrules/" + str(dirlist)
            headers = {
                "api-secret-key": tenant1key,
                "api-version": "v1",
                "Content-Type": "application/json",
            }
            response = requests.request(
                "GET", url, headers=headers, data=payload, verify=cert
            )
            describe = str(response.text)
            allfirewallrule.append(describe)
            firewalljson = json.loads(describe)
            allfirewallrulename.append(str(firewalljson["name"]))
            print(
                "#" + str(count) + " Firewall rule name: " + str(firewalljson["name"]),
                flush=True,
            )
            print("#" + str(count) + " Firewall rule ID: " + dirlist, flush=True)
    print("Done!", flush=True)
    print("Replacing firewall rule IDs configuration in tenant 2...", flush=True)
    for count, describe in enumerate(allfirewallrule):
        firewalljson = json.loads(describe)
        if "scheduleID" in firewalljson:
            indexnum = t1scheduleid.index(str(firewalljson["scheduleID"]))
            firewalljson["scheduleID"] = t2scheduleid[indexnum]
        if "contextID" in firewalljson:
            indexnum = t1contextid.index(str(firewalljson["contextID"]))
            firewalljson["contextID"] = t2contextid[indexnum]
        if "sourceIPListID" in firewalljson:
            indexnum = t1iplistid.index(str(firewalljson["sourceIPListID"]))
            firewalljson["sourceIPListID"] = t2iplistid[indexnum]
        if "sourceMACListID" in firewalljson:
            indexnum = t1maclistid.index(str(firewalljson["sourceMACListID"]))
            firewalljson["sourceMACListID"] = t2maclistid[indexnum]
        if "sourcePortListID" in firewalljson:
            indexnum = t1portlistid.index(str(firewalljson["sourcePortListID"]))
            firewalljson["sourcePortListID"] = t2portlistid[indexnum]
        if "destinationIPListID" in firewalljson:
            indexnum = t1iplistid.index(str(firewalljson["destinationIPListID"]))
            firewalljson["destinationIPListID"] = t2iplistid[indexnum]
        if "destinationMACListID" in firewalljson:
            indexnum = t1maclistid.index(str(firewalljson["destinationMACListID"]))
            firewalljson["destinationMACListID"] = t2maclistid[indexnum]
        if "destinationPortListID" in firewalljson:
            indexnum = t1portlistid.index(str(firewalljson["destinationPortListID"]))
            firewalljson["destinationPortListID"] = t2portlistid[indexnum]
        describe = json.dumps(firewalljson)
        allfirewallrule[count] = describe
    for count, dirlist in enumerate(allfirewallrulename):
        payload = (
            '{"searchCriteria": [{"fieldName": "name","stringValue": "'
            + dirlist
            + '"}]}'
        )
        url = url_link_final_2 + "api/firewallrules/search"
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
                            allfirewallruleidnew1.append(str(indexid))
                            allfirewallruleidold.append(count)

                            payload = allfirewallrule[count]
                            url = url_link_final_2 + "api/firewallrules/" + str(indexid)
                            headers = {
                                "api-secret-key": tenant2key,
                                "api-version": "v1",
                                "Content-Type": "application/json",
                            }
                            response = requests.request(
                                "POST", url, headers=headers, data=payload, verify=cert
                            )
                            print(
                                "#" + str(count) + " Firewall rule ID: " + indexid,
                                flush=True,
                            )
                        else:
                            endIndex = indexpart.find("}", startIndex + 1)
                            if (
                                startIndex != -1 and endIndex != -1
                            ):  # i.e. both quotes were found
                                indexid = indexpart[startIndex + 1 : endIndex]
                                allfirewallruleidnew1.append(str(indexid))
                                allfirewallruleidold.append(count)

                                payload = allfirewallrule[count]
                                url = (
                                    url_link_final_2
                                    + "api/firewallrules/"
                                    + str(indexid)
                                )
                                headers = {
                                    "api-secret-key": tenant2key,
                                    "api-version": "v1",
                                    "Content-Type": "application/json",
                                }
                                response = requests.request(
                                    "POST",
                                    url,
                                    headers=headers,
                                    data=payload,
                                    verify=cert,
                                )
                                print(
                                    "#" + str(count) + " Firewall rule ID: " + indexid,
                                    flush=True,
                                )
                else:
                    print(describe, flush=True)
                    print(payload, flush=True)
            else:
                allfirewallcustomrule.append(count)
        else:
            print(describe, flush=True)
            print(payload, flush=True)
    print("Done!", flush=True)
    return (
        allfirewallrule,
        allfirewallruleidnew1,
        allfirewallruleidold,
        allfirewallcustomrule,
    )


def FirewallCustom(
    allfirewallrule, allfirewallcustomrule, url_link_final_2, tenant2key
):
    allfirewallruleidnew2 = []
    if allfirewallcustomrule:
        print("Creating Firewall Custom Rule...", flush=True)
        for count, indexnum in enumerate(allfirewallcustomrule):
            payload = allfirewallrule[indexnum]
            url = url_link_final_2 + "api/firewallrules"
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
                        allfirewallruleidnew2.append(str(indexid))
                        print(
                            "#" + str(count) + " Firewall rule ID: " + indexid,
                            flush=True,
                        )
                    else:
                        endIndex = indexpart.find("}", startIndex + 1)
                        if (
                            startIndex != -1 and endIndex != -1
                        ):  # i.e. both quotes were found
                            indexid = indexpart[startIndex + 1 : endIndex]
                            allfirewallruleidnew2.append(str(indexid))
                            print(
                                "#" + str(count) + " Firewall rule ID: " + indexid,
                                flush=True,
                            )
            else:
                print(describe, flush=True)
                print(payload, flush=True)
        print("Done!", flush=True)
    # print("all new firewall rule custom rule")
    # print(allfirewallruleidnew2)
    return allfirewallruleidnew2


def FirewallReplace(
    allofpolicy,
    allfirewallruleidnew1,
    allfirewallruleidnew2,
    firewallruleid,
    allfirewallruleidold,
    allfirewallcustomrule,
    t1statefulid,
    t2statefulid,
):
    if allofpolicy:
        for count, describe in enumerate(allofpolicy):
            taskjson = json.loads(describe)
            indexid = taskjson["firewall"]
            if "globalStatefulConfigurationID" in taskjson["firewall"]:
                indexnum = t1statefulid.index(
                    str(taskjson["firewall"]["globalStatefulConfigurationID"])
                )
                taskjson["firewall"]["globalStatefulConfigurationID"] = t2statefulid[
                    indexnum
                ]
            if "ruleIDs" in taskjson["firewall"]:
                if allfirewallruleidnew1 or allfirewallruleidnew2:
                    for count1, this in enumerate(taskjson["firewall"]["ruleIDs"]):
                        checkindex = firewallruleid.index(str(this))
                        if checkindex in allfirewallruleidold:
                            checkindex1 = allfirewallruleidold.index(checkindex)
                            taskjson["firewall"]["ruleIDs"][
                                count1
                            ] = allfirewallruleidnew1[checkindex1]
                        elif checkindex in allfirewallcustomrule:
                            checkindex1 = allfirewallcustomrule.index(checkindex)
                            taskjson["firewall"]["ruleIDs"][
                                count1
                            ] = allfirewallruleidnew2[checkindex1]
            allofpolicy[count] = json.dumps(taskjson)
    return allofpolicy
