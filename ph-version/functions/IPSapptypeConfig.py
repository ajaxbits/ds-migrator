import sys
import os
import time
from time import sleep
import requests
import urllib3
import json

cert = False

def IPSappGet(allofpolicy):
    ipsappid = []
    print ("IPS application types in Tenant 1", flush=True)
    for describe in allofpolicy:
        namejson = json.loads(describe)
        if 'applicationTypeIDs' in namejson['intrusionPrevention']: 
            for count, here2 in enumerate(namejson['intrusionPrevention']['applicationTypeIDs']):
                ipsappid.append(str(here2))
        '''
        index = describe.find('\"intrusionPrevention\"')
        if index != -1:
            indexpart = describe[index+20:]
            startIndex = indexpart.find('}')
            if startIndex != -1: #i.e. if the first quote was found
                endIndex = indexpart.find('}', startIndex + 1)
                if startIndex != -1 and endIndex != -1: #i.e. both quotes were found
                    indexid = indexpart[startIndex+1:endIndex]
                    index = indexid.find('applicationTypeIDs')
                    if index != -1:
                        indexpart = indexid[index+18:]
                        startIndex = indexpart.find('[')
                        if startIndex != -1: #i.e. if the first quote was found
                            endIndex = indexpart.find(']', startIndex + 1)
                            if startIndex != -1 and endIndex != -1: #i.e. both quotes were found
                                indexid1 = indexpart[startIndex+1:endIndex]
                                indexid2 = indexid1.split(", ")
                                ipsappid.extend(indexid2)
                                '''
    ipsappid = list(dict.fromkeys(ipsappid))
    print(ipsappid, flush=True)
    return ipsappid

def IPSappDescribe(ipsappid, t1portlistid, t2portlistid, url_link_final, tenant1key, url_link_final_2, tenant2key):
    allipsapp = []
    allipsappname = []
    allipsappidnew1 = []
    allipsappidold = []
    allipscustomapp = []
    print("Searching IPS application types in Tenant 1...", flush=True)  
    if ipsappid:
        for count, dirlist in enumerate(ipsappid):
            payload  = {}
            url = url_link_final + 'api/applicationtypes/' + str(dirlist)
            headers = {
                "api-secret-key": tenant1key,
                "api-version": "v1",
                "Content-Type": "application/json",
            }
            response = requests.request("GET", url, headers=headers, data=payload, verify=cert)
            describe = str(response.text)
            allipsapp.append(describe)
            ipsappjson = json.loads(describe)
            allipsappname.append(str(ipsappjson['name']))
            print("#" + str(count) + " IPS Application Type name: " + str(ipsappjson['name']), flush=True)
            '''
            index = describe.find('name')
            if index != -1:
                indexpart = describe[index+5:]
                startIndex = indexpart.find('\"')
                if startIndex != -1: #i.e. if the first quote was found
                    endIndex = indexpart.find(',', startIndex + 1)
                    if startIndex != -1 and endIndex != -1: #i.e. both quotes were found
                        indexid = indexpart[startIndex+1:endIndex-1]
                        allipsappname.append(str(indexid))
                        print("#" + str(count) + " IPS Application Type name: " + str(indexid), flush=True)
                        '''
            index3 = describe.find('portListID')
            if index3 != -1:
                indexpart = describe[index3+10:]
                startIndex = indexpart.find(':')
                if startIndex != -1: #i.e. if the first quote was found
                    endIndex3 = indexpart.find(',', startIndex + 1)
                    if startIndex != -1 and endIndex3 != -1: #i.e. both quotes were found
                        indexid1 = indexpart[startIndex+1:endIndex3]
                        indexid5 = describe[index3:index3+10+endIndex3]
                        indexnum = t1portlistid.index(indexid1)
                        listpart = indexid5.replace(indexid1, t2portlistid[indexnum])
                        allipsapp[count] = describe.replace(indexid5, listpart)
            print("#" + str(count) + " IPS Application Type ID: " + dirlist, flush=True)
    print("Done!", flush=True)
    print("Searching and Modifying IPS application types in Tenant 2...", flush=True)       
    for count, dirlist in enumerate(allipsappname):
        payload = "{\"searchCriteria\": [{\"fieldName\": \"name\",\"stringValue\": \"" + dirlist + "\"}]}"
        url = url_link_final_2 + 'api/applicationtypes/search'
        headers = {
        "api-secret-key": tenant2key,
        "api-version": "v1",
        "Content-Type": "application/json",
        }
        response = requests.request("POST", url, headers=headers, data=payload, verify=cert)
        describe = str(response.text)
        taskjson = json.loads(describe)
        if not 'message' in taskjson:
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
                            allipsappidnew1.append(str(indexid))
                            allipsappidold.append(count)
                            payload = allipsapp[count]
                            url = url_link_final_2 + 'api/applicationtypes/' + str(indexid)
                            headers = {
                            "api-secret-key": tenant2key,
                            "api-version": "v1",
                            "Content-Type": "application/json",
                            }
                            response = requests.request("POST", url, headers=headers, data=payload, verify=cert)
                            print("#" + str(count) + " IPS Application Type ID: " + indexid, flush=True)
                else:
                    print(describe, flush=True)
                    print(payload, flush=True)
            else:
                allipscustomapp.append(count)
        else:
            print(describe, flush=True)
            print(payload, flush=True)
    print("Done!", flush=True)
    #print("Tenant 2 default IPS application type", flush=True)
    #print(allipsappidnew1, flush=True)
    return allipsapp, allipsappidnew1, allipsappidold, allipscustomapp

