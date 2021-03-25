import os
import sys
import datetime
import time
import requests
import urllib3
import traceback
from functions.ListAllPolicy import ListAllPolicy
from functions.GetPolicy import GetPolicy
from functions.FirewallConfig import FirewallGet

from ips_rules_transform import ips_rules_transform

OLD_API_KEY = os.environ.get("OLD_API_KEY")
OLD_HOST = os.environ.get("OLD_HOST")
NEW_API_KEY = os.environ.get("NEW_API_KEY")
NEW_HOST = os.environ.get("NEW_HOST")
cert = False

old_policy_name_enum, old_policy_id_list = ListAllPolicy(OLD_HOST, OLD_API_KEY)

antimalwareconfig, og_allofpolicy = GetPolicy(old_policy_id_list, OLD_HOST, OLD_API_KEY)

firewallruleid, policystateful = FirewallGet(og_allofpolicy)

mod_allofpolicy, t1portlistid, t2portlistid = ips_rules_transform(
    og_allofpolicy, OLD_HOST, OLD_API_KEY, NEW_HOST, NEW_API_KEY
)


# def li_config_transform(allofpolicy):
#     aop_replace_li_rules = LIReplace(
#         allofpolicy,
#         allliruleidnew1,
#         allliruleidnew2,
#         liruleid,
#         allliruleidold,
#         alllicustomrule,
#     )
#     final = aop_replace_li_rules
#     return final


# if __name__ == "__main__":
#     li_config_transform(og_allofpolicy)
