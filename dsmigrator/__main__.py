import datetime
import logging
import os
import sys
import time
import traceback
from datetime import datetime

import click
import deepsecurity
import requests
import urllib3
import yaml
from rich.console import Console, OverflowMethod
from rich.logging import RichHandler
from rich.traceback import install

import dsmigrator.api_config
from dsmigrator.antimalware import am_config_transform, am_validate_create
from dsmigrator.computer_groups import computer_group_listmaker
from dsmigrator.firewall import firewall_config_transform
from dsmigrator.integrity import im_config_transform
from dsmigrator.ips import ips_rules_transform
from dsmigrator.lists import (
    context_listmaker,
    directory_listmaker,
    ip_listmaker,
    mac_listmaker,
    port_listmaker,
    schedule_listmaker,
    stateful_listmaker,
)
from dsmigrator.loginspection import li_config_transform
from dsmigrator.policies import (
    AddPolicy,
    GetPolicy,
    ListAllPolicy,
    delete_cloud_one_policies,
)
from dsmigrator.proxy import proxy_edit
from dsmigrator.system_settings import settings_transfer
from dsmigrator.tasks import ebt_listmaker, st_listmaker

install()

console = Console()


def ascii_art():
    console.print(
        """\
                                                      
              %###################,               
          #############################           
       ######################\\.         `#        
     #################################,    \\      
   #####################################     #    
  #######################################     #   
 ##############  ########################    .##  
(##########(    ########################     ###( 
#####(              ###################     ##### 
######(      ########################     (###### 
 #####       #######################      ########
 ####       ######################      ######### 
  ###       ###################      ############ 
   #        ###############       (#############  
    #         #######.         ###############&   
      \\                   .##################     
        %.          ######################        
           \\###########################           
               ###################               
    """,
        style="bold red",
        overflow="crop",
    )


ascii_art()
console.print(
    "Welcome to the Trend Micro Policy Migration Tool",
    style="bold red",
)


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


def validate_api_keys(ctx, param, api_key):
    try:
        last_equal = api_key[-1] == "="
        first_validation_bit = api_key.split("-")
        last_validation_bit = first_validation_bit[4].split(":")
        clean_list = [i for i in first_validation_bit[0:4]]
        clean_list.append(last_validation_bit[0])
        validate_list = [len(i) for i in clean_list]
        validate_list.append(last_equal)

        if validate_list == [8, 4, 4, 4, 12, True]:
            return api_key
        else:
            raise click.BadParameter(
                "Invalid API key format, please double-check the input."
            )
    except IndexError:
        raise click.BadParameter(
            "Invalid API key format, please double-check the input."
        )


@click.command(cls=CommandWithConfigFile("config_file"))
@click.option("--config-file", type=click.Path(), is_eager=True)
@click.option(
    "-ou",
    "--original-url",
    prompt="Old DSM address and port (e.g. https://10.10.10.10:4119/)",
    help="A resolvable FQDN for the old DSM, with port number (e.g. https://192.168.1.1:4119/)",
    envvar="ORIGINAL_URL",
)
@click.option(
    "-oa",
    "--original-api-key",
    callback=validate_api_keys,
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
        console.rule("Delete C1 Policies")
        delete_cloud_one_policies(NEW_API_KEY)

    old_policy_id_list = ListAllPolicy(OLD_HOST, OLD_API_KEY)

    console.rule("Initial Data Collection")
    antimalwareconfig, allofpolicy = GetPolicy(
        old_policy_id_list, OLD_HOST, OLD_API_KEY
    )

    console.rule("Anti-Malware Configurations")
    amdirectorylist, amfileextensionlist, amfilelist, allamconfig = am_config_transform(
        antimalwareconfig, OLD_HOST, OLD_API_KEY
    )

    console.rule("Lists")
    amalldirectorynew, amallfileextentionnew, amallfilelistnew = directory_listmaker(
        amdirectorylist,
        amfileextensionlist,
        amfilelist,
        OLD_HOST,
        OLD_API_KEY,
        NEW_API_KEY,
    )

    t1portlistid, t2portlistid = port_listmaker(
        OLD_HOST, OLD_API_KEY, NEW_HOST, NEW_API_KEY
    )
    t1maclistid, t2maclistid = mac_listmaker(
        OLD_HOST, OLD_API_KEY, NEW_HOST, NEW_API_KEY
    )
    t1iplistid, t2iplistid = ip_listmaker(OLD_HOST, OLD_API_KEY, NEW_HOST, NEW_API_KEY)
    (
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

    console.rule("DSM Settings")
    settings_transfer(OLD_HOST, OLD_API_KEY, NEW_HOST, NEW_API_KEY, stateful_dict)

    proxy_edit(allofpolicy, t1iplistid, t2iplistid, t1portlistid, t2portlistid)

    # TRANSFORM
    console.rule("Intrusion Prevention Module")
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
    console.rule("Anti-Malware Module")
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
    console.rule("Integrity Monitoring Module")
    allofpolicy = im_config_transform(
        allofpolicy, OLD_HOST, OLD_API_KEY, NEW_HOST, NEW_API_KEY
    )
    console.rule("Log Inspection Module")
    allofpolicy = li_config_transform(
        allofpolicy, OLD_HOST, OLD_API_KEY, NEW_HOST, NEW_API_KEY
    )
    console.rule("Firewall Module")
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
    console.rule("Final Policy Migration")
    policy_dict = AddPolicy(allofpolicy, NEW_API_KEY)
    if tasks:
        console.rule("Tasks")
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
