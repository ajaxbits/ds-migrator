import json

import requests
import urllib3
from deepsecurity.rest import ApiException
from nested_lookup import nested_lookup, nested_update

from dsmigrator.api_config import (
    ApplicationTypesApiInstance,
    IntrusionPreventionApiInstance,
)
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
        OLD_HOST,
        OLD_API_KEY,
        NEW_HOST,
        NEW_API_KEY,
    )

    aop_replace_ips_rules = IPSReplace(allofpolicy, ipsruleid_dict, ipscustomrule_dict)
    aop_replace_ips_apps = IPSappReplace(
        aop_replace_ips_rules, ipsappid_dict, ipscustomapp_dict
    )
    final = aop_replace_ips_apps
    return final


def IPSappGet(allofpolicy):
    # Takes in allofpolicy and creates a skeleton id dict
    ipsappid = []
    for describe in allofpolicy:
        namejson = json.loads(describe)
        if "applicationTypeIDs" in namejson["intrusionPrevention"]:
            for assigned_app_id in namejson["intrusionPrevention"][
                "applicationTypeIDs"
            ]:
                ipsappid.append(assigned_app_id)
    ipsappid_dict = dict.fromkeys(ipsappid)
    print("IPS application types in Tenant 1:", flush=True)
    print(ipsappid, flush=True)
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

    print("Searching IPS application types in Tenant 1...", flush=True)
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
                "GET", url, headers=headers, data=payload, verify=cert
            )
            describe = str(response.text)
            try:
                ipsappjson = json.loads(describe)
                allipsappname.append(str(ipsappjson["name"]))
                print(
                    "#"
                    + str(count)
                    + " IPS Application Type name: "
                    + str(ipsappjson["name"]),
                    flush=True,
                )
                old_port_list_id = ipsappjson.get("portListID")
                if old_port_list_id is not None:
                    indexnum = t1portlistid.index(str(old_port_list_id))
                    ipsappjson["portListID"] = t2portlistid[indexnum]
                allipsapp.append(json.dumps(ipsappjson))
                print(
                    "#" + str(count) + " IPS Application Type ID: " + name, flush=True
                )
            except:
                print(describe)
    print("Done!", flush=True)
    print("Searching and Modifying IPS application types in Tenant 2...", flush=True)
    # add printing to this
    ipsappid_dict, allipscustomapp = validate_create_dict_custom(
        allipsapp, ipsappid_dict, ipsapp_api_instance, "IPS Application Type"
    )
    # for count, ipsapp in enumerate(allipsapp):
    #     namecheck = 1
    #     rename = 1
    #     ipsapp_json = json.loads(ipsapp)
    #     old_ipsapp_id = ipsapp_json["ID"]
    #     old_ipsapp_name = ipsapp_json["name"]
    #     while namecheck != -1:
    #         try:
    #             new_ipsapp_id = ipsapp_api_instance.search(old_ipsapp_name)
    #             if new_ipsapp_id is not None:
    #                 ipsappid_dict[old_ipsapp_id] = new_ipsapp_id
    #                 print(
    #                     "#" + str(count) + " IPS Application Type: " + old_ipsapp_name,
    #                     flush=True,
    #                 )
    #             else:
    #                 allipscustomapp.append(json.dumps(ipsapp_json))
    #             namecheck = -1
    #         except ApiException as e:
    #             if "already exists" in e.body:
    #                 print(
    #                     f"{old_ipsapp_name} already exists in new tenant, renaming..."
    #                 )
    #                 ipsapp_json["name"] = old_ipsapp_name + " {" + str(rename) + "}"
    #                 rename = rename + 1
    #             else:
    #                 print(e.body, flush=True)
    if allipscustomapp:
        ipscustomapp_dict = validate_create_dict(
            allipscustomapp, ipsapp_api_instance, "IPS Custom App"
        )
    print("Done!", flush=True)
    return ipsappid_dict, ipscustomapp_dict


# def IPSappCustom(allipsapp, allipscustomapp, url_link_final_2, tenant2key):
#     allipsappidnew2 = []
#     if allipscustomapp:
#         print("Creating IPS application Type Custom Rule...", flush=True)
#         for count, indexnum in enumerate(allipscustomapp):
#             payload = allipsapp[indexnum]
#             url = url_link_final_2 + "api/applicationtypes"
#             headers = {
#                 "api-secret-key": tenant2key,
#                 "api-version": "v1",
#                 "Content-Type": "application/json",
#             }
#             response = requests.request(
#                 "POST", url, headers=headers, data=payload, verify=cert
#             )
#             describe = str(response.text)
#             index = describe.find('"ID"')
#             if index != -1:
#                 indexpart = describe[index + 4 :]
#                 startIndex = indexpart.find(":")
#                 if startIndex != -1:  # i.e. if the first quote was found
#                     endIndex = indexpart.find("}", startIndex + 1)
#                     if (
#                         startIndex != -1 and endIndex != -1
#                     ):  # i.e. both quotes were found
#                         indexid = indexpart[startIndex + 1 : endIndex]
#                         allipsappidnew2.append(str(indexid))
#                         print(
#                             "#"
#                             + str(count)
#                             + " IPS Application Type ID: "
#                             + str(indexid),
#                             flush=True,
#                         )
#             else:
#                 print(describe, flush=True)
#                 print(payload, flush=True)
#         print("Done!", flush=True)
#     return allipsappidnew2


