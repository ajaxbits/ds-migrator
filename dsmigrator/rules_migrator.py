import sys, warnings
import os
import deepsecurity
from deepsecurity.rest import ApiException
import json
import xml.etree.ElementTree as ET
from dsmigrator.migrator_utils import http_list_get, http_search

if not sys.warnoptions:
    warnings.simplefilter("ignore")


class RulesApiInstance:
    def __init__(self, module, OLD_HOST, OLD_API_KEY, cert):
        self.module = module
        self.OLD_HOST = OLD_HOST
        self.OLD_API_KEY = OLD_API_KEY
        self.api_version = "v1"
        self.cert = cert

    def search(self, rule_list):
        if self.module == "ip":
            http_search(
                "intrusion_prevention_rules",
                rule_list,
                self.OLD_HOST,
                self.OLD_API_KEY,
                self.cert,
                "ID",
            )
        elif self.module == "li":
            http_search(
                "log_inspection_rules",
                rule_list,
                self.OLD_HOST,
                self.OLD_API_KEY,
                self.cert,
                "ID",
            )
        elif self.module == "im":
            http_search(
                "integrity_monitoring_rules",
                rule_list,
                self.OLD_HOST,
                self.OLD_API_KEY,
                self.cert,
                "ID",
            )


class EditedRules(RulesApiInstance):
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


class Config(RulesApiInstance):
    def __init__(self, module, rules_file, OLD_HOST, OLD_API_KEY, cert):
        RulesApiInstance.__init__(self, module, OLD_HOST, OLD_API_KEY, cert)
        self.rules_file = rules_file
        self.rules = EditedRules(self.rules_file, self.module)


def add_module_rules(api_instance, edited_rules_list):
    rule_list = {
        "module": api_instance.module,
        "date": edited_rules_list.xml.attrib["date"],
        "rules": [],
    }
    edited_rules_details = api_instance.search(edited_rules_list.edited_rules)
    for edited_rule in edited_rules_details:
        rule = json.loads(edited_rule)
        rule_list["rules"].append(
            {
                "identifier": int(rule.get("identifier")),
                "details": {
                    "name": rule.get("name"),
                    "description": rule.get("description"),
                },
            }
        )
    return rule_list


if __name__ == "__main__":
    cert = False
    OLD_API_KEY = os.environ.get("ORIGINAL_API_KEY")
    OLD_HOST = os.environ.get("ORIGINAL_URL")

    ip = Config(
        "ip", "./xml/Intrusion_Prevention_Rules.xml", OLD_HOST, OLD_API_KEY, cert
    )
    im = Config(
        "im", "./xml/Integrity_Monitoring_Rules.xml", OLD_HOST, OLD_API_KEY, cert
    )
    li = Config("li", "./xml/Log_Inspection_Rules.xml", OLD_HOST, OLD_API_KEY, cert)

    try:
        rule_list = [
            add_module_rules(ip, ip.rules),
            add_module_rules(im, im.rules),
            add_module_rules(li, li.rules),
        ]
    except ApiException as e:
        print(e)

    json_output = json.dumps(rule_list, indent=2)
    open("./customized_rules.json", "a").write(json_output)
