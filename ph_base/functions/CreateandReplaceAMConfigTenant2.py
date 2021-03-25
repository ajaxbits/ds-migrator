import sys
import os
import time
from time import sleep
import requests
import urllib3
import json

cert = False

def AmconfigTenant2(allamconfig, url_link_final_2, tenant2key):
    allamconfignew = []
    print("Creating Anti-Malware Configuration to Tenant2", flush=True)
    if allamconfig:
        for count, dirlist in enumerate(allamconfig):
            rename = 1
            namecheck = 1
            if dirlist != 0:
                oldjson = json.loads(dirlist)
                oldname = oldjson['name']
                while namecheck != -1:
                    payload = dirlist
                    url = url_link_final_2 + 'api/antimalwareconfigurations'
                    headers = {
                    "api-secret-key": tenant2key,
                    "api-version": "v1",
                    "Content-Type": "application/json",
                    }
                    response = requests.request("POST", url, headers=headers, data=payload, verify=cert)
                    describe = str(response.text)
                    amjson = json.loads(describe)
                    if not 'message' in amjson:
                        print("#" + str(count) + " Anti-Malware Config name: " + amjson['name'], flush=True)
                        print("#" + str(count) + " Anti-Malware Config ID: " + str(amjson['ID']), flush=True)
                        allamconfignew.append(str(amjson['ID']))
                        namecheck = -1
                    else:
                        if 'name already exists' in amjson['message']:
                            oldjson['name'] = oldname + " {" + str(rename) + "}"
                            dirlist = json.dumps(oldjson)
                            rename = rename + 1
                        else:
                            print(describe, flush=True)
                            namecheck = -1
                    '''
                    index = describe.find('name already exists')
                    if index != -1:
                        describe1 = allamconfig[count]
                        index = describe1.find('name')
                        if index != -1:
                            indexpart = describe1[index+5:]
                            startIndex = indexpart.find('\"')
                            if startIndex != -1: #i.e. if the first quote was found
                                endIndex = indexpart.find(',', startIndex + 1)
                                if startIndex != -1 and endIndex != -1: #i.e. both quotes were found
                                    indexid = indexpart[startIndex+1:endIndex-1]
                                    startIndex2 = indexid.find('(')
                                    if startIndex2 != -1:
                                        endIndex2 = indexid.find(')', startIndex2 + 1)
                                        if startIndex2 != -1 and endIndex2 != -1: #i.e. both quotes were found
                                            indexid = indexid[startIndex2+1:endIndex2]
                                            dirlist = describe1[:index+5+startIndex+startIndex2+1] + str(rename) + describe1[index+5+startIndex+startIndex2+endIndex2-2:]
                                            rename = rename + 1
                                    else:
                                        newname = indexid + " (" + str(rename) + ")"
                                        dirlist = describe1[:index+5+startIndex+1] + newname + describe1[index+5+startIndex+endIndex-2:]
                                        rename = rename + 1
                    index = describe.find('\"ID\"')
                    if index != -1:
                        indexpart = describe[index+4:]
                        startIndex = indexpart.find(':')
                        if startIndex != -1: #i.e. if the first quote was found
                            endIndex = indexpart.find(',', startIndex + 1)
                            if startIndex != -1 and endIndex != -1: #i.e. both quotes were found
                                indexid = indexpart[startIndex+1:endIndex]
                                allamconfignew.append(str(indexid))
                                namecheck = -1
                            else:   
                                endIndex = indexpart.find('}', startIndex + 1)
                                if startIndex != -1 and endIndex != -1: #i.e. both quotes were found
                                    indexid = indexpart[startIndex+1:endIndex]
                                    allamconfignew.append(str(indexid))   
                                    namecheck = -1
                                    '''
    print("New AM Config ID", flush=True)
    print(allamconfignew, flush=True)
    return allamconfignew

def AmReplaceConfig(allofpolicy, antimalwareconfig, allamconfignew):
    count = 0
    for describe in allofpolicy:
        count1 = 0
        index = describe.find('realTimeScanConfigurationID')
        if index != -1:
            indexpart = describe[index+28:]
            startIndex = indexpart.find(':')
            if startIndex != -1: #i.e. if the first quote was found
                endIndex = indexpart.find(',', startIndex + 1)
                if startIndex != -1 and endIndex != -1: #i.e. both quotes were found
                    indexid = indexpart[startIndex+1:endIndex]
                    for dirlist in antimalwareconfig:
                        if int(dirlist) != 0:
                            if indexid == dirlist:
                                describe = describe[:index+28+startIndex+1] + allamconfignew[count1] + describe[index+28+startIndex+endIndex:]
                            count1 = count1 + 1    
        count1 = 0
        index = describe.find('manualScanConfigurationID')
        if index != -1:
            indexpart = describe[index+26:]
            startIndex = indexpart.find(':')
            if startIndex != -1: #i.e. if the first quote was found
                endIndex = indexpart.find(',', startIndex + 1)
                if startIndex != -1 and endIndex != -1: #i.e. both quotes were found
                    indexid = indexpart[startIndex+1:endIndex]
                    for dirlist in antimalwareconfig:
                        if int(dirlist) != 0:
                            if indexid == dirlist:
                                describe = describe[:index+26+startIndex+1] + allamconfignew[count1] + describe[index+26+startIndex+endIndex:]
                            count1 = count1 + 1          
        count1 = 0
        index = describe.find('scheduledScanConfigurationID')
        if index != -1:
            indexpart = describe[index+29:]
            startIndex = indexpart.find(':')
            if startIndex != -1: #i.e. if the first quote was found
                endIndex = indexpart.find('}', startIndex + 1)
                if startIndex != -1 and endIndex != -1: #i.e. both quotes were found
                    indexid = indexpart[startIndex+1:endIndex]
                    for dirlist in antimalwareconfig:
                        if int(dirlist) != 0:
                            if indexid == dirlist:
                                describe = describe[:index+29+startIndex+1] + allamconfignew[count1] + describe[index+29+startIndex+endIndex:]
                            count1 = count1 + 1

        allofpolicy[count] = describe
        count = count + 1
    return allofpolicy