def IPSappReplace(allofpolicy, ipsappid_dict, ipscustomapp_dict):
    for count, policy in enumerate(allofpolicy):
        policyjson = json.loads(policy)
        if "applicationTypeIDs" in policyjson["intrusionPrevention"]:
            all_ipsapp_ids_list = policyjson["intrusionPrevention"][
                "applicationTypeIDs"
            ]
            for id in all_ipsapp_ids_list:
                new_ipsapp_id = ipsappid_dict.get(id)
                new_ipscustomapp_id = ipscustomapp_dict.get(id)
                if new_ipsapp_id is not None:
                    id = new_ipsapp_id
                elif new_ipscustomapp_id is not None:
                    id = new_ipscustomapp_id
        allofpolicy[count] = json.dumps(policyjson)
    return allofpolicy


def IPSGet(allofpolicy):
    # Takes in allofpolicy and creates a skeleton id dict
    ipsruleid = []
    for describe in allofpolicy:
        namejson = json.loads(describe)
        if "applicationTypeIDs" in namejson["intrusionPrevention"]:
            for assigned_app_id in namejson["intrusionPrevention"][
                "applicationTypeIDs"
            ]:
                ipsruleid.append(assigned_app_id)
    ipsruleid_dict = dict.fromkeys(ipsruleid)
    print("IPS rules in Tenant 1:", flush=True)
    print(ipsruleid, flush=True)
    return ipsruleid_dict


def IPSDescribe(
    ipsruleid_dict,
    t1scheduleid,
    t2scheduleid,
    t1contextid,
    t2contextid,
    url_link_final,
    tenant1key,
    url_link_final_2,
    tenant2key,
):
    allipsrule = []
    allipsrulename = []
    ipsrule_api_instance = IntrusionPreventionApiInstance(tenant2key)
    print("Searching IPS rules in Tenant 1...", flush=True)

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
                "GET", url, headers=headers, data=payload, verify=cert
            )
            describe = str(response.text)
            try:
                ipsjson = json.loads(describe)
                allipsrulename.append(str(ipsjson["name"]))
                print(
                    "#" + str(count) + " IPS Rule name: " + str(ipsjson["name"]),
                    flush=True,
                )
                if "scheduleID" in ipsjson:
                    indexnum = t1scheduleid.index(str(ipsjson["scheduleID"]))
                    ipsjson["scheduleID"] = t2scheduleid[indexnum]
                if "contextID" in ipsjson:
                    indexnum = t1contextid.index(str(ipsjson["contextID"]))
                    ipsjson["contextID"] = t2contextid[indexnum]

                print("#" + str(count) + " IPS Rule ID: " + describe, flush=True)
                allipsrule[count] = json.dumps(ipsjson)
            except:
                print(describe)

            # allipsrule.append(describe)
            # ipsjson = json.loads(describe)
            # allipsrulename.append(str(ipsjson["name"]))
            # print(
            #     "#" + str(count) + " IPS rule name: " + str(ipsjson["name"]), flush=True
            # )
            # index3 = describe.find("applicationTypeID")
            # if index3 != -1:
            #     indexpart = describe[index3 + 17 :]
            #     startIndex = indexpart.find(":")
            #     if startIndex != -1:  # i.e. if the first quote was found
            #         endIndex3 = indexpart.find(",", startIndex + 1)
            #         if (
            #             startIndex != -1 and endIndex3 != -1
            #         ):  # i.e. both quotes were found
            #             indexid1 = indexpart[startIndex + 1 : endIndex3]
            #             checkindex = ipsappid.index(indexid1)
            #             if checkindex in allipsappidold:
            #                 checkindex1 = allipsappidold.index(checkindex)
            #                 replaceid = allipsappidnew1[checkindex1]
            #             elif checkindex in allipscustomapp:
            #                 checkindex1 = allipscustomapp.index(checkindex)
            #                 replaceid = allipsappidnew2[checkindex1]
            #             indexid5 = describe[index3 : index3 + 17 + endIndex3]
            #             listpart = indexid5.replace(indexid1, replaceid)
            #             allipsrule[count] = describe.replace(indexid5, listpart)
            # ipsjson = json.loads(allipsrule[count])
            print("#" + str(count) + " IPS rule ID: " + dirlist, flush=True)
    print("Done!", flush=True)
    print("Searching and Modifying IPS rule in Tenant 2...", flush=True)
    ipsruleid_dict, allipscustomrule = validate_create_dict_custom(
        allipsrule, ipsruleid_dict, ipsrule_api_instance, "IPS Rule"
    )
    # ips_api_instance = IntrusionPreventionApiInstance(tenant2key)
    # for count, dirlist in enumerate(allipsrule):
    #     dirlist = json.loads(dirlist)
    #     try:
    #         rule_id = ips_api_instance.search(dirlist.get("name"))
    #         if dirlist.get("template") is not None:
    #             allipscustomrule.append(json.dumps(dirlist))
    #         else:
    #             allipsruleidnew1.append(str(rule_id))
    #             allipsruleidold.append(count)
    #             print(
    #                 "#" + str(count) + " IPS rule ID: " + str(rule_id),
    #                 flush=True,
    #             )
    #     except ApiException as e:
    #         print(e)
    if allipscustomrule:
        ipscustomrule_dict = validate_create_dict(
            allipscustomrule, ipsrule_api_instance, "IPS Custom Rule"
        )
    print("Done!", flush=True)
    return ipsruleid_dict, ipscustomrule_dict


