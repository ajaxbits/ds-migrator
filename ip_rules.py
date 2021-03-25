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
import os
from ph_get_policy import GetPolicy
from ph_list_policies import ListAllPolicy

cert = False
OLD_API_KEY = os.environ.get("OLD_API_KEY")
OLD_HOST = os.environ.get("OLD_HOST")


class RestApiConfiguration:
    def __init__(self, overrides=False):
        user_config = json.load(open("./config.json", "r"))
        self.configuration = deepsecurity.Configuration()
        self.api_client = deepsecurity.ApiClient(self.configuration)
        self.overrides = overrides
        self.configuration.host = (
            f"{user_config['original_hostname']}:{user_config['original_port']}/api"
        )
        self.configuration.api_key["api-secret-key"] = user_config[
            "original_api_secret_key"
        ]
        self.api_version = "v1"


# TODO import this properly, no create() method
class PoliciesApiInstance(RestApiConfiguration):
    def __init__(self, overrides=False):
        super().__init__(overrides)
        self.api_instance = deepsecurity.PoliciesApi(self.api_client)

    def list(self):
        return self.api_instance.list_policies(
            self.api_version, overrides=self.overrides
        ).policies


class IpRulesApiInstance(RestApiConfiguration):
    def __init__(self, overrides=False):
        super().__init__(overrides)
        self.api_instance = deepsecurity.IntrusionPreventionRulesApi(self.api_client)

    def list(self):
        return self.api_instance.list_intrusion_prevention_rules(
            self.api_version
        ).intrusion_prevention_rules

    def search_name(self, name):
        search_criteria = deepsecurity.SearchCriteria()
        search_criteria.field_name = "name"
        search_criteria.string_value = "%" + name + "%"  # defaults to wildcard
        search_criteria.string_test = "equal"
        search_filter = deepsecurity.SearchFilter()
        search_filter.search_criteria = [search_criteria]
        ip_rules_search_results = self.api_instance.search_intrusion_prevention_rules(
            "v1", search_filter=search_filter
        )
        for rule in ip_rules_search_results.intrusion_prevention_rules:
            return rule.id


class LiRulesApiInstance(RestApiConfiguration):
    def __init__(self, overrides=False):
        super().__init__(overrides)
        self.api_instance = deepsecurity.LogInspectionRulesApi(self.api_client)

    def list(self):
        return self.api_instance.list_log_inspection_rules(
            self.api_version
        ).log_inspection_rules


def get_ips_rules(all_policy_list):
    ipsappid = []
    print("IPS rules in old deployment", flush=True)
    for policy in all_policy_list:
        if policy.intrusion_prevention.rule_ids:
            for count, ruleid in enumerate(policy.intrusion_prevention.rule_ids):
                ipsappid.append(ruleid)
    ipsappid = list(dict.fromkeys(ipsappid))
    print(ipsappid, flush=True)
    return ipsappid


def get_ips_apps(all_policy_list):
    ipsappid = []
    print("IPS application types in Tenant 1", flush=True)
    for policy in all_policy_list:
        if policy.intrusion_prevention.application_type_ids:
            for count, appid in enumerate(
                policy.intrusion_prevention.application_type_ids
            ):
                ipsappid.append(appid)
    ipsappid = list(dict.fromkeys(ipsappid))
    print(ipsappid, flush=True)
    return ipsappid


def get_port_list(url_link_final, tenant1key):
    t1portlistall = []
    t1portlistname = []
    t1portlistid = []
    print("Getting All Port List...", flush=True)
    payload = {}
    url = url_link_final + "/portlists"
    # TODO change back
    # url = url_link_final + "api/portlists"
    headers = {
        "api-secret-key": tenant1key,
        "api-version": "v1",
        "Content-Type": "application/json",
    }
    response = requests.request("GET", url, headers=headers, data=payload, verify=cert)
    describe = str(response.text)
    describe2 = str(response.text)
    namejson = json.loads(describe)
    for count, here in enumerate(namejson["portLists"]):
        t1portlistall.append(str(json.dumps(here)))
        t1portlistname.append(str(here["name"]))
        print("#" + str(count) + " Port List name: " + str(here["name"]), flush=True)
        t1portlistid.append(str(here["ID"]))
        print("#" + str(count) + " Port List ID: " + str(here["ID"]), flush=True)
    print("Done!", flush=True)
    return t1portlistall, t1portlistname, t1portlistid


if __name__ == "__main__":

    # AUTHENTICATION
    username = "admin"
    password = "MwbdKr3NBwGKkeG5p8K7NdfToG"
    hostname = "https://ajax-ds20-t-dsmelb-idi20586foba-797956631.us-east-2.elb.amazonaws.com/webservice/Manager?WSDL"
    tenant = ""

    # session = Session()
    # session.verify = False
    # url = hostname
    # transport = Transport(session=session, timeout=1800)
    # client = Client(url, transport=transport)
    # factory = client.type_factory("ns0")
    # sID = client.service.authenticate(username=username, password=password)
    # # TODO Move to end of file ##############################################
    # client.service.endSession(sID)

    # output a list of json
    # old_ips_rules = client.service.DPIRuleRetrieveAll(sID)
    new_ips_instance = IpRulesApiInstance()
    new_ips_rules = new_ips_instance.list()

    # getting allofpolicy using REST for now
    # TODO make this soap using the mapping you discovered
    old_policies_instance = PoliciesApiInstance()

    old_allofpolicy = ListAllPolicy(
        "https://ajax-ds20-t-dsmelb-idi20586foba-797956631.us-east-2.elb.amazonaws.com:443/",
        OLD_API_KEY,
    )

    # print(get_port_list(old_policies_instance.configuration.host, OLD_API_KEY))

    # print(ipsrules.search_identifier("1004232"))
    # print(identifier_dict(response, "SOAP"))
    # print(identifier_dict(ipsruleslist, "REST"))

    # print(generate_rules_rosetta(old_rules, new_rules))
