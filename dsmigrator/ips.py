import json
from typing import Dict, List

import requests
import urllib3
from deepsecurity.rest import ApiException
from nested_lookup import nested_lookup, nested_update

from dsmigrator.api_config import (
    ApplicationTypesApiInstance,
    IntrusionPreventionApiInstance,
)

from dsmigrator.logging import log

from dsmigrator.migrator_utils import (
    validate_create,
    validate_create_dict,
    validate_create_dict_custom,
)

cert = False


def ips_rules_transform(
    allofpolicy,
    t1portlistid,
    t2portlistid,
    t1scheduleid,
    t2scheduleid,
    t1contextid,
    t2contextid,
    OLD_HOST,
    OLD_API_KEY,
    NEW_HOST,
    NEW_API_KEY,
):
    og_ipsruleid_dict = IPSGet(allofpolicy)
    og_ipsappid_dict = IPSappGet(allofpolicy)

    ipsappid_dict, ipscustomapp_dict = IPSappDescribe(
        og_ipsappid_dict,
        t1portlistid,
        t2portlistid,
        OLD_HOST,
        NEW_HOST,
        OLD_API_KEY,
        NEW_API_KEY,
    )

    ipsruleid_dict, ipscustomrule_dict = IPSDescribe(
        og_ipsruleid_dict,
        t1scheduleid,
        t2scheduleid,
        t1contextid,
        t2contextid,
        ipsappid_dict,
        ipscustomapp_dict,
        OLD_HOST,
        OLD_API_KEY,
        NEW_HOST,
        NEW_API_KEY,
    )

    aop_replace_ips_apps = IPSappReplace(allofpolicy, ipsappid_dict, ipscustomapp_dict)
    aop_replace_ips_rules = IPSReplace(
        aop_replace_ips_apps, ipsruleid_dict, ipscustomrule_dict
    )
    return aop_replace_ips_rules


def IPSappGet(allofpolicy: List[str]) -> Dict[int, None]:
    """
    Parses allofpolicy and returns an IPS app skeleton dict

    Args:
        allofpolicy (List[str]): allofpolicy list of json strings

    Returns:
        Dict[int, None]: ips app id dict, with oldids, ready to be matched with new ids
    """
    ipsappid = []
    for describe in allofpolicy:
        namejson = json.loads(describe)
        if "applicationTypeIDs" in namejson["intrusionPrevention"]:
            for assigned_app_id in namejson["intrusionPrevention"][
                "applicationTypeIDs"
            ]:
                ipsappid.append(assigned_app_id)
    ipsappid_dict = dict.fromkeys(ipsappid)
    log.info("IPS application types in Tenant 1:")
    log.info(ipsappid)
    return ipsappid_dict


def IPSappDescribe(
    ipsappid_dict,
    t1portlistid,
    t2portlistid,
    url_link_final,
    url_link_final_2,
    tenant1key,
    tenant2key,
):
    allipsapp = []
    allipsappname = []
    allipscustomapp = []
    ipsapp_api_instance = ApplicationTypesApiInstance(tenant2key)

    log.info("Searching IPS application types in Tenant 1...")
    if ipsappid_dict:
        for count, name in enumerate(list(ipsappid_dict.keys())):
            payload = {}
            url = url_link_final + "api/applicationtypes/" + str(name)
            headers = {
                "api-secret-key": tenant1key,
                "api-version": "v1",
                "Content-Type": "application/json",
            }
            response = requests.request(
                "GET",
                url,
                headers=headers,
                data=payload,
                verify=cert,
            )
            describe = str(response.text)
            try:
                ipsappjson = json.loads(describe)
                allipsappname.append(str(ipsappjson["name"]))
                log.info(
                    "#"
                    + str(count)
                    + " IPS Application Type name: "
                    + str(ipsappjson["name"]),
                )
                old_port_list_id = ipsappjson.get("portListID")
                if old_port_list_id is not None:
                    indexnum = t1portlistid.index(str(old_port_list_id))
                    ipsappjson["portListID"] = t2portlistid[indexnum]
                allipsapp.append(json.dumps(ipsappjson))
                log.info(
                    "#"
                    + str(count)
                    + " IPS Application Type ID: "
                    + str(ipsappjson["ID"]),
                )
            except:

                log.info(describe)
    log.info("Done!")
    log.info("Searching and Modifying IPS application types in Tenant 2...")

    allipscustomapp = []
    for (count, object) in enumerate(allipsapp):
        namecheck = 1
        rename = 1
        object_json = json.loads(object)
        old_id = object_json["ID"]
        old_name = object_json["name"]
        while namecheck != -1:
            try:
                new_id = ipsapp_api_instance.search(old_name)
                if new_id is not None:
                    ipsappid_dict[old_id] = new_id
                    log.info(
                        f"#{str(count)} IPS Application Type: {old_name}",
                    )
                else:
                    allipscustomapp.append(json.dumps(object_json))
                namecheck = -1
            except ApiException as e:
                if "already exists" in e.body:
                    log.info(f"{old_name} already exists in new tenant, renaming...")
                    object_json["name"] = old_name + " {" + str(rename) + "}"
                    rename = rename + 1
                else:
                    log.info(e.body)
                    pass
    log.info("Done!")
    if allipscustomapp:
        ipscustomapp_dict = validate_create_dict(
            allipscustomapp, ipsapp_api_instance, "IPS Custom App"
        )
    else:
        ipscustomapp_dict = {}
    log.info("Done!")
    return ipsappid_dict, ipscustomapp_dict


