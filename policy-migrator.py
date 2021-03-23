from __future__ import print_function
import sys, warnings
import deepsecurity
from deepsecurity.rest import ApiException
import json

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

        if context == "old":
            self.configuration.host = (
                f"{user_config['original_hostname']}:{user_config['original_port']}/api"
            )
            self.configuration.api_key["api-secret-key"] = user_config[
                "original_api_secret_key"
            ]
            self.api_version = user_config["original_api_version"]
        else:
            self.configuration.host = (
                f"{user_config['new_hostname']}:{user_config['new_port']}/api"
            )
            self.configuration.api_key["api-secret-key"] = user_config[
                "new_api_secret_key"
            ]
            self.api_version = user_config["new_api_version"]

    def list(self):
        return self.api_instance.list_policies(
            self.api_version, overrides=self.overrides
        )


old_policies = PoliciesApiInstance("old")
new_policies = PoliciesApiInstance("new")
print(new_policies.list())
print(old_policies.list())


# class EditedRules(ApiInstance):
#     def __init__(self, file, module):
#         self.file = file
#         self.module = module
#         self.xml = ET.parse(file).getroot()
#         self.edited_rules = []
#         iterator = {
#             "ip": "PayloadFilter2",
#             "im": "IntegrityRule",
#             "li": "LogInspectionRule",
#         }

#         for rule in self.xml.iter(iterator[self.module]):
#             for child in rule.iter("UserEdited"):
#                 if child.text == "true":
#                     rule_id = rule.attrib["id"]
#                     self.edited_rules.append(int(rule_id))


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


# class Config:
#     def __init__(self, module, rules_file):
#         self.module = module
#         self.rules_file = rules_file
#         self.api = ApiInstance(self.module)
#         self.rules = EditedRules(self.rules_file, self.module)
