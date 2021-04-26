import sys
import os
import time
from time import sleep
import requests
import urllib3
import urllib3
import json
from dsmigrator.logging import console
from dsmigrator.api_config import (
    DirectoryListsApiInstance,
    FileListsApiInstance,
    FileExtensionListsApiInstance,
)
from dsmigrator.migrator_utils import (
    validate_create,
    value_exists,
    rename_json,
    safe_request,
)

cert = False


def directory_listmaker(
    amdirectorylist, amfileextensionlist, amfilelist, OLD_HOST, OLD_API_KEY, NEW_API_KEY
):
    og_alldirectory = DirListTenant1(amdirectorylist, OLD_HOST, OLD_API_KEY)
    og_allfileextension = FileExtensionListTenant1(
        amfileextensionlist, OLD_HOST, OLD_API_KEY
    )
    og_allfilelist = FileListTenant1(amfilelist, OLD_HOST, OLD_API_KEY)

    alldirectory, allfilelist, allfileextension = RenameLists(
        og_alldirectory, og_allfilelist, og_allfileextension
    )

    amalldirectorynew = DirListTenant2(alldirectory, NEW_API_KEY)
    amallfileextensionnew = FileExtensionListTenant2(allfileextension, NEW_API_KEY)
    amallfilelistnew = FileListTenant2(allfilelist, NEW_API_KEY)

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
    return t1portlistid, t2portlistid


def mac_listmaker(OLD_HOST, OLD_API_KEY, NEW_HOST, NEW_API_KEY):
    t1maclistall, t1maclistname, t1maclistid = MacListGet(OLD_HOST, OLD_API_KEY)
    t2maclistid = MacListCreate(t1maclistall, t1maclistname, NEW_HOST, NEW_API_KEY)
    return t1maclistid, t2maclistid


def ip_listmaker(OLD_HOST, OLD_API_KEY, NEW_HOST, NEW_API_KEY):
    t1iplistname, t1iplistid = IpListGet(OLD_HOST, OLD_API_KEY)
    t2iplistid = IpListCreate(t1iplistid, t1iplistname, NEW_HOST, NEW_API_KEY)
    return t1iplistid, t2iplistid


def stateful_listmaker(OLD_HOST, OLD_API_KEY, NEW_HOST, NEW_API_KEY):
    t1statefulall, t1statefulname, t1statefulid = StatefulGet(OLD_HOST, OLD_API_KEY)
    t2statefulid = StatefulCreate(t1statefulall, t1statefulname, NEW_HOST, NEW_API_KEY)
    stateful_dict = {0: 0}
    for i in t1statefulid:
        index = t1statefulid.index(i)
        if index < len(t2statefulid):
            stateful_dict[int(i)] = int(t2statefulid[index])
    return t1statefulid, t2statefulid, stateful_dict


def context_listmaker(OLD_HOST, OLD_API_KEY, NEW_HOST, NEW_API_KEY):
    t1contextall, t1contextname, t1contextid = ContextGet(OLD_HOST, OLD_API_KEY)
    t2contextid = ContextCreate(t1contextall, t1contextname, NEW_HOST, NEW_API_KEY)
    return t1contextid, t2contextid


def schedule_listmaker(OLD_HOST, OLD_API_KEY, NEW_HOST, NEW_API_KEY):
    t1scheduleall, t1schedulename, t1scheduleid = ScheduleGet(OLD_HOST, OLD_API_KEY)
    t2scheduleid = ScheduleCreate(t1scheduleall, t1schedulename, NEW_HOST, NEW_API_KEY)
    return t1scheduleid, t2scheduleid


def DirListTenant1(directorylist, url_link_final, tenant1key):
    alldirectory = []
    console.log("Getting lists from Tenant 1, if any.")
    for dirlist in directorylist:
        payload = {}
        url = url_link_final + "api/directorylists/" + str(dirlist)
        headers = {
            "api-secret-key": tenant1key,
            "api-version": "v1",
            "Content-Type": "application/json",
        }
        response = requests.request(
            "GET",
            url,
            headers=headers,
            data=payload,
            verify=cert,
        )
        describe = str(response.text)
        alldirectory.append(describe)
    console.log("Tenant1 directory list")
    console.log(directorylist)
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
            "GET",
            url,
            headers=headers,
            data=payload,
            verify=cert,
        )
        describe = str(response.text)
        allfileextention.append(describe)
    console.log("Tenant1 file extention list")
    console.log(fileextentionlist)
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
            "GET",
            url,
            headers=headers,
            data=payload,
            verify=cert,
        )
        describe = str(response.text)
        allfilelist.append(describe)
    console.log("Tenant1 file list")
    console.log(filelist)
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


