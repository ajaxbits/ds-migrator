import json
import deepsecurity
from deepsecurity.rest import ApiException
import re
import os


def to_snake(camel_case):
    pattern = re.compile(r"(?<!^)(?=[A-Z])")
    snake = pattern.sub("_", camel_case).lower()
    snake = snake.replace("application_type_i_d", "application_type_id")
    return snake


class RestApiConfiguration:
    def __init__(
        self, NEW_API_KEY, NEW_HOST="https://cloudone.trendmicro.com", overrides=False
    ):
        self.configuration = deepsecurity.Configuration()
        self.api_client = deepsecurity.ApiClient(self.configuration)
        self.overrides = overrides
        self.configuration.host = "https://cloudone.trendmicro.com/api"
        self.configuration.api_key["api-secret-key"] = NEW_API_KEY
        self.api_version = "v1"

    def name_search_filter(self, name):
        criteria = deepsecurity.SearchCriteria()
        criteria.field_name = "name"
        criteria.string_test = "equal"
        criteria.string_value = f"%{name}%"
        return deepsecurity.SearchFilter(None, [criteria])


class SystemSettingsApiInstance(RestApiConfiguration):
    def __init__(self, NEW_API_KEY, overrides=False):
        RestApiConfiguration.__init__(self, NEW_API_KEY, overrides)
        self.api_instance = deepsecurity.SystemSettingsApi(self.api_client)

    def modify(self, json_settings):
        settings = deepsecurity.SystemSettings()
        for key in json_settings:
            setattr(settings, to_snake(key), json_settings[key])
        self.api_instance.modify_system_settings(settings, self.api_version)
        return settings


class ComputerGroupsApiInstance(RestApiConfiguration):
    def __init__(self, NEW_API_KEY, overrides=False):
        RestApiConfiguration.__init__(self, NEW_API_KEY, overrides)
        self.api_instance = deepsecurity.ComputerGroupsApi(self.api_client)

    def search(self, name):
        filter = self.name_search_filter(name)
        results = self.api_instance.search_computer_groups("v1", search_filter=filter)
        if results.computer_groups:
            return results.computer_groups[0].id

    def create(self, json_group):
        group = deepsecurity.ComputerGroup()
        for key in json_group:
            if not key == "ID":
                setattr(group, to_snake(key), json_group[key])
        self.api_instance.create_computer_group(group, self.api_version)
        return group.name


class EventBasedTasksApiInstance(RestApiConfiguration):
    def __init__(self, NEW_API_KEY, overrides=False):
        RestApiConfiguration.__init__(self, NEW_API_KEY, overrides)
        self.api_instance = deepsecurity.EventBasedTasksApi(self.api_client)

    def search(self, name):
        filter = self.name_search_filter(name)
        results = self.api_instance.search_event_based_tasks("v1", search_filter=filter)
        if results.event_based_tasks:
            return results.event_based_tasks[0].id

    def create(self, json_task):
        task = deepsecurity.EventBasedTask()
        for key in json_task:
            if not key == "ID":
                setattr(task, to_snake(key), json_task[key])
        self.api_instance.create_event_based_task(task, self.api_version)
        return task.name


class ScheduledTasksApiInstance(RestApiConfiguration):
    def __init__(self, NEW_API_KEY, overrides=False):
        RestApiConfiguration.__init__(self, NEW_API_KEY, overrides)
        self.api_instance = deepsecurity.ScheduledTasksApi(self.api_client)

    def search(self, name):
        filter = self.name_search_filter(name)
        results = self.api_instance.search_scheduled_tasks("v1", search_filter=filter)
        if results.scheduled_tasks:
            return results.scheduled_tasks[0].id

    def create(self, json_task):
        task = deepsecurity.ScheduledTask()
        for key in json_task:
            if not key == "ID":
                setattr(task, to_snake(key), json_task[key])
        self.api_instance.create_scheduled_task(task, self.api_version)
        return task.name


class DirectoryListsApiInstance(RestApiConfiguration):
    def __init__(self, NEW_API_KEY, overrides=False):
        RestApiConfiguration.__init__(self, NEW_API_KEY, overrides)
        self.api_instance = deepsecurity.DirectoryListsApi(self.api_client)

    def search(self, name):
        filter = self.name_search_filter(name)
        results = self.api_instance.search_directory_lists("v1", search_filter=filter)
        if results.directory_lists:
            return results.directory_lists[0].id

    def create(self, json_dirlist):
        dirlist = deepsecurity.DirectoryList()
        for key in json_dirlist:
            if not key == "ID":
                setattr(dirlist, to_snake(key), json_dirlist[key])
        self.api_instance.create_directory_list(dirlist, self.api_version)
        return dirlist.name


