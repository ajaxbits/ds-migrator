import sys
import os
import time
from time import sleep
import requests
import urllib3
import json

cert = False

def MacListGet(url_link_final, tenant1key):
    t1maclistall = []
    t1maclistname = []
    t1maclistid = []
    print("Getting All Mac List...", flush=True)
    payload  = {}
    url = url_link_final + 'api/maclists'
    headers = {
        "api-secret-key": tenant1key,
        "api-version": "v1",
        "Content-Type": "application/json",
    }
    response = requests.request("GET", url, headers=headers, data=payload, verify=cert)
    describe = str(response.text)
    describe2 = str(response.text)
    namejson = json.loads(describe)
    for count, here in enumerate(namejson['macLists']):
        t1maclistall.append(str(json.dumps(here)))
        t1maclistname.append(str(here['name']))
        print("#" + str(count) + " Mac List name: " + str(here['name']), flush=True)
        t1maclistid.append(str(here['ID']))
        print("#" + str(count) + " Mac List ID: " + str(here['ID']), flush=True)

    '''
    index = describe.find('\"macLists\"')
    if index != -1:
        indexpart = describe[index+10:]
        startIndex = 0
        while startIndex != -1: 
            startIndex = indexpart.find('{')
            if startIndex != -1: #i.e. if the first quote was found
                endIndex = indexpart.find('}', startIndex + 1)
                if startIndex != -1 and endIndex != -1: #i.e. both quotes were found
                    indexid = indexpart[startIndex:endIndex+1]
                    t1maclistall.append(str(indexid))
                    indexpart = indexpart[endIndex:]
    count = 0
    while index != -1:
        index = describe2.find('\"name\"')
        if index != -1:
            indexpart = describe2[index+6:]
            startIndex = indexpart.find('\"')
            if startIndex != -1: #i.e. if the first quote was found
                endIndex = indexpart.find(',', startIndex + 1)
                if startIndex != -1 and endIndex != -1: #i.e. both quotes were found
                    indexid = indexpart[startIndex+1:endIndex-1]
                    t1maclistname.append(str(indexid))
                    print("#" + str(count) + " Mac List name: " + indexid, flush=True)
                    describe2 = indexpart[endIndex:]
                    index = describe2.find('\"ID\"')
                    if index != -1:
                        indexpart = describe2[index+3:]
                        startIndex = indexpart.find(':')
                        if startIndex != -1: #i.e. if the first quote was found
                            endIndex = indexpart.find('}', startIndex + 1)
                            if startIndex != -1 and endIndex != -1: #i.e. both quotes were found
                                indexid = indexpart[startIndex+1:endIndex]
                                t1maclistid.append(str(indexid))
                                print("#" + str(count) + " Mac List ID: " + indexid, flush=True)
                                describe2 = indexpart[endIndex:]
        count += 1
        '''
    #print(t1maclistid)
    print("Done!", flush=True)
    return t1maclistall, t1maclistname, t1maclistid

def MacListCreate(t1maclistall, t1maclistname, url_link_final_2, tenant2key):
    t2maclistid = []
    print("Transfering All Mac List...", flush=True)
    for count, dirlist in enumerate(t1maclistname):
        payload = "{\"searchCriteria\": [{\"fieldName\": \"name\",\"stringValue\": \"" + dirlist + "\"}]}"
        url = url_link_final_2 + 'api/maclists/search'
        headers = {
        "api-secret-key": tenant2key,
        "api-version": "v1",
        "Content-Type": "application/json",
        }
        response = requests.request("POST", url, headers=headers, data=payload, verify=cert)
        describe = str(response.text)
        index = describe.find(dirlist)
        if index != -1:
            index = describe.find("\"ID\"")
            if index != -1:
                indexpart = describe[index+4:]
                startIndex = indexpart.find(':')
                if startIndex != -1: #i.e. if the first quote was found
                    endIndex = indexpart.find('}', startIndex + 1)
                    if startIndex != -1 and endIndex != -1: #i.e. both quotes were found
                        indexid = indexpart[startIndex+1:endIndex]
                        payload = t1maclistall[count]
                        url = url_link_final_2 + 'api/maclists/' + str(indexid)
                        headers = {
                        "api-secret-key": tenant2key,
                        "api-version": "v1",
                        "Content-Type": "application/json",
                        }
                        response = requests.request("POST", url, headers=headers, data=payload, verify=cert)
                        t2maclistid.append(str(indexid))
                        print("#" + str(count) + " MAC List ID: " + indexid, flush=True)
        else:
            payload = t1maclistall[count]
            url = url_link_final_2 + 'api/maclists'
            headers = {
            "api-secret-key": tenant2key,
            "api-version": "v1",
            "Content-Type": "application/json",
            }
            response = requests.request("POST", url, headers=headers, data=payload, verify=cert)
            describe = str(response.text)
            index = describe.find("\"ID\"")
            if index != -1:
                indexpart = describe[index+4:]
                startIndex = indexpart.find(':')
                if startIndex != -1: #i.e. if the first quote was found
                    endIndex = indexpart.find('}', startIndex + 1)
                    if startIndex != -1 and endIndex != -1: #i.e. both quotes were found
                        indexid = indexpart[startIndex+1:endIndex]
                        t2maclistid.append(str(indexid))
                        print("#" + str(count) + " MAC List ID: " + indexid, flush=True)
            else:
                print(describe, flush=True)
                print(payload, flush=True)
    #print("Finished Transfering All Mac List.")
    #print(t2maclistid)
    print("Done!", flush=True)
    return t2maclistid