def DirListTenant2(alldirectory, NEW_API_KEY):
    console.log("Creating directory list in tenant 2, if any")
    alldirectorynew = []
    if alldirectory:
        alldirectorynew = validate_create(
            alldirectory, DirectoryListsApiInstance(NEW_API_KEY), "directory"
        )
    console.log(alldirectorynew)
    return alldirectorynew


def FileListTenant2(allfile, NEW_API_KEY):
    console.log("Creating file list in tenant 2, if any")
    allfilenew = []
    if allfile:
        allfilenew = validate_create(allfile, FileListsApiInstance(NEW_API_KEY), "file")
    console.log("new file list")
    console.log(allfilenew)
    return allfilenew


def FileExtensionListTenant2(allfileext, NEW_API_KEY):
    console.log("Creating file extension list in tenant 2, if any")
    allfileextnew = []
    if allfileext:
        allfileextnew = validate_create(
            allfileext, FileExtensionListsApiInstance(NEW_API_KEY), "file extension"
        )
    console.log("new file extension list")
    console.log(allfileextnew)
    return allfileextnew


def PortListGet(url_link_final, tenant1key):
    t1portlistall = []
    t1portlistname = []
    t1portlistid = []
    console.log("Getting All Port List...")
    url = url_link_final + "api/portlists"
    response = safe_request(tenant1key, "GET", url, payload={}, cert=cert)
    describe = str(response.text)
    ports_json = json.loads(describe).get("portLists")
    if ports_json is not None:
        for count, here in enumerate(ports_json):
            t1portlistall.append(str(json.dumps(here)))
            t1portlistname.append(str(here["name"]))
            console.log("#" + str(count) + " Port List name: " + str(here["name"]))
            t1portlistid.append(str(here["ID"]))
            console.log("#" + str(count) + " Port List ID: " + str(here["ID"]))
        console.log("Done!")
    return t1portlistall, t1portlistname, t1portlistid


def PortListCreate(t1portlistall, t1portlistname, url_link_final_2, tenant2key):
    t2portlistid = []
    console.log("Transfering All Port List...")
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
            "POST",
            url,
            headers=headers,
            data=payload,
            verify=cert,
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
                            "POST",
                            url,
                            headers=headers,
                            data=payload,
                            verify=cert,
                        )
                        t2portlistid.append(str(indexid))
                        console.log("#" + str(count) + " Port List ID: " + indexid)
        else:
            payload = t1portlistall[count]
            url = url_link_final_2 + "api/portlists"
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
                        console.log("#" + str(count) + " Port List ID:" + indexid)
            else:
                console.log(describe)
                console.log(payload)
    console.log("Done!")
    return t2portlistid


def MacListGet(url_link_final, tenant1key):
    t1maclistall = []
    t1maclistname = []
    t1maclistid = []
    console.log("Getting All Mac List...")
    url = url_link_final + "api/maclists"
    response = safe_request(tenant1key, "GET", url, payload={}, cert=cert)
    describe = str(response.text)
    mac_json = json.loads(describe).get("macLists")
    if mac_json is not None:
        for count, here in enumerate(mac_json):
            t1maclistall.append(json.dumps(here))
            t1maclistname.append(str(here["name"]))
            console.log("#" + str(count) + " Mac List name: " + str(here["name"]))
            t1maclistid.append(str(here["ID"]))
            console.log("#" + str(count) + " Mac List ID: " + str(here["ID"]))

        console.log("Done!")
    return t1maclistall, t1maclistname, t1maclistid


def MacListCreate(t1maclistall, t1maclistname, url_link_final_2, tenant2key):
    t2maclistid = []
    console.log("Transfering All Mac List...")
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
            "POST",
            url,
            headers=headers,
            data=payload,
            verify=cert,
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
                            "POST",
                            url,
                            headers=headers,
                            data=payload,
                            verify=cert,
                        )
                        t2maclistid.append(str(indexid))
                        console.log("#" + str(count) + " MAC List ID: " + indexid)
        else:
            payload = t1maclistall[count]
            url = url_link_final_2 + "api/maclists"
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
                        console.log("#" + str(count) + " MAC List ID: " + indexid)
            else:
                console.log(describe)
                console.log(payload)
    console.log("Done!")
    return t2maclistid


