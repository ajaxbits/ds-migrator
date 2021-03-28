import sys
import os
import time
from time import sleep
import requests
import urllib3
import json
from dsmigrator.api_config import (
    DirectoryListsApiInstance,
    FileListsApiInstance,
    FileExtensionListsApiInstance,
)
from dsmigrator.migrator_utils import validate_create

cert = False


def directory_listmaker(
    amdirectorylist,
    amfileextensionlist,
    amfilelist,
    OLD_HOST,
    OLD_API_KEY,
):
    og_alldirectory = DirListTenant1(amdirectorylist, OLD_HOST, OLD_API_KEY)
    og_allfileextension = FileExtensionListTenant1(
        amfileextensionlist, OLD_HOST, OLD_API_KEY
    )
    og_allfilelist = FileListTenant1(amfilelist, OLD_HOST, OLD_API_KEY)

    alldirectory, allfilelist, allfileextension = RenameLists(
        og_alldirectory, og_allfilelist, og_allfileextension
    )

    amalldirectorynew = DirListTenant2(alldirectory)
    amallfileextensionnew = FileExtensionListTenant2(allfileextension)
    amallfilelistnew = FileListTenant2(allfilelist)

    return (
        amalldirectorynew,
        amallfileextensionnew,
        amallfilelistnew,
    )


def port_listmaker(
    OLD_HOST,
    OLD_API_KEY,
    NEW_HOST,
    NEW_API_KEY,
):
    t1portlistall, t1portlistname, t1portlistid = PortListGet(OLD_HOST, OLD_API_KEY)
    t2portlistid = PortListCreate(t1portlistall, t1portlistname, NEW_HOST, NEW_API_KEY)
    return (t1portlistall, t1portlistname, t1portlistid, t2portlistid)


def mac_listmaker(OLD_HOST, OLD_API_KEY, NEW_HOST, NEW_API_KEY):
    t1maclistall, t1maclistname, t1maclistid = MacListGet(OLD_HOST, OLD_API_KEY)
    t2maclistid = MacListCreate(t1maclistid, t1maclistname, NEW_HOST, NEW_API_KEY)
    return t1maclistall, t1maclistname, t1maclistid, t2maclistid


def ip_listmaker(OLD_HOST, OLD_API_KEY, NEW_HOST, NEW_API_KEY):
    t1iplistall, t1iplistname, t1iplistid = IpListGet(OLD_HOST, OLD_API_KEY)
    t2iplistid = IpListCreate(t1iplistid, t1iplistname, NEW_HOST, NEW_API_KEY)
    return t1iplistall, t1iplistname, t1iplistid, t2iplistid


def stateful_listmaker(OLD_HOST, OLD_API_KEY, NEW_HOST, NEW_API_KEY):
    t1statefulall, t1statefulname, t1statefulid = StatefulGet(OLD_HOST, OLD_API_KEY)
    t2statefulid = StatefulCreate(t1statefulall, t1statefulname, NEW_HOST, NEW_API_KEY)
    return t1statefulall, t1statefulname, t1statefulid, t2statefulid


def ebt_listmaker(OLD_HOST, OLD_API_KEY, NEW_HOST, NEW_API_KEY):
    enum_oldetname, etIDs = ListEventTask(OLD_HOST, OLD_API_KEY)
    allet, nameet = GetEventTask(etIDs, OLD_HOST, OLD_API_KEY)
    CreateEventTask(allet, nameet, NEW_HOST, NEW_API_KEY)


def st_listmaker(OLD_HOST, OLD_API_KEY, NEW_HOST, NEW_API_KEY):
    enum_oldstname, stIDs = ListScheduledTask(OLD_HOST, OLD_API_KEY)
    allst, namest = GetScheduledTask(stIDs, OLD_HOST, OLD_API_KEY)
    CreateScheduledTask(allst, namest, NEW_HOST, NEW_API_KEY)


def DirListTenant1(directorylist, url_link_final, tenant1key):
    alldirectory = []
    print("Getting lists from Tenant 1, if any.", flush=True)
    for dirlist in directorylist:
        payload = {}
        url = url_link_final + "api/directorylists/" + str(dirlist)
        headers = {
            "api-secret-key": tenant1key,
            "api-version": "v1",
            "Content-Type": "application/json",
        }
        response = requests.request(
            "GET", url, headers=headers, data=payload, verify=cert
        )
        describe = str(response.text)
        alldirectory.append(describe)
    print("Tenant1 directory list", flush=True)
    print(directorylist, flush=True)
    return alldirectory


