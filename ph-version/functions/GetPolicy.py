import sys
import os
import time
from time import sleep
import requests
import urllib3

cert = False

def GetPolicy(policyIDs, url_link_final, tenant1key):
    antimalwareconfig = []
    allofpolicy = []
    i = 0
    print ("Getting Policy from Tenant 1", flush=True)
    for count, part in enumerate(policyIDs):
        
        payload  = {}
        url = url_link_final + 'api/policies/' + str(part)
        headers = {
            "api-secret-key": tenant1key,
            "api-version": "v1",
            "Content-Type": "application/json",
        }
        response = requests.request("GET", url, headers=headers, data=payload, verify=cert)
        
        describe = str(response.text)
        i = i + 1
        allofpolicy.append(describe)
        print ("#" + str(count) + " Policy ID: " + str(part), flush=True)
        rtscan = describe.find('realTimeScanConfigurationID')
        if rtscan != -1:
            rtpart = describe[rtscan+28:]
            startIndex = rtpart.find(':')
            if startIndex != -1: #i.e. if the first quote was found
                endIndex = rtpart.find(',', startIndex + 1)
                if startIndex != -1 and endIndex != -1: #i.e. both quotes were found
                    rtid = rtpart[startIndex+1:endIndex]
                    antimalwareconfig.append(str(rtid))
        
        mscan = describe.find('manualScanConfigurationID')
        if mscan != -1:
            mpart = describe[mscan+26:]
            startIndex = mpart.find(':')
            if startIndex != -1: #i.e. if the first quote was found
                endIndex = mpart.find(',', startIndex + 1)
                if startIndex != -1 and endIndex != -1: #i.e. both quotes were found
                    mid = mpart[startIndex+1:endIndex]
                    antimalwareconfig.append(str(mid))
        
        sscan = describe.find('scheduledScanConfigurationID')
        if sscan != -1:
            spart = describe[sscan+29:]
            startIndex = spart.find(':')
            if startIndex != -1: #i.e. if the first quote was found
                endIndex = spart.find('}', startIndex + 1)
                if startIndex != -1 and endIndex != -1: #i.e. both quotes were found
                    ssid = spart[startIndex+1:endIndex]
                    antimalwareconfig.append(str(ssid))
    antimalwareconfig = list(dict.fromkeys(antimalwareconfig))
    return antimalwareconfig, allofpolicy