def IpListGet(url_link_final, tenant1key):
    t1iplistall = []
    t1iplistname = []
    t1iplistid = []
    console.log("Getting All IP List...")
    payload = {}
    url = url_link_final + "api/iplists"
    headers = {
        "api-secret-key": tenant1key,
        "api-version": "v1",
        "Content-Type": "application/json",
    }
    response = requests.request(
        "GET",
        url,
        headers=headers,
        data=payload,
        verify=cert,
    )
    describe = str(response.text)
    ip_json = json.loads(describe).get("ipLists")
    if ip_json:
        for count, here in enumerate(ip_json):
            t1iplistall.append(str(json.dumps(here)))
            t1iplistname.append(str(here["name"]))
            console.log("#" + str(count) + " IP List name: " + str(here["name"]))
            t1iplistid.append(str(here["ID"]))
            console.log("#" + str(count) + " IP List ID: " + str(here["ID"]))
        console.log("Done!")
    return t1iplistname, t1iplistid


def IpListCreate(t1iplistall, t1iplistname, url_link_final_2, tenant2key):
    t2iplistid = []
    console.log("Transfering All IP List...")
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
            "POST",
            url,
            headers=headers,
            data=payload,
            verify=cert,
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
                            "POST",
                            url,
                            headers=headers,
                            data=payload,
                            verify=cert,
                        )
                        t2iplistid.append(str(indexid))
                        console.log("#" + str(count) + " IP List ID: " + indexid)
        else:
            payload = t1iplistall[count]
            url = url_link_final_2 + "api/iplists"
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
                        console.log("#" + str(count) + " IP List ID: " + indexid)
            else:
                console.log(describe)
                console.log(payload)
    console.log("Done!")
    return t2iplistid


def StatefulGet(url_link_final, tenant1key):
    t1statefulall = []
    t1statefulname = []
    t1statefulid = []
    console.log("Getting All Stateful Configuration...")
    payload = {}
    url = url_link_final + "api/statefulconfigurations"
    headers = {
        "api-secret-key": tenant1key,
        "api-version": "v1",
        "Content-Type": "application/json",
    }
    response = requests.request(
        "GET",
        url,
        headers=headers,
        data=payload,
        verify=cert,
    )
    describe = str(response.text)
    stateful_json = json.loads(describe).get("statefulConfigurations")
    if stateful_json is not None:
        for count, here in enumerate(stateful_json):
            t1statefulall.append(str(json.dumps(here)))
            t1statefulname.append(str(here["name"]))
            console.log(
                "#" + str(count) + " Stateful Config name: " + str(here["name"]),
            )
            t1statefulid.append(str(here["ID"]))
            console.log("#" + str(count) + " Stateful Config ID: " + str(here["ID"]))
        console.log("Done")
    return t1statefulall, t1statefulname, t1statefulid


def StatefulCreate(t1statefulall, t1statefulname, url_link_final_2, tenant2key):
    t2statefulid = []
    console.log("Transfering All Stateful Configuration...")
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
                "POST",
                url,
                headers=headers,
                data=payload,
                verify=cert,
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
                            "POST",
                            url,
                            headers=headers,
                            data=payload,
                            verify=cert,
                        )
                        describe = str(response.text)
                        taskjson1 = json.loads(describe)
                        t2statefulid.append(str(taskjson1["ID"]))
                        console.log(
                            "#"
                            + str(count)
                            + " Stateful Config name: "
                            + taskjson1["name"],
                        )
                        console.log(
                            "#"
                            + str(count)
                            + " Stateful Config ID: "
                            + str(taskjson1["ID"]),
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
                        "POST",
                        url,
                        headers=headers,
                        data=payload,
                        verify=cert,
                    )
                    describe = str(response.text)
                    taskjson = json.loads(describe)
                    t2statefulid.append(str(taskjson["ID"]))
                    console.log(
                        "#" + str(count) + " Stateful Config name: " + taskjson["name"],
                    )
                    console.log(
                        "#"
                        + str(count)
                        + " Stateful Config ID: "
                        + str(taskjson["ID"]),
                    )
            else:
                console.log(describe)
                console.log(payload)
    console.log("Done!")
    return t2statefulid


def ContextGet(url_link_final, tenant1key):
    t1contextall = []
    t1contextname = []
    t1contextid = []
    console.log("Getting All Context Configuration...")
    payload = {}
    url = url_link_final + "api/contexts"
    headers = {
        "api-secret-key": tenant1key,
        "api-version": "v1",
        "Content-Type": "application/json",
    }
    response = requests.request(
        "GET",
        url,
        headers=headers,
        data=payload,
        verify=cert,
    )
    describe = str(response.text)
    contexts_json = json.loads(describe).get("contexts")
    if contexts_json is not None:
        for count, here in enumerate(contexts_json):
            t1contextall.append(str(json.dumps(here)))
            t1contextname.append(str(here["name"]))
            console.log(
                "#" + str(count) + " Context Config name: " + str(here["name"]),
            )
            t1contextid.append(str(here["ID"]))
            console.log("#" + str(count) + " Context Config ID: " + str(here["ID"]))
        console.log("Done")
    return t1contextall, t1contextname, t1contextid