def FileExtensionListTenant1(fileextentionlist, url_link_final, tenant1key):
    allfileextention = []
    for dirlist in fileextentionlist:
        payload = {}
        url = url_link_final + "api/fileextensionlists/" + str(dirlist)
        headers = {
            "api-secret-key": tenant1key,
            "api-version": "v1",
            "Content-Type": "application/json",
        }
        response = requests.request(
            "GET", url, headers=headers, data=payload, verify=cert
        )
        describe = str(response.text)
        allfileextention.append(describe)
    print("Tenant1 file extention list", flush=True)
    print(fileextentionlist, flush=True)
    return allfileextention


def FileListTenant1(filelist, url_link_final, tenant1key):
    allfilelist = []
    for dirlist in filelist:
        payload = {}
        url = url_link_final + "api/filelists/" + str(dirlist)
        headers = {
            "api-secret-key": tenant1key,
            "api-version": "v1",
            "Content-Type": "application/json",
        }
        response = requests.request(
            "GET", url, headers=headers, data=payload, verify=cert
        )
        describe = str(response.text)
        allfilelist.append(describe)
    print("Tenant1 file list", flush=True)
    print(filelist, flush=True)
    return allfilelist


def RenameLists(alldirectory, allfilelist, allfileextention):
    count = 0
    if alldirectory:
        for describe in alldirectory:
            descjson = json.loads(describe)
            descjson["name"] = descjson["name"] + " - Migrated"
            alldirectory[count] = json.dumps(descjson)
            count = count + 1

    count = 0
    if allfilelist:
        for describe in allfilelist:
            descjson = json.loads(describe)
            descjson["name"] = descjson["name"] + " - Migrated"
            allfilelist[count] = json.dumps(descjson)
            count = count + 1
    count = 0
    if allfileextention:
        for describe in allfileextention:
            descjson = json.loads(describe)
            descjson["name"] = descjson["name"] + " - Migrated"
            allfileextention[count] = json.dumps(descjson)
            count = count + 1
    return alldirectory, allfilelist, allfileextention


def DirListTenant2(alldirectory):
    print("Creating directory list in tenant 2, if any", flush=True)
    if alldirectory:
        alldirectorynew = validate_create(
            alldirectory, DirectoryListsApiInstance(), "directory"
        )
    print("new directory list", flush=True)
    print(alldirectorynew, flush=True)
    return alldirectorynew


def FileListTenant2(allfile):
    print("Creating file list in tenant 2, if any", flush=True)
    if allfile:
        allfilenew = validate_create(allfile, FileListsApiInstance(), "file")
    print("new file list", flush=True)
    print(allfilenew, flush=True)
    return allfilenew


def FileExtensionListTenant2(allfileext):
    print("Creating file extension list in tenant 2, if any", flush=True)
    if allfileext:
        allfileextnew = validate_create(
            allfileext, FileExtensionListsApiInstance(), "file extension"
        )
        print("new file extension list", flush=True)
        print(allfileextnew, flush=True)
        return allfileextnew


def PortListGet(url_link_final, tenant1key):
    t1portlistall = []
    t1portlistname = []
    t1portlistid = []
    print("Getting All Port List...", flush=True)
    payload = {}
    url = url_link_final + "api/portlists"
    headers = {
        "api-secret-key": tenant1key,
        "api-version": "v1",
        "Content-Type": "application/json",
    }
    response = requests.request("GET", url, headers=headers, data=payload, verify=cert)
    describe = str(response.text)
    describe2 = str(response.text)
    namejson = json.loads(describe)
    for count, here in enumerate(namejson["portLists"]):
        t1portlistall.append(str(json.dumps(here)))
        t1portlistname.append(str(here["name"]))
        print("#" + str(count) + " Port List name: " + str(here["name"]), flush=True)
        t1portlistid.append(str(here["ID"]))
        print("#" + str(count) + " Port List ID: " + str(here["ID"]), flush=True)
    print("Done!", flush=True)
    return t1portlistall, t1portlistname, t1portlistid