def IPSappReplace(allofpolicy, ipsappid_dict, ipscustomapp_dict):
    for count, policy in enumerate(allofpolicy):
        policyjson = json.loads(policy)
        if "applicationTypeIDs" in policyjson["intrusionPrevention"]:
            all_ipsapp_ids_list = policyjson["intrusionPrevention"][
                "applicationTypeIDs"
            ]
            for index, ipsapp_id in enumerate(all_ipsapp_ids_list):
                new_ipsapp_id = ipsappid_dict.get(ipsapp_id)
                new_ipscustomapp_id = ipscustomapp_dict.get(ipsapp_id)
                if new_ipsapp_id is not None:
                    all_ipsapp_ids_list[index] = new_ipsapp_id
                elif new_ipscustomapp_id is not None:
                    all_ipsapp_ids_list[index] = new_ipscustomapp_id
        allofpolicy[count] = json.dumps(policyjson)
    return allofpolicy


def IPSGet(allofpolicy):
    # Takes in allofpolicy and creates a skeleton id dict
    ipsruleid = []
    for describe in allofpolicy:
        namejson = json.loads(describe)
        if "ruleIDs" in namejson["intrusionPrevention"]:
            for assigned_rule_id in namejson["intrusionPrevention"]["ruleIDs"]:
                ipsruleid.append(assigned_rule_id)
    ipsruleid_dict = dict.fromkeys(ipsruleid)
    log.info("IPS rules in Tenant 1:")
    log.info(ipsruleid)
    return ipsruleid_dict


def IPSDescribe(
    ipsruleid_dict,
    t1scheduleid,
    t2scheduleid,
    t1contextid,
    t2contextid,
    ips_appid_dict,
    ipscustomapp_dict,
    url_link_final,
    tenant1key,
    url_link_final_2,
    tenant2key,
):
    allipsrule = []
    allipsrulename = []
    ipsrule_api_instance = IntrusionPreventionApiInstance(tenant2key)
    log.info("Searching IPS rules in Tenant 1...")

    if ipsruleid_dict:
        for count, dirlist in enumerate(list(ipsruleid_dict.keys())):
            payload = {}
            url = url_link_final + "api/intrusionpreventionrules/" + str(dirlist)
            headers = {
                "api-secret-key": tenant1key,
                "api-version": "v1",
                "Content-Type": "application/json",
            }
            response = requests.request(
                "GET",
                url,
                headers=headers,
                data=payload,
                verify=cert,
            )
            describe = str(response.text)
            try:
                ipsjson = json.loads(describe)
                allipsrulename.append(str(ipsjson["name"]))
                log.info(
                    "#" + str(count) + " IPS Rule name: " + str(ipsjson["name"]),
                )
                old_appid = ipsjson.get("applicationTypeID")
                new_premade_appid = ips_appid_dict.get(old_appid)
                new_custom_appid = ipscustomapp_dict.get(old_appid)
                if new_premade_appid is not None:
                    ipsjson["applicationTypeID"] = new_premade_appid
                elif new_custom_appid is not None:
                    ipsjson["applicationTypeID"] = new_custom_appid
                if "scheduleID" in ipsjson:
                    indexnum = t1scheduleid.index(str(ipsjson["scheduleID"]))
                    ipsjson["scheduleID"] = t2scheduleid[indexnum]
                if "contextID" in ipsjson:
                    indexnum = t1contextid.index(str(ipsjson["contextID"]))
                    ipsjson["contextID"] = t2contextid[indexnum]

                log.info("#" + str(count) + " IPS Rule ID: " + str(ipsjson["ID"]))
                allipsrule.append(json.dumps(ipsjson))
            except:
                log.info(describe)

    log.info("Done!")
    log.info("Searching and Modifying IPS rule in Tenant 2...")
    ipsruleid_dict, allipscustomrule = validate_create_dict_custom(
        allipsrule, ipsruleid_dict, ipsrule_api_instance, "IPS Rule"
    )
    if allipscustomrule:
        ipscustomrule_dict = validate_create_dict(
            allipscustomrule, ipsrule_api_instance, "IPS Custom Rule"
        )
    else:
        ipscustomrule_dict = {}
    log.info("Done!")
    return ipsruleid_dict, ipscustomrule_dict


def IPSReplace(
    allofpolicy: List[str],
    ipsruleid_dict: Dict[int, int],
    ipscustomrule_dict: Dict[int, int],
) -> List[str]:
    """
    Takes in the rule dictionaries for custom and predefined rules and transforms allofpolicy to match1

    Args:
        allofpolicy (List[str]): list of json strings representing policies
        ipsruleid_dict (Dict[int, int]): mapping of oldid:newid for ipsrules
        ipscustomrule_dict (Dict[int, int]): mapping of oldid:newid for ips custom rules

    Returns:
        List[str]: allofpolicy with ips rule ids modified
    """
    for count, policy in enumerate(allofpolicy):
        policyjson = json.loads(policy)
        if "ruleIDs" in policyjson["intrusionPrevention"]:
            all_ips_rule_ids_list = policyjson["intrusionPrevention"]["ruleIDs"]
            for index, ipsrule_id in enumerate(all_ips_rule_ids_list):
                new_ipsrule_id = ipsruleid_dict.get(ipsrule_id)
                new_ipscustomrule_id = ipscustomrule_dict.get(ipsrule_id)
                if new_ipsrule_id is not None:
                    all_ips_rule_ids_list[index] = new_ipsrule_id
                elif new_ipscustomrule_id is not None:
                    all_ips_rule_ids_list[index] = new_ipscustomrule_id
                else:
                    all_ips_rule_ids_list.remove(ipsrule_id)
                    log.warning(f"Removing ips rule {ipsrule_id} as outlined earlier.")
        allofpolicy[count] = json.dumps(policyjson)
    return allofpolicy