class FileExtensionListsApiInstance(RestApiConfiguration):
    def __init__(self, NEW_API_KEY, overrides=False):
        RestApiConfiguration.__init__(self, NEW_API_KEY, overrides)
        self.api_instance = deepsecurity.FileExtensionListsApi(self.api_client)

    def search(self, name):
        filter = self.name_search_filter(name)
        results = self.api_instance.search_file_extension_lists(
            "v1", search_filter=filter
        )
        if results.file_extension_lists:
            return results.file_extension_lists[0].id

    def create(self, json_extlist):
        extlist = deepsecurity.FileExtensionList()
        for key in json_extlist:
            if not key == "ID":
                setattr(extlist, to_snake(key), json_extlist[key])
        self.api_instance.create_file_extension_list(extlist, self.api_version)
        return extlist.name


class FileListsApiInstance(RestApiConfiguration):
    def __init__(self, NEW_API_KEY, overrides=False):
        RestApiConfiguration.__init__(self, NEW_API_KEY, overrides)
        self.api_instance = deepsecurity.FileListsApi(self.api_client)

    def search(self, name):
        filter = self.name_search_filter(name)
        results = self.api_instance.search_file_lists("v1", search_filter=filter)
        if results.file_lists:
            return results.file_lists[0].id

    def create(self, json_filelist):
        filelist = deepsecurity.FileList()
        for key in json_filelist:
            if not key == "ID":
                setattr(filelist, to_snake(key), json_filelist[key])
        self.api_instance.create_file_list(filelist, self.api_version)
        return filelist.name


class ApplicationTypesApiInstance(RestApiConfiguration):
    def __init__(self, NEW_API_KEY, overrides=False):
        RestApiConfiguration.__init__(self, NEW_API_KEY, overrides)
        self.api_instance = deepsecurity.ApplicationTypesApi(self.api_client)

    # def get(self, id):
    #     return self.api_instance.describe_application_type(id, "v1")

    def search(self, name):
        filter = self.name_search_filter(name)
        results = self.api_instance.search_application_types("v1", search_filter=filter)
        if results.application_types:
            return results.application_types[0].id

    def create(self, json_application_types_list):
        application_type = deepsecurity.ApplicationType()
        for key in json_application_types_list:
            if not key == "ID":
                setattr(
                    application_type,
                    to_snake(key),
                    json_application_types_list[key],
                )
        self.api_instance.create_application_type(application_type, self.api_version)
        return application_type.name


class AMConfigApiInstance(RestApiConfiguration):
    def __init__(self, NEW_API_KEY, overrides=False):
        RestApiConfiguration.__init__(self, NEW_API_KEY, overrides)
        self.api_instance = deepsecurity.AntiMalwareConfigurationsApi(self.api_client)

    def search(self, name):
        filter = self.name_search_filter(name)
        results = self.api_instance.search_anti_malwares("v1", search_filter=filter)
        if results.anti_malware_configurations:
            return results.anti_malware_configurations[0].id

    def create(self, json):
        list = deepsecurity.AntiMalwareConfiguration()
        for key in json:
            if not key == "ID":
                setattr(list, to_snake(key), json[key])
        self.api_instance.create_anti_malware(list, self.api_version)
        return list.name


class FirewallApiInstance(RestApiConfiguration):
    def __init__(self, NEW_API_KEY, overrides=False):
        RestApiConfiguration.__init__(self, NEW_API_KEY, overrides)
        self.api_instance = deepsecurity.FirewallRulesApi(self.api_client)

    def search(self, name):
        filter = self.name_search_filter(name)
        results = self.api_instance.search_firewall_rules("v1", search_filter=filter)
        if results.firewall_rules:
            return results.firewall_rules[0].id

    def create(self, json):
        object = deepsecurity.FirewallRule()
        for key in json:
            if not key == "ID":
                setattr(object, to_snake(key), json[key])
        self.api_instance.create_firewall_rule(object, self.api_version)
        return object.name