def PortListCreate(t1portlistall, t1portlistname, url_link_final_2, tenant2key):
    t2portlistid = []
    print("Transfering All Port List...", flush=True)
    for count, dirlist in enumerate(t1portlistname):
        payload = (
            '{"searchCriteria": [{"fieldName": "name","stringValue": "'
            + dirlist
            + '"}]}'
        )
        url = url_link_final_2 + "api/portlists/search"
        headers = {
            "api-secret-key": tenant2key,
            "api-version": "v1",
            "Content-Type": "application/json",
        }
        response = requests.request(
            "POST", url, headers=headers, data=payload, verify=cert
        )
        describe = str(response.text)
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
                        payload = t1portlistall[count]
                        url = url_link_final_2 + "api/portlists/" + str(indexid)
                        headers = {
                            "api-secret-key": tenant2key,
                            "api-version": "v1",
                            "Content-Type": "application/json",
                        }
                        response = requests.request(
                            "POST", url, headers=headers, data=payload, verify=cert
                        )
                        t2portlistid.append(str(indexid))
                        print("#" + str(count) + " Port List ID:" + indexid, flush=True)
        else:
            payload = t1portlistall[count]
            url = url_link_final_2 + "api/portlists"
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
                        t2portlistid.append(str(indexid))
                        print("#" + str(count) + " Port List ID:" + indexid, flush=True)
            else:
                print(describe, flush=True)
                print(payload, flush=True)
    print("Done!", flush=True)
    return t2portlistid


def MacListGet(url_link_final, tenant1key):
    t1maclistall = []
    t1maclistname = []
    t1maclistid = []
    print("Getting All Mac List...", flush=True)
    payload = {}
    url = url_link_final + "api/maclists"
    headers = {
        "api-secret-key": tenant1key,
        "api-version": "v1",
        "Content-Type": "application/json",
    }
    response = requests.request("GET", url, headers=headers, data=payload, verify=cert)
    describe = str(response.text)
    describe2 = str(response.text)
    namejson = json.loads(describe)
    for count, here in enumerate(namejson["macLists"]):
        t1maclistall.append(str(json.dumps(here)))
        t1maclistname.append(str(here["name"]))
        print("#" + str(count) + " Mac List name: " + str(here["name"]), flush=True)
        t1maclistid.append(str(here["ID"]))
        print("#" + str(count) + " Mac List ID: " + str(here["ID"]), flush=True)

    print("Done!", flush=True)
    return t1maclistall, t1maclistname, t1maclistid


def MacListCreate(t1maclistall, t1maclistname, url_link_final_2, tenant2key):
    t2maclistid = []
    print("Transfering All Mac List...", flush=True)
    for count, dirlist in enumerate(t1maclistname):
        payload = (
            '{"searchCriteria": [{"fieldName": "name","stringValue": "'
            + dirlist
            + '"}]}'
        )
        url = url_link_final_2 + "api/maclists/search"
        headers = {
            "api-secret-key": tenant2key,
            "api-version": "v1",
            "Content-Type": "application/json",
        }
        response = requests.request(
            "POST", url, headers=headers, data=payload, verify=cert
        )
        describe = str(response.text)
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
                        payload = t1maclistall[count]
                        url = url_link_final_2 + "api/maclists/" + str(indexid)
                        headers = {
                            "api-secret-key": tenant2key,
                            "api-version": "v1",
                            "Content-Type": "application/json",
                        }
                        response = requests.request(
                            "POST", url, headers=headers, data=payload, verify=cert
                        )
                        t2maclistid.append(str(indexid))
                        print("#" + str(count) + " MAC List ID: " + indexid, flush=True)
        else:
            payload = t1maclistall[count]
            url = url_link_final_2 + "api/maclists"
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
                        t2maclistid.append(str(indexid))
                        print("#" + str(count) + " MAC List ID: " + indexid, flush=True)
            else:
                print(describe, flush=True)
                print(payload, flush=True)
    print("Done!", flush=True)
    return t2maclistid


def IpListGet(url_link_final, tenant1key):
    t1iplistall = []
    t1iplistname = []
    t1iplistid = []
    print("Getting All IP List...", flush=True)
    payload = {}
    url = url_link_final + "api/iplists"
    headers = {
        "api-secret-key": tenant1key,
        "api-version": "v1",
        "Content-Type": "application/json",
    }
    response = requests.request("GET", url, headers=headers, data=payload, verify=cert)
    describe = str(response.text)
    describe2 = str(response.text)
    namejson = json.loads(describe)
    for count, here in enumerate(namejson["ipLists"]):
        t1iplistall.append(str(json.dumps(here)))
        t1iplistname.append(str(here["name"]))
        print("#" + str(count) + " IP List name: " + str(here["name"]), flush=True)
        t1iplistid.append(str(here["ID"]))
        print("#" + str(count) + " IP List ID: " + str(here["ID"]), flush=True)
    print("Done!", flush=True)
    return t1iplistall, t1iplistname, t1iplistid