# def IPSCustom(allipscustomrule, url_link_final_2, tenant2key):
#     allipsruleidnew2 = validate_create(
#         allipscustomrule,
#         IntrusionPreventionApiInstance(tenant2key),
#         "Custom Intrusion Prevention Rule",
#     )
#     print("Done!", flush=True)
#     return allipsruleidnew2


def IPSReplace(allofpolicy, ipsruleid_dict, ipscustomrule_dict):
    for count, policy in enumerate(allofpolicy):
        policyjson = json.loads(policy)
        if "ruleIDs" in policyjson["intrusionPrevention"]:
            all_ips_rule_ids_list = policyjson["intrusionPrevention"]["ruleIDs"]
            for id in all_ips_rule_ids_list:
                new_ipsrule_id = ipsruleid_dict.get(id)
                new_ipscustomrule_id = ipscustomrule_dict.get(id)
                if new_ipsrule_id is not None:
                    id = new_ipsrule_id
                elif new_ipscustomrule_id is not None:
                    id = new_ipscustomrule_id
        allofpolicy[count] = json.dumps(policyjson)
    return allofpolicy

    # for count, policy in enumerate(allofpolicy):
    #     index = policy.find('"intrusionPrevention"')
    #     if index != -1:
    #         indexpart = policy[index + 20 :]
    #         startIndex = indexpart.find("}")
    #         if startIndex != -1:  # i.e. if the first quote was found
    #             endIndex = indexpart.find("}", startIndex + 1)
    #             if startIndex != -1 and endIndex != -1:  # i.e. both quotes were found
    #                 indexid = indexpart[startIndex + 1 : endIndex]
    #                 index2 = indexid.find("ruleIDs")
    #                 if index2 != -1:
    #                     indexpart2 = indexid[index2 + 9 :]
    #                     startIndex2 = indexpart2.find("[")
    #                     if startIndex2 != -1:  # i.e. if the first quote was found
    #                         endIndex2 = indexpart2.find("]", startIndex2 + 1)
    #                         if (
    #                             startIndex2 != -1 and endIndex2 != -1
    #                         ):  # i.e. both quotes were found
    #                             indexid2 = indexpart2[startIndex2 + 1 : endIndex2]
    #                             indexid3 = indexpart2[startIndex2 + 1 : endIndex2]
    #                             indexid2 = indexid2.replace(" ", "")
    #                             indexid4 = indexid2.split(",")
    #                             if allipsruleidnew1 or allipsruleidnew2:
    #                                 for count1, this in enumerate(indexid4):
    #                                     checkindex = ipsruleid.index(this)
    #                                     if checkindex in allipsruleidold:
    #                                         checkindex1 = allipsruleidold.index(
    #                                             checkindex
    #                                         )
    #                                         indexid4[count1] = allipsruleidnew1[
    #                                             checkindex1
    #                                         ]
    #                                     elif checkindex in allipscustomrule:
    #                                         checkindex1 = allipscustomrule.index(
    #                                             checkindex
    #                                         )
    #                                         indexid4[count1] = allipsruleidnew2[
    #                                             checkindex1
    #                                         ]
    #                                 indexid2 = ",".join(indexid4)
    #                             modulepart = policy[index : index + 20 + endIndex]
    #                             modulepart2 = modulepart.replace(indexid3, indexid2)
    #                             allofpolicy[count] = policy.replace(
    #                                 modulepart, modulepart2
    #                             )
    # return allofpolicy
