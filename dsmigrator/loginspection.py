import sys
import os
import time
from time import sleep
import requests
import urllib3
import json

cert = False


def li_config_transform(allofpolicy, OLD_HOST, OLD_API_KEY, NEW_HOST, NEW_API_KEY):
    liruleid = LIGet(allofpolicy)

    alllirule, allliruleidnew1, allliruleidold, alllicustomrule = LIDescribe(
        liruleid, OLD_HOST, OLD_API_KEY, NEW_HOST, NEW_API_KEY
    )

    allliruleidnew2 = LICustom(alllirule, alllicustomrule, NEW_HOST, NEW_API_KEY)

    aop_replace_li_rules = LIReplace(
        allofpolicy,
        allliruleidnew1,
        allliruleidnew2,
        liruleid,
        allliruleidold,
        alllicustomrule,
    )
    final = aop_replace_li_rules
    return final


def LIGet(allofpolicy):
    liruleid = []
    print("Log Inspection rules in Tenant 1", flush=True)
    for describe in allofpolicy:
        namejson = json.loads(describe)
        if "ruleIDs" in namejson["logInspection"]:
            for count, here2 in enumerate(namejson["logInspection"]["ruleIDs"]):
                liruleid.append(str(here2))
    liruleid = list(dict.fromkeys(liruleid))
    print(liruleid, flush=True)
    return liruleid


def LIDescribe(liruleid, url_link_final, tenant1key, url_link_final_2, tenant2key):
    alllirule = []
    alllirulename = []
    allliruleidnew1 = []
    allliruleidold = []
    alllicustomrule = []
    print("Searching LI rules in Tenant 1...", flush=True)
    if liruleid:
        for count, dirlist in enumerate(liruleid):
            payload = {}
            url = url_link_final + "api/loginspectionrules/" + str(dirlist)
            headers = {
                "api-secret-key": tenant1key,
                "api-version": "v1",
                "Content-Type": "application/json",
            }
            response = requests.request(
                "GET", url, headers=headers, data=payload, verify=cert
            )
            describe = str(response.text)
            alllirule.append(describe)
            lijson = json.loads(describe)
            alllirulename.append(str(lijson["name"]))
            print(
                "#" + str(count) + " LI rule name: " + str(lijson["name"]), flush=True
            )
            print("#" + str(count) + " LI rule ID: " + dirlist, flush=True)
    print("Done!", flush=True)
    print("Searching and Modifying LI rule in Tenant 2...", flush=True)
    for count, dirlist in enumerate(alllirulename):
        payload = (
            '{"searchCriteria": [{"fieldName": "name","stringValue": "'
            + dirlist
            + '"}]}'
        )
        url = url_link_final_2 + "api/loginspectionrules/search"
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
                        endIndex = indexpart.find("}", startIndex + 1)
                        if (
                            startIndex != -1 and endIndex != -1
                        ):  # i.e. both quotes were found
                            indexid = indexpart[startIndex + 1 : endIndex]
                            allliruleidnew1.append(str(indexid))
                            allliruleidold.append(count)
                            print(
                                "#" + str(count) + " LI rule ID: " + indexid, flush=True
                            )
                else:
                    print(describe, flush=True)
                    print(payload, flush=True)
            else:
                alllicustomrule.append(count)
        else:
            print(describe, flush=True)
            print(payload, flush=True)
    return alllirule, allliruleidnew1, allliruleidold, alllicustomrule


def LICustom(alllirule, alllicustomrule, url_link_final_2, tenant2key):
    allliruleidnew2 = []
    if alllicustomrule:
        print("Creating new custom LI rule in Tenant 2...", flush=True)
        for count, indexnum in enumerate(alllicustomrule):
            payload = alllirule[indexnum]
            url = url_link_final_2 + "api/loginspectionrules"
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
                        allliruleidnew2.append(str(indexid))
                        print("#" + str(count) + " LI rule ID: " + indexid, flush=True)
            else:
                print(describe, flush=True)
                print(payload, flush=True)
        # print("all new LI rule custom rule", flush=True)
        # print(allliruleidnew2, flush=True)
        print("Done!", flush=True)
    return allliruleidnew2


def LIReplace(
    allofpolicy,
    allliruleidnew1,
    allliruleidnew2,
    liruleid,
    allliruleidold,
    alllicustomrule,
):
    for count, describe in enumerate(allofpolicy):
        index = describe.find('"logInspection"')
        if index != -1:
            indexpart = describe[index + 14 :]
            startIndex = indexpart.find("}")
            if startIndex != -1:  # i.e. if the first quote was found
                endIndex = indexpart.find("}", startIndex + 1)
                if startIndex != -1 and endIndex != -1:  # i.e. both quotes were found
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
                                if allliruleidnew1 or allliruleidnew2:
                                    for count1, this in enumerate(indexid4):
                                        checkindex = liruleid.index(this)
                                        if checkindex in allliruleidold:
                                            checkindex1 = allliruleidold.index(
                                                checkindex
                                            )
                                            indexid4[count1] = allliruleidnew1[
                                                checkindex1
                                            ]
                                        elif checkindex in alllicustomrule:
                                            checkindex1 = alllicustomrule.index(
                                                checkindex
                                            )
                                            indexid4[count1] = allliruleidnew2[
                                                checkindex1
                                            ]
                                    indexid2 = ",".join(indexid4)
                                modulepart = describe[index : index + 14 + endIndex]
                                modulepart2 = modulepart.replace(indexid3, indexid2)
                                allofpolicy[count] = describe.replace(
                                    modulepart, modulepart2
                                )
    return allofpolicy
