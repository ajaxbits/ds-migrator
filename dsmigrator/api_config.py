import json
import deepsecurity
import re
import os

OLD_API_KEY = os.environ.get("OLD_API_KEY")
OLD_HOST = os.environ.get("OLD_HOST")
NEW_API_KEY = os.environ.get("NEW_API_KEY")
NEW_HOST = os.environ.get("NEW_HOST")
cert = False


def to_snake(camel_case):
    pattern = re.compile(r"(?<!^)(?=[A-Z])")
    snake = pattern.sub("_", camel_case).lower()
    return snake


class RestApiConfiguration:
    def __init__(self, overrides=False):
        # user_config = json.load(open("../config.json", "r"))
        self.configuration = deepsecurity.Configuration()
        self.api_client = deepsecurity.ApiClient(self.configuration)
        self.overrides = overrides
        self.configuration.host = f"{NEW_HOST}/api"
        self.configuration.api_key["api-secret-key"] = NEW_API_KEY
        self.api_version = "v1"

    def name_search_filter(self, name):
        criteria = deepsecurity.SearchCriteria()
        criteria.field_name = "name"
        criteria.string_test = "equal"
        criteria.string_value = f"%{name}%"
        return deepsecurity.SearchFilter(None, [criteria])


class DirectoryListsApiInstance(RestApiConfiguration):
    def __init__(self, overrides=False):
        super().__init__(overrides)
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
        self.api_instance.create_directory_list(json_dirlist, self.api_version)
        return dirlist.name


class FileExtensionListsApiInstance(RestApiConfiguration):
    def __init__(self, overrides=False):
        super().__init__(overrides)
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
        self.api_instance.create_file_extension_list(json_extlist, self.api_version)
        return extlist.name


class FileListsApiInstance(RestApiConfiguration):
    def __init__(self, overrides=False):
        super().__init__(overrides)
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
        self.api_instance.create_file_list(json_filelist, self.api_version)
        return filelist.name


class AMConfigApiInstance(RestApiConfiguration):
    def __init__(self, overrides=False):
        super().__init__(overrides)
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
        self.api_instance.create_anti_malware(json, self.api_version)
        return list.name


class FirewallApiInstance(RestApiConfiguration):
    def __init__(self, overrides=False):
        super().__init__(overrides)
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
        self.api_instance.create_firewall_rule(json, self.api_version)
        return object.name


class PolicyApiInstance(RestApiConfiguration):
    def __init__(self, overrides=False):
        super().__init__(overrides)
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
