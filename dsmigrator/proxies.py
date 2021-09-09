import json
import os

import dsmigrator.api as api
import dsmigrator.migrator_utils as utility


def _find_used_proxies(dsm_policies: list) -> list:
    dsm_used_proxies = set()

    for p in dsm_policies:
        try:
            if (
                p["policySettings"][
                    "antiMalwareSettingSmartProtectionGlobalServerUseProxyEnabled"
                ]["value"]
                == "true"
            ):
                dsm_used_proxies.add(
                    int(
                        p["policySettings"][
                            "platformSettingSmartProtectionAntiMalwareGlobalServerProxyId"
                        ]["value"]
                    )
                )
        except (KeyError, AttributeError):
            pass
        try:
            if (
                p["policySettings"][
                    "webReputationSettingSmartProtectionGlobalServerUseProxyEnabled"
                ]["value"]
                == "true"
            ):
                dsm_used_proxies.add(
                    int(
                        p["policySettings"][
                            "webReputationSettingSmartProtectionWebReputationGlobalServerProxyId"
                        ]["value"]
                    )
                )
        except (KeyError, AttributeError):
            pass
        try:
            if (
                p["policySettings"][
                    "platformSettingSmartProtectionGlobalServerUseProxyEnabled"
                ]["value"]
                == "true"
            ):
                dsm_used_proxies.add(
                    int(
                        p["policySettings"][
                            "platformSettingSmartProtectionGlobalServerProxyId"
                        ]["value"]
                    )
                )
        except (KeyError, AttributeError):
            pass

    return list(dsm_used_proxies)


def _load_created_proxies_mappings() -> dict:
    id_mapping = {}
    mapping_file = os.environ["MIG_PROXY_MAPPING"]
    with open(mapping_file) as mapping_json:
        mapping = json.load(mapping_json)

    for m in mapping["proxies"]:
        id_mapping[int(m["dsmId"])] = int(m["c1wsId"])

    return id_mapping


def do_proxies(dsm_api_config: api.ApiConfig, c1ws_api_config: api.ApiConfig, migration_task_response: dict):

    dsm_policies = dsm_api_config.get_policies()["policies"]

    # 1a Find proxies used in DSM policies
    dsm_used_proxies = _find_used_proxies(dsm_policies)

    if len(dsm_used_proxies) == 0:
        print("no proxy is used in DSM policies, skipped.")
        return

    print(f"[1a] used proxies: {dsm_used_proxies}")

    # 1b create proxies on C1WS.
    # 1c keep the mapping
    id_mapping = _load_created_proxies_mappings()
    print(f"[1c] mappings of proxies referred by policy settings {id_mapping}")

    if not all(used_id in id_mapping for used_id in dsm_used_proxies):
        print("not all used proxy id are mapped to C1WS")

    # 2a Find proxy usages in DSM policies
    for p in dsm_policies:
        policy_settings = {}
        # 2b collect proxy ids in DSM and map to C1WS id
        try:
            if (
                p["policySettings"][
                    "antiMalwareSettingSmartProtectionGlobalServerUseProxyEnabled"
                ]["value"]
                == "true"
            ):
                c1ws_id = id_mapping[
                    int(
                        p["policySettings"][
                            "platformSettingSmartProtectionAntiMalwareGlobalServerProxyId"
                        ]["value"]
                    )
                ]
                policy_settings[
                    "platformSettingSmartProtectionAntiMalwareGlobalServerProxyId"
                ] = {"value": str(c1ws_id)}
        except (KeyError, AttributeError):
            pass
        try:
            if (
                p["policySettings"][
                    "webReputationSettingSmartProtectionGlobalServerUseProxyEnabled"
                ]["value"]
                == "true"
            ):
                c1ws_id = id_mapping[
                    int(
                        p["policySettings"][
                            "webReputationSettingSmartProtectionWebReputationGlobalServerProxyId"
                        ]["value"]
                    )
                ]
                policy_settings[
                    "webReputationSettingSmartProtectionWebReputationGlobalServerProxyId"
                ] = {"value": str(c1ws_id)}
        except (KeyError, AttributeError):
            pass
        try:
            if (
                p["policySettings"][
                    "platformSettingSmartProtectionGlobalServerUseProxyEnabled"
                ]["value"]
                == "true"
            ):
                c1ws_id = id_mapping[
                    int(
                        p["policySettings"][
                            "platformSettingSmartProtectionGlobalServerProxyId"
                        ]["value"]
                    )
                ]
                policy_settings["platformSettingSmartProtectionGlobalServerProxyId"] = {
                    "value": str(c1ws_id)
                }
        except (KeyError, AttributeError):
            pass

        if len(policy_settings) > 0:
            # 2c if there are proxy referring settings, look up policy mapping
            c1ws_policy_id = utility.get_c1ws_policy_id(int(p["ID"]), migration_task_response)

            # 2d update c1ws policy
            print(f"[2d] update Policy {c1ws_policy_id} for \n {policy_settings}")
            policy_data = {"policySettings": policy_settings}
            c1ws_api_config.update_policy(c1ws_policy_id, policy_data)
