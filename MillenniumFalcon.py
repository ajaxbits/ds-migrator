import requests
import json
import logging
from logging import getLogger, StreamHandler, FileHandler, Formatter

"""

Before running this script, you need to enable the forwarding of system events to Amazon SNS in the C1WS configuration.
Then, change the parameters in the <SETTINGS> section to suit your environment.

CAUTION!!: Do not edit anything except <SETTINGS> section.

"""

# xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx#
# xxxxxxxxxxxxxxxxxxxx <SETTINGS> xxxxxxxxxxxxxxxxxxxxxx#
# xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx#

dsm_fqdn = "<CHANGEME>"
ds_api_key = "<CHANGEME>"
c1ws_api_key = "<CHANGEME>"

# xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx#

# logging
logger = getLogger("Falcon")
logger.setLevel(logging.DEBUG)

# log stream
stream_handler = StreamHandler()
stream_handler.setLevel(logging.INFO)
handler_format = Formatter("%(asctime)s [%(levelname)s] - %(message)s")
stream_handler.setFormatter(handler_format)
logger.addHandler(stream_handler)

# log file output
file_handler = FileHandler("MillenniumFalcon.log", "a")
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(handler_format)
logger.addHandler(file_handler)

requests.packages.urllib3.disable_warnings()
dsm_endpoint = "https://" + dsm_fqdn + "/api"
c1ws_endpoint = "https://cloudone.trendmicro.com/api/"
target_tag_list = ["Splunk", "DSA3", "DSA4"]
migrate_list = []
logo = """
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

___  ____ _ _                  _                ______    _                 
|  \/  (_) | |                (_)               |  ___|  | |                
| .  . |_| | | ___ _ __  _ __  _ _   _ _ __ ___ | |_ __ _| | ___ ___  _ __  
| |\/| | | | |/ _ \ '_ \| '_ \| | | | | '_ ` _ \|  _/ _` | |/ __/ _ \| '_ \ 
| |  | | | | |  __/ | | | | | | | |_| | | | | | | || (_| | | (_| (_) | | | |
\_|  |_/_|_|_|\___|_| |_|_| |_|_|\__,_|_| |_| |_\_| \__,_|_|\___\___/|_| |_|
                                                                            
                                                                            
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
"""


def list_system_settings():
    url = c1ws_endpoint + "systemsettings/platformSettingEventForwardingSnsEnabled"

    headers = {"api-version": "v1", "api-secret-key": c1ws_api_key}

    try:
        response = requests.get(url, headers=headers, verify=False)
        if response.status_code != 200:
            logger.error("[C1WS API]" + str(response.status_code))
            exit()
        ans = json.loads(response.text)
        logger.debug(ans)
        logger.info("[OK]List System Settings api call succeeded")
        return ans
    except Exception as e:
        logger.error(e)
        exit()


def check_sns_setting(json_response):
    sets = json_response
    try:
        sns_settring = sets["value"]
        if sns_settring == "true":
            logger.info("[OK]Find Amazon SNS setting")
            pass
        else:
            logger.warning("You need to setup C1WS Amzon SNS setting\n")
            exit()
    except KeyError:
        logger.warning("cannot find Amzon SNS setting on your C1WS!")
        logger.error(KeyError)
        exit()
    except Exception as e:
        logger.error(e)
        exit()


def check_aws_account():
    arn = "arn:aws:iam::"
    url = c1ws_endpoint + "/awsconnectors"
    headers = {"api-version": "v1", "api-secret-key": c1ws_api_key}

    try:
        response = requests.get(url, headers=headers, verify=False)
        ans = json.loads(response.text)
        res = ans["awsConnectors"][0]["crossAccountRoleArn"]
        logger.debug(res)
        if arn in res:
            logger.info("[OK]Find AWS Connector")
            print("\n")
            return
    except IndexError:
        logger.info("cannot find AWS connector setting on your C1WS!")
        logger.error(IndexError)
        print("\n")
        exit()
    except Exception as e:
        logger.error(e)
        print("\n")
        exit()


def list_computers():
    url = dsm_endpoint + "/computers?expand=ec2VirtualMachineSummary"
    headers = {"api-version": "v1", "api-secret-key": ds_api_key}
    try:
        response = requests.get(url, headers=headers, verify=False)
        if response.status_code != 200:
            logger.error("[Deep Security API]" + str(response.status_code))
            exit()
        ans = json.loads(response.text)
        logger.debug(ans)
        logger.info("[OK]List Computers api call succeeded")
        return ans
    except Exception as e:
        logger.error(e)
        exit()


def filter(json_response):
    kick = json_response
    comps = kick["computers"]

    try:
        for x in comps:
            displayName = x["displayName"]
            DSA_id = x["ID"]
            if displayName in target_tag_list:
                migrate_list.append(DSA_id)
            else:
                pass
    except KeyError:
        logger.error("cannot find target!")
    except Exception as e:
        logger.error(e)
        exit()


