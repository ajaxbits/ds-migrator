from __future__ import print_function
import sys, warnings
import deepsecurity
from deepsecurity.rest import ApiException
import json

# Load user config
user_config = json.load(open("./config.json", "r"))

# Setup
if not sys.warnoptions:
    warnings.simplefilter("ignore")


class UserConfiguration:
    def __init__(self, user_config):
        self.configuration = deepsecurity.Configuration()
        self.user_config = user_config

    def set_old_creds(self):
        self.configuration.host = f"{self.user_config['original_hostname']}:{self.user_config['original_port']}/api"
        self.configuration.api_key["api-secret-key"] = self.user_config[
            "original_api_secret_key"
        ]

    def set_new_creds(self):
        self.configuration.host = (
            f"{self.user_config['new_hostname']}:{self.user_config['new_port']}/api"
        )
        self.configuration.api_key["api-secret-key"] = self.user_config[
            "new_api_secret_key"
        ]


# TODO figure out this ordering
configuration = UserConfiguration(user_config)
api_version = user_config["original_api_version"]


class PolicyList:
    def __init__(self, configuration=configuration, api_version=api_version):
        self.api_instance = deepsecurity.PoliciesApi(
            deepsecurity.ApiClient(configuration)
        )
        self.list = self.api_instance.list_policies(api_version).policies
        self.api_version = api_version

    def create(self, object):
        return self.api_instance.create_policy(object, self.api_version)


class ScheduledTasksList:
    def __init__(self, configuration=configuration, api_version=api_version):
        self.api_instance = deepsecurity.ScheduledTasksApi(
            deepsecurity.ApiClient(configuration)
        )
        self.list = self.api_instance.list_scheduled_tasks(api_version).scheduled_tasks
        self.api_version = api_version

    def create(self, object):
        return self.api_instance.create_scheduled_task(object, self.api_version)


class EventBasedTasksList:
    def __init__(self, configuration=configuration, api_version=api_version):
        self.api_instance = deepsecurity.EventBasedTasksApi(
            deepsecurity.ApiClient(configuration)
        )
        self.list = self.api_instance.list_event_based_tasks(
            api_version
        ).event_based_tasks
        self.api_version = api_version

    def create(self, object):
        return self.api_instance.create_event_based_task(object, self.api_version)


def migrate_module(export_object):
    for old_object in export_object.list:
        try:
            api_response = export_object.create(old_object)
            return api_response
        except ApiException as e:
            print(e)


def set_new_creds(configuration=configuration):
    configuration.host = f"{user_config['new_hostname']}:{user_config['new_port']}/api"
    configuration.api_key["api-secret-key"] = user_config["new_api_secret_key"]
    return configuration


def set_old_creds(configuration=configuration):
    configuration.host = f"{user_config['old_hostname']}:{user_config['old_port']}/api"
    configuration.api_key["api-secret-key"] = user_config["old_api_secret_key"]
    return configuration


def migrate_all(configuration):
    configuration.set_old_creds
    modules = [PolicyList(), ScheduledTasksList(), EventBasedTasksList()]
    # insert a module to back up all configs
    configuration.set_new_creds
    for i in modules:
        migrate_module(i)


migrate_all(configuration)
