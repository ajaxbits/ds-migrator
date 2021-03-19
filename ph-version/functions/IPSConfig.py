import sys
import os
import time
from time import sleep
import requests
import urllib3
import json

cert = False

def IPSGet(allofpolicy):
    ipsruleid = []
    print ("IPS rules in Tenant 1", flush=True)
    for describe in allofpolicy:
        namejson = json.loads(describe)
        if 'ruleIDs' in namejson['intrusionPrevention']: 
            for count, here2 in enumerate(namejson['intrusionPrevention']['ruleIDs']):
                ipsruleid.append(str(here2))
        '''
        index = describe.find('\"intrusionPrevention\"')
        if index != -1:
            indexpart = describe[index+20:]
            startIndex = indexpart.find('}')
            if startIndex != -1: #i.e. if the first quote was found
                endIndex = indexpart.find('}', startIndex + 1)
                if startIndex != -1 and endIndex != -1: #i.e. both quotes were found
                    indexid = indexpart[startIndex+1:endIndex]
                    index = indexid.find('ruleIDs')
                    if index != -1:
                        indexpart = indexid[index+9:]
                        startIndex = indexpart.find('[')
                        if startIndex != -1: #i.e. if the first quote was found
                            endIndex = indexpart.find(']', startIndex + 1)
                            if startIndex != -1 and endIndex != -1: #i.e. both quotes were found
                                indexid1 = indexpart[startIndex+1:endIndex]
                                indexid2 = indexid1.split(", ")
                                ipsruleid.extend(indexid2)
                                '''
    ipsruleid = list(dict.fromkeys(ipsruleid))
    print(ipsruleid, flush=True)
    return ipsruleid

def IPSDescribe(ipsruleid, ipsappid, allipsappidnew1, allipsappidnew2, allipsappidold, allipscustomapp, url_link_final, tenant1key, url_link_final_2, tenant2key):
    allipsrule = []
    allipsrulename = []
    allipsruleidnew1 = []
    allipsruleidold = []
    allipscustomrule = []
    print("Searching IPS rules in Tenant 1...", flush=True)  
    if ipsruleid:
        for count, dirlist in enumerate(ipsruleid):
            payload  = {}
            url = url_link_final + 'api/intrusionpreventionrules/' + str(dirlist)
            headers = {
                "api-secret-key": tenant1key,
                "api-version": "v1",
                "Content-Type": "application/json",
            }
            response = requests.request("GET", url, headers=headers, data=payload, verify=cert)
            describe = str(response.text)
            allipsrule.append(describe)
            ipsjson = json.loads(describe)
            allipsrulename.append(str(ipsjson['name']))
            print("#" + str(count) + " IPS rule name: " + str(ipsjson['name']), flush=True)
            '''
            index = describe.find('name')
            if index != -1:
                indexpart = describe[index+5:]
                startIndex = indexpart.find('\"')
                if startIndex != -1: #i.e. if the first quote was found
                    endIndex = indexpart.find('\"description\"', startIndex + 1)
                    if startIndex != -1 and endIndex != -1: #i.e. both quotes were found
                        indexid = indexpart[startIndex+1:endIndex-2]
                        allipsrulename.append(str(indexid))
                        print("#" + str(count) + " IPS rule name: " + str(indexid), flush=True)
                        '''
            
            index3 = describe.find('applicationTypeID')
            if index3 != -1:
                indexpart = describe[index3+17:]
                startIndex = indexpart.find(':')
                if startIndex != -1: #i.e. if the first quote was found
                    endIndex3 = indexpart.find(',', startIndex + 1)
                    if startIndex != -1 and endIndex3 != -1: #i.e. both quotes were found
                        indexid1 = indexpart[startIndex+1:endIndex3]
                        checkindex = ipsappid.index(indexid1)
                        if checkindex in allipsappidold:
                            checkindex1 = allipsappidold.index(checkindex)
                            replaceid = allipsappidnew1[checkindex1]
                        elif checkindex in allipscustomapp:
                            checkindex1 = allipscustomapp.index(checkindex)
                            replaceid = allipsappidnew2[checkindex1]
                        indexid5 = describe[index3:index3+17+endIndex3]
                        listpart = indexid5.replace(indexid1, replaceid)
                        allipsrule[count] = describe.replace(indexid5, listpart)
            print("#" + str(count) + " IPS rule ID: " + dirlist, flush=True)
    print("Done!", flush=True)
    print("Searching and Modifying IPS rule in Tenant 2...", flush=True)    
    for count, dirlist in enumerate(allipsrulename):
        payload = "{\"searchCriteria\": [{\"fieldName\": \"name\",\"stringValue\": \"" + dirlist + "\"}]}"
        url = url_link_final_2 + 'api/intrusionpreventionrules/search'
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
                        endIndex = indexpart.find(',', startIndex + 1)
                        if startIndex != -1 and endIndex != -1: #i.e. both quotes were found
                            indexid = indexpart[startIndex+1:endIndex]
                            allipsruleidnew1.append(str(indexid))
                            allipsruleidold.append(count)
                            print("#" + str(count) + " IPS rule ID: " + str(indexid), flush=True)
                        else:
                            endIndex = indexpart.find('}', startIndex + 1)
                            if startIndex != -1 and endIndex != -1: #i.e. both quotes were found
                                indexid = indexpart[startIndex+1:endIndex]
                                allipsruleidnew1.append(str(indexid))
                                allipsruleidold.append(count)
                                print("#" + str(count) + " IPS rule ID: " + str(indexid), flush=True)
                else:
                    print(describe, flush=True)
                    print(payload, flush=True)
            else:
                allipscustomrule.append(count)
        else:
            print(describe, flush=True)
            print(payload, flush=True)
    print("Done!", flush=True)
    #print("Tenant 2 default IPS rules", flush=True)
    #print(allipsruleidnew1, flush=True)
    return allipsrule, allipsruleidnew1, allipsruleidold, allipscustomrule

