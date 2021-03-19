import sys
import os
import time
from time import sleep
import requests
import urllib3
import json

cert = False

def AddPolicy(allofpolicy, url_link_final_2, tenant2key):
    print ("Creating Policy to Tenant 2 with new ID", flush=True)  
    for count, dirlist in enumerate(allofpolicy):
        rename = 1
        namecheck = 1
        oldpolicyjson = json.loads(dirlist)
        oldname = oldpolicyjson['name']
        while namecheck != -1:
            payload = dirlist
            url = url_link_final_2 + 'api/policies'
            headers = {
            "api-secret-key": tenant2key,
            "api-version": "v1",
            "Content-Type": "application/json",
            }
            response = requests.request("POST", url, headers=headers, data=payload, verify=cert)
            describe = str(response.text)
            policyjson = json.loads(describe)
            if not 'message' in policyjson:
                print("#" + str(count) + " Policy name: " + policyjson['name'], flush=True)
                print("#" + str(count) + " Policy ID: " + str(policyjson['ID']), flush=True)
                namecheck = -1
            else:
                if 'name already exists' in policyjson['message']:
                    oldpolicyjson['name'] = oldname + " {" + str(rename) + "}"
                    dirlist = json.dumps(oldpolicyjson)
                    rename = rename + 1
                else:
                    print(describe, flush=True)
                    namecheck = -1
'''
            index = describe.find('\"ID\"')
            if index != -1:
                indexpart = describe[index+4:]
                startIndex = indexpart.find(':')
                if startIndex != -1: #i.e. if the first quote was found
                    endIndex = indexpart.find(',', startIndex + 1)
                    if startIndex != -1 and endIndex != -1: #i.e. both quotes were found
                        indexid = indexpart[startIndex+1:endIndex]
                        print(indexid, flush=True)
                        namecheck = -1
                    else:
                        endIndex = indexpart.find('}', startIndex + 1)
                        if startIndex != -1 and endIndex != -1: #i.e. both quotes were found
                            indexid = indexpart[startIndex+1:endIndex]
                            print(indexid, flush=True)
                            namecheck = -1
            if namecheck != -1:
                index = describe.find('name already exists')
                if index != -1:
                    describe1 = allofpolicy[count]
                    index = describe1.find('\"name\"')
                    if index != -1:
                        indexpart = describe1[index+6:]
                        startIndex = indexpart.find('\"')
                        if startIndex != -1: #i.e. if the first quote was found
                            endIndex = indexpart.find(',', startIndex + 1)
                            if startIndex != -1 and endIndex != -1: #i.e. both quotes were found
                                indexid = indexpart[startIndex+1:endIndex-1]
                                startIndex2 = indexid.find('{')
                                if startIndex2 != -1:
                                    endIndex2 = indexid.find('}', startIndex2 + 1)
                                    if startIndex2 != -1 and endIndex2 != -1: #i.e. both quotes were found
                                        indexid = indexid[startIndex2+1:endIndex2]
                                        dirlist = describe1[:index+6+startIndex+startIndex2+1] + str(rename) + describe1[index+6+startIndex+startIndex2+endIndex2-2:]
                                        rename = rename + 1                      
                                else:
                                    newname = indexid + " {" + str(rename) + "}"
                                    dirlist = describe1[:index+6+startIndex+1] + newname + describe1[index+6+startIndex+endIndex-2:]
                                    rename = rename + 1   
            else:
                    print(describe, flush=True)
                    namecheck = -1
                    '''
                