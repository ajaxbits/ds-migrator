from dsmigrator.api_config import (
    DirectoryListsApiInstance,
    FileListsApiInstance,
    FileExtensionListsApiInstance,
)
from dsmigrator.migrator_utils import validate_create


def DirListTenant2(alldirectory):
    print("Creating directory list in tenant 2, if any", flush=True)
    if alldirectory:
        alldirectorynew = validate_create(
            alldirectory, DirectoryListsApiInstance(), "directory"
        )
    print("new directory list", flush=True)
    print(alldirectorynew, flush=True)
    return alldirectorynew


def FileListTenant2(allfile):
    print("Creating file list in tenant 2, if any", flush=True)
    if allfile:
        allfilenew = validate_create(allfile, FileListsApiInstance(), "file")
    print("new file list", flush=True)
    print(allfilenew, flush=True)
    return allfilenew


def FileExtensionListTenant2(allfileext):
    print("Creating file extension list in tenant 2, if any", flush=True)
    if allfileext:
        allfileextnew = validate_create(
            allfileext, FileExtensionListsApiInstance(), "file extension"
        )
        print("new file extension list", flush=True)
        print(allfileextnew, flush=True)
        return allfileextnew