def create_c1ws_link():
    url = dsm_endpoint + "/workloadsecuritylinks"

    payload = json.dumps(
        {
            "workloadSecurityUrl": "app.deepsecurity.trendmicro.com",
            "workloadSecurityAPIKey": c1ws_api_key,
            "workloadSecurityCA": "-----BEGIN CERTIFICATE-----\nMIIEPjCCAyagAwIBAgIESlOMKDANBgkqhkiG9w0BAQsFADCBvjELMAkGA1UEBhMC\nVVMxFjAUBgNVBAoTDUVudHJ1c3QsIEluYy4xKDAmBgNVBAsTH1NlZSB3d3cuZW50\ncnVzdC5uZXQvbGVnYWwtdGVybXMxOTA3BgNVBAsTMChjKSAyMDA5IEVudHJ1c3Qs\nIEluYy4gLSBmb3IgYXV0aG9yaXplZCB1c2Ugb25seTEyMDAGA1UEAxMpRW50cnVz\ndCBSb290IENlcnRpZmljYXRpb24gQXV0aG9yaXR5IC0gRzIwHhcNMDkwNzA3MTcy\nNTU0WhcNMzAxMjA3MTc1NTU0WjCBvjELMAkGA1UEBhMCVVMxFjAUBgNVBAoTDUVu\ndHJ1c3QsIEluYy4xKDAmBgNVBAsTH1NlZSB3d3cuZW50cnVzdC5uZXQvbGVnYWwt\ndGVybXMxOTA3BgNVBAsTMChjKSAyMDA5IEVudHJ1c3QsIEluYy4gLSBmb3IgYXV0\naG9yaXplZCB1c2Ugb25seTEyMDAGA1UEAxMpRW50cnVzdCBSb290IENlcnRpZmlj\nYXRpb24gQXV0aG9yaXR5IC0gRzIwggEiMA0GCSqGSIb3DQEBAQUAA4IBDwAwggEK\nAoIBAQC6hLZy254Ma+KZ6TABp3bqMriVQRrJ2mFOWHLP/vaCeb9zYQYKpSfYs1/T\nRU4cctZOMvJyig/3gxnQaoCAAEUesMfnmr8SVycco2gvCoe9amsOXmXzHHfV1IWN\ncCG0szLni6LVhjkCsbjSR87kyUnEO6fe+1R9V77w6G7CebI6C1XiUJgWMhNcL3hW\nwcKUs/Ja5CeanyTXxuzQmyWC48zCxEXFjJd6BmsqEZ+pCm5IO2/b1BEZQvePB7/1\nU1+cPvQXLOZprE4yTGJ36rfo5bs0vBmLrpxR57d+tVOxMyLlbc9wPBr64ptntoP0\njaWvYkxN4FisZDQSA/i2jZRjJKRxAgMBAAGjQjBAMA4GA1UdDwEB/wQEAwIBBjAP\nBgNVHRMBAf8EBTADAQH/MB0GA1UdDgQWBBRqciZ60B7vfec7aVHUbI2fkBJmqzAN\nBgkqhkiG9w0BAQsFAAOCAQEAeZ8dlsa2eT8ijYfThwMEYGprmi5ZiXMRrEPR9RP/\njTkrwPK9T3CMqS/qF8QLVJ7UG5aYMzyorWKiAHarWWluBh1+xLlEjZivEtRh2woZ\nRkfz6/djwUAFQKXSt/S1mja/qYh2iARVBCuch38aNzx+LaUa2NSJXsq9rD1s2G2v\n1fN2D807iDginWyTmsQ9v4IbZT+mD12q/OWyFcq1rca8PdCE6OoGcrBNOTJ4vz4R\nnAuknZoh8/CbCzB428Hch0P+vGOaysXCHMnHjf87ElgI5rY97HosTvuDls4MPGmH\nVHOkc8KT/1EQrBVUAdj8BbGJoX90g5pJ19xOe4pIb4tF9g==\n-----END CERTIFICATE-----\n",
        }
    )
    headers = {
        "api-version": "v1",
        "Content-Type": "application/json",
        "api-secret-key": ds_api_key,
    }
    try:
        response = requests.post(url, headers=headers, data=payload, verify=False)
        ans = json.loads(response.text)
        logger.info("c1ws link:" + str(ans) + "\n")
    except Exception as e:
        logger.error(e)
        exit()


def list_policies():
    url = c1ws_endpoint + "policies"

    headers = {"api-version": "v1", "api-secret-key": c1ws_api_key}

    try:
        response = requests.get(url, headers=headers, verify=False)
        ans = json.loads(response.text)
        logger.debug(ans)
        return ans
    except Exception as e:
        logger.error(e)
        exit()


def filter_policies(json_response):
    kick = json_response
    pols = kick["policies"]

    try:
        for x in pols:
            pol_name = x["name"]
            pol_id = x["ID"]
            target_pol = "Challenge_Policy"
            if pol_name == target_pol:
                return pol_id
            else:
                pass
    except KeyError:
        logger.error("cannot find Challenge_Policy!")
    except Exception as e:
        logger.error(e)
        exit()


