import sys
import os
import time
from time import sleep
import requests
import urllib3
import json

cert = False

def DirListTenant2(alldirectory, url_link_final_2, tenant2key):
    alldirectorynew = []
    print("Creating list to tenant 2, if any", flush=True)
    if alldirectory:
        for count, dirlist in enumerate(alldirectory):
            rename = 1
            namecheck = 1
            oldjson = json.loads(dirlist)
            oldname = oldjson['name']
            while namecheck != -1:
                payload = dirlist
                url = url_link_final_2 + 'api/directorylists'
                headers = {
                "api-secret-key": tenant2key,
                "api-version": "v1",
                "Content-Type": "application/json",
                }
                response = requests.request("POST", url, headers=headers, data=payload, verify=cert)
                describe = str(response.text)
                idjson = json.loads(describe)
                if not 'message' in idjson:
                    print("#" + str(count) + " Directory List ID: " + str(idjson['ID']), flush=True)
                    alldirectorynew.append(str(idjson['ID']))
                    namecheck = -1
                else:
                    if 'name already exists' in idjson['message']:
                        oldjson['name'] = oldname + " {" + str(rename) + "}"
                        dirlist = json.dumps(oldjson)
                        rename = rename + 1
                    else:
                        print(describe, flush=True)
                        namecheck = -1
                '''
                index = describe.find('name already exists')
                if index != -1:
                    describe1 = alldirectory[count]
                    index = describe1.find('name')
                    if index != -1:
                        indexpart = describe1[index+5:]
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
                                        dirlist = describe1[:index+5+startIndex+startIndex2+1] + str(rename) + describe1[index+5+startIndex+startIndex2+endIndex2-2:]
                                        rename = rename + 1
                                else:
                                    newname = indexid + " {" + str(rename) + "}"
                                    dirlist = describe1[:index+5+startIndex+1] + newname + describe1[index+5+startIndex+endIndex-2:]
                                    rename = rename + 1
                index = describe.find('\"ID\"')
                if index != -1:
                    indexpart = describe[index+4:]
                    startIndex = indexpart.find(':')
                    if startIndex != -1: #i.e. if the first quote was found
                        endIndex = indexpart.find('}', startIndex + 1)
                        if startIndex != -1 and endIndex != -1: #i.e. both quotes were found
                            indexid = indexpart[startIndex+1:endIndex]
                            alldirectorynew.append(str(indexid))
                            namecheck = -1
                            '''
                
    print("new directory list", flush=True)
    print(alldirectorynew, flush=True)
    
    return alldirectorynew

def FileExtensionListTenant2(allfileextention, url_link_final_2, tenant2key):
    allfileextentionnew = []
    if allfileextention:
        for count, dirlist in enumerate(allfileextention):
            rename = 1
            namecheck = 1
            oldjson = json.loads(dirlist)
            oldname = oldjson['name']
            while namecheck != -1:
                payload = dirlist
                url = url_link_final_2 + 'api/fileextensionlists'
                headers = {
                "api-secret-key": tenant2key,
                "api-version": "v1",
                "Content-Type": "application/json",
                }
                response = requests.request("POST", url, headers=headers, data=payload, verify=cert)
                describe = str(response.text)
                idjson = json.loads(describe)
                if not 'message' in idjson:
                    print("#" + str(count) + " File Extension List ID: " + str(idjson['ID']), flush=True)
                    allfileextentionnew.append(str(idjson['ID']))
                    namecheck = -1
                else:
                    if 'name already exists' in idjson['message']:
                        oldjson['name'] = oldname + " {" + str(rename) + "}"
                        dirlist = json.dumps(oldjson)
                        rename = rename + 1
                    else:
                        print(describe, flush=True)
                        namecheck = -1
                '''
                index = describe.find('name already exists')
                if index != -1:
                    describe1 = allfileextention[count]
                    index = describe1.find('name')
                    if index != -1:
                        indexpart = describe1[index+5:]
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
                                        dirlist = describe1[:index+5+startIndex+startIndex2+1] + str(rename) + describe1[index+5+startIndex+startIndex2+endIndex2-2:]
                                        rename = rename + 1
                                else:
                                    newname = indexid + " {" + str(rename) + "}"
                                    dirlist = describe1[:index+5+startIndex+1] + newname + describe1[index+5+startIndex+endIndex-2:]
                                    rename = rename + 1
                index = describe.find('\"ID\"')
                if index != -1:
                    indexpart = describe[index+4:]
                    startIndex = indexpart.find(':')
                    if startIndex != -1: #i.e. if the first quote was found
                        endIndex = indexpart.find('}', startIndex + 1)
                        if startIndex != -1 and endIndex != -1: #i.e. both quotes were found
                            indexid = indexpart[startIndex+1:endIndex]
                            allfileextentionnew.append(str(indexid))  
                            namecheck = -1
                            '''
    print("new file extention", flush=True)
    print(allfileextentionnew, flush=True)
    return allfileextentionnew

def FileListTenant2(allfilelist, url_link_final_2, tenant2key):
    allfilelistnew = []
    if allfilelist:
        for count, dirlist in enumerate(allfilelist):
            rename = 1
            namecheck = 1
            oldjson = json.loads(dirlist)
            oldname = oldjson['name']
            while namecheck != -1:
                payload = dirlist
                url = url_link_final_2 + 'api/filelists'
                headers = {
                "api-secret-key": tenant2key,
                "api-version": "v1",
                "Content-Type": "application/json",
                }
                response = requests.request("POST", url, headers=headers, data=payload, verify=cert)
                describe = str(response.text)
                idjson = json.loads(describe)
                if not 'message' in idjson:
                    print("#" + str(count) + " File List ID: " + str(idjson['ID']), flush=True)
                    allfilelistnew.append(str(idjson['ID']))
                    namecheck = -1
                else:
                    if 'name already exists' in idjson['message']:
                        oldjson['name'] = oldname + " {" + str(rename) + "}"
                        dirlist = json.dumps(oldjson)
                        rename = rename + 1
                    else:
                        print(describe, flush=True)
                        namecheck = -1
                '''
                index = describe.find('name already exists')
                if index != -1:
                    describe1 = allfilelist[count]
                    index = describe1.find('name')
                    if index != -1:
                        indexpart = describe1[index+5:]
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
                                        dirlist = describe1[:index+5+startIndex+startIndex2+1] + str(rename) + describe1[index+5+startIndex+startIndex2+endIndex2-2:]
                                        rename = rename + 1
                                else:
                                    newname = indexid + " {" + str(rename) + "}"
                                    dirlist = describe1[:index+5+startIndex+1] + newname + describe1[index+5+startIndex+endIndex-2:]
                                    rename = rename + 1
                index = describe.find('\"ID\"')
                if index != -1:
                    indexpart = describe[index+4:]
                    startIndex = indexpart.find(':')
                    if startIndex != -1: #i.e. if the first quote was found
                        endIndex = indexpart.find('}', startIndex + 1)
                        if startIndex != -1 and endIndex != -1: #i.e. both quotes were found
                            indexid = indexpart[startIndex+1:endIndex]
                            allfilelistnew.append(str(indexid))
                            namecheck = -1
                            '''
    print("new file list", flush=True)
    print(allfilelistnew, flush=True) 
    return allfilelistnew
