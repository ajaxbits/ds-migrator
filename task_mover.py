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
api_instance = deepsecurity.ScheduledTasksApi(deepsecurity.ApiClient(configuration))
api_version = user_config["original_api_version"]

try:
    task_list = api_instance.list_scheduled_tasks(api_version).scheduled_tasks
except ApiException as e:
    print(
        "an exception occurred when calling scheduledtasksapi.list_scheduled_tasks: %s\n"
        % e
    )

# change context
configuration.host = f"{user_config['new_hostname']}:{user_config['new_port']}/api"
configuration.api_key["api-secret-key"] = user_config["new_api_secret_key"]
api_version = user_config["new_api_version"]

for old_task in task_list:
    try:
        api_response = api_instance.create_scheduled_task(old_task, api_version)
    except ApiException as e:
        print(
            "an exception occurred when calling scheduledtasksapi.list_scheduled_tasks: %s\n"
            % e
        )
