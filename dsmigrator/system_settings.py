import sys
import os
import requests
import urllib3
import json
from dsmigrator.api_config import SystemSettingsApiInstance
from deepsecurity.rest import ApiException

cert = False


def ListSettings(url_link_final, tenant1key):
    payload = {}
    url = url_link_final + "api/systemsettings"
    headers = {
        "api-secret-key": tenant1key,
        "api-version": "v1",
        "Content-Type": "application/json",
    }
    response = requests.request("GET", url, headers=headers, data=payload, verify=cert)
    describe = str(response.text)
    settings_dict = json.loads(describe)
    # print(settings_dict)
    return settings_dict


no_fly_list = [
    "platformSettingAgentInitiatedActivationToken",
    "platformSettingApiSoapWebServiceEnabled",
    "platformSettingApiStatusMonitoringEnabled",
    "platformSettingAzureSsoCertificate",
    "platformSettingContentSecurityPolicy",
    "platformSettingContentSecurityPolicyReportOnlyEnabled",
    "platformSettingHttpPublicKeyPinPolicy",
    "platformSettingHttpPublicKeyPinPolicyReportOnlyEnabled",
    "platformSettingHttpStrictTransportEnabled",
    "platformSettingLoadBalancerHeartbeatAddress",
    "platformSettingLoadBalancerHeartbeatPort",
    "platformSettingLoadBalancerManagerAddress",
    "platformSettingLoadBalancerManagerPort",
    "platformSettingLoadBalancerRelayAddress",
    "platformSettingLoadBalancerRelayPort",
    "platformSettingLogoBinaryImageImg",
    "platformSettingNewTenantDownloadSecurityUpdateEnabled",
    "platformSettingPrimaryTenantAllowTenantAddVmwareVcenterEnabled",
    "platformSettingPrimaryTenantAllowTenantConfigureForgotPasswordEnabled",
    "platformSettingPrimaryTenantAllowTenantConfigureRememberMeOptionEnabled",
    "platformSettingPrimaryTenantAllowTenantConfigureSiemEnabled",
    "platformSettingPrimaryTenantAllowTenantConfigureSnmpEnabled",
    "platformSettingPrimaryTenantAllowTenantConfigureSnsEnabled",
    "platformSettingPrimaryTenantAllowTenantControlImpersonationEnabled",
    "platformSettingPrimaryTenantAllowTenantDatabaseState",
    "platformSettingPrimaryTenantAllowTenantRunComputerDiscoveryEnabled",
    "platformSettingPrimaryTenantAllowTenantRunPortScanEnabled",
    "platformSettingPrimaryTenantAllowTenantSyncWithCloudAccountEnabled",
    "platformSettingPrimaryTenantAllowTenantSynchronizeLdapDirectoriesEnabled",
    "platformSettingPrimaryTenantAllowTenantUseDefaultRelayGroupEnabled",
    "platformSettingPrimaryTenantAllowTenantUseScheduledRunScriptTaskEnabled",
    "platformSettingPrimaryTenantLockAndHideTenantDataPrivacyOptionEnabled",
    "platformSettingPrimaryTenantLockAndHideTenantSmtpTabEnabled",
    "platformSettingPrimaryTenantLockAndHideTenantStorageTabEnabled",
    "platformSettingPrimaryTenantShareConnectedThreatDefensesEnabled",
    "platformSettingPrimaryTenantShareManagedDetectResponsesEnabled",
    "platformSettingProductUsageDataCollectionEnabled",
    "platformSettingProxyManagerCloudProxyId",
    "platformSettingProxyManagerUpdateProxyId",
    "platformSettingRecommendationCpuUsageLevel",
    "platformSettingRetainServerLogDuration",
    "platformSettingSamlServiceProviderCertificate",
    "platformSettingSamlServiceProviderCertificateExpiryWarningDays",
    "platformSettingSamlServiceProviderEntityId",
    "platformSettingSamlServiceProviderName",
    "platformSettingSamlServiceProviderPrivateKey",
    "platformSettingSignInPageMessage",
    "platformSettingTenantProtectionUsageMonitoringComputerId1",
    "platformSettingTenantProtectionUsageMonitoringComputerId2",
    "platformSettingTenantProtectionUsageMonitoringComputerId3",
    "platformSettingUpdateAgentSoftwareUseDownloadCenterOnMissingDeepSecurityManagerEnabled",
    "platformSettingUpdateImportedSoftwareAutoDownloadEnabled",
    "platformSettingUserEnforceTermsAndConditionsEnabled",
    "platformSettingUserEnforceTermsAndConditionsMessage",
    "platformSettingUserEnforceTermsAndConditionsTitle",
    "platformSettingVmwareNsxManagerNode",
    "platformSettingDsmAsXbcAgentFeatureEnabled",
    "platformSettingUpgradeOnActivationEnabled",
    "firewallSettingGlobalStatefulConfigId",
]


def TransferSettings(settings_dict, no_fly_list, stateful_dict, tenant2key):
    print("Transferring system settings...", flush=True)
    sanitized_settings_dict = {}
    for setting, value_dict in settings_dict.items():
        if setting not in no_fly_list:
            sanitized_settings_dict[setting] = value_dict
    try:
        SystemSettingsApiInstance(tenant2key).modify(sanitized_settings_dict)
    except ApiException as e:
        print(e.body)
        pass


def settings_transfer(
    OLD_HOST, OLD_API_KEY, NEW_HOST, NEW_API_KEY, stateful_dict, no_fly_list=no_fly_list
):
    settings_dict = ListSettings(OLD_HOST, OLD_API_KEY)
    TransferSettings(settings_dict, no_fly_list, stateful_dict, NEW_API_KEY)