def IPSCustom(allipsrule, allipscustomrule, url_link_final_2, tenant2key):
    allipsruleidnew2 = []
    if allipscustomrule:
        print("Creating new custom IPS rule in Tenant 2...", flush=True)
        for count, indexnum in enumerate(allipscustomrule):
            payload = allipsrule[indexnum]
            url = url_link_final_2 + 'api/intrusionpreventionrules'
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
                    endIndex = indexpart.find(',', startIndex + 1)
                    if startIndex != -1 and endIndex != -1: #i.e. both quotes were found
                        indexid = indexpart[startIndex+1:endIndex]
                        allipsruleidnew2.append(str(indexid))
                        print("#" + str(count) + " IPS rule ID: " + str(indexid), flush=True)
                    else:
                        endIndex = indexpart.find('}', startIndex + 1)
                        if startIndex != -1 and endIndex != -1: #i.e. both quotes were found
                            indexid = indexpart[startIndex+1:endIndex]
                            allipsruleidnew2.append(str(indexid))
                            print("#" + str(count) + " IPS rule ID: " + str(indexid), flush=True)
            else:
                print(describe, flush=True)
                print(payload, flush=True)
        print("Done!", flush=True)
    #print("all new IPS rule custom rule", flush=True)
    #print(allipsruleidnew2, flush=True)
    return allipsruleidnew2

def IPSReplace(allofpolicy, allipsruleidnew1, allipsruleidnew2, ipsruleid, allipsruleidold, allipscustomrule):
    for count, describe in enumerate(allofpolicy):
        index = describe.find('\"intrusionPrevention\"')
        if index != -1:
            indexpart = describe[index+20:]
            startIndex = indexpart.find('}')
            if startIndex != -1: #i.e. if the first quote was found
                endIndex = indexpart.find('}', startIndex + 1)
                if startIndex != -1 and endIndex != -1: #i.e. both quotes were found
                    indexid = indexpart[startIndex+1:endIndex]
                    index2 = indexid.find('ruleIDs')
                    if index2 != -1:
                        indexpart2 = indexid[index2+9:]
                        startIndex2 = indexpart2.find('[')
                        if startIndex2 != -1: #i.e. if the first quote was found
                            endIndex2 = indexpart2.find(']', startIndex2 + 1)
                            if startIndex2 != -1 and endIndex2 != -1: #i.e. both quotes were found
                                indexid2 = indexpart2[startIndex2+1:endIndex2]
                                indexid3 = indexpart2[startIndex2+1:endIndex2]
                                indexid4 = indexid2.split(", ")
                                if allipsruleidnew1 or allipsruleidnew2:
                                    for count1, this in enumerate(indexid4):
                                        checkindex = ipsruleid.index(this)
                                        if checkindex in allipsruleidold:
                                            checkindex1 = allipsruleidold.index(checkindex)
                                            indexid4[count1] = allipsruleidnew1[checkindex1]
                                        elif checkindex in allipscustomrule:
                                            checkindex1 = allipscustomrule.index(checkindex)
                                            indexid4[count1] = allipsruleidnew2[checkindex1]
                                    indexid2 = ",".join(indexid4)
                                modulepart = describe[index:index+20+endIndex]
                                modulepart2 = modulepart.replace(indexid3, indexid2)
                                allofpolicy[count] = describe.replace(modulepart, modulepart2)
    return allofpolicy