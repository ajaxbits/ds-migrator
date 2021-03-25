import sys
import os
import time
from time import sleep
import requests
import urllib3
import json

cert = False

def RenamePolicy(allofpolicy):
    if allofpolicy:
        for count, describe in enumerate(allofpolicy):
            policyjson = json.loads(describe)
            policyjson['name'] = policyjson['name'] + " - Migrated"
            policyjson['parentID'] = "1"
            allofpolicy[count] = json.dumps(policyjson)
            
            '''
            index = describe.find('\"name\"')
            if index != -1:
                indexpart = describe[index+6:]
                startIndex = indexpart.find('\"')
                if startIndex != -1: #i.e. if the first quote was found
                    endIndex = indexpart.find(',', startIndex + 1)
                    if startIndex != -1 and endIndex != -1: #i.e. both quotes were found
                        indexid = indexpart[startIndex+1:endIndex-1]
                        newname = indexid + " - Migrated"
                        change1 = describe[:index+6+startIndex+1] + newname + describe[index+6+startIndex+endIndex-2:]
            index = change1.find('parentID')
            if index != -1:
                indexpart = change1[index+8:]
                startIndex = indexpart.find(':')
                if startIndex != -1: #i.e. if the first quote was found
                    endIndex = indexpart.find(',', startIndex + 1)
                    if startIndex != -1 and endIndex != -1: #i.e. both quotes were found
                        indexid = indexpart[startIndex+1:endIndex]
                        newname = "1"
                        allofpolicy[count] = change1[:index+8+startIndex+1] + newname + change1[index+8+startIndex+endIndex-1:]
                        '''

    return allofpolicy