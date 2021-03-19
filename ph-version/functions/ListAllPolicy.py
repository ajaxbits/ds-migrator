import sys
import os
import time
from time import sleep
import requests
import urllib3
import json
cert = False

def ListAllPolicy(url_link_final, tenant1key):
    payload  = {}
    url = url_link_final + 'api/policies'
    headers = {
        "api-secret-key": tenant1key,
        "api-version": "v1",
        "Content-Type": "application/json",
    }
    response = requests.request("GET", url, headers=headers, data=payload, verify=cert)
    describe = str(response.text)
    index = 0
    oldpolicyname = []
    oldpolicyid = []
    namejson = json.loads(describe)
    for here in namejson['policies']:
        oldpolicyname.append(str(here['name']))
        oldpolicyid.append(str(here['ID']))
    '''
    while index != -1:
        index = describe.find('\"name\"')
        if index != -1:
            indexpart = describe[index+6:]
            startIndex = indexpart.find('\"')
            if startIndex != -1: #i.e. if the first quote was found
                endIndex = indexpart.find(',', startIndex + 1)
                if startIndex != -1 and endIndex != -1: #i.e. both quotes were found
                    indexid = indexpart[startIndex+1:endIndex-1]
                    oldpolicyname.append(str(indexid))
        index = describe.find('\"ID\"')
        if index != -1:
            indexpart = describe[index+4:]
            startIndex = indexpart.find(':')
            if startIndex != -1: #i.e. if the first quote was found
                endIndex = indexpart.find(',', startIndex + 1)
                if startIndex != -1 and endIndex != -1: #i.e. both quotes were found
                    indexid = indexpart[startIndex+1:endIndex]
                    oldpolicyid.append(str(indexid))
                    describe = indexpart[endIndex:]
                else:
                    endIndex = indexpart.find('}', startIndex + 1)
                    if startIndex != -1 and endIndex != -1: #i.e. both quotes were found
                        indexid = indexpart[startIndex+1:endIndex]
                        oldpolicyid.append(str(indexid))
                        describe = indexpart[endIndex:]
                        '''

    return enumerate(oldpolicyname), oldpolicyid