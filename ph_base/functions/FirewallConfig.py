import sys
import os
import time
from time import sleep
import requests
import urllib3
import json

cert = False

def FirewallGet(allofpolicy):
    firewallruleid = []
    policystateful = []
#find all Firewall rules
    print ("Firewall rules in Tenant 1", flush=True)
    for describe in allofpolicy:
        namejson = json.loads(describe)
        if 'globalStatefulConfigurationID' in namejson['firewall']:   
            policystateful.append(str(namejson['firewall']['globalStatefulConfigurationID']))
        if 'ruleIDs' in namejson['firewall']: 
            for count, here2 in enumerate(namejson['firewall']['ruleIDs']):
                firewallruleid.append(str(here2))
        '''
        index = describe.find('\"firewall\"')
        if index != -1:
            indexpart = describe[index+9:]
            startIndex = indexpart.find('}')
            if startIndex != -1: #i.e. if the first quote was found
                endIndex = indexpart.find('}', startIndex + 1)
                if startIndex != -1 and endIndex != -1: #i.e. both quotes were found
                    indexid = indexpart[startIndex+1:endIndex]
                    index = indexid.find('globalStatefulConfigurationID')
                    if index != -1:
                        indexpart = indexid[index+29:]
                        startIndex = indexpart.find(':')
                        if startIndex != -1: #i.e. if the first quote was found
                            endIndex = indexpart.find(',', startIndex + 1)
                            if startIndex != -1 and endIndex != -1: #i.e. both quotes were found
                                indexid1 = indexpart[startIndex+1:endIndex]
                                policystateful.append(str(indexid1))
                    index = indexid.find('ruleIDs')
                    if index != -1:
                        indexpart = indexid[index+9:]
                        startIndex = indexpart.find('[')
                        if startIndex != -1: #i.e. if the first quote was found
                            endIndex = indexpart.find(']', startIndex + 1)
                            if startIndex != -1 and endIndex != -1: #i.e. both quotes were found
                                indexid1 = indexpart[startIndex+1:endIndex]
                                indexid2 = indexid1.split(",")
                                firewallruleid.extend(indexid2)
                                '''
    firewallruleid = list(dict.fromkeys(firewallruleid))
    print(firewallruleid, flush=True)
    return firewallruleid, policystateful

def FirewallDescribe(firewallruleid, t1iplistid, t2iplistid, t1maclistid, t2maclistid, t1portlistid, t2portlistid, url_link_final, tenant1key, url_link_final_2, tenant2key):
    allfirewallrule = []
    allfirewallrulename = []
    allfirewallruleidnew1 = []
    allfirewallruleidold = []
    allfirewallcustomrule = []
