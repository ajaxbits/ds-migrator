import os
import sys
import datetime
import time
import requests
import urllib3
import traceback
from functions.ListAllPolicy import ListAllPolicy
from functions.GetPolicy import GetPolicy
from functions.AMconfigtenant1 import AMconfigtenant1
from functions.CreateandReplaceAMConfigTenant2 import AmconfigTenant2, AmReplaceConfig
from functions.AMCheckandRename import AmConfigCheck, RenameAmConfig
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


def am_validate_create(
    allofpolicy, antimalwareconfig, allamconfig, amdirectorylist, amalldirectorynew, amfileextentionlist, amallfileextentionnew, amfilelist, amallfilelistnew, NEW_HOST, NEW_API_KEY
):
    mod_allamconfig = AmConfigCheck(
        allamconfig,
        amdirectorylist,
        amalldirectorynew,
        amfileextentionlist,
        amallfileextentionnew,
        amfilelist,
        amallfilelistnew,
    )

    allamconfig = RenameAmConfig(allamconfig)

    allamconfignew = AmconfigTenant2(allamconfig, NEW_HOST, NEW_API_KEY)

    aop_replace_am_configs = AmReplaceConfig(
        allofpolicy, antimalwareconfig, allamconfignew
    )
    final = aop_replace_am_configs
    return final
