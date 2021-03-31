import os
import sys
import datetime
import time
import requests
import urllib3
import traceback
import logging
from datetime import datetime
import dsmigrator.api_config
from dsmigrator.policies import ListAllPolicy, GetPolicy, AddPolicy
from dsmigrator.proxy import proxy_edit
from dsmigrator.ips import ips_rules_transform
from dsmigrator.antimalware import am_config_transform, am_validate_create
from dsmigrator.integrity import im_config_transform
from dsmigrator.loginspection import li_config_transform
from dsmigrator.firewall import firewall_config_transform
from dsmigrator.lists import (
    directory_listmaker,
    port_listmaker,
    mac_listmaker,
    ip_listmaker,
    stateful_listmaker,
    ebt_listmaker,
    st_listmaker,
    context_listmaker,
    schedule_listmaker,
)


def main(verify=False):
    if verify == False:
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    OLD_API_KEY = os.environ.get("OLD_API_KEY")
    OLD_HOST = os.environ.get("OLD_HOST")
    NEW_API_KEY = os.environ.get("NEW_API_KEY")
    NEW_HOST = os.environ.get("NEW_HOST")
    cert = False

    old_policy_name_enum, old_policy_id_list = ListAllPolicy(OLD_HOST, OLD_API_KEY)

    antimalwareconfig, allofpolicy = GetPolicy(
        old_policy_id_list, OLD_HOST, OLD_API_KEY
    )

    amdirectorylist, amfileextensionlist, amfilelist, allamconfig = am_config_transform(
        antimalwareconfig, OLD_HOST, OLD_API_KEY
    )

    amalldirectorynew, amallfileextentionnew, amallfilelistnew = directory_listmaker(
        amdirectorylist,
        amfileextensionlist,
        amfilelist,
        OLD_HOST,
        OLD_API_KEY,
    )
    print(amalldirectorynew, amallfileextentionnew, amallfilelistnew)

    t1portlistall, t1portlistname, t1portlistid, t2portlistid = port_listmaker(
        OLD_HOST, OLD_API_KEY, NEW_HOST, NEW_API_KEY
    )
    t1maclistall, t1maclistname, t1maclistid, t2maclistid = mac_listmaker(
        OLD_HOST, OLD_API_KEY, NEW_HOST, NEW_API_KEY
    )
    t1iplistall, t1iplistname, t1iplistid, t2iplistid = ip_listmaker(
        OLD_HOST, OLD_API_KEY, NEW_HOST, NEW_API_KEY
    )
    t1statefulall, t1statefulname, t1statefulid, t2statefulid = stateful_listmaker(
        OLD_HOST, OLD_API_KEY, NEW_HOST, NEW_API_KEY
    )
    t1contextid, t2contextid = context_listmaker(
        OLD_HOST, OLD_API_KEY, NEW_HOST, NEW_API_KEY
    )
    t1scheduleid, t2scheduleid = schedule_listmaker(
        OLD_HOST, OLD_API_KEY, NEW_HOST, NEW_API_KEY
    )

    ebt_listmaker(OLD_HOST, OLD_API_KEY, NEW_HOST, NEW_API_KEY)
    st_listmaker(OLD_HOST, OLD_API_KEY, NEW_HOST, NEW_API_KEY)
    proxy_edit(allofpolicy, t1iplistid, t2iplistid, t1portlistid, t2portlistid)

    # TRANSFORM
    allofpolicy = ips_rules_transform(
        allofpolicy,
        t1portlistid,
        t2portlistid,
        t1scheduleid,
        t2scheduleid,
        t1contextid,
        t2contextid,
        OLD_HOST,
        OLD_API_KEY,
        NEW_HOST,
        NEW_API_KEY,
    )
    # print(allofpolicy[1])
    allofpolicy = am_validate_create(
        allofpolicy,
        antimalwareconfig,
        allamconfig,
        amdirectorylist,
        amalldirectorynew,
        amfileextensionlist,
        amallfileextentionnew,
        amfilelist,
        amallfilelistnew,
        NEW_HOST,
        NEW_API_KEY,
    )
    # print(allofpolicy[1])
    allofpolicy = im_config_transform(
        allofpolicy, OLD_HOST, OLD_API_KEY, NEW_HOST, NEW_API_KEY
    )
    allofpolicy = li_config_transform(
        allofpolicy, OLD_HOST, OLD_API_KEY, NEW_HOST, NEW_API_KEY
    )
    allofpolicy = firewall_config_transform(
        allofpolicy,
        t1iplistid,
        t2iplistid,
        t1maclistid,
        t2maclistid,
        t1portlistid,
        t2portlistid,
        t1statefulid,
        t2statefulid,
        t1scheduleid,
        t2scheduleid,
        t1contextid,
        t2contextid,
        OLD_HOST,
        OLD_API_KEY,
        NEW_HOST,
        NEW_API_KEY,
    )

    AddPolicy(allofpolicy)


if __name__ == "__main__":
    main()
    # logger = logging.getLogger()
    # filename = datetime.now().strftime("migrator_%H_%M_%d_%m_%Y.log")
    # out_file_handler = logging.FileHandler(filename)
    # out_file_handler.setLevel(logging.DEBUG)
    # stdout_handler = logging.StreamHandler(sys.stdout)

    # logger.addHandler(out_file_handler)
    # logger.addHandler(stdout_handler)

    # logger.debug(main())
