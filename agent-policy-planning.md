# Planning for adding Agent Migration

Create a workload security link (check to see if I'll have to replace the `workloadSecurityCA` below):

```python
def create_c1ws_link():
    url = dsm_endpoint + "/workloadsecuritylinks"

    payload = json.dumps({
    "workloadSecurityUrl": "app.deepsecurity.trendmicro.com",
    "workloadSecurityAPIKey": c1ws_api_key,
    "workloadSecurityCA": "-----BEGIN CERTIFICATE-----\nMIIEPjCCAyagAwIBAgIESlOMKDANBgkqhkiG9w0BAQsFADCBvjELMAkGA1UEBhMC\nVVMxFjAUBgNVBAoTDUVudHJ1c3QsIEluYy4xKDAmBgNVBAsTH1NlZSB3d3cuZW50\ncnVzdC5uZXQvbGVnYWwtdGVybXMxOTA3BgNVBAsTMChjKSAyMDA5IEVudHJ1c3Qs\nIEluYy4gLSBmb3IgYXV0aG9yaXplZCB1c2Ugb25seTEyMDAGA1UEAxMpRW50cnVz\ndCBSb290IENlcnRpZmljYXRpb24gQXV0aG9yaXR5IC0gRzIwHhcNMDkwNzA3MTcy\nNTU0WhcNMzAxMjA3MTc1NTU0WjCBvjELMAkGA1UEBhMCVVMxFjAUBgNVBAoTDUVu\ndHJ1c3QsIEluYy4xKDAmBgNVBAsTH1NlZSB3d3cuZW50cnVzdC5uZXQvbGVnYWwt\ndGVybXMxOTA3BgNVBAsTMChjKSAyMDA5IEVudHJ1c3QsIEluYy4gLSBmb3IgYXV0\naG9yaXplZCB1c2Ugb25seTEyMDAGA1UEAxMpRW50cnVzdCBSb290IENlcnRpZmlj\nYXRpb24gQXV0aG9yaXR5IC0gRzIwggEiMA0GCSqGSIb3DQEBAQUAA4IBDwAwggEK\nAoIBAQC6hLZy254Ma+KZ6TABp3bqMriVQRrJ2mFOWHLP/vaCeb9zYQYKpSfYs1/T\nRU4cctZOMvJyig/3gxnQaoCAAEUesMfnmr8SVycco2gvCoe9amsOXmXzHHfV1IWN\ncCG0szLni6LVhjkCsbjSR87kyUnEO6fe+1R9V77w6G7CebI6C1XiUJgWMhNcL3hW\nwcKUs/Ja5CeanyTXxuzQmyWC48zCxEXFjJd6BmsqEZ+pCm5IO2/b1BEZQvePB7/1\nU1+cPvQXLOZprE4yTGJ36rfo5bs0vBmLrpxR57d+tVOxMyLlbc9wPBr64ptntoP0\njaWvYkxN4FisZDQSA/i2jZRjJKRxAgMBAAGjQjBAMA4GA1UdDwEB/wQEAwIBBjAP\nBgNVHRMBAf8EBTADAQH/MB0GA1UdDgQWBBRqciZ60B7vfec7aVHUbI2fkBJmqzAN\nBgkqhkiG9w0BAQsFAAOCAQEAeZ8dlsa2eT8ijYfThwMEYGprmi5ZiXMRrEPR9RP/\njTkrwPK9T3CMqS/qF8QLVJ7UG5aYMzyorWKiAHarWWluBh1+xLlEjZivEtRh2woZ\nRkfz6/djwUAFQKXSt/S1mja/qYh2iARVBCuch38aNzx+LaUa2NSJXsq9rD1s2G2v\n1fN2D807iDginWyTmsQ9v4IbZT+mD12q/OWyFcq1rca8PdCE6OoGcrBNOTJ4vz4R\nnAuknZoh8/CbCzB428Hch0P+vGOaysXCHMnHjf87ElgI5rY97HosTvuDls4MPGmH\nVHOkc8KT/1EQrBVUAdj8BbGJoX90g5pJ19xOe4pIb4tF9g==\n-----END CERTIFICATE-----\n"
    })
    headers = {
    'api-version': 'v1',
    'Content-Type': 'application/json',
    'api-secret-key': ds_api_key
    }
    try:
        response = requests.post(url, headers=headers, data=payload, verify=False)
        ans = json.loads(response.text)
        logger.info("c1ws link:" + str(ans) + "\n")
    except Exception as e:
        logger.error(e)
        exit()
```

Somehow filter the list of agents and the policies attached, creating a list of tuples of form `(computer IDs to Move, old_policy_id)`

Then, transform `old_policy_id` to `new_policy_id` using the hard work you've done earlier in the program. Although, perhaps write some backup logic that remaps policy ids based on name? Just in case they want to make it modular/the policy part fails.

Create computer move tasks using the tuples generated above:

```python
def create_movetask(computerID, policyID):
    url = dsm_endpoint + "/computermovetasks"
    DSA_ID = computerID
    POLICY_ID = policyID

    payload = json.dumps({
    "computerID": DSA_ID,
    "workloadSecurityPolicyID": POLICY_ID,
    "moveState": "move-requested"
    })
    headers = {
    'api-version': 'v1',
    'Content-Type': 'application/json',
    'api-secret-key': ds_api_key
    }

    response = requests.post(url, headers=headers, data=payload, verify=False)
    ans = json.loads(response.text)
    logger.info("ID" + str(DSA_ID) + ":" + str(ans))
```

Then tie it all together in a module
