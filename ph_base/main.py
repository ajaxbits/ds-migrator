import os
import sys
import datetime
import time
import requests
import urllib3
import traceback
from ips_rules_transform import ips_rules_transform
from functions.ListAllPolicy import ListAllPolicy
from functions.GetPolicy import GetPolicy
from functions.AddPolicytoT2 import AddPolicy

OLD_API_KEY = os.environ.get("OLD_API_KEY")
OLD_HOST = os.environ.get("OLD_HOST")
NEW_API_KEY = os.environ.get("NEW_API_KEY")
NEW_HOST = os.environ.get("NEW_HOST")
cert = False

old_policy_name_enum, old_policy_id_list = ListAllPolicy(OLD_HOST, OLD_API_KEY)

antimalwareconfig, og_allofpolicy = GetPolicy(old_policy_id_list, OLD_HOST, OLD_API_KEY)

# transform_ips
allofpolicy = ips_rules_transform(og_allofpolicy)

AddPolicy(allofpolicy, NEW_HOST, NEW_API_KEY)
