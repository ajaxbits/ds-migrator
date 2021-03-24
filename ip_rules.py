import requests
import deepsecurity
import json
import csv
from datetime import date
from zeep.client import Client
from requests import Session
from zeep.transports import Transport
from datetime import datetime
from zeep import helpers
from migrator import RestApiConfiguration


class IpRulesApiInstance(RestApiConfiguration):
    def __init__(self, overrides=False):
        super().__init__(overrides)
        self.api_instance = deepsecurity.IntrusionPreventionRulesApi(self.api_client)

    def list(self):
        return self.api_instance.list_intrusion_prevention_rules(
            self.api_version
        ).intrusion_prevention_rules


class LiRulesApiInstance(RestApiConfiguration):
    def __init__(self, overrides=False):
        super().__init__(overrides)
        self.api_instance = deepsecurity.LogInspectionRulesApi(self.api_client)

    def list(self):
        return self.api_instance.list_log_inspection_rules(
            self.api_version
        ).log_inspection_rules


def generate_tuples(json_list, type):
    ip_mapping = []
    if type == "SOAP":
        for i in json_list:
            ip_mapping.append((i.ID, i.identifier))
    else:
        for i in json_list:
            ip_mapping.append((i.id, i.identifier))
    return ip_mapping


def generate_rules_rosetta(old_rules, new_rules):
    # take lists of old and new rules and make a list of tuples
    # of the form (oldid, newid)
    corrected_rule_list = []
    for id_old, identifier_old in old_rules:
        for id_new, identifier_new in new_rules:
            if identifier_old == identifier_new:
                corrected_rule_list.append((id_old, id_new))
    return corrected_rule_list


if __name__ == "__main__":

    # AUTHENTICATION
    username = "admin"
    password = "MwbdKr3NBwGKkeG5p8K7NdfToG"
    hostname = "https://ajax-ds20-t-dsmelb-idi20586foba-797956631.us-east-2.elb.amazonaws.com/webservice/Manager?WSDL"
    tenant = ""

    session = Session()
    session.verify = False
    url = hostname
    transport = Transport(session=session, timeout=1800)
    client = Client(url, transport=transport)
    factory = client.type_factory("ns0")
    sID = client.service.authenticate(username=username, password=password)

    # output a list of json
    response = client.service.DPIRuleRetrieveAll(sID)
    print(response)

    ipsrules = IpRulesApiInstance()
    ipsruleslist = ipsrules.list()

    old_rules = generate_tuples(response, "SOAP")
    new_rules = generate_tuples(ipsruleslist, "REST")

    client.service.endSession(sID)
