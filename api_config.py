import json
import deepsecurity

class RestApiConfiguration:
    def __init__(self, overrides=False):
        user_config = json.load(open("./config.json", "r"))
        self.configuration = deepsecurity.Configuration()
        self.api_client = deepsecurity.ApiClient(self.configuration)
        self.overrides = overrides
        self.configuration.host = (
            f"{user_config['new_hostname']}:{user_config['new_port']}/api"
        )
        self.configuration.api_key["api-secret-key"] = user_config["new_api_secret_key"]
        self.api_version = "v1"


