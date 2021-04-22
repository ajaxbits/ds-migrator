import os
import sys
import datetime
import deepsecurity
import time
import requests
import urllib3
import traceback
import logging
import click
from datetime import datetime
import dsmigrator.api_config
from dsmigrator.policies import (
    ListAllPolicy,
    GetPolicy,
    AddPolicy,
    delete_cloud_one_policies,
)
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
    context_listmaker,
    schedule_listmaker,
)
from dsmigrator.tasks import ebt_listmaker, st_listmaker
from dsmigrator.computer_groups import computer_group_listmaker
from dsmigrator.system_settings import settings_transfer
import yaml


class Logger(object):
    def flush(self):
        pass

    def __init__(self):
        self.terminal = sys.stdout
        filename = datetime.now().strftime("migrator_%H_%M_%d_%m_%Y.log")
        self.log = open(f"./{filename}", "a")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)


# override the click invoke method
def CommandWithConfigFile(config_file_param_name):
    class CustomCommandClass(click.Command):
        def invoke(self, ctx):
            config_file = ctx.params[config_file_param_name]
            if config_file is not None:
                with open(config_file) as f:
                    config_data = yaml.safe_load(f)
                    for param, value in ctx.params.items():
                        if value is None and param in config_data:
                            ctx.params[param] = config_data[param]
                            ctx.params[param].prompt = None

            return super(CustomCommandClass, self).invoke(ctx)

    return CustomCommandClass


@click.command(cls=CommandWithConfigFile("config_file"))
@click.option("--config-file", type=click.Path(), is_eager=True)
@click.option(
    "-ou",
    "--original-url",
    prompt="Old DSM url",
    help="A resolvable FQDN for the old DSM, with port number (e.g. https://192.168.1.1:4119)",
    envvar="ORIGINAL_URL",
)
@click.option(
    "-oa",
    "--original-api-key",
    prompt="Old DSM API key",
    help="API key for the old DSM with Full Access permissions",
    envvar="ORIGINAL_API_KEY",
)
@click.option(
    "-nu",
    "--new-url",
    default="https://cloudone.trendmicro.com/",
    show_default=True,
    help="Destination url",
)
@click.option(
    "-coa",
    "--cloud-one-api-key",
    prompt="New Cloud One API key",
    help="API key for Cloud One Workload Security with Full Access permissions",
    envvar="CLOUD_ONE_API_KEY",
)
@click.option(
    "-d",
    "--delete-policies/--keep-policies",
    is_flag=True,
    default=False,
    prompt="Do you want to wipe existing policies in Cloud One? (not required, but will give best results)",
    help="Wipes existing policies in Cloud One (not required, but will give best results)",
)
@click.option(
    "-t",
    "--tasks",
    is_flag=True,
    help="(BETA) Enable the task migrator (may be buggy)",
)
@click.option(
    "-k",
    "--insecure",
    is_flag=True,
    help="Suppress the InsecureRequestWarning for self-signed certificates",
)
@click.option(
    "-c",
    "--cert",
    default=False,
    show_default=True,
    help="(Optional) Allows the use of a cert file",
)
def main(
    config_file,
    original_url,
    original_api_key,
    new_url,
    cloud_one_api_key,
    cert,
    insecure,
    tasks,
    delete_policies,
):
    """Moves your on-prem DS deployment to the cloud!"""
    sys.stdout = Logger()
    sys.stderr = sys.stdout

    OLD_API_KEY = original_api_key
    OLD_HOST = original_url
    NEW_API_KEY = cloud_one_api_key
    NEW_HOST = new_url

    if insecure:
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    if delete_policies:
        delete_cloud_one_policies(NEW_API_KEY)

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
        NEW_API_KEY,
    )

    t1portlistall, t1portlistname, t1portlistid, t2portlistid = port_listmaker(
        OLD_HOST, OLD_API_KEY, NEW_HOST, NEW_API_KEY
    )
    t1maclistall, t1maclistname, t1maclistid, t2maclistid = mac_listmaker(
        OLD_HOST, OLD_API_KEY, NEW_HOST, NEW_API_KEY
    )
    t1iplistall, t1iplistname, t1iplistid, t2iplistid = ip_listmaker(
        OLD_HOST, OLD_API_KEY, NEW_HOST, NEW_API_KEY
    )
    (
        t1statefulall,
        t1statefulname,
        t1statefulid,
        t2statefulid,
        stateful_dict,
    ) = stateful_listmaker(OLD_HOST, OLD_API_KEY, NEW_HOST, NEW_API_KEY)
    t1contextid, t2contextid = context_listmaker(
        OLD_HOST, OLD_API_KEY, NEW_HOST, NEW_API_KEY
    )
    t1scheduleid, t2scheduleid = schedule_listmaker(
        OLD_HOST, OLD_API_KEY, NEW_HOST, NEW_API_KEY
    )

    print(stateful_dict)
    try:
        settings_transfer(OLD_HOST, OLD_API_KEY, NEW_HOST, NEW_API_KEY, stateful_dict)
    except Exception:
        pass

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
    policy_dict = AddPolicy(allofpolicy, NEW_API_KEY)
    if tasks:
        computer_group_dict = computer_group_listmaker(
            OLD_HOST, OLD_API_KEY, NEW_HOST, NEW_API_KEY
        )
        ebt_listmaker(
            policy_dict,
            computer_group_dict,
            OLD_HOST,
            OLD_API_KEY,
            NEW_HOST,
            NEW_API_KEY,
        )
        st_listmaker(
            policy_dict,
            computer_group_dict,
            OLD_HOST,
            OLD_API_KEY,
            NEW_HOST,
            NEW_API_KEY,
        )


if __name__ == "__main__":
    main()  # pylint: disable=no-value-for-parameter