def check_policy(id):
    url = c1ws_endpoint + "policies/" + str(id) + "?overrides=false"
    headers = {"api-version": "v1", "api-secret-key": c1ws_api_key}

    try:
        response = requests.get(url, headers=headers, verify=False)
        ans = json.loads(response.text)
        logger.debug(ans)

        # Security Module Status
        AM = ans["antiMalware"]["moduleStatus"]["status"]
        WRS = ans["webReputation"]["moduleStatus"]["status"]
        ACM = ans["activityMonitoring"]["moduleStatus"]["status"]
        FW = ans["firewall"]["moduleStatus"]["status"]
        IPS = ans["intrusionPrevention"]["moduleStatus"]["status"]
        IM = ans["integrityMonitoring"]["moduleStatus"]["status"]
        LI = ans["logInspection"]["moduleStatus"]["status"]
        AC = ans["applicationControl"]["moduleStatus"]["status"]

        # Policy Settings
        WRS_SecurityLevel = ans["policySettings"]["webReputationSettingSecurityLevel"][
            "value"
        ]

        if AM != "active":
            logger.warning(
                "The AM setting in Challenge_Policy is incorrect. Check the document for the challenge, please."
            )
            exit()
        elif WRS != "active":
            logger.warning(
                "The WRS setting in Challenge_Policy is incorrect. Check the document for the challenge, please."
            )
            exit()
        elif WRS_SecurityLevel != "Medium":
            mes = "Challenge_Policy WRS Security Level is " + WRS_SecurityLevel
            logger.info(mes)
            logger.warning(
                "The WRS setting in Challenge_Policy is incorrect. Check the document for the challenge, please."
            )
            exit()
        elif ACM != "inactive":
            logger.warning(
                "The Activity Monitoring setting in Challenge_Policy is incorrect. Check the document for the challenge, please."
            )
            exit()
        elif FW != "inactive":
            logger.warning(
                "The Firewall setting in Challenge_Policy is incorrect. Check the document for the challenge, please."
            )
            exit()
        elif IPS != "active":
            logger.warning(
                "The IPS setting in Challenge_Policy is incorrect. Check the document for the challenge, please."
            )
            exit()
        elif IM != "inactive":
            logger.warning(
                "The Integrity Monitoring setting in Challenge_Policy is incorrect. Check the document for the challenge, please."
            )
            exit()
        elif LI != "inactive":
            logger.warning(
                "The Log Inspection setting in Challenge_Policy is incorrect. Check the document for the challenge, please."
            )
            exit()
        elif AC != "inactive":
            logger.warning(
                "The Application Control setting in Challenge_Policy is incorrect. Check the document for the challenge, please."
            )
            exit()
        else:
            logger.info("Challenge_Policy check finish" + "\n")
            return
    except KeyError:
        logger.error("cannot find module keys!")
        exit()
    except Exception as e:
        logger.error(e)
        exit()


def create_movetask(computerID, policyID):
    url = dsm_endpoint + "/computermovetasks"
    DSA_ID = computerID
    POLICY_ID = policyID

    payload = json.dumps(
        {
            "computerID": DSA_ID,
            "workloadSecurityPolicyID": POLICY_ID,
            "moveState": "move-requested",
        }
    )
    headers = {
        "api-version": "v1",
        "Content-Type": "application/json",
        "api-secret-key": ds_api_key,
    }

    response = requests.post(url, headers=headers, data=payload, verify=False)
    ans = json.loads(response.text)
    logger.info("ID" + str(DSA_ID) + ":" + str(ans))


def main():
    print(logo)
    logger.info("START!!")
    print("\n")

    # check c1ws sns and AWS connector setting
    print(">>>STEP.0. C1WS SNS/AWS connector Check...")
    c1ws_settings = list_system_settings()
    check_sns_setting(c1ws_settings)
    # check aws connector
    check_aws_account()

    # search target
    print(">>>STEP1. DSM List Computers...")
    res = list_computers()
    filter(res)
    logger.info("migration target DSA ID list: " + str(migrate_list))
    if migrate_list == []:
        logger.warning("Do Nothing!")
        exit()
    else:
        print("\n")

    # search policy
    print(">>>STEP2. List Policies...")
    policies = list_policies()
    challege_pol = filter_policies(policies)
    logger.info("target policy ID: " + str(challege_pol))
    if challege_pol is None:
        logger.warning("cannot find Challenge_Policy")
        exit()
    check_policy(challege_pol)

    # create link
    print(">>>STEP3. Create a Workload Security Link...")
    create_c1ws_link()

    # move task
    print(">>>STEP4. Create a Computer Move Task...")
    for x in migrate_list:
        create_movetask(x, challege_pol)


if __name__ == "__main__":
    main()
