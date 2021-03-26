import sys
import os
import time
from time import sleep
import requests
import urllib3
import json

def ProxyEdit(allofpolicy, t1iplistid, t2iplistid, t1portlistid, t2portlistid):
    if allofpolicy:
        for count, describe in enumerate(allofpolicy):
            policyjson = json.loads(describe)
            if 'true' in policyjson['policySettings']['antiMalwareSettingSmartProtectionGlobalServerUseProxyEnabled']['value']:
                policyjson['policySettings']['antiMalwareSettingSmartProtectionGlobalServerUseProxyEnabled']['value'] = 'false'

            if 'true' in policyjson['policySettings']['webReputationSettingSmartProtectionGlobalServerUseProxyEnabled']['value']:
                policyjson['policySettings']['webReputationSettingSmartProtectionGlobalServerUseProxyEnabled']['value'] = 'false'

            if 'true' in policyjson['policySettings']['platformSettingSmartProtectionGlobalServerUseProxyEnabled']['value']:
                policyjson['policySettings']['platformSettingSmartProtectionGlobalServerUseProxyEnabled']['value'] = 'false'

            policyjson['policySettings']['platformSettingSmartProtectionAntiMalwareGlobalServerProxyId']['value'] = ''
            policyjson['policySettings']['webReputationSettingSmartProtectionWebReputationGlobalServerProxyId']['value'] = ''
            policyjson['policySettings']['platformSettingSmartProtectionGlobalServerProxyId']['value'] = ''

            here = policyjson['policySettings']['firewallSettingReconnaissanceExcludeIpListId']['value']
            if here:
                if here != 'NONE':
                    indexnum = t1iplistid.index(here)
                    policyjson['policySettings']['firewallSettingReconnaissanceExcludeIpListId']['value'] = t2iplistid[indexnum]

            here = policyjson['policySettings']['firewallSettingReconnaissanceIncludeIpListId']['value']
            if here:
                if here != 'NONE':
                    indexnum = t1iplistid.index(here)
                    policyjson['policySettings']['firewallSettingReconnaissanceIncludeIpListId']['value'] = t2iplistid[indexnum]

            here = policyjson['policySettings']['firewallSettingEventLogFileIgnoreSourceIpListId']['value']
            if here:
                if here != 'NONE':
                    indexnum = t1iplistid.index(here)
                    policyjson['policySettings']['firewallSettingEventLogFileIgnoreSourceIpListId']['value'] = t2iplistid[indexnum]

            here = policyjson['policySettings']['webReputationSettingMonitorPortListId']['value']
            if here:
                if here != '80,8080':
                    indexnum = t1portlistid.index(here)
                    policyjson['policySettings']['webReputationSettingMonitorPortListId']['value'] = t2portlistid[indexnum]

            '''
            index = describe.find('antiMalwareSettingSmartProtectionGlobalServerUseProxyEnabled')
            if index != -1:
                indexpart = describe[index:]
                startIndex = indexpart.find('{')
                if startIndex != -1: #i.e. if the first quote was found
                    endIndex = indexpart.find('}', startIndex + 1)
                    if startIndex != -1 and endIndex != -1: #i.e. both quotes were found
                        indexid = indexpart[startIndex+1:endIndex]
                        value = indexid.find("true")
                        if value != -1:
                            describe = describe[:index+startIndex+value+1] + "false" + describe[index+endIndex-1:]
            index = describe.find('webReputationSettingSmartProtectionGlobalServerUseProxyEnabled')
            if index != -1:
                indexpart = describe[index:]
                startIndex = indexpart.find('{')
                if startIndex != -1: #i.e. if the first quote was found
                    endIndex = indexpart.find('}', startIndex + 1)
                    if startIndex != -1 and endIndex != -1: #i.e. both quotes were found
                        indexid = indexpart[startIndex+1:endIndex]
                        value = indexid.find("true")
                        if value != -1:
                            describe = describe[:index+startIndex+value+1] + "false" + describe[index+endIndex-1:]
            index = describe.find('platformSettingSmartProtectionGlobalServerUseProxyEnabled')
            if index != -1:
                indexpart = describe[index:]
                startIndex = indexpart.find('{')
                if startIndex != -1: #i.e. if the first quote was found
                    endIndex = indexpart.find('}', startIndex + 1)
                    if startIndex != -1 and endIndex != -1: #i.e. both quotes were found
                        indexid = indexpart[startIndex+1:endIndex]
                        value = indexid.find("true")
                        if value != -1:
                            describe = describe[:index+startIndex+value+1] + "false" + describe[index+endIndex-1:]
            index = describe.find('platformSettingSmartProtectionAntiMalwareGlobalServerProxyId')
            if index != -1:
                indexpart = describe[index:]
                startIndex = indexpart.find('{')
                if startIndex != -1: #i.e. if the first quote was found
                    endIndex = indexpart.find('}', startIndex + 1)
                    if startIndex != -1 and endIndex != -1: #i.e. both quotes were found
                        indexid = indexpart[startIndex+1:endIndex]
                        value = indexid.find("value")
                        if value != -1:
                            valuepart = indexid[value+7:]
                            startvalue = valuepart.find('\"')
                            if startvalue != -1:
                                endvalue = valuepart.find('\"', startvalue+1)
                                if startvalue != -1 and endvalue != -1:
                                    describe = describe[:index+startIndex+value+7+startvalue+2] + "" + describe[index+startIndex+value+7+startvalue+endvalue+1:]
            index = describe.find('webReputationSettingSmartProtectionWebReputationGlobalServerProxyId')
            if index != -1:
                indexpart = describe[index:]
                startIndex = indexpart.find('{')
                if startIndex != -1: #i.e. if the first quote was found
                    endIndex = indexpart.find('}', startIndex + 1)
                    if startIndex != -1 and endIndex != -1: #i.e. both quotes were found
                        indexid = indexpart[startIndex+1:endIndex]
                        value = indexid.find("value")
                        if value != -1:
                            valuepart = indexid[value+7:]
                            startvalue = valuepart.find('\"')
                            if startvalue != -1:
                                endvalue = valuepart.find('\"', startvalue+1)
                                if startvalue != -1 and endvalue != -1:
                                    describe = describe[:index+startIndex+value+7+startvalue+2] + "" + describe[index+startIndex+value+7+startvalue+endvalue+1:]
            index = describe.find('platformSettingSmartProtectionGlobalServerProxyId')
            if index != -1:
                indexpart = describe[index:]
                startIndex = indexpart.find('{')
                if startIndex != -1: #i.e. if the first quote was found
                    endIndex = indexpart.find('}', startIndex + 1)
                    if startIndex != -1 and endIndex != -1: #i.e. both quotes were found
                        indexid = indexpart[startIndex+1:endIndex]
                        value = indexid.find("value")
                        if value != -1:
                            valuepart = indexid[value+7:]
                            startvalue = valuepart.find('\"')
                            if startvalue != -1:
                                endvalue = valuepart.find('\"', startvalue+1)
                                if startvalue != -1 and endvalue != -1:
                                    describe = describe[:index+startIndex+value+7+startvalue+2] + "" + describe[index+startIndex+value+7+startvalue+endvalue+1:]
            index = describe.find('firewallSettingReconnaissanceExcludeIpListId')
            if index != -1:
                indexpart = describe[index:]
                startIndex = indexpart.find('{')
                if startIndex != -1: #i.e. if the first quote was found
                    endIndex = indexpart.find('}', startIndex + 1)
                    if startIndex != -1 and endIndex != -1: #i.e. both quotes were found
                        indexid = indexpart[startIndex+1:endIndex]
                        value = indexid.find("value")
                        if value != -1:
                            valuepart = indexid[value+7:]
                            startvalue = valuepart.find('\"')
                            if startvalue != -1:
                                endvalue = valuepart.find('\"', startvalue+1)
                                if startvalue != -1 and endvalue != -1:
                                    indexid1 = valuepart[startvalue+1:endvalue]
                                    if indexid1 != "" and indexid1 != 'NONE':
                                        indexid5 = describe[index:index+endIndex]
                                        indexnum = t1iplistid.index(indexid1)
                                        listpart = indexid5.replace(indexid1, t2iplistid[indexnum])
                                        describe = describe.replace(indexid5, listpart)
            index = describe.find('firewallSettingReconnaissanceIncludeIpListId')
            if index != -1:
                indexpart = describe[index:]
                startIndex = indexpart.find('{')
                if startIndex != -1: #i.e. if the first quote was found
                    endIndex = indexpart.find('}', startIndex + 1)
                    if startIndex != -1 and endIndex != -1: #i.e. both quotes were found
                        indexid = indexpart[startIndex+1:endIndex]
                        value = indexid.find("value")
                        if value != -1:
                            valuepart = indexid[value+7:]
                            startvalue = valuepart.find('\"')
                            if startvalue != -1:
                                endvalue = valuepart.find('\"', startvalue+1)
                                if startvalue != -1 and endvalue != -1:
                                    indexid1 = valuepart[startvalue+1:endvalue]
                                    if indexid1 != "" and indexid1 != 'NONE':
                                        indexid5 = describe[index:index+endIndex]
                                        indexnum = t1iplistid.index(indexid1)
                                        listpart = indexid5.replace(indexid1, t2iplistid[indexnum])
                                        describe = describe.replace(indexid5, listpart)
            index = describe.find('firewallSettingEventLogFileIgnoreSourceIpListId')
            if index != -1:
                indexpart = describe[index:]
                startIndex = indexpart.find('{')
                if startIndex != -1: #i.e. if the first quote was found
                    endIndex = indexpart.find('}', startIndex + 1)
                    if startIndex != -1 and endIndex != -1: #i.e. both quotes were found
                        indexid = indexpart[startIndex+1:endIndex]
                        value = indexid.find("value")
                        if value != -1:
                            valuepart = indexid[value+7:]
                            startvalue = valuepart.find('\"')
                            if startvalue != -1:
                                endvalue = valuepart.find('\"', startvalue+1)
                                if startvalue != -1 and endvalue != -1:
                                    indexid1 = valuepart[startvalue+1:endvalue]
                                    if indexid1 != "" and indexid1 != 'NONE':
                                        indexid5 = describe[index:index+endIndex]
                                        indexnum = t1iplistid.index(indexid1)
                                        listpart = indexid5.replace(indexid1, t2iplistid[indexnum])
                                        describe = describe.replace(indexid5, listpart)
            index = describe.find('webReputationSettingMonitorPortListId')
            if index != -1:
                indexpart = describe[index:]
                startIndex = indexpart.find('{')
                if startIndex != -1: #i.e. if the first quote was found
                    endIndex = indexpart.find('}', startIndex + 1)
                    if startIndex != -1 and endIndex != -1: #i.e. both quotes were found
                        indexid = indexpart[startIndex+1:endIndex]
                        value = indexid.find("value")
                        if value != -1:
                            valuepart = indexid[value+7:]
                            startvalue = valuepart.find('\"')
                            if startvalue != -1:
                                endvalue = valuepart.find('\"', startvalue+1)
                                if startvalue != -1 and endvalue != -1:
                                    indexid1 = valuepart[startvalue+1:endvalue]
                                    if indexid1 != "" and indexid1 != '80,8080':
                                        indexid5 = describe[index:index+endIndex]
                                        indexnum = t1portlistid.index(indexid1)
                                        listpart = indexid5.replace(indexid1, t2portlistid[indexnum])
                                        describe = describe.replace(indexid5, listpart)
                                        '''
            allofpolicy[count] = json.dumps(policyjson)
    return allofpolicy