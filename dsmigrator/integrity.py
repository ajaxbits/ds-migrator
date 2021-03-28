import sys
import os
import time
from time import sleep
import requests
import urllib3
import json

cert = False


def im_config_transform(allofpolicy, OLD_HOST, OLD_API_KEY, NEW_HOST, NEW_API_KEY):
    imruleid = IMGet(allofpolicy)

    allimrule, allimruleidnew1, allimruleidold, allimcustomrule = IMDescribe(
        imruleid, OLD_HOST, OLD_API_KEY, NEW_HOST, NEW_API_KEY
    )

    allimruleidnew2 = IMCustom(allimrule, allimcustomrule, NEW_HOST, NEW_API_KEY)
    aop_replace_im_rules = IMReplace(
        allofpolicy,
        allimruleidnew1,
        allimruleidnew2,
        imruleid,
        allimruleidold,
        allimcustomrule,
    )
    final = aop_replace_im_rules
    return final


def IMGet(allofpolicy):
    imruleid = []
    print("IM rules in Tenant 1", flush=True)
    for describe in allofpolicy:
        namejson = json.loads(describe)
        if "ruleIDs" in namejson["integrityMonitoring"]:
            for count, here2 in enumerate(namejson["integrityMonitoring"]["ruleIDs"]):
                imruleid.append(str(here2))
    imruleid = list(dict.fromkeys(imruleid))
    print(imruleid, flush=True)
    return imruleid


def IMDescribe(imruleid, url_link_final, tenant1key, url_link_final_2, tenant2key):
    allimrule = []
    allimrulename = []
    allimruleidnew1 = []
    allimruleidold = []
    allimcustomrule = []
    print("Searching IM rules in Tenant 1...", flush=True)
    if imruleid:
        for count, dirlist in enumerate(imruleid):
            payload = {}
            url = url_link_final + "api/integritymonitoringrules/" + str(dirlist)
            headers = {
                "api-secret-key": tenant1key,
                "api-version": "v1",
                "Content-Type": "application/json",
            }
            response = requests.request(
                "GET", url, headers=headers, data=payload, verify=cert
            )
            describe = str(response.text)
            allimrule.append(describe)
            imjson = json.loads(describe)
            allimrulename.append(str(imjson["name"]))
            print(
                "#" + str(count) + " IPS rule name: " + str(imjson["name"]), flush=True
            )
            print("#" + str(count) + " IM rule ID: " + str(dirlist), flush=True)
    print("Done!", flush=True)
    print("Searching and Modifying IM rule in Tenant 2...", flush=True)
    for count, dirlist in enumerate(allimrulename):
        payload = (
            '{"searchCriteria": [{"fieldName": "name","stringValue": "'
            + dirlist
            + '"}]}'
        )
        url = url_link_final_2 + "api/integritymonitoringrules/search"
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
                            allimruleidnew1.append(str(indexid))
                            allimruleidold.append(count)
                            print(
                                "#" + str(count) + " IM rule ID: " + str(indexid),
                                flush=True,
                            )
                        else:
                            endIndex = indexpart.find("}", startIndex + 1)
                            if (
                                startIndex != -1 and endIndex != -1
                            ):  # i.e. both quotes were found
                                indexid = indexpart[startIndex + 1 : endIndex]
                                allimruleidnew1.append(str(indexid))
                                allimruleidold.append(count)
                                print(
                                    "#" + str(count) + " IM rule ID: " + str(indexid),
                                    flush=True,
                                )
                else:
                    print(describe, flush=True)
                    print(payload, flush=True)
            else:
                allimcustomrule.append(count)
        else:
            print(describe, flush=True)
            print(payload, flush=True)
    print("Done!", flush=True)
    return allimrule, allimruleidnew1, allimruleidold, allimcustomrule


def IMCustom(allimrule, allimcustomrule, url_link_final_2, tenant2key):
    allimruleidnew2 = []
    if allimcustomrule:
        print("Creating new custom IM rule in Tenant 2...", flush=True)
        for count, indexnum in enumerate(allimcustomrule):
            payload = allimrule[indexnum]
            url = url_link_final_2 + "api/integritymonitoringrules"
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
                    endIndex = indexpart.find("}", startIndex + 1)
                    if (
                        startIndex != -1 and endIndex != -1
                    ):  # i.e. both quotes were found
                        indexid = indexpart[startIndex + 1 : endIndex]
                        allimruleidnew2.append(str(indexid))
                        print(
                            "#" + str(count) + " IM rule ID: " + str(indexid),
                            flush=True,
                        )
            else:
                print(describe, flush=True)
                print(payload, flush=True)
        print("Done!", flush=True)

    return allimruleidnew2


def IMReplace(
    allofpolicy,
    allimruleidnew1,
    allimruleidnew2,
    imruleid,
    allimruleidold,
    allimcustomrule,
):
    for count, describe in enumerate(allofpolicy):
        index = describe.find('"integrityMonitoring"')
        if index != -1:
            indexpart = describe[index + 20 :]
            startIndex = indexpart.find("}")
            if startIndex != -1:  # i.e. if the first quote was found
                endIndex = indexpart.find("}", startIndex + 1)
                if startIndex != -1 and endIndex != -1:  # i.e. both quotes were found
                    indexid = indexpart[startIndex + 1 : endIndex]
                    index2 = indexid.find("ruleIDs")
                    if index2 != -1:
                        indexpart2 = indexid[index2 + 7 :]
                        startIndex2 = indexpart2.find("[")
                        if startIndex2 != -1:  # i.e. if the first quote was found
                            endIndex2 = indexpart2.find("]", startIndex2 + 1)
                            if (
                                startIndex2 != -1 and endIndex2 != -1
                            ):  # i.e. both quotes were found
                                indexid2 = indexpart2[startIndex2 + 1 : endIndex2]
                                indexid3 = indexpart2[startIndex2 + 1 : endIndex2]
                                indexid4 = indexid2.split(", ")
                                if allimruleidnew1 or allimruleidnew2:
                                    for count1, this in enumerate(indexid4):
                                        checkindex = imruleid.index(this)
                                        if checkindex in allimruleidold:
                                            checkindex1 = allimruleidold.index(
                                                checkindex
                                            )
                                            indexid4[count1] = allimruleidnew1[
                                                checkindex1
                                            ]
                                        elif checkindex in allimcustomrule:
                                            checkindex1 = allimcustomrule.index(
                                                checkindex
                                            )
                                            indexid4[count1] = allimruleidnew2[
                                                checkindex1
                                            ]
                                    indexid2 = ",".join(indexid4)
                                modulepart = describe[index : index + 20 + endIndex]
                                modulepart2 = modulepart.replace(indexid3, indexid2)
                                allofpolicy[count] = describe.replace(
                                    modulepart, modulepart2
                                )
    return allofpolicy
