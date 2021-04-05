import os
import sys
import datetime
import deepsecurity
import time
import requests
import urllib3
import traceback
import logging
import click
from datetime import datetime
from tasks import ebt_listmaker, st_listmaker

if __name__ == "__main__":
    allst = [
        '{"name":"Daily Check for Security Updates","type":"check-for-security-updates","scheduleDetails":{"timeZone":"UTC","recurrenceType":"daily","dailyScheduleParameters":{"startTime":1617309600000,"frequencyType":"everyday"}},"enabled":true,"lastRunTime":1617593801747,"nextRunTime":1617655200000,"checkForSecurityUpdatesTaskParameters":{"computerFilter":{"type":"all-computers"},"timeout":"never"},"ID":7}',
        '{"name":"Daily Check for Software Updates","type":"check-for-software-updates","scheduleDetails":{"timeZone":"UTC","recurrenceType":"daily","dailyScheduleParameters":{"startTime":1617309600000,"frequencyType":"everyday"}},"enabled":true,"lastRunTime":1617593801747,"nextRunTime":1617655200000,"ID":8}',
        '{"name":"Daily Discover Computers","type":"discover-computers","scheduleDetails":{"timeZone":"UTC","recurrenceType":"daily","dailyScheduleParameters":{"startTime":1617638100000,"frequencyType":"everyday"}},"enabled":true,"lastRunTime":1617638140971,"nextRunTime":1617724500000,"discoverComputersTaskParameters":{"discoveryType":"range","scanDiscoveredComputers":false,"resolveIPs":true,"computerGroupID":0,"iprangeLow":"10.0.1.1","iprangeHigh":"10.0.1.254"},"ID":13}',
        '{"name":"Weekly Check for Security Updates","type":"check-for-security-updates","scheduleDetails":{"timeZone":"UTC","recurrenceType":"weekly","weeklyScheduleParameters":{"startTime":1617638100000,"interval":1,"days":["monday"]}},"enabled":true,"lastRunTime":1617638140971,"nextRunTime":1618242900000,"checkForSecurityUpdatesTaskParameters":{"computerFilter":{"type":"all-computers"},"timeout":"never"},"ID":14}',
        '{"name":"Hourly Check for Security Updates","type":"check-for-security-updates","scheduleDetails":{"timeZone":"UTC","recurrenceType":"hourly","hourlyScheduleParameters":{"minutesPastTheHour":"55"}},"enabled":true,"lastRunTime":1617648951780,"nextRunTime":1617652500000,"checkForSecurityUpdatesTaskParameters":{"computerFilter":{"type":"all-computers"},"timeout":"never"},"ID":15}',
        '{"name":"Monthly Check for Security Updates","type":"check-for-security-updates","scheduleDetails":{"timeZone":"UTC","recurrenceType":"monthly","monthlyScheduleParameters":{"startTime":1617638100000,"frequencyType":"day-of-month","dayOfMonth":5,"months":["january","feburary","march","april","may","june","july","august","september","october","november","december"]}},"enabled":true,"lastRunTime":1617638140971,"nextRunTime":1620230100000,"checkForSecurityUpdatesTaskParameters":{"computerFilter":{"type":"all-computers"},"timeout":"never"},"ID":16}',
        '{"name":"Once Only Check for Security Updates","type":"check-for-security-updates","scheduleDetails":{"timeZone":"UTC","recurrenceType":"none","onceOnlyScheduleParameters":{"startTime":1617638100000}},"enabled":true,"lastRunTime":1617638140971,"checkForSecurityUpdatesTaskParameters":{"computerFilter":{"type":"all-computers"},"timeout":"never"},"ID":17}',
        '{"name":"Hourly Check for Software Updates","type":"check-for-software-updates","scheduleDetails":{"timeZone":"UTC","recurrenceType":"hourly","hourlyScheduleParameters":{"minutesPastTheHour":"55"}},"enabled":true,"lastRunTime":1617648951780,"nextRunTime":1617652500000,"ID":18}',
        '{"name":"Weekly Check for Software Updates","type":"check-for-software-updates","scheduleDetails":{"timeZone":"UTC","recurrenceType":"weekly","weeklyScheduleParameters":{"startTime":1617638400000,"interval":1,"days":["monday"]}},"enabled":true,"lastRunTime":1617638448153,"nextRunTime":1618243200000,"ID":19}',
        '{"name":"Monthly Check for Software Updates","type":"check-for-software-updates","scheduleDetails":{"timeZone":"UTC","recurrenceType":"monthly","monthlyScheduleParameters":{"startTime":1617638400000,"frequencyType":"day-of-month","dayOfMonth":5,"months":["january","feburary","march","april","may","june","july","august","september","october","november","december"]}},"enabled":true,"lastRunTime":1617638448153,"nextRunTime":1620230400000,"ID":20}',
        '{"name":"Once Only Check for Software Updates","type":"check-for-software-updates","scheduleDetails":{"timeZone":"UTC","recurrenceType":"none","onceOnlyScheduleParameters":{"startTime":1617638400000}},"enabled":true,"lastRunTime":1617638448153,"ID":21}',
        '{"name":"Once Only Check for Software Updates 22","type":"check-for-software-updates","scheduleDetails":{"timeZone":"UTC","recurrenceType":"none","onceOnlyScheduleParameters":{"startTime":1617638400000}},"enabled":true,"lastRunTime":1617638448153,"ID":22}',
        '{"name":"Daily Send Policy","type":"send-policy","scheduleDetails":{"timeZone":"UTC","recurrenceType":"daily","dailyScheduleParameters":{"startTime":1617644100000,"frequencyType":"everyday"}},"enabled":true,"lastRunTime":1617644148643,"nextRunTime":1617730500000,"sendPolicyTaskParameters":{"computerFilter":{"type":"computers-in-group-or-subgroup","computerGroupID":1}},"ID":27}',
        '{"name":"supr Discover Computers","type":"discover-computers","scheduleDetails":{"timeZone":"UTC","recurrenceType":"daily","dailyScheduleParameters":{"startTime":1617644400000,"frequencyType":"everyday"}},"enabled":true,"lastRunTime":1617644428312,"nextRunTime":1617730800000,"discoverComputersTaskParameters":{"discoveryType":"range","scanDiscoveredComputers":false,"resolveIPs":true,"computerGroupID":1,"iprangeLow":"10.0.1.1","iprangeHigh":"10.0.1.254"},"ID":28}',
        '{"name":"Daily Scan Computers for Integrity Changes","type":"scan-for-integrity-changes","scheduleDetails":{"timeZone":"UTC","recurrenceType":"daily","dailyScheduleParameters":{"startTime":1617644400000,"frequencyType":"everyday"}},"enabled":true,"lastRunTime":1617644428312,"nextRunTime":1617730800000,"scanForIntegrityChangesTaskParameters":{"computerFilter":{"type":"computers-using-policy-or-subpolicy","policyID":1},"trustedComputers":"trusted-computers-only"},"ID":29}',
        '{"name":"Daily Scan Computers for Integrity Changes_2","type":"scan-for-integrity-changes","scheduleDetails":{"timeZone":"UTC","recurrenceType":"daily","dailyScheduleParameters":{"startTime":1617644400000,"frequencyType":"everyday"}},"enabled":true,"lastRunTime":1617644428312,"nextRunTime":1617730800000,"scanForIntegrityChangesTaskParameters":{"computerFilter":{"type":"computers-in-group-or-subgroup","computerGroupID":1},"trustedComputers":"trusted-computers-only"},"ID":30}',
    ]
    computer_group_dict = {1: 6, 0: 0}
    policy_dict = {
        1: 443,
        2: 444,
        3: 445,
        4: 446,
        5: 447,
        6: 448,
        7: 449,
        8: 450,
        9: 451,
        10: 452,
        11: 453,
    }

    OLD_HOST = os.environ.get("ORIGINAL_URL")
    OLD_API_KEY = os.environ.get("ORIGINAL_API_KEY")
    NEW_API_KEY = os.environ.get("CLOUD_ONE_API_KEY")
    NEW_HOST = "https://cloudone.trendmicro.com"
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    st_listmaker(
        policy_dict, computer_group_dict, OLD_HOST, OLD_API_KEY, NEW_HOST, NEW_API_KEY
    )
