import os
import sys
import datetime
import time
import requests
import urllib3
import traceback
from functions.DirFileExtRenListTenant1 import (
    DirListTenant1,
    FileExtensionListTenant1,
    FileListTenant1,
    RenameLists,
)
from functions.DirFileExtListTenant2 import (
    DirListTenant2,
    FileExtensionListTenant2,
    FileListTenant2,
)
from functions.PortListGetT1CreateT2 import PortListGet, PortListCreate
from functions.MACListGetT1CreateT2 import MacListGet, MacListCreate
from functions.IPListGetT1CreateT2 import IpListGet, IpListCreate


def directory_listmaker(
    amdirectorylist,
    amfileextentionlist,
    amfilelist,
    OLD_HOST,
    OLD_API_KEY,
    NEW_HOST,
    NEW_API_KEY,
):
    og_alldirectory = DirListTenant1(amdirectorylist, OLD_HOST, OLD_API_KEY)
    og_allfileextention = FileExtensionListTenant1(
        amfileextentionlist, OLD_HOST, OLD_API_KEY
    )
    og_allfilelist = FileListTenant1(amfilelist, OLD_HOST, OLD_API_KEY)

    alldirectory, allfilelist, allfileextention = RenameLists(
        og_alldirectory, og_allfilelist, og_allfileextention
    )

    amalldirectorynew = DirListTenant2(alldirectory, NEW_HOST, NEW_API_KEY)
    amallfileextentionnew = FileExtensionListTenant2(
        allfileextention, NEW_HOST, NEW_API_KEY
    )
    amallfilelistnew = FileListTenant2(allfileextention, NEW_HOST, NEW_API_KEY)

    return (
        amalldirectorynew,
        amallfileextentionnew,
        amallfilelistnew,
    )


def port_listmaker(
    OLD_HOST,
    OLD_API_KEY,
    NEW_HOST,
    NEW_API_KEY,
):
    t1portlistall, t1portlistname, t1portlistid = PortListGet(OLD_HOST, OLD_API_KEY)
    t2portlistid = PortListCreate(t1portlistall, t1portlistname, NEW_HOST, NEW_API_KEY)
    return (t1portlistall, t1portlistname, t1portlistid, t2portlistid)


def mac_listmaker(OLD_HOST, OLD_API_KEY, NEW_HOST, NEW_API_KEY):
    t1maclistall, t1maclistname, t1maclistid = MacListGet(OLD_HOST, OLD_API_KEY)
    t2maclistid = MacListCreate(t1maclistid, t1maclistname, NEW_HOST, NEW_API_KEY)
    return t1maclistall, t1maclistname, t1maclistid, t2maclistid


def ip_listmaker(OLD_HOST, OLD_API_KEY, NEW_HOST, NEW_API_KEY):
    t1iplistall, t1iplistname, t1iplistid = IpListGet(OLD_HOST, OLD_API_KEY)
    t2iplistid = IpListCreate(t1iplistid, t1iplistname, NEW_HOST, NEW_API_KEY)
    return t1iplistall, t1iplistname, t1iplistid, t2iplistid
