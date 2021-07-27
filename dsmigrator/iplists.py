import requests
import dsmigrator.api as api
import dsmigrator.migrator_utils as utility

ip_list_keys = [
    "firewallSettingReconnaissanceExcludeIpListId",
    "firewallSettingReconnaissanceIncludeIpListId",
    "firewallSettingEventLogFileIgnoreSourceIpListId",
]


def _find_used_ip_lists(dsm_policies: list) -> list:
    dsm_used_ip_set = set()

    for p in dsm_policies:
        for key in ip_list_keys:
            try:
                dsm_used_ip_set.add(int(p["policySettings"][key]["value"]))
            except (KeyError, AttributeError):
                pass
    return list(dsm_used_ip_set)


def _update_or_create_ip_list(
    dsm_used_ip_lists: list,
    dsm_api_config: api.ApiConfig,
    c1ws_api_config: api.ApiConfig,
) -> dict:
    id_mapping = {}
    for id in dsm_used_ip_lists:
        data = dsm_api_config.get_ip_list(id)
        ip_list = None
        if id < 8:  # built-in rules, try update it first
            try:
                ip_list = c1ws_api_config.update_ip_list(id, data)
                id_mapping[id] = id
                print(f"c1ws ip list {id} updated")
            except requests.exceptions.HTTPError:
                pass
        if ip_list is None:  # create the ip list anyway
            try:
                data["name"] += utility.get_suffix()
                ip_list = c1ws_api_config.create_ip_list(data)
                id_mapping[id] = int(ip_list["ID"])
                print(f"c1ws ip list {ip_list['ID']} created for dsm ip list {id}")
            except requests.exceptions.HTTPError:
                pass
    return id_mapping


def do_ip_lists(dsm_api_config: api.ApiConfig, c1ws_api_config: api.ApiConfig, migration_task_response: dict):

    dsm_policies = dsm_api_config.get_policies()["policies"]
    print(dsm_policies)

    # 1a Find IP list IDs used in DSM policies
    dsm_used_ip_lists = _find_used_ip_lists(dsm_policies)

    print(f"[1a] used ip lists: {dsm_used_ip_lists}")

    # 1b update-or-create IP lists on C1WS.
    # 1c keep the mapping
    id_mapping = _update_or_create_ip_list(
        dsm_used_ip_lists, dsm_api_config, c1ws_api_config
    )

    print(f"[1c] mappings of ip lists referred by policy settings: {id_mapping}")

    # 2a Find IP list usages in DSM policies
    for p in dsm_policies:
        policy_settings = {}
        # 2b collect ip list in DSM and map to C1WS id
        for key in ip_list_keys:
            try:
                c1ws_id = id_mapping[int(p["policySettings"][key]["value"])]
                policy_settings[key] = {"value": str(c1ws_id)}
            except (KeyError, AttributeError):
                pass

        if len(policy_settings) > 0:
            # 2c if there are ip list referring settings, look up policy mapping
            c1ws_policy_id = utility.get_c1ws_policy_id(int(p["ID"]), migration_task_response)

            # 2d update c1ws policy
            print(f"[2d] update Policy {c1ws_policy_id} for \n {policy_settings}")
            policy_data = {"policySettings": policy_settings}
            c1ws_api_config.update_policy(c1ws_policy_id, policy_data)
