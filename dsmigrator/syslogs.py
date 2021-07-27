import json
import os

import dsmigrator.api as api
import dsmigrator.migrator_utils as utility

syslog_config_keys = [
    "activityMonitoringSettingSyslogConfigId",
    "antiMalwareSettingSyslogConfigId",
    "applicationControlSettingSyslogConfigId",
    "firewallSettingSyslogConfigId",
    "integrityMonitoringSettingSyslogConfigId",
    "logInspectionSettingSyslogConfigId",
    "webReputationSettingSyslogConfigId",
]


def _find_used_syslog_configs(dsm_policies: list) -> list:
    dsm_used_syslog_config_set = set()

    for p in dsm_policies:
        for key in syslog_config_keys:
            try:
                dsm_used_syslog_config_set.add(int(p["policySettings"][key]["value"]))
            except (KeyError, AttributeError):
                pass
    return list(dsm_used_syslog_config_set)


def _load_created_syslog_config_mappings() -> dict:
    id_mapping = {}
    mapping_file = os.environ["MIG_SYSLOG_MAPPING"]
    with open(mapping_file) as mapping_json:
        mapping = json.load(mapping_json)

    for m in mapping["syslogConfigurations"]:
        id_mapping[int(m["dsmId"])] = int(m["c1wsId"])

    return id_mapping


def do_syslog_configs(dsm_api_config: api.ApiConfig, c1ws_api_config: api.ApiConfig, migration_task_response: dict):

    dsm_policies = dsm_api_config.get_policies()["policies"]

    # 1a Find syslog configs used in DSM policies
    dsm_used_syslog_configs = _find_used_syslog_configs(dsm_policies)

    if len(dsm_used_syslog_configs) == 0:
        print("no syslog config is used in DSM policies, skipped.")
        return

    print(f"[1a] used syslog configs: {dsm_used_syslog_configs}")

    # 1b create syslog config on C1WS.
    # 1c keep the mapping
    id_mapping = _load_created_syslog_config_mappings()
    print(f"[1c] mappings of syslog configs referred by policy settings: {id_mapping}")

    if not all(used_id in id_mapping for used_id in dsm_used_syslog_configs):
        print("not all used syslog config id are mapped to C1WS")

    # 2a Find syslog usages in DSM policies
    for p in dsm_policies:
        policy_settings = {}
        # 2b collect syslog config ids in DSM and map to C1WS id
        for key in syslog_config_keys:
            try:
                c1ws_id = id_mapping[int(p["policySettings"][key]["value"])]
                policy_settings[key] = {"value": str(c1ws_id)}
            except (KeyError, AttributeError):
                pass

        if len(policy_settings) > 0:
            # 2c if there are syslog config referring settings, look up policy mapping
            c1ws_policy_id = utility.get_c1ws_policy_id(int(p["ID"]), migration_task_response)

            # 2d update c1ws policy
            print(f"[2d] update Policy {c1ws_policy_id} for \n {policy_settings}")
            policy_data = {"policySettings": policy_settings}
            c1ws_api_config.update_policy(c1ws_policy_id, policy_data)
