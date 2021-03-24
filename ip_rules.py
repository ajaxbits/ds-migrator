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
from api_config import RestApiConfiguration


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


def identifier_dict(json_list, type):
    ip_mapping = {}
    if type == "SOAP":
        for i in json_list:
            ip_mapping[i.ID] = i.identifier
    else:
        for i in json_list:
            ip_mapping[i.id] = i.identifier
    return ip_mapping


def filter_tuples(id_list, full_dict):
    filtered = {}
    for i in id_list:
        filtered[i] = full_dict[i]
    return filtered


def generate_rules_rosetta(old_rules_dict, all_new_rules):
    # take lists of old and new rules and make a dict
    # of the form {oldid: newid,...}
    corrected_rule_list = []
    for old_identifier in old_rules_dict.values():
        for new_id, new_identifier in all_new_rules.items():
            if old_identifier == new_identifier:
                corrected_rule_list.append(new_id)

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
    # print(response)

    ipsrules = IpRulesApiInstance()
    ipsruleslist = ipsrules.list()

    print(identifier_dict(response, "SOAP"))
    # print(identifier_dict(ipsruleslist, "REST"))

    # print(generate_rules_rosetta(old_rules, new_rules))

    client.service.endSession(sID)