def IPSappCustom(allipsapp, allipscustomapp, url_link_final_2, tenant2key):
    allipsappidnew2 = []
    if allipscustomapp:
        print("Creating IPS application Type Custom Rule...", flush=True)
        for count, indexnum in enumerate(allipscustomapp):
            payload = allipsapp[indexnum]
            url = url_link_final_2 + 'api/applicationtypes'
            headers = {
            "api-secret-key": tenant2key,
            "api-version": "v1",
            "Content-Type": "application/json",
            }
            response = requests.request("POST", url, headers=headers, data=payload, verify=cert)
            describe = str(response.text)
            index = describe.find('\"ID\"')
            if index != -1:
                indexpart = describe[index+4:]
                startIndex = indexpart.find(':')
                if startIndex != -1: #i.e. if the first quote was found
                    endIndex = indexpart.find('}', startIndex + 1)
                    if startIndex != -1 and endIndex != -1: #i.e. both quotes were found
                        indexid = indexpart[startIndex+1:endIndex]
                        allipsappidnew2.append(str(indexid))
                        print("#" + str(count) + " IPS Application Type ID: " + str(indexid), flush=True)
            else:
                print(describe, flush=True)
                print(payload, flush=True)
        print("Done!", flush=True)
    #print("all new IPS custom application", flush=True)
    #print(allipsappidnew2, flush=True)
    return allipsappidnew2

def IPSappReplace(allofpolicy, allipsappidnew1, allipsappidnew2, ipsappid, allipsappidold, allipscustomapp):
    for count, describe in enumerate(allofpolicy):
        taskjson = json.loads(describe)
        if 'applicationTypeIDs' in taskjson['intrusionPrevention']:
            if allipsappidnew1 or allipsappidnew2:
                for count1, this in enumerate(taskjson['intrusionPrevention']['applicationTypeIDs']):
                    checkindex = ipsappid.index(str(this))
                    if checkindex in allipsappidold:
                        checkindex1 = allipsappidold.index(checkindex)
                        taskjson['intrusionPrevention']['applicationTypeIDs'][count1] = allipsappidnew1[checkindex1]
                    elif checkindex in allipscustomapp:
                        checkindex1 = allipscustomapp.index(checkindex)
                        taskjson['intrusionPrevention']['applicationTypeIDs'][count1] = allipsappidnew2[checkindex1]
        allofpolicy[count] = json.dumps(taskjson)
        
        '''
        index = describe.find('\"intrusionPrevention\"')
        if index != -1:
            indexpart = describe[index+20:]
            startIndex = indexpart.find('}')
            if startIndex != -1: #i.e. if the first quote was found
                endIndex = indexpart.find('}', startIndex + 1)
                if startIndex != -1 and endIndex != -1: #i.e. both quotes were found
                    indexid = indexpart[startIndex+1:endIndex]
                    index2 = indexid.find('applicationTypeIDs')
                    if index2 != -1:
                        indexpart2 = indexid[index2+9:]
                        startIndex2 = indexpart2.find('[')
                        if startIndex2 != -1: #i.e. if the first quote was found
                            endIndex2 = indexpart2.find(']', startIndex2 + 1)
                            if startIndex2 != -1 and endIndex2 != -1: #i.e. both quotes were found
                                indexid2 = indexpart2[startIndex2+1:endIndex2]
                                indexid3 = indexpart2[startIndex2+1:endIndex2]
                                indexid4 = indexid2.split(", ")
                                if allipsappidnew1 or allipsappidnew2:
                                    for count1, this in enumerate(indexid4):
                                        checkindex = ipsappid.index(this)
                                        if checkindex in allipsappidold:
                                            checkindex1 = allipsappidold.index(checkindex)
                                            indexid4[count1] = allipsappidnew1[checkindex1]
                                        elif checkindex in allipscustomapp:
                                            checkindex1 = allipscustomapp.index(checkindex)
                                            indexid4[count1] = allipsappidnew2[checkindex1]
                                    indexid2 = ",".join(indexid4)
                                modulepart = describe[index:index+20+endIndex]
                                modulepart2 = modulepart.replace(indexid3, indexid2)
                                allofpolicy[count] = describe.replace(modulepart, modulepart2)
                                '''
    return allofpolicy
