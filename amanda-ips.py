import requests
import json
import csv
from datetime import date
from zeep.client import Client
from requests import Session
from zeep.transports import Transport
from datetime import datetime
from zeep import helpers

# AUTHENTICATION
# api_key = ''
tenant = ""
username = ""
password = ""

hostname = "app.deepsecurity.trendmicro.com"

session = Session()
session.verify = True
transport = Transport(session=session, timeout=1800)
url = "https://{0}/webservice/Manager?WSDL".format(hostname)
client = Client(url, transport=transport)
factory = client.type_factory("ns0")

sID = client.service.authenticateTenant(
    tenantName=tenant, username=username, password=password
)

response = client.service.DPIRuleRetrieveAll(sID)
print(response)

client.service.endSession(sID)