class ApplicationControlRulesetsApiInstance(RestApiConfiguration):
    def __init__(self, NEW_API_KEY, overrides=False):
        RestApiConfiguration.__init__(self, NEW_API_KEY, overrides)
        self.api_instance = deepsecurity.RulesetsApi(self.api_client)

    def create(self, json, inventory_id):
        ruleset = deepsecurity.Ruleset()
        for key in json:
            if not key == "ID":
                setattr(ruleset, to_snake(key), json[key])
        try:
            self.api_instance.create_ruleset(ruleset, inventory_id, self.api_version)
            return ruleset.name
        except ApiException as e:
            print(
                "An exception occurred when calling RulesetsApi.create_ruleset: %s\n"
                % e
            )
            pass


class PolicyApiInstance(RestApiConfiguration):
    def __init__(self, NEW_API_KEY, overrides=False):
        RestApiConfiguration.__init__(self, NEW_API_KEY, overrides)
        self.api_instance = deepsecurity.PoliciesApi(self.api_client)

    def search(self, name):
        filter = self.name_search_filter(name)
        results = self.api_instance.search_policies("v1", search_filter=filter)
        if results.policies:
            return results.policies[0]

    def create(self, json):
        policy = deepsecurity.Policy()
        for key in json:
            if not key == "ID":
                setattr(policy, to_snake(key), json[key])
        self.api_instance.create_policy(policy, self.api_version)
        return policy.name

    def modify_parent(self, id, newparentid):
        policy = deepsecurity.Policy()
        policy.parent_id = newparentid
        self.api_instance.modify_policy(
            id, policy, self.api_version, overrides=self.overrides
        )

    def modify_real_time_id(self, id, newid):
        policy = deepsecurity.Policy()
        policy.anti_malware.real_time_scan_configuration_id = newid
        self.api_instance.modify_policy(
            id, policy, self.api_version, overrides=self.overrides
        )


class LogInspectionApiInstance(RestApiConfiguration):
    def __init__(self, NEW_API_KEY, overrides=False):
        RestApiConfiguration.__init__(self, NEW_API_KEY, overrides)
        self.api_instance = deepsecurity.LogInspectionRulesApi(self.api_client)

    def search(self, name):
        filter = self.name_search_filter(name)
        results = self.api_instance.search_log_inspection_rules(
            "v1", search_filter=filter
        )
        if results.log_inspection_rules:
            return results.log_inspection_rules[0].id

    def create(self, json):
        object = deepsecurity.LogInspectionRule()
        for key in json:
            if not key == "ID":
                setattr(object, to_snake(key), json[key])
        self.api_instance.create_log_inspection_rule(object, self.api_version)
        return object.name


class IntrusionPreventionApiInstance(RestApiConfiguration):
    def __init__(self, NEW_API_KEY, overrides=False):
        RestApiConfiguration.__init__(self, NEW_API_KEY, overrides)
        self.api_instance = deepsecurity.IntrusionPreventionRulesApi(self.api_client)

    def search(self, name):
        filter = self.name_search_filter(name)
        results = self.api_instance.search_intrusion_prevention_rules(
            "v1", search_filter=filter
        )
        if results.intrusion_prevention_rules:
            return results.intrusion_prevention_rules[0].id

    def create(self, json):
        object = deepsecurity.IntrusionPreventionRule()
        for key in json:
            if not key == "ID":
                setattr(object, to_snake(key), json[key])
        self.api_instance.create_intrusion_prevention_rule(object, self.api_version)
        return object.name


class IntegrityMonitoringApiInstance(RestApiConfiguration):
    def __init__(self, NEW_API_KEY, overrides=False):
        RestApiConfiguration.__init__(self, NEW_API_KEY, overrides)
        self.api_instance = deepsecurity.IntegrityMonitoringRulesApi(self.api_client)

    def search(self, name):
        filter = self.name_search_filter(name)
        results = self.api_instance.search_integrity_monitoring_rules(
            "v1", search_filter=filter
        )
        if results.integrity_monitoring_rules:
            return results.integrity_monitoring_rules[0].id

    def create(self, json):
        object = deepsecurity.IntegrityMonitoringRule()
        for key in json:
            if not key == "ID":
                setattr(object, to_snake(key), json[key])
        self.api_instance.create_integrity_monitoring_rule(
            self.api_version, integrity_monitoring_rule=object
        )
        return object.name
