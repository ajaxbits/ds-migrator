import requests
import json
import sys
import time
from dsmigrator.logging import log


requests.packages.urllib3.disable_warnings(
    requests.packages.urllib3.exceptions.InsecureRequestWarning
)


class ApiConfig:
    """
    API configuration to access DSM or C1WS
    """

    def __init__(self, api_endpoint, api_key, verify_server_cert):
        self.api_endpoint = (
            api_endpoint if api_endpoint[-1] != "/" else api_endpoint[:-1]
        )
        self.api_key = api_key
        self.verify_server_cert = verify_server_cert

    def _compose_uri(self, api_path_and_queries) -> str:
        uri = self.api_endpoint
        if api_path_and_queries[0] != "/":
            uri += "/"
        uri += api_path_and_queries
        return uri

    def get_policies(self) -> dict:
        uri = self._compose_uri("/policies?overrides=true")
        r = requests.get(
            uri,
            verify=self.verify_server_cert,
            headers={"api-secret-key": self.api_key, "api-version": "v1"},
        )
        r.raise_for_status()
        return r.json()

    def update_policy(self, policy_id: int, data) -> dict:
        uri = self._compose_uri(f"/policies/{policy_id}")
        r = requests.post(
            uri,
            json=data,
            verify=self.verify_server_cert,
            headers={
                "api-secret-key": self.api_key,
                "api-version": "v1",
                "content-type": "application/json",
            },
        )
        r.raise_for_status()
        return r.json()

    def get_ip_list(self, ip_list_id: int) -> dict:
        uri = self._compose_uri(f"/iplists/{ip_list_id}")
        r = requests.get(
            uri,
            verify=self.verify_server_cert,
            headers={"api-secret-key": self.api_key, "api-version": "v1"},
        )
        r.raise_for_status()
        return r.json()

    def create_ip_list(self, data) -> dict:
        return self.update_ip_list(None, data)

    def update_ip_list(self, policy_id, data) -> dict:
        uri = (
            self._compose_uri("/iplists")
            if policy_id == None
            else self._compose_uri(f"/iplists/{policy_id}")
        )
        r = requests.post(
            uri,
            json=data,
            verify=self.verify_server_cert,
            headers={
                "api-secret-key": self.api_key,
                "api-version": "v1",
                "content-type": "application/json",
            },
        )
        r.raise_for_status()
        return r.json()

    def check_api_access(self) -> bool:
        url = self._compose_uri(f"/apikeys/current")
        result = None
        key_list = [i.split("-") for i in self.api_key.split(":")]
        first_identifier = key_list[0][0]
        key_list[0] = ["*" * len(i) for i in key_list[0][1:]]
        key_list[0].insert(0, first_identifier)
        key_list[1:] = [["*" * len(x) for x in i] for i in key_list[1:]]
        obfuscated_key = ":".join(["-".join(i) for i in key_list])
        try:
            payload = {}
            headers = {
                "api-secret-key": self.api_key,
                "api-version": "v1",
                "Content-Type": "application/json",
            }
            response = requests.request(
                "GET",
                url,
                headers=headers,
                data=payload,
                verify=self.verify_server_cert,
            )
            log.info(f"Checking api key {obfuscated_key}...")
            if "active" and "true" in response.text:
                result = True
            else:
                log.error(response.text)
                result = False
                log.error(
                    "Double-check that your api key is correct, active, and has 'Full Access' permissions."
                )
                log.error("Aborting...")
                sys.exit(0)
        except Exception as e:
            log.exception(e)
            result = False
            log.error(
                "Double-check that your api key is correct, active, and has 'Full Access' permissions."
            )
            log.error("Aborting...")
            sys.exit(0)
        return result


class DSMApi(ApiConfig):
    def __init__(self, api_endpoint, api_key, verify_server_cert):
        ApiConfig.__init__(self, api_endpoint, api_key, verify_server_cert)

    def create_policy_migration_task(self):
        uri = self._compose_uri(f"/policymigrationtasks")

        r = requests.post(
            uri,
            data={},
            verify=self.verify_server_cert,
            headers={
                "api-secret-key": self.api_key,
                "api-version": "v1",
                "content-type": "application/json",
            },
        )
        r.raise_for_status()
        return r.json()

    def describe_policy_migration_task(self, policy_migration_task_id):
        uri = self._compose_uri(f"/policymigrationtasks/{policy_migration_task_id}")

        r = requests.get(
            uri,
            verify=self.verify_server_cert,
            headers={
                "api-secret-key": self.api_key,
                "api-version": "v1",
                "content-type": "application/json",
            },
        )
        r.raise_for_status()
        return r.json()


class WorkloadApi(ApiConfig):
    def __init__(self, api_endpoint, api_key, verify_server_cert):
        ApiConfig.__init__(self, api_endpoint, api_key, verify_server_cert)

    def describe_policy_import_task(self, policy_import_task_id: int) -> dict:
        uri = self._compose_uri(f"/policyimporttasks/{policy_import_task_id}")
        r = requests.get(
            uri,
            verify=self.verify_server_cert,
            headers={"api-secret-key": self.api_key, "api-version": "v1"},
        )
        r.raise_for_status()
        return r.json()
