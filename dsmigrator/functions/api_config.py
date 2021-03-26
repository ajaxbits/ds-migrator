import json
import deepsecurity
import re


def to_snake(camel_case):
    pattern = re.compile(r"(?<!^)(?=[A-Z])")
    snake = pattern.sub("_", camel_case).lower()
    return snake


class RestApiConfiguration:
    def __init__(self, overrides=False):
        user_config = json.load(open("../config.json", "r"))
        self.configuration = deepsecurity.Configuration()
        self.api_client = deepsecurity.ApiClient(self.configuration)
        self.overrides = overrides
        self.configuration.host = (
            f"{user_config['new_hostname']}:{user_config['new_port']}/api"
        )
        self.configuration.api_key["api-secret-key"] = user_config["new_api_secret_key"]
        self.api_version = "v1"


class DirectoryListsApiInstance(RestApiConfiguration):
    def __init__(self, overrides=False):
        super().__init__(overrides)
        self.api_instance = deepsecurity.DirectoryListsApi(self.api_client)

    def create(self, json_dirlist):
        dirlist = deepsecurity.DirectoryList()
        for key in json_dirlist:
            if not key == "ID":
                setattr(dirlist, to_snake(key), json_dirlist[key])
        self.api_instance.create_directory_list(json_dirlist, self.api_version)
        return dirlist.name, dirlist.id
