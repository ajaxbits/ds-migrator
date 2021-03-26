from DirFileExtRenListTenant1 import (
    DirListTenant1,
    FileExtensionListTenant1,
    FileListTenant1,
    RenameLists,
)
from DirFileExtListTenant2 import (
    DirListTenant2,
    FileExtensionListTenant2,
    FileListTenant2,
)
from PortListGetT1CreateT2 import PortListGet, PortListCreate
from MACListGetT1CreateT2 import MacListGet, MacListCreate
from IPListGetT1CreateT2 import IpListGet, IpListCreate
from StatefulGetT1CreateT2 import StatefulGet, StatefulCreate
from ListGetCreateEBT import ListEventTask, GetEventTask, CreateEventTask
from ListGetCreateST import (
    ListScheduledTask,
    GetScheduledTask,
    CreateScheduledTask,
)


def directory_listmaker(
    amdirectorylist,
    amfileextensionlist,
    amfilelist,
    OLD_HOST,
    OLD_API_KEY,
):
    og_alldirectory = DirListTenant1(amdirectorylist, OLD_HOST, OLD_API_KEY)
    og_allfileextension = FileExtensionListTenant1(
        amfileextensionlist, OLD_HOST, OLD_API_KEY
    )
    og_allfilelist = FileListTenant1(amfilelist, OLD_HOST, OLD_API_KEY)

    alldirectory, allfilelist, allfileextension = RenameLists(
        og_alldirectory, og_allfilelist, og_allfileextension
    )

    amalldirectorynew = DirListTenant2(alldirectory)
    amallfileextensionnew = FileExtensionListTenant2(allfileextension)
    amallfilelistnew = FileListTenant2(allfilelist)

    return (
        amalldirectorynew,
        amallfileextensionnew,
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


def stateful_listmaker(OLD_HOST, OLD_API_KEY, NEW_HOST, NEW_API_KEY):
    t1statefulall, t1statefulname, t1statefulid = StatefulGet(OLD_HOST, OLD_API_KEY)
    t2statefulid = StatefulCreate(t1statefulall, t1statefulname, NEW_HOST, NEW_API_KEY)
    return t1statefulall, t1statefulname, t1statefulid, t2statefulid


def ebt_listmaker(OLD_HOST, OLD_API_KEY, NEW_HOST, NEW_API_KEY):
    enum_oldetname, etIDs = ListEventTask(OLD_HOST, OLD_API_KEY)
    allet, nameet = GetEventTask(etIDs, OLD_HOST, OLD_API_KEY)
    CreateEventTask(allet, nameet, NEW_HOST, NEW_API_KEY)


def st_listmaker(OLD_HOST, OLD_API_KEY, NEW_HOST, NEW_API_KEY):
    enum_oldstname, stIDs = ListScheduledTask(OLD_HOST, OLD_API_KEY)
    allst, namest = GetScheduledTask(stIDs, OLD_HOST, OLD_API_KEY)
    CreateScheduledTask(allst, namest, NEW_HOST, NEW_API_KEY)
