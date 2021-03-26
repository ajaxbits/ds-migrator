import sys
import os
import time
from time import sleep
import requests
import urllib3
import json

cert = False


def ListAllPolicy(url_link_final, tenant1key):
    payload = {}
    url = url_link_final + "api/policies"
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
    for here in namejson["policies"]:
        oldpolicyname.append(str(here["name"]))
        oldpolicyid.append(str(here["ID"]))
    return enumerate(oldpolicyname), oldpolicyid
