import sys
import os
import time
from time import sleep
import requests
import urllib3
import json
from api_config import AMConfigApiInstance
from migrator_utils import validate_create

cert = False


def AmconfigTenant2(allamconfig):
    allamconfignew = []
    print("Creating Anti-Malware Configuration to Tenant2", flush=True)
    if allamconfig:
        validate_create(allamconfig, AMConfigApiInstance, "anti malware")
    print("New AM Config ID", flush=True)
    print(allamconfignew, flush=True)
    return allamconfignew


def AmReplaceConfig(allofpolicy, antimalwareconfig, allamconfignew):
    count = 0
    for describe in allofpolicy:
        count1 = 0
        index = describe.find("realTimeScanConfigurationID")
        if index != -1:
            indexpart = describe[index + 28 :]
            startIndex = indexpart.find(":")
            if startIndex != -1:  # i.e. if the first quote was found
                endIndex = indexpart.find(",", startIndex + 1)
                if startIndex != -1 and endIndex != -1:  # i.e. both quotes were found
                    indexid = indexpart[startIndex + 1 : endIndex]
                    for dirlist in antimalwareconfig:
                        if int(dirlist) != 0:
                            if indexid == dirlist:
                                describe = (
                                    describe[: index + 28 + startIndex + 1]
                                    + allamconfignew[count1]
                                    + describe[index + 28 + startIndex + endIndex :]
                                )
                            count1 = count1 + 1
        count1 = 0
        index = describe.find("manualScanConfigurationID")
        if index != -1:
            indexpart = describe[index + 26 :]
            startIndex = indexpart.find(":")
            if startIndex != -1:  # i.e. if the first quote was found
                endIndex = indexpart.find(",", startIndex + 1)
                if startIndex != -1 and endIndex != -1:  # i.e. both quotes were found
                    indexid = indexpart[startIndex + 1 : endIndex]
                    for dirlist in antimalwareconfig:
                        if int(dirlist) != 0:
                            if indexid == dirlist:
                                describe = (
                                    describe[: index + 26 + startIndex + 1]
                                    + allamconfignew[count1]
                                    + describe[index + 26 + startIndex + endIndex :]
                                )
                            count1 = count1 + 1
        count1 = 0
        index = describe.find("scheduledScanConfigurationID")
        if index != -1:
            indexpart = describe[index + 29 :]
            startIndex = indexpart.find(":")
            if startIndex != -1:  # i.e. if the first quote was found
                endIndex = indexpart.find("}", startIndex + 1)
                if startIndex != -1 and endIndex != -1:  # i.e. both quotes were found
                    indexid = indexpart[startIndex + 1 : endIndex]
                    for dirlist in antimalwareconfig:
                        if int(dirlist) != 0:
                            if indexid == dirlist:
                                describe = (
                                    describe[: index + 29 + startIndex + 1]
                                    + allamconfignew[count1]
                                    + describe[index + 29 + startIndex + endIndex :]
                                )
                            count1 = count1 + 1

        allofpolicy[count] = describe
        count = count + 1
    return allofpolicy
