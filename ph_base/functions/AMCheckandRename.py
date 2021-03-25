import sys
import os
import time
from time import sleep
import requests
import urllib3
import json

cert = False

def AmConfigCheck(allamconfig, directorylist, alldirectorynew, fileextentionlist, allfileextentionnew, filelist, allfilelistnew):

    count = 0
    for describe in allamconfig:
        count1 = 0
        index = describe.find('\"directoryListID\"')
        if index != -1:
            indexpart = describe[index+17:]
            startIndex = indexpart.find(':')
            if startIndex != -1: #i.e. if the first quote was found
                endIndex = indexpart.find(',', startIndex + 1)
                if startIndex != -1 and endIndex != -1: #i.e. both quotes were found
                    indexid = indexpart[startIndex+1:endIndex]
                    for dirlist in directorylist:
                        if indexid == dirlist:
                            if alldirectorynew:
                                describe = describe[:index+17+startIndex+1] + alldirectorynew[count1] + describe[index+17+startIndex+endIndex:]
                        count1 = count1 + 1   
        count1 = 0
        index = describe.find('excludedDirectoryListID')
        if index != -1:
            indexpart = describe[index+24:]
            startIndex = indexpart.find(':')
            if startIndex != -1: #i.e. if the first quote was found
                endIndex = indexpart.find(',', startIndex + 1)
                if startIndex != -1 and endIndex != -1: #i.e. both quotes were found
                    indexid = indexpart[startIndex+1:endIndex]
                    for dirlist in directorylist:
                        if indexid == dirlist:
                            if alldirectorynew:
                                describe = describe[:index+24+startIndex+1] + alldirectorynew[count1] + describe[index+24+startIndex+endIndex:]
                        count1 = count1 + 1
        count1 = 0
        index = describe.find('excludedFileExtensionListID')
        if index != -1:
            indexpart = describe[index+28:]
            startIndex = indexpart.find(':')
            if startIndex != -1: #i.e. if the first quote was found
                endIndex = indexpart.find(',', startIndex + 1)
                if startIndex != -1 and endIndex != -1: #i.e. both quotes were found
                    indexid = indexpart[startIndex+1:endIndex]
                    for dirlist in fileextentionlist:
                        if indexid == dirlist:
                            if allfileextentionnew:
                                describe = describe[:index+28+startIndex+1] + allfileextentionnew[count1] + describe[index+28+startIndex+endIndex:]
                        count1 = count1 + 1
        count1 = 0
        index = describe.find('\"fileExtensionListID\"')
        if index != -1:
            indexpart = describe[index+21]
            startIndex = indexpart.find(':')
            if startIndex != -1: #i.e. if the first quote was found
                endIndex = indexpart.find(',', startIndex + 1)
                if startIndex != -1 and endIndex != -1: #i.e. both quotes were found
                    indexid = indexpart[startIndex+1:endIndex]
                    for dirlist in fileextentionlist:
                        if indexid == dirlist:
                            if allfileextentionnew:
                                describe = describe[:index+21+startIndex+1] + allfileextentionnew[count1] + describe[index+21+startIndex+endIndex:]
                        count1 = count1 + 1
        count1 = 0
        index = describe.find('excludedFileListID')
        if index != -1:
            indexpart = describe[index+19:]
            startIndex = indexpart.find(':')
            if startIndex != -1: #i.e. if the first quote was found
                endIndex = indexpart.find(',', startIndex + 1)
                if startIndex != -1 and endIndex != -1: #i.e. both quotes were found
                    indexid = indexpart[startIndex+1:endIndex]
                    for dirlist in filelist:
                        if indexid == dirlist:
                            if allfilelistnew:
                                describe = describe[:index+19+startIndex+1] + allfilelistnew[count1] + describe[index+19+startIndex+endIndex:]
                        count1 = count1 + 1
        count1 = 0        
        index = describe.find('excludedProcessImageFileListID')
        if index != -1:
            indexpart = describe[index+31:]
            startIndex = indexpart.find(':')
            if startIndex != -1: #i.e. if the first quote was found
                endIndex = indexpart.find(',', startIndex + 1)
                if startIndex != -1 and endIndex != -1: #i.e. both quotes were found
                    indexid = indexpart[startIndex+1:endIndex]
                    for dirlist in filelist:
                        if indexid == dirlist:
                            if allfilelistnew:
                                describe = describe[:index+31+startIndex+1] + allfilelistnew[count1] + describe[index+31+startIndex+endIndex:]
                        count1 = count1 + 1
        allamconfig[count] = describe
        count = count + 1
    return allamconfig

def RenameAmConfig(allamconfig):
    count = 0
    if allamconfig:
        for describe in allamconfig:
            amjson = json.loads(describe)
            amjson['name'] = amjson['name'] + " - Migrated"
            allamconfig[count] = json.dumps(amjson)
            count = count + 1
        '''    
        index = describe.find('name')
        if index != -1:
            indexpart = describe[index+5:]
            startIndex = indexpart.find('\"')
            if startIndex != -1: #i.e. if the first quote was found
                endIndex = indexpart.find(',', startIndex + 1)
                if startIndex != -1 and endIndex != -1: #i.e. both quotes were found
                    indexid = indexpart[startIndex+1:endIndex-1]
                    newname = indexid + " - Migrated"
                    allamconfig[count] = describe[:index+5+startIndex+1] + newname + describe[index+5+startIndex+endIndex-2:]
                    '''
    return allamconfig