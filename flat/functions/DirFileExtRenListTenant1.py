import sys
import os
import time
from time import sleep
import requests
import urllib3
import json

cert = False


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
