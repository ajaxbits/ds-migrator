import os
import sys
import datetime
import time
import requests
import urllib3
import traceback
from functions.ListAllPolicy import ListAllPolicy
from functions.GetPolicy import GetPolicy
from functions.IPSConfig import IPSGet, IPSDescribe, IPSCustom, IPSReplace
from functions.IPSapptypeConfig import (
    IPSappGet,
    IPSappDescribe,
    IPSappCustom,
    IPSappReplace,
)


def ips_rules_transform(
    allofpolicy,
    t1portlistid,
    t2portlistid,
    OLD_HOST,
    OLD_API_KEY,
    NEW_HOST,
    NEW_API_KEY,
):
    og_ipsruleid = IPSGet(allofpolicy)
    og_ipsappid = IPSappGet(allofpolicy)

    allipsapp, allipsappidnew1, allipsappidold, allipscustomapp = IPSappDescribe(
        og_ipsappid,
        t1portlistid,
        t2portlistid,
        OLD_HOST,
        OLD_API_KEY,
        NEW_HOST,
        NEW_API_KEY,
    )

    allipsappidnew2 = IPSappCustom(allipsapp, allipscustomapp, NEW_HOST, NEW_API_KEY)

    allipsrule, allipsruleidnew1, allipsruleidold, allipscustomrule = IPSDescribe(
        og_ipsruleid,
        og_ipsappid,
        allipsappidnew1,
        allipsappidnew2,
        allipsappidold,
        allipscustomapp,
        OLD_HOST,
        OLD_API_KEY,
        NEW_HOST,
        NEW_API_KEY,
    )

    allipsruleidnew2 = IPSCustom(allipsrule, allipscustomrule, NEW_HOST, NEW_API_KEY)

    # 1. Creates a rosetta of rule ids
    # 2. Transfers over custom rules
    # 3. outputs allofpolicy with the replacements
    aop_replace_ips_rules = IPSReplace(
        allofpolicy,
        allipsruleidnew1,
        allipsruleidnew2,
        og_ipsruleid,
        allipsruleidold,
        allipscustomrule,
    )
    aop_replace_ips_apps = IPSappReplace(
        aop_replace_ips_rules,
        allipsappidnew1,
        allipsappidnew2,
        og_ipsappid,
        allipsappidold,
        allipscustomapp,
    )
    final = aop_replace_ips_apps
    return final
