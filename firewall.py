import os
import sys
import datetime
import time
import requests
import urllib3
import traceback
from functions.ListAllPolicy import ListAllPolicy
from functions.GetPolicy import GetPolicy
from functions.FirewallConfig import (
    FirewallGet,
    FirewallDescribe,
    FirewallCustom,
    FirewallReplace,
)

from ips_rules_transform import ips_rules_transform

OLD_API_KEY = os.environ.get("OLD_API_KEY")
OLD_HOST = os.environ.get("OLD_HOST")
NEW_API_KEY = os.environ.get("NEW_API_KEY")
NEW_HOST = os.environ.get("NEW_HOST")
cert = False

old_policy_name_enum, old_policy_id_list = ListAllPolicy(OLD_HOST, OLD_API_KEY)

antimalwareconfig, og_allofpolicy = GetPolicy(old_policy_id_list, OLD_HOST, OLD_API_KEY)


def firewall_config_transform(
    allofpolicy,
    t1iplistid,
    t2iplistid,
    t1maclistid,
    t2maclistid,
    t1portlistid,
    t2portlistid,
    t1statefulid,
    t2statefulid,
    OLD_HOST,
    OLD_API_KEY,
    NEW_HOST,
    NEW_API_KEY,
):
    firewallruleid, policystateful = FirewallGet(allofpolicy)
    (
        allfirewallrule,
        allfirewallruleidnew1,
        allfirewallruleidold,
        allfirewallcustomrule,
    ) = FirewallDescribe(
        firewallruleid,
        t1iplistid,
        t2iplistid,
        t1maclistid,
        t2maclistid,
        t1portlistid,
        t2portlistid,
        OLD_HOST,
        OLD_API_KEY,
        NEW_HOST,
        NEW_API_KEY,
    )
    allfirewallruleidnew2 = FirewallCustom(
        allfirewallrule, allfirewallcustomrule, NEW_HOST, NEW_API_KEY
    )

    new_allofpolicy = FirewallReplace(
        allofpolicy,
        allfirewallruleidnew1,
        allfirewallruleidnew2,
        firewallruleid,
        allfirewallruleidold,
        allfirewallcustomrule,
        t1statefulid,
        t2statefulid,
    )
    return new_allofpolicy
