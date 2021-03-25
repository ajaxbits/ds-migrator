import sys
import os
import time
from time import sleep
import requests
import urllib3
import json

cert = False

def ListScheduledTask(url_link_final, tenant1key):
    payload = {}
    url = url_link_final + 'api/scheduledtasks'
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
    for here in namejson['scheduledTasks']:
        oldstname.append(str(here['name']))
        oldstid.append(str(here['ID']))
    return enumerate(oldstname), oldstid

'''
    while index != -1:
        index = describe.find('\"name\"')
        if index != -1:
            indexpart = describe[index+6:]
            startIndex = indexpart.find('\"')
            if startIndex != -1: 
                endIndex = indexpart.find(',', startIndex + 1)
                if startIndex != -1 and endIndex != -1: 
                    indexid = indexpart[startIndex+1:endIndex-1]
                    oldstname.append(str(indexid))
        index = describe.find('\"ID\"')
        if index != -1:
            indexpart = describe[index+4:]
            startIndex = indexpart.find(':')
            if startIndex != -1: 
                endIndex = indexpart.find(',', startIndex + 1)
                if startIndex != -1 and endIndex != -1: 
                    indexid = indexpart[startIndex+1:endIndex]
                    oldstid.append(str(indexid))
                    describe = indexpart[endIndex:]
                else:
                    endIndex = indexpart.find('}', startIndex + 1)
                    if startIndex != -1 and endIndex != -1: 
                        indexid = indexpart[startIndex+1:endIndex]
                        oldstid.append(str(indexid))
                        describe = indexpart[endIndex:]
'''

def GetScheduledTask(stIDs, url_link_final, tenant1key):
    allst = []
    namest = []
    print ('Getting Target Task...', flush=True)
    if stIDs:
        for part in stIDs:
            payload = {}
            url = url_link_final + 'api/scheduledtasks/' + str(part)
            headers = {
            "api-secret-key": tenant1key,
            "api-version": "v1",
            "Content-Type": "application/json",
            }
            response = requests.request("GET", url, headers=headers, data=payload, verify=cert)
            describe = str(response.text)
            allst.append(describe)
            namejson = json.loads(describe)
            namest.append(str(namejson['name']))
            print(namejson['name'], flush=True)
            '''
            index = describe.find('\"name\"')
            if index != -1:
                indexpart = describe[index+6:]
                startIndex = indexpart.find('\"')
                if startIndex != -1: #i.e. if the first quote was found
                    endIndex = indexpart.find(',', startIndex + 1)
                    if startIndex != -1 and endIndex != -1: #i.e. both quotes were found
                        indexid = indexpart[startIndex+1:endIndex-1]
                        namest.append(str(indexid))
                        describe = indexpart[endIndex:]
                        '''
    #print(allst, flush=True)
    #print(namest, flush=True)
    return allst, namest

def CreateScheduledTask(allst, namest, url_link_final_2, tenant2key):
    print ('Creating Task to target Account...', flush=True)
    if namest:
        for count, dirlist in enumerate(namest):
            print(dirlist, flush=True)
            payload = "{\"searchCriteria\": [{\"fieldName\": \"name\",\"stringValue\": \"" + dirlist + "\"}]}"
            url = url_link_final_2 + 'api/scheduledtasks/search'
            headers = {
            "api-secret-key": tenant2key,
            "api-version": "v1",
            "Content-Type": "application/json",
            }
            response = requests.request("POST", url, headers=headers, data=payload, verify=cert)
            describe = str(response.text)
            index = describe.find(dirlist)
            taskjson = json.loads(describe)
            if not 'message' in taskjson:
                if taskjson['scheduledTasks']:
                    for here in taskjson['scheduledTasks']:
                        indexid = here['ID']
                        payload = allst[count]
                        url = url_link_final_2 + 'api/scheduledtasks/' + str(indexid)
                        headers = {
                        "api-secret-key": tenant2key,
                        "api-version": "v1",
                        "Content-Type": "application/json",
                        }
                        response = requests.request("POST", url, headers=headers, data=payload, verify=cert)
                        describe = str(response.text)
                        taskjson2 = json.loads(describe)
                        print("#" + str(count) + " Schedule Task name: " + taskjson2['name'], flush=True)
                        print("#" + str(count) + " Schedule ID: " + str(taskjson2['ID']), flush=True)
                else:
                    payload = allst[count]
                    url = url_link_final_2 + 'api/scheduledtasks'
                    headers = {
                    "api-secret-key": tenant2key,
                    "api-version": "v1",
                    "Content-Type": "application/json",
                    }
                    response = requests.request("POST", url, headers=headers, data=payload, verify=cert)
                    describe = str(response.text)
                    taskjson2 = json.loads(describe)
                    print("#" + str(count) + " Schedule Task name: " + taskjson2['name'], flush=True)
                    print("#" + str(count) + " Schedule ID: " + str(taskjson2['ID']), flush=True)
            else:
                print(describe, flush=True)
                print(payload, flush=True)
                    
            '''
            if index != -1:
                index = describe.find("\"ID\"")
                if index != -1:
                    indexpart = describe[index+4:]
                    startIndex = indexpart.find(':')
                    if startIndex != -1: #i.e. if the first quote was found
                        endIndex = indexpart.find('}', startIndex + 1)
                        if startIndex != -1 and endIndex != -1: #i.e. both quotes were found
                            indexid = indexpart[startIndex+1:endIndex]
                            payload = allst[count]
                            url = url_link_final_2 + 'api/scheduledtasks/' + str(indexid)
                            headers = {
                            "api-secret-key": tenant2key,
                            "api-version": "v1",
                            "Content-Type": "application/json",
                            }
                            response = requests.request("POST", url, headers=headers, data=payload, verify=cert)
                            describe = str(response.text)
                            taskjson = json.loads(describe)
                            print("#" + str(count) + " Schedule Task name: " + taskjson['name'], flush=True)
                            print("#" + str(count) + " Schedule ID: " + taskjson['ID'], flush=True)
            else:
                payload = allst[count]
                url = url_link_final_2 + 'api/scheduledtasks'
                headers = {
                "api-secret-key": tenant2key,
                "api-version": "v1",
                "Content-Type": "application/json",
                }
                response = requests.request("POST", url, headers=headers, data=payload, verify=cert)
                describe = str(response.text)
                taskjson = json.loads(describe)
                print("#" + str(count) + " Schedule Task name: " + taskjson['name'], flush=True)
                print("#" + str(count) + " Schedule ID: " + taskjson['ID'], flush=True)
            '''
            #print(str(response.text), flush=True)