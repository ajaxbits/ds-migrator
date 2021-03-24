from __future__ import print_function
import re
import requests
import urllib3
from time import sleep
import sys, warnings, os, time
import deepsecurity
from deepsecurity.rest import ApiException
import json
import csv
from datetime import date
from zeep.client import Client
from requests import Session
from zeep.transports import Transport
from datetime import datetime
from zeep import helpers
import os

# configuration
username = "admin"
password = "MwbdKr3NBwGKkeG5p8K7NdfToG"
hostname = "https://ajax-ds20-t-dsmelb-idi20586foba-797956631.us-east-2.elb.amazonaws.com/webservice/Manager?WSDL"
tenant = ""

# Setup
if not sys.warnoptions:
    warnings.simplefilter("ignore")


def to_snake(camel_case):
    pattern = re.compile(r"(?<!^)(?=[A-Z])")
    snake = pattern.sub("_", camel_case).lower()
    return snake


class RestApiConfiguration:
    def __init__(self, overrides=False):
        user_config = json.load(open("./config.json", "r"))
        self.configuration = deepsecurity.Configuration()
        self.api_client = deepsecurity.ApiClient(self.configuration)
        self.overrides = overrides
        self.configuration.host = (
            f"{user_config['new_hostname']}:{user_config['new_port']}/api"
        )
        self.configuration.api_key["api-secret-key"] = user_config["new_api_secret_key"]
        self.api_version = "v1"


class PoliciesApiInstance(RestApiConfiguration):
    def __init__(self, overrides=False):
        super().__init__(overrides)
        self.api_instance = deepsecurity.PoliciesApi(self.api_client)

    def list(self):
        return self.api_instance.list_policies(
            self.api_version, overrides=self.overrides
        )

    def create(self, policy_object):
        policy = deepsecurity.Policy()
        for key in policy_object:
            setattr(policy, to_snake(key), policy_object[key])
        # TODO change
        policy.name = "testing"
        return self.api_instance.create_policy(policy, self.api_version)


def gen_unique_dict(old_policies_list, new_policies_list):
    # generate a dict with unique policies in the old dsm
    unique = []
    duplicates = []
    if new_policies_list == []:
        unique = old_policies_list
    else:
        for old_policy in old_policies_list:
            for new_policy in new_policies_list:
                if (
                    old_policy.name == new_policy.name
                    and old_policy.description == new_policy.description
                ):
                    duplicates.append(old_policy)
                else:
                    unique.append(old_policy)
    return {"unique": unique, "duplicates": duplicates}


# create SOAP session
session = Session()
session.verify = False
url = hostname
transport = Transport(session=session, timeout=1800)
client = Client(url, transport=transport)
factory = client.type_factory("ns0")
sID = client.service.authenticate(username=username, password=password)

# get policies and dedupe
old_policies_list = client.service.securityProfileRetrieveAll(sID)
new_policies_list = PoliciesApiInstance("new").list().policies
policies_dict = gen_unique_dict(old_policies_list, new_policies_list)
# print(policies_dict)

###############################PH#####################################

cert = False

policyIDs = []
for i in policies_dict["unique"]:
    policyIDs.append(i.ID)


def RestHttpGetPolicy(policyIDs, url_link_final, tenant1key):
    antimalwareconfig = []
    allofpolicy = []
    i = 0
    print("Getting Policy from Tenant 1", flush=True)
    for count, part in enumerate(policyIDs):

        payload = {}
        url = url_link_final + "api/policies/" + str(part)
        headers = {
            "api-secret-key": tenant1key,
            "api-version": "v1",
            "Content-Type": "application/json",
        }
        response = requests.request(
            "GET", url, headers=headers, data=payload, verify=cert
        )

        describe = str(response.text)
        i = i + 1
        allofpolicy.append(describe)
        print("#" + str(count) + " Policy ID: " + str(part), flush=True)
        rtscan = describe.find("realTimeScanConfigurationID")
        if rtscan != -1:
            rtpart = describe[rtscan + 28 :]
            startIndex = rtpart.find(":")
            if startIndex != -1:  # i.e. if the first quote was found
                endIndex = rtpart.find(",", startIndex + 1)
                if startIndex != -1 and endIndex != -1:  # i.e. both quotes were found
                    rtid = rtpart[startIndex + 1 : endIndex]
                    antimalwareconfig.append(str(rtid))

        mscan = describe.find("manualScanConfigurationID")
        if mscan != -1:
            mpart = describe[mscan + 26 :]
            startIndex = mpart.find(":")
            if startIndex != -1:  # i.e. if the first quote was found
                endIndex = mpart.find(",", startIndex + 1)
                if startIndex != -1 and endIndex != -1:  # i.e. both quotes were found
                    mid = mpart[startIndex + 1 : endIndex]
                    antimalwareconfig.append(str(mid))

        sscan = describe.find("scheduledScanConfigurationID")
        if sscan != -1:
            spart = describe[sscan + 29 :]
            startIndex = spart.find(":")
            if startIndex != -1:  # i.e. if the first quote was found
                endIndex = spart.find("}", startIndex + 1)
                if startIndex != -1 and endIndex != -1:  # i.e. both quotes were found
                    ssid = spart[startIndex + 1 : endIndex]
                    antimalwareconfig.append(str(ssid))
    antimalwareconfig = list(dict.fromkeys(antimalwareconfig))
    return antimalwareconfig, allofpolicy


full_script = RestHttpGetPolicy(
    policyIDs,
    "https://ajax-ds20-t-dsmelb-idi20586foba-797956631.us-east-2.elb.amazonaws.com/",
    "3177CE32-B1C7-EF55-112E-5FD7E8425F8B:nqdzbK24j6zuj89djtY+UTpDw1TtesuJVcbYWEY5d7w=",
)


first_policy = full_script[1][0]

first_policy_dict = json.loads(first_policy)

rest = PoliciesApiInstance()


def create(policy_object):
    policy = deepsecurity.Policy()
    for key in policy_object:
        setattr(policy, to_snake(key), policy_object[key])
    # TODO change
    policy.name = "testing"
    rest.api_instance.create_policy(policy, rest.api_version)


create(first_policy_dict)

# rest.create(first_policy)

###############################PH#####################################

# IMPORTANT! close the session, so there's not a session pileup
client.service.endSession(sID)
