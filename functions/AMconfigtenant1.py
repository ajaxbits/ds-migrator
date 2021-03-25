import sys
import os
import time
from time import sleep
import requests
import urllib3

cert = False

def AMconfigtenant1(antimalwareconfig, url_link_final, tenant1key):
#Describe each AM config from tenant1
    allamconfig = []
    directorylist = []
    fileextentionlist = []
    filelist = []
    print ("Getting Anti-Malware configuration from Tenant 1", flush=True)
    for count, amconfig in enumerate(antimalwareconfig):
        if int(amconfig) != 0:
            payload  = {}
            url = url_link_final + 'api/antimalwareconfigurations/' + str(amconfig)
            headers = {
                "api-secret-key": tenant1key,
                "api-version": "v1",
                "Content-Type": "application/json",
            }
            response = requests.request("GET", url, headers=headers, data=payload, verify=cert)
            
            describe = str(response.text)
            allamconfig.append(describe)
            index = describe.find('directoryListID')
            if index != -1:
                indexpart = describe[index+16:]
                startIndex = indexpart.find(':')
                if startIndex != -1: #i.e. if the first quote was found
                    endIndex = indexpart.find(',', startIndex + 1)
                    if startIndex != -1 and endIndex != -1: #i.e. both quotes were found
                        indexid = indexpart[startIndex+1:endIndex]
                        directorylist.append(str(indexid))
            index = describe.find('excludedDirectoryListID')
            if index != -1:
                indexpart = describe[index+24:]
                startIndex = indexpart.find(':')
                if startIndex != -1: #i.e. if the first quote was found
                    endIndex = indexpart.find(',', startIndex + 1)
                    if startIndex != -1 and endIndex != -1: #i.e. both quotes were found
                        indexid = indexpart[startIndex+1:endIndex]
                        directorylist.append(str(indexid))
            index = describe.find('excludedFileExtensionListID')
            if index != -1:
                indexpart = describe[index+28:]
                startIndex = indexpart.find(':')
                if startIndex != -1: #i.e. if the first quote was found
                    endIndex = indexpart.find(',', startIndex + 1)
                    if startIndex != -1 and endIndex != -1: #i.e. both quotes were found
                        indexid = indexpart[startIndex+1:endIndex]
                        fileextentionlist.append(str(indexid))
            index = describe.find('fileExtensionListID')
            if index != -1:
                indexpart = describe[index+20:]
                startIndex = indexpart.find(':')
                if startIndex != -1: #i.e. if the first quote was found
                    endIndex = indexpart.find(',', startIndex + 1)
                    if startIndex != -1 and endIndex != -1: #i.e. both quotes were found
                        indexid = indexpart[startIndex+1:endIndex]
                        fileextentionlist.append(str(indexid))
            index = describe.find('excludedFileListID')
            if index != -1:
                indexpart = describe[index+19:]
                startIndex = indexpart.find(':')
                if startIndex != -1: #i.e. if the first quote was found
                    endIndex = indexpart.find(',', startIndex + 1)
                    if startIndex != -1 and endIndex != -1: #i.e. both quotes were found
                        indexid = indexpart[startIndex+1:endIndex]
                        filelist.append(str(indexid))           
            index = describe.find('excludedProcessImageFileListID')
            if index != -1:
                indexpart = describe[index+31:]
                startIndex = indexpart.find(':')
                if startIndex != -1: #i.e. if the first quote was found
                    endIndex = indexpart.find(',', startIndex + 1)
                    if startIndex != -1 and endIndex != -1: #i.e. both quotes were found
                        indexid = indexpart[startIndex+1:endIndex]
                        filelist.append(str(indexid)) 
            print("#" + str(count) + " Anti-Malware Config ID: " + str(amconfig), flush=True)
    directorylist = list(dict.fromkeys(directorylist))
    fileextentionlist = list(dict.fromkeys(fileextentionlist))
    filelist = list(dict.fromkeys(filelist))
    return directorylist, fileextentionlist, filelist, allamconfig