def ContextCreate(t1contextall, t1contextname, url_link_final_2, tenant2key):
    t2contextid = []
    console.log("Transfering All Context Configuration...")
    if t1contextname:
        for count, dirlist in enumerate(t1contextname):
            payload = (
                '{"searchCriteria": [{"fieldName": "name","stringValue": "'
                + dirlist
                + '"}]}'
            )
            url = url_link_final_2 + "api/contexts/search"
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
            describe = str(response.text)
            taskjson = json.loads(describe)
            if not "message" in taskjson:
                if taskjson["contexts"]:
                    for here in taskjson["contexts"]:
                        indexid = here["ID"]
                        payload = t1contextall[count]
                        url = url_link_final_2 + "api/contexts/" + str(indexid)
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
                        describe = str(response.text)
                        taskjson1 = json.loads(describe)
                        t2contextid.append(str(taskjson1["ID"]))
                        console.log(
                            "#"
                            + str(count)
                            + " Context Config name: "
                            + taskjson1["name"],
                        )
                        console.log(
                            "#"
                            + str(count)
                            + " Context Config ID: "
                            + str(taskjson1["ID"]),
                        )
                else:
                    payload = t1contextall[count]
                    url = url_link_final_2 + "api/contexts"
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
                    describe = str(response.text)
                    taskjson = json.loads(describe)
                    t2contextid.append(str(taskjson["ID"]))
                    console.log(
                        "#" + str(count) + " Context Config name: " + taskjson["name"],
                    )
                    console.log(
                        "#" + str(count) + " Context Config ID: " + str(taskjson["ID"]),
                    )
            else:
                console.log(describe)
                console.log(payload)
    console.log("Done!")
    return t2contextid


def ScheduleGet(url_link_final, tenant1key):
    t1scheduleall = []
    t1schedulename = []
    t1scheduleid = []
    console.log("Getting All Schedule Configuration...")
    payload = {}
    url = url_link_final + "api/schedules"
    headers = {
        "api-secret-key": tenant1key,
        "api-version": "v1",
        "Content-Type": "application/json",
    }
    response = requests.request(
        "GET",
        url,
        headers=headers,
        data=payload,
        verify=cert,
    )
    describe = str(response.text)
    schedules_json = json.loads(describe).get("schedules")
    if schedules_json is not None:
        for count, here in enumerate(schedules_json):
            t1scheduleall.append(str(json.dumps(here)))
            t1schedulename.append(str(here["name"]))
            console.log(
                "#" + str(count) + " Schedule Config name: " + str(here["name"]),
            )
            t1scheduleid.append(str(here["ID"]))
            console.log("#" + str(count) + " Schedule Config ID: " + str(here["ID"]))
        console.log("Done")
    return t1scheduleall, t1schedulename, t1scheduleid


def ScheduleCreate(t1scheduleall, t1schedulename, url_link_final_2, tenant2key):
    t2scheduleid = []
    console.log("Transfering All Schedule Configuration...")
    if t1schedulename:
        for count, dirlist in enumerate(t1schedulename):
            payload = (
                '{"searchCriteria": [{"fieldName": "name","stringValue": "'
                + dirlist
                + '"}]}'
            )
            url = url_link_final_2 + "api/schedules/search"
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
            describe = str(response.text)
            taskjson = json.loads(describe)
            if not "message" in taskjson:
                if taskjson["schedules"]:
                    for here in taskjson["schedules"]:
                        indexid = here["ID"]
                        payload = t1scheduleall[count]
                        url = url_link_final_2 + "api/schedules/" + str(indexid)
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
                        describe = str(response.text)
                        taskjson1 = json.loads(describe)
                        t2scheduleid.append(str(taskjson1["ID"]))
                        console.log(
                            "#"
                            + str(count)
                            + " Schedule Config name: "
                            + taskjson1["name"],
                        )
                        console.log(
                            "#"
                            + str(count)
                            + " Schedule Config ID: "
                            + str(taskjson1["ID"]),
                        )
                else:
                    payload = t1scheduleall[count]
                    url = url_link_final_2 + "api/schedules"
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
                    describe = str(response.text)
                    taskjson = json.loads(describe)
                    t2scheduleid.append(str(taskjson["ID"]))
                    console.log(
                        "#" + str(count) + " Schedule Config name: " + taskjson["name"],
                    )
                    console.log(
                        "#"
                        + str(count)
                        + " Schedule Config ID: "
                        + str(taskjson["ID"]),
                    )
            else:
                console.log(describe)
                console.log(payload)
    console.log("Done!")
    return t2scheduleid
