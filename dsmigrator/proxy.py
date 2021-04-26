import sys
import os
import time
from time import sleep
import requests
import urllib3
import urllib3
import json
from dsmigrator.logging import console, log


def proxy_edit(allofpolicy, t1iplistid, t2iplistid, t1portlistid, t2portlistid):
    if allofpolicy:
        for count, describe in enumerate(allofpolicy):
            policyjson = json.loads(describe)
            if (
                "true"
                in policyjson["policySettings"][
                    "antiMalwareSettingSmartProtectionGlobalServerUseProxyEnabled"
                ]["value"]
            ):
                policyjson["policySettings"][
                    "antiMalwareSettingSmartProtectionGlobalServerUseProxyEnabled"
                ]["value"] = "false"

            if (
                "true"
                in policyjson["policySettings"][
                    "webReputationSettingSmartProtectionGlobalServerUseProxyEnabled"
                ]["value"]
            ):
                policyjson["policySettings"][
                    "webReputationSettingSmartProtectionGlobalServerUseProxyEnabled"
                ]["value"] = "false"

            if (
                "true"
                in policyjson["policySettings"][
                    "platformSettingSmartProtectionGlobalServerUseProxyEnabled"
                ]["value"]
            ):
                policyjson["policySettings"][
                    "platformSettingSmartProtectionGlobalServerUseProxyEnabled"
                ]["value"] = "false"

            policyjson["policySettings"][
                "platformSettingSmartProtectionAntiMalwareGlobalServerProxyId"
            ]["value"] = ""
            policyjson["policySettings"][
                "webReputationSettingSmartProtectionWebReputationGlobalServerProxyId"
            ]["value"] = ""
            policyjson["policySettings"][
                "platformSettingSmartProtectionGlobalServerProxyId"
            ]["value"] = ""

            here = policyjson["policySettings"][
                "firewallSettingReconnaissanceExcludeIpListId"
            ]["value"]
            if here:
                if here != "NONE":
                    indexnum = t1iplistid.index(here)
                    policyjson["policySettings"][
                        "firewallSettingReconnaissanceExcludeIpListId"
                    ]["value"] = t2iplistid[indexnum]

            here = policyjson["policySettings"][
                "firewallSettingReconnaissanceIncludeIpListId"
            ]["value"]
            if here:
                if here != "NONE":
                    indexnum = t1iplistid.index(here)
                    policyjson["policySettings"][
                        "firewallSettingReconnaissanceIncludeIpListId"
                    ]["value"] = t2iplistid[indexnum]

            here = policyjson["policySettings"][
                "firewallSettingEventLogFileIgnoreSourceIpListId"
            ]["value"]
            if here:
                if here != "NONE":
                    indexnum = t1iplistid.index(here)
                    try:
                        policyjson["policySettings"][
                            "firewallSettingEventLogFileIgnoreSourceIpListId"
                        ]["value"] = t2iplistid[indexnum]
                    except Exception as e:
                        log.exception(e)
                        log.error(
                            f"Error in policy settings transfer for firewall event exceptions for {policyjson.get('name')}. Transfer will continue, but double check after transfer."
                        )
                        pass

            here = policyjson["policySettings"][
                "webReputationSettingMonitorPortListId"
            ]["value"]
            if here:
                if here != "80,8080":
                    indexnum = t1portlistid.index(here)
                    policyjson["policySettings"][
                        "webReputationSettingMonitorPortListId"
                    ]["value"] = t2portlistid[indexnum]
            allofpolicy[count] = json.dumps(policyjson)
    return allofpolicy
