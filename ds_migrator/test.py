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
