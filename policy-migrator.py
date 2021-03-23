from __future__ import print_function
import requests
import sys, warnings
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


class PoliciesApiInstance:
    def __init__(self, context, overrides=False):
        user_config = json.load(open("./config.json", "r"))
        self.configuration = deepsecurity.Configuration()
        self.api_client = deepsecurity.ApiClient(self.configuration)
        self.api_instance = deepsecurity.PoliciesApi(self.api_client)
        self.overrides = overrides
        self.configuration.host = (
            f"{user_config['new_hostname']}:{user_config['new_port']}/api"
        )
        self.configuration.api_key["api-secret-key"] = user_config["new_api_secret_key"]
        self.api_version = user_config["new_api_version"]

    def list(self):
        return self.api_instance.list_policies(
            self.api_version, overrides=self.overrides
        )


def gen_unique_dict(old_policies_list, new_policies_list):
    unique = []
    duplicates = []
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


# IMPORTANT! close the session, so there's not a session pileup
client.service.endSession(sID)