#describe Firewall rules
    print("Searching and Modifying Firewall rules in Tenant 1...", flush=True)
    if firewallruleid:
        for count, dirlist in enumerate(firewallruleid):
            payload  = {}
            url = url_link_final + 'api/firewallrules/' + str(dirlist)
            headers = {
                "api-secret-key": tenant1key,
                "api-version": "v1",
                "Content-Type": "application/json",
            }
            response = requests.request("GET", url, headers=headers, data=payload, verify=cert)
            describe = str(response.text)
            allfirewallrule.append(describe)
            firewalljson = json.loads(describe)
            allfirewallrulename.append(str(firewalljson['name']))
            print("#" + str(count) + " Firewall rule name: " + str(firewalljson['name']), flush=True)
            '''
            index = describe.find('name')
            if index != -1:
                indexpart = describe[index+5:]
                startIndex = indexpart.find('\"')
                if startIndex != -1: #i.e. if the first quote was found
                    endIndex = indexpart.find(',', startIndex + 1)
                    if startIndex != -1 and endIndex != -1: #i.e. both quotes were found
                        indexid = indexpart[startIndex+1:endIndex-1]
                        allfirewallrulename.append(str(indexid))
                        print("#" + str(count) + " Firewall rule name: " + str(indexid), flush=True)
                        '''
            print("#" + str(count) + " Firewall rule ID: " + dirlist, flush=True)
    print("Done!", flush=True)
    print("Replacing firewall rule IDs configuration in tenant 2...", flush=True)
    for count, describe in enumerate(allfirewallrule):
        index3 = describe.find('sourceIPListID')
        if index3 != -1:
            indexpart = describe[index3+14:]
            startIndex = indexpart.find(':')
            if startIndex != -1: #i.e. if the first quote was found
                endIndex3 = indexpart.find(',', startIndex + 1)
                if startIndex != -1 and endIndex3 != -1: #i.e. both quotes were found
                    indexid1 = indexpart[startIndex+1:endIndex3]
                    indexid5 = describe[index3:index3+14+endIndex3]
                    indexnum = t1iplistid.index(indexid1)
                    listpart = indexid5.replace(indexid1, t2iplistid[indexnum])
                    describe = describe.replace(indexid5, listpart)
        index3 = describe.find('sourceMACListID')
        if index3 != -1:
            indexpart = describe[index3+15:]
            startIndex = indexpart.find(':')
            if startIndex != -1: #i.e. if the first quote was found
                endIndex3 = indexpart.find(',', startIndex + 1)
                if startIndex != -1 and endIndex3 != -1: #i.e. both quotes were found
                    indexid1 = indexpart[startIndex+1:endIndex3]
                    indexid5 = describe[index3:index3+15+endIndex3]
                    indexnum = t1maclistid.index(indexid1)
                    listpart = indexid5.replace(indexid1, t2maclistid[indexnum])
                    describe = describe.replace(indexid5, listpart)
        index3 = describe.find('sourcePortListID')
        if index3 != -1:
            indexpart = describe[index3+16:]
            startIndex = indexpart.find(':')
            if startIndex != -1: #i.e. if the first quote was found
                endIndex3 = indexpart.find(',', startIndex + 1)
                if startIndex != -1 and endIndex3 != -1: #i.e. both quotes were found
                    indexid1 = indexpart[startIndex+1:endIndex3]
                    indexid5 = describe[index3:index3+16+endIndex3]
                    indexnum = t1portlistid.index(indexid1)
                    listpart = indexid5.replace(indexid1, t2portlistid[indexnum])
                    describe = describe.replace(indexid5, listpart)
        index3 = describe.find('destinationIPListID')
        if index3 != -1:
            indexpart = describe[index3+19:]
            startIndex = indexpart.find(':')
            if startIndex != -1: #i.e. if the first quote was found
                endIndex3 = indexpart.find(',', startIndex + 1)
                if startIndex != -1 and endIndex3 != -1: #i.e. both quotes were found
                    indexid1 = indexpart[startIndex+1:endIndex3]
                    indexid5 = describe[index3:index3+19+endIndex3]
                    indexnum = t1iplistid.index(indexid1)
                    listpart = indexid5.replace(indexid1, t2iplistid[indexnum])
                    describe = describe.replace(indexid5, listpart)
        index3 = describe.find('destinationMACListID')
        if index3 != -1:
            indexpart = describe[index3+20:]
            startIndex = indexpart.find(':')
            if startIndex != -1: #i.e. if the first quote was found
                endIndex3 = indexpart.find(',', startIndex + 1)
                if startIndex != -1 and endIndex3 != -1: #i.e. both quotes were found
                    indexid1 = indexpart[startIndex+1:endIndex3]
                    indexid5 = describe[index3:index3+20+endIndex3]
                    indexnum = t1maclistid.index(indexid1)
                    listpart = indexid5.replace(indexid1, t2maclistid[indexnum])
                    describe = describe.replace(indexid5, listpart)
        index3 = describe.find('destinationPortListID')
        if index3 != -1:
            indexpart = describe[index3+21:]
            startIndex = indexpart.find(':')
            if startIndex != -1: #i.e. if the first quote was found
                endIndex3 = indexpart.find(',', startIndex + 1)
                if startIndex != -1 and endIndex3 != -1: #i.e. both quotes were found
                    indexid1 = indexpart[startIndex+1:endIndex3]
                    indexid5 = describe[index3:index3+21+endIndex3]
                    indexnum = t1portlistid.index(indexid1)
                    listpart = indexid5.replace(indexid1, t2portlistid[indexnum])
                    describe = describe.replace(indexid5, listpart)
        allfirewallrule[count] = describe
    for count, dirlist in enumerate(allfirewallrulename):
        payload = "{\"searchCriteria\": [{\"fieldName\": \"name\",\"stringValue\": \"" + dirlist + "\"}]}"
        url = url_link_final_2 + 'api/firewallrules/search'
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
                            allfirewallruleidnew1.append(str(indexid))
                            allfirewallruleidold.append(count)

                            payload = allfirewallrule[count]
                            url = url_link_final_2 + 'api/firewallrules/' + str(indexid)
                            headers = {
                            "api-secret-key": tenant2key,
                            "api-version": "v1",
                            "Content-Type": "application/json",
                            }
                            response = requests.request("POST", url, headers=headers, data=payload, verify=cert)
                            print("#" + str(count) + " Firewall rule ID: " + indexid, flush=True)
                        else:
                            endIndex = indexpart.find('}', startIndex + 1)
                            if startIndex != -1 and endIndex != -1: #i.e. both quotes were found
                                indexid = indexpart[startIndex+1:endIndex]
                                allfirewallruleidnew1.append(str(indexid))
                                allfirewallruleidold.append(count) 

                                payload = allfirewallrule[count]
                                url = url_link_final_2 + 'api/firewallrules/' + str(indexid)
                                headers = {
                                "api-secret-key": tenant2key,
                                "api-version": "v1",
                                "Content-Type": "application/json",
                                }
                                response = requests.request("POST", url, headers=headers, data=payload, verify=cert)
                                print("#" + str(count) + " Firewall rule ID: " + indexid, flush=True)
                else:
                    print(describe, flush=True)
                    print(payload, flush=True)
            else:
                allfirewallcustomrule.append(count)
        else:
            print(describe, flush=True)
            print(payload, flush=True)
    #print("Tenant 2 default firewall rules")
    #print(allfirewallruleidnew1)
    print("Done!", flush=True)
    return allfirewallrule, allfirewallruleidnew1, allfirewallruleidold, allfirewallcustomrule