def IpListCreate(t1iplistall, t1iplistname, url_link_final_2, tenant2key):
    t2iplistid = []
    print("Transfering All IP List...", flush=True)
    for count, dirlist in enumerate(t1iplistname):
        payload = (
            '{"searchCriteria": [{"fieldName": "name","stringValue": "'
            + dirlist
            + '"}]}'
        )
        url = url_link_final_2 + "api/iplists/search"
        headers = {
            "api-secret-key": tenant2key,
            "api-version": "v1",
            "Content-Type": "application/json",
        }
        response = requests.request(
            "POST", url, headers=headers, data=payload, verify=cert
        )
        describe = str(response.text)
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
                        payload = t1iplistall[count]
                        url = url_link_final_2 + "api/iplists/" + str(indexid)
                        headers = {
                            "api-secret-key": tenant2key,
                            "api-version": "v1",
                            "Content-Type": "application/json",
                        }
                        response = requests.request(
                            "POST", url, headers=headers, data=payload, verify=cert
                        )
                        t2iplistid.append(str(indexid))
                        print("#" + str(count) + " IP List ID: " + indexid, flush=True)
        else:
            payload = t1iplistall[count]
            url = url_link_final_2 + "api/iplists"
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
                        t2iplistid.append(str(indexid))
                        print("#" + str(count) + " IP List ID: " + indexid, flush=True)
            else:
                print(describe, flush=True)
                print(payload, flush=True)
    # print("Finished Transfering All IP List.")
    # print(t2iplistid)
    print("Done!", flush=True)
    return t2iplistid


def StatefulGet(url_link_final, tenant1key):
    t1statefulall = []
    t1statefulname = []
    t1statefulid = []
    print("Getting All Stateful Configuration...", flush=True)
    payload = {}
    url = url_link_final + "api/statefulconfigurations"
    headers = {
        "api-secret-key": tenant1key,
        "api-version": "v1",
        "Content-Type": "application/json",
    }
    response = requests.request("GET", url, headers=headers, data=payload, verify=cert)
    describe = str(response.text)
    describe2 = str(response.text)
    namejson = json.loads(describe)
    for count, here in enumerate(namejson["statefulConfigurations"]):
        t1statefulall.append(str(json.dumps(here)))
        t1statefulname.append(str(here["name"]))
        print(
            "#" + str(count) + " Stateful Config name: " + str(here["name"]), flush=True
        )
        t1statefulid.append(str(here["ID"]))
        print("#" + str(count) + " Stateful Config ID: " + str(here["ID"]), flush=True)
    print("Done", flush=True)
    return t1statefulall, t1statefulname, t1statefulid


def StatefulCreate(t1statefulall, t1statefulname, url_link_final_2, tenant2key):
    t2statefulid = []
    print("Transfering All Stateful Configuration...", flush=True)
    if t1statefulname:
        for count, dirlist in enumerate(t1statefulname):
            payload = (
                '{"searchCriteria": [{"fieldName": "name","stringValue": "'
                + dirlist
                + '"}]}'
            )
            url = url_link_final_2 + "api/statefulconfigurations/search"
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
                if taskjson["statefulConfigurations"]:
                    for here in taskjson["statefulConfigurations"]:
                        indexid = here["ID"]
                        payload = t1statefulall[count]
                        url = (
                            url_link_final_2
                            + "api/statefulconfigurations/"
                            + str(indexid)
                        )
                        headers = {
                            "api-secret-key": tenant2key,
                            "api-version": "v1",
                            "Content-Type": "application/json",
                        }
                        response = requests.request(
                            "POST", url, headers=headers, data=payload, verify=cert
                        )
                        describe = str(response.text)
                        taskjson1 = json.loads(describe)
                        t2statefulid.append(str(taskjson1["ID"]))
                        print(
                            "#"
                            + str(count)
                            + " Stateful Config name: "
                            + taskjson1["name"],
                            flush=True,
                        )
                        print(
                            "#"
                            + str(count)
                            + " Stateful Config ID: "
                            + str(taskjson1["ID"]),
                            flush=True,
                        )
                else:
                    payload = t1statefulall[count]
                    url = url_link_final_2 + "api/statefulconfigurations"
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
                    t2statefulid.append(str(taskjson["ID"]))
                    print(
                        "#" + str(count) + " Stateful Config name: " + taskjson["name"],
                        flush=True,
                    )
                    print(
                        "#"
                        + str(count)
                        + " Stateful Config ID: "
                        + str(taskjson["ID"]),
                        flush=True,
                    )
            else:
                print(describe, flush=True)
                print(payload, flush=True)
    print("Done!", flush=True)
    return t2statefulid


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
    index = 0
    oldetname = []
    oldetid = []
    namejson = json.loads(describe)
    for here in namejson["eventBasedTasks"]:
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
    print(allet, flush=True)
    print(nameet, flush=True)
    return allet, nameet


