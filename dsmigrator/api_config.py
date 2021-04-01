import json
import deepsecurity
import re
import os


def to_snake(camel_case):
    pattern = re.compile(r"(?<!^)(?=[A-Z])")
    snake = pattern.sub("_", camel_case).lower()
    return snake


def to_class_name(snake_case):
    temp = str(snake_case).split("_")
    class_name = temp[0] + "".join(ele.title() for ele in temp)
    return class_name


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

    def create(self, json_task, type):
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
