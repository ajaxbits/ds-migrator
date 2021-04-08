from __future__ import print_function
from pathlib import Path
import click
import sys, warnings
import deepsecurity
from deepsecurity.rest import ApiException
import json
import xml.etree.ElementTree as ET


@click.command()
@click.option(
    "-x",
    "--xml-folder",
    prompt="Path to XML folder with IM, LI, and IPS rule export files",
    help="Path to XML folder with IM, LI, and IPS rule export files. NOTE that the files must be named 'Intrusion_Prevention_Rules.xml', 'Log_Inspection_Rules.xml', and 'Integrity_Monitoring_Rules.xml'",
    default="./xml/",
)
@click.option(
    "-ou",
    "--original-url",
    prompt="Old DSM url",
    help="A resolvable FQDN for the old DSM, with port number (e.g. https://192.168.1.1:4119)",
    envvar="ORIGINAL_URL",
)
@click.option(
    "-oa",
    "--original-api-key",
    prompt="Old DSM API key",
    hide_input=True,
    help="API key for the old DSM with Full Access permissions",
    envvar="ORIGINAL_API_KEY",
)
@click.option(
    "--outfile",
    help="Path to output json file",
    default="./CUSTOMIZED_RULES.json",
)
@click.option(
    "-k",
    "--insecure",
    is_flag=True,
    help="Suppress the InsecureRequestWarning for self-signed certificates",
)
@click.option(
    "-c",
    "--cert",
    default=False,
    show_default=True,
    help="(Optional) Allows the use of a cert file",
)
def main(xml_folder, outfile, original_url, original_api_key, insecure, cert=False):
    print("Searching for customized rules...")

    class ApiInstance:
        def __init__(self, module, ORIGINAL_URL, ORIGINAL_API_KEY, cert=False):
            self.module = module
            self.configuration = deepsecurity.Configuration()
            self.configuration.host = f"{ORIGINAL_URL}/api"
            self.configuration.api_key["api-secret-key"] = ORIGINAL_API_KEY
            self.api_version = "v1"

        def search(self, search_filter):
            if self.module == "Intrusion Prevention":
                api_instance = deepsecurity.IntrusionPreventionRulesApi(
                    deepsecurity.ApiClient(self.configuration)
                )
                return api_instance.search_intrusion_prevention_rules(
                    self.api_version, search_filter=search_filter
                ).intrusion_prevention_rules
            elif self.module == "Log Inspection":
                api_instance = deepsecurity.LogInspectionRulesApi(
                    deepsecurity.ApiClient(self.configuration)
                )
                return api_instance.search_log_inspection_rules(
                    self.api_version, search_filter=search_filter
                ).log_inspection_rules
            elif self.module == "Integrity Monitoring":
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
                "Intrusion Prevention": "PayloadFilter2",
                "Integrity Monitoring": "IntegrityRule",
                "Log Inspection": "LogInspectionRule",
            }
            for rule in self.xml.iter(iterator[self.module]):
                for child in rule.iter("UserEdited"):
                    if child.text == "true":
                        rule_id = rule.attrib["id"]
                        self.edited_rules.append(int(rule_id))
            if len(self.edited_rules) > 1:
                print(f"Found {len(self.edited_rules)} customized {self.module} rules!")
            elif self.edited_rules:
                print(f"Found {len(self.edited_rules)} customized {self.module} rule!")
            else:
                print(f"No customized {self.module} rules detected.")

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

    class Config(ApiInstance):
        def __init__(
            self, module, rules_file, ORIGINAL_URL, ORIGINAL_API_KEY, cert=False
        ):
            self.api = ApiInstance(module, ORIGINAL_URL, ORIGINAL_API_KEY, cert)
            self.rules = EditedRules(rules_file, module)

    if not sys.warnoptions:
        warnings.simplefilter("ignore")

    ip = Config(
        "Intrusion Prevention",
        f"{xml_folder}Intrusion_Prevention_Rules.xml",
        original_url,
        original_api_key,
        cert,
    )
    im = Config(
        "Integrity Monitoring",
        f"{xml_folder}Integrity_Monitoring_Rules.xml",
        original_url,
        original_api_key,
        cert,
    )
    li = Config(
        "Log Inspection",
        f"{xml_folder}Log_Inspection_Rules.xml",
        original_url,
        original_api_key,
        cert,
    )
    print(f"Creating report at {outfile}...")
    try:
        rule_list = [
            add_module_rules(ip.api, ip.rules),
            add_module_rules(im.api, im.rules),
            add_module_rules(li.api, li.rules),
        ]
    except ApiException as e:
        print(e)
    json_output = json.dumps(rule_list, indent=2)
    open(outfile, "w").write(json_output)
    print("DONE!")


if __name__ == "__main__":
    main()  # pylint: disable=no-value-for-parameter