def FirewallCustom(allfirewallrule, allfirewallcustomrule, url_link_final_2, tenant2key):
    allfirewallruleidnew2 = []
    if allfirewallcustomrule:
        print("Creating Firewall Custom Rule...", flush=True)
        for count, indexnum in enumerate(allfirewallcustomrule):
            payload = allfirewallrule[indexnum]
            url = url_link_final_2 + 'api/firewallrules'
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
                        allfirewallruleidnew2.append(str(indexid))
                        print("#" + str(count) + " Firewall rule ID: " + indexid, flush=True)
                    else:
                        endIndex = indexpart.find('}', startIndex + 1)
                        if startIndex != -1 and endIndex != -1: #i.e. both quotes were found
                            indexid = indexpart[startIndex+1:endIndex]
                            allfirewallruleidnew2.append(str(indexid))
                            print("#" + str(count) + " Firewall rule ID: " + indexid, flush=True)
            else:
                print(describe, flush=True)
                print(payload, flush=True)
        print("Done!", flush=True)
    #print("all new firewall rule custom rule")
    #print(allfirewallruleidnew2)
    return allfirewallruleidnew2

def FirewallReplace(allofpolicy, allfirewallruleidnew1, allfirewallruleidnew2, firewallruleid, allfirewallruleidold, allfirewallcustomrule, t1statefulid, t2statefulid):
    if allofpolicy:
        for count, describe in enumerate(allofpolicy):
            taskjson = json.loads(describe)
            indexid = taskjson['firewall']
            if 'globalStatefulConfigurationID' in taskjson['firewall']:
                indexnum = t1statefulid.index(str(taskjson['firewall']['globalStatefulConfigurationID']))
                taskjson['firewall']['globalStatefulConfigurationID'] = t2statefulid[indexnum]
            if 'ruleIDs' in taskjson['firewall']:
                if allfirewallruleidnew1 or allfirewallruleidnew2:
                    for count1, this in enumerate(taskjson['firewall']['ruleIDs']):
                        checkindex = firewallruleid.index(str(this))
                        if checkindex in allfirewallruleidold:
                            checkindex1 = allfirewallruleidold.index(checkindex)
                            taskjson['firewall']['ruleIDs'][count1] = allfirewallruleidnew1[checkindex1]
                        elif checkindex in allfirewallcustomrule:
                            checkindex1 = allfirewallcustomrule.index(checkindex)
                            taskjson['firewall']['ruleIDs'][count1] = allfirewallruleidnew2[checkindex1]
            allofpolicy[count] = json.dumps(taskjson)
            '''
            index = describe.find('\"firewall\"')
            if index != -1:
                indexpart = describe[index+9:]
                startIndex = indexpart.find('}')
                if startIndex != -1: #i.e. if the first quote was found
                    endIndex = indexpart.find('}', startIndex + 1)
                    if startIndex != -1 and endIndex != -1: #i.e. both quotes were found
                        indexid = indexpart[startIndex+1:endIndex]
                        index3 = indexid.find('globalStatefulConfigurationID')
                        if index3 != -1:
                            indexpart = indexid[index3+29:]
                            startIndex = indexpart.find(':')
                            if startIndex != -1: #i.e. if the first quote was found
                                endIndex3 = indexpart.find(',', startIndex + 1)
                                if startIndex != -1 and endIndex3 != -1: #i.e. both quotes were found
                                    indexid1 = indexpart[startIndex+1:endIndex3]
                                    indexid5 = indexid[index3:index3+29+endIndex3]
                                    indexnum = t1statefulid.index(indexid1)
                                    statefulpart = indexid5.replace(indexid1, t2statefulid[indexnum])
                                    describe = describe.replace(indexid5, statefulpart)
                        index2 = indexid.find('ruleIDs')
                        if index2 != -1:
                            indexpart2 = indexid[index2+9:]
                            startIndex2 = indexpart2.find('[')
                            if startIndex2 != -1: #i.e. if the first quote was found
                                endIndex2 = indexpart2.find(']', startIndex2 + 1)
                                if startIndex2 != -1 and endIndex2 != -1: #i.e. both quotes were found
                                    indexid2 = indexpart2[startIndex2+1:endIndex2]
                                    indexid3 = indexpart2[startIndex2+1:endIndex2]
                                    indexid4 = indexid2.split(",")
                                    if allfirewallruleidnew1 or allfirewallruleidnew2:
                                        for count1, this in enumerate(indexid4):
                                            checkindex = firewallruleid.index(this)
                                            if checkindex in allfirewallruleidold:
                                                checkindex1 = allfirewallruleidold.index(checkindex)
                                                indexid4[count1] = allfirewallruleidnew1[checkindex1]
                                            elif checkindex in allfirewallcustomrule:
                                                checkindex1 = allfirewallcustomrule.index(checkindex)
                                                indexid4[count1] = allfirewallruleidnew2[checkindex1]
                                        indexid2 = ",".join(indexid4)
                                    modulepart = describe[index:index+9+endIndex]
                                    modulepart2 = modulepart.replace(indexid3, indexid2)
                                    allofpolicy[count] = describe.replace(modulepart, modulepart2)
                                    '''
    return allofpolicy