def CreateEventTask(allet, nameet, url_link_final_2, tenant2key):
    print("Creating Task to target Account...", flush=True)
    if nameet:
        for count, dirlist in enumerate(nameet):
            payload = (
                '{"searchCriteria": [{"fieldName": "name","stringValue": "'
                + dirlist
                + '"}]}'
            )
            url = url_link_final_2 + "api/eventbasedtasks/search"
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
                if taskjson["eventBasedTasks"]:
                    for here in taskjson["eventBasedTasks"]:
                        indexid = here["ID"]
                        payload = allet[count]
                        url = url_link_final_2 + "api/eventbasedtasks/" + str(indexid)
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
                        print(
                            "#"
                            + str(count)
                            + " Event Based Task name: "
                            + taskjson["name"],
                            flush=True,
                        )
                        print(
                            "#"
                            + str(count)
                            + " Event Based ID: "
                            + str(taskjson["ID"]),
                            flush=True,
                        )
                else:
                    payload = allet[count]
                    url = url_link_final_2 + "api/eventbasedtasks"
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
                    print(
                        "#"
                        + str(count)
                        + " Event Based Task name: "
                        + taskjson["name"],
                        flush=True,
                    )
                    print(
                        "#" + str(count) + " Event Based ID: " + str(taskjson["ID"]),
                        flush=True,
                    )
            else:
                print(describe, flush=True)
                print(payload, flush=True)


def ListScheduledTask(url_link_final, tenant1key):
    payload = {}
    url = url_link_final + "api/scheduledtasks"
    headers = {
        "api-secret-key": tenant1key,
        "api-version": "v1",
        "Content-Type": "application/json",
    }
    response = requests.request("GET", url, headers=headers, data=payload, verify=cert)
    describe = str(response.text)
    index = 0
    oldstname = []
    oldstid = []
    namejson = json.loads(str(response.text))
    for here in namejson["scheduledTasks"]:
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
            print(namejson["name"], flush=True)
    return allst, namest


def CreateScheduledTask(allst, namest, url_link_final_2, tenant2key):
    print("Creating Task to target Account...", flush=True)
    if namest:
        for count, dirlist in enumerate(namest):
            print(dirlist, flush=True)
            payload = (
                '{"searchCriteria": [{"fieldName": "name","stringValue": "'
                + dirlist
                + '"}]}'
            )
            url = url_link_final_2 + "api/scheduledtasks/search"
            headers = {
                "api-secret-key": tenant2key,
                "api-version": "v1",
                "Content-Type": "application/json",
            }
            response = requests.request(
                "POST", url, headers=headers, data=payload, verify=cert
            )
            describe = str(response.text)
            index = describe.find(dirlist)
            taskjson = json.loads(describe)
            if not "message" in taskjson:
                if taskjson["scheduledTasks"]:
                    for here in taskjson["scheduledTasks"]:
                        indexid = here["ID"]
                        payload = allst[count]
                        url = url_link_final_2 + "api/scheduledtasks/" + str(indexid)
                        headers = {
                            "api-secret-key": tenant2key,
                            "api-version": "v1",
                            "Content-Type": "application/json",
                        }
                        response = requests.request(
                            "POST", url, headers=headers, data=payload, verify=cert
                        )
                        describe = str(response.text)
                        taskjson2 = json.loads(describe)
                        print(
                            "#"
                            + str(count)
                            + " Schedule Task name: "
                            + taskjson2["name"],
                            flush=True,
                        )
                        print(
                            "#" + str(count) + " Schedule ID: " + str(taskjson2["ID"]),
                            flush=True,
                        )
                else:
                    payload = allst[count]
                    url = url_link_final_2 + "api/scheduledtasks"
                    headers = {
                        "api-secret-key": tenant2key,
                        "api-version": "v1",
                        "Content-Type": "application/json",
                    }
                    response = requests.request(
                        "POST", url, headers=headers, data=payload, verify=cert
                    )
                    describe = str(response.text)
                    taskjson2 = json.loads(describe)
                    print(
                        "#" + str(count) + " Schedule Task name: " + taskjson2["name"],
                        flush=True,
                    )
                    print(
                        "#" + str(count) + " Schedule ID: " + str(taskjson2["ID"]),
                        flush=True,
                    )
            else:
                print(describe, flush=True)
                print(payload, flush=True)
