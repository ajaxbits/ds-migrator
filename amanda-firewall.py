#!/usr/bin/env python

from datetime import datetime
from datetime import timedelta
from zeep.client import Client
from requests import Session
from zeep.transports import Transport

hostname = ""
user = ""
pwd = ""
port = 443


def CreateEventIDFilter(factory, id, operator):
    EnumOperator = factory.EnumOperator(operator)
    IDFilterTransport = factory.IDFilterTransport(id=id, operator=EnumOperator)
    return IDFilterTransport


def CreateHostFilter(factory, groupID, hostID, securityProfileID, enumType):
    EnumHostFilter = factory.EnumHostFilterType(enumType)
    HostFilterTransport = factory.HostFilterTransport(
        hostGroupID=groupID,
        hostID=hostID,
        securityProfileID=securityProfileID,
        type=EnumHostFilter,
    )
    return HostFilterTransport


def CreateFileFilter(factory, TimeRangeFrom, TimeRangeTo, TimeSpecific, type):
    Timetype = factory.EnumTimeFilterType(type)
    TimeFilterTransport = factory.TimeFilterTransport(
        rangeFrom=TimeRangeFrom,
        rangeTo=TimeRangeTo,
        specificTime=TimeSpecific,
        type=Timetype,
    )
    return TimeFilterTransport


# Create Zeep session
session = Session()
# False for self signed certs, True for production
session.verify = False
transport = Transport(session=session, timeout=600)
# Get the WSDL from our DSM
url = "https://{0}:{1}/webservice/Manager?WSDL".format(hostname, port)
client = Client(url, transport=transport)
# Build the factory to construct the types for this DSM's WSDL.
factory = client.type_factory("ns0")

# Authenticate to the DSM
sID = client.service.authenticate(username=user, password=pwd)

# This gets all firewall events in the last 7 days from every host
firewallEvent = client.service.firewallEventRetrieve(
    timeFilter=CreateFileFilter(factory, None, None, None, "LAST_7_DAYS"),
    hostFilter=CreateHostFilter(factory, None, None, None, "ALL_HOSTS"),
    eventIdFilter=CreateEventIDFilter(factory, 0, "GREATER_THAN"),
    sID=sID,
)

# Get all events for policy {myPolicy} in the last 6 months
Now = datetime.utcnow()
SixMonthsAgo = Now - timedelta(days=180)
myPolicy = 3
firewallEvent = client.service.firewallEventRetrieve(
    timeFilter=CreateFileFilter(factory, SixMonthsAgo, Now, None, "CUSTOM_RANGE"),
    hostFilter=CreateHostFilter(
        factory, None, None, myPolicy, "HOSTS_USING_SECURITY_PROFILE"
    ),
    eventIdFilter=CreateEventIDFilter(factory, 0, "GREATER_THAN"),
    sID=sID,
)

if firewallEvent != None and firewallEvent.firewallEvents != None:
    print("Policy {0} has been used in the last 6 months".format(myPolicy))
else:
    print("Policy {0} has NOT been used in the last 6 months".format(myPolicy))


# Logout of DSM
client.service.endSession(sID)
