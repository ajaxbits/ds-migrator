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

def
# Directory Lists
# NOTE that only lists that are attached to am configs will be transferred
og_alldirectory = DirListTenant1(directorylist, OLD_HOST, OLD_API_KEY)
og_allfileextention = FileExtensionListTenant1(fileextentionlist, OLD_HOST, OLD_API_KEY)
og_allfilelist = FileListTenant1(filelist, OLD_HOST, OLD_API_KEY)

alldirectory, allfilelist, allfileextention = RenameLists(
    og_alldirectory, og_allfilelist, og_allfileextention
)

alldirectorynew = DirListTenant2(alldirectory, NEW_HOST, NEW_API_KEY)
allfileextentionnew = FileExtensionListTenant2(allfileextention, NEW_HOST, NEW_API_KEY)
allfilelistnew = FileListTenant2(allfileextention, NEW_HOST, NEW_API_KEY)


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
