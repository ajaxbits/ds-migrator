import sys
import os
import time
from time import sleep
import requests
import urllib3

cert = False

def DirListTenant1(directorylist, url_link_final, tenant1key):
    alldirectory = []
    print ("Getting lists from Tenant 1, if any.")                
    for dirlist in directorylist:
        payload  = {}
        url = url_link_final + 'api/directorylists/' + str(dirlist)
        headers = {
            "api-secret-key": tenant1key,
            "api-version": "v1",
            "Content-Type": "application/json",
        }
        response = requests.request("GET", url, headers=headers, data=payload, verify=cert)
        describe = str(response.text)
        #describe = describe[:-1]
        #describe = describe[2:]
        alldirectory.append(describe)
    print("Tenant1 directory list")
    print(directorylist)
    return alldirectory