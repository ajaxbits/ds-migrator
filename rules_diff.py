from __future__ import print_function
import sys, warnings
import deepsecurity
from deepsecurity.rest import ApiException
import json
import xml.etree.ElementTree as ET

# Setup
if not sys.warnoptions:
    warnings.simplefilter("ignore")


class ApiInstance:
    def __init__(self, module):
        self.module = module
        user_config = json.load(open("./config.json", "r"))
        self.configuration = deepsecurity.Configuration()
        self.configuration.host = (
            f"{user_config['original_hostname']}:{user_config['original_port']}/api"
        )
        self.configuration.api_key["api-secret-key"] = user_config[
            "original_api_secret_key"
        ]
        self.api_version = user_config["original_api_version"]

    def search(self, search_filter):
        if self.module == "ip":
            api_instance = deepsecurity.IntrusionPreventionRulesApi(
                deepsecurity.ApiClient(self.configuration)
            )
            return api_instance.search_intrusion_prevention_rules(
                self.api_version, search_filter=search_filter
            ).intrusion_prevention_rules

        elif self.module == "li":
            api_instance = deepsecurity.LogInspectionRulesApi(
                deepsecurity.ApiClient(self.configuration)
            )
            return api_instance.search_log_inspection_rules(
                self.api_version, search_filter=search_filter
            ).log_inspection_rules

        elif self.module == "im":
            api_instance = deepsecurity.IntegrityMonitoringRulesApi(
                deepsecurity.ApiClient(self.configuration)
            )
            return api_instance.search_integrity_monitoring_rules(
                self.api_version, search_filter=search_filter
            ).integrity_monitoring_rules


class EditedRules(ApiInstance):
    def __init__(self, file, module):
        self.file = file
        self.module = module
        self.xml = ET.parse(file).getroot()
        self.edited_rules = []
        iterator = {
            "ip": "PayloadFilter2",
            "im": "IntegrityRule",
            "li": "LogInspectionRule",
        }

        for rule in self.xml.iter(iterator[self.module]):
            for child in rule.iter("UserEdited"):
                if child.text == "true":
                    rule_id = rule.attrib["id"]
                    self.edited_rules.append(int(rule_id))


def add_module_rules(api_instance, edited_rules_list):
    rule_list = {
        "module": api_instance.module,
        "date": edited_rules_list.xml.attrib["date"],
        "rules": [],
    }
    for edited_rule in edited_rules_list.edited_rules:
        search_criteria = deepsecurity.SearchCriteria()
        search_criteria.id_value = edited_rule
        search_criteria.id_test = "equal"
        search_filter = deepsecurity.SearchFilter()
        search_filter.search_criteria = [search_criteria]
        rule = api_instance.search(search_filter=search_filter)[0]
        rule_list["rules"].append(
            {
                "identifier": int(rule.identifier),
                "details": {
                    "name": rule.name,
                    "description": rule.description,
                },
            }
        )
    return rule_list


class Config:
    def __init__(self, module, rules_file):
        self.module = module
        self.rules_file = rules_file
        self.api = ApiInstance(self.module)
        self.rules = EditedRules(self.rules_file, self.module)


ip = Config("ip", "./xml/Intrusion_Prevention_Rules.xml")
im = Config("im", "./xml/Integrity_Monitoring_Rules.xml")
li = Config("li", "./xml/Log_Inspection_Rules.xml")

try:
    rule_list = [
        add_module_rules(ip.api, ip.rules),
        add_module_rules(im.api, im.rules),
        add_module_rules(li.api, li.rules),
    ]
except ApiException as e:
    print(e)

json_output = json.dumps(rule_list, indent=2)
open("./lists/customized_rules.json", "w").write(json_output)
