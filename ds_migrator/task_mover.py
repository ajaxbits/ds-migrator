from __future__ import print_function
import sys, warnings
import deepsecurity
from deepsecurity.rest import ApiException
import json

# Load user config
user_config = json.load(open("./config.json", "r"))

# Setup
if not sys.warnoptions:
    warnings.simplefilter("ignore")
configuration = deepsecurity.Configuration()
configuration.host = (
    f"{user_config['original_hostname']}:{user_config['original_port']}/api"
)

# Authentication
configuration.api_key["api-secret-key"] = user_config["original_api_secret_key"]

# Initialization
# Set Any Required Values
scheduled_api_instance = deepsecurity.ScheduledTasksApi(
    deepsecurity.ApiClient(configuration)
)
event_based_api_instance = deepsecurity.EventBasedTasksApi(
    deepsecurity.ApiClient(configuration)
)
api_version = user_config["original_api_version"]

try:
    scheduled_task_list = scheduled_api_instance.list_scheduled_tasks(
        api_version
    ).scheduled_tasks
    event_based_task_list = event_based_api_instance.list_event_based_tasks(
        api_version
    ).event_based_tasks
except ApiException as e:
    print(e)

# change context
configuration.host = f"{user_config['new_hostname']}:{user_config['new_port']}/api"
configuration.api_key["api-secret-key"] = user_config["new_api_secret_key"]
api_version = user_config["new_api_version"]

# migrate scheduled tasks
for old_task in scheduled_task_list:
    try:
        api_response = scheduled_api_instance.create_scheduled_task(
            old_task, api_version
        )
    except ApiException as e:
        print(
            "an exception occurred when calling scheduledtasksapi.create_scheduled_task: %s\n"
            % e
        )

# migrate event-based tasks
for old_task in event_based_task_list:
    try:
        api_response = event_based_api_instance.create_event_based_task(
            old_task, api_version
        )
    except ApiException as e:
        print(
            "an exception occurred when calling eventbasedtasksapi.create_event_based_task: %s\n"
            % e
        )
