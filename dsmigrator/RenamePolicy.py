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
            policyjson["name"] = policyjson["name"] + " - Migrated"
            policyjson["parentID"] = "1"
            allofpolicy[count] = json.dumps(policyjson)
    return allofpolicy
