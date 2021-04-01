import unittest
import urllib3
import json
import os
from dsmigrator.lists import *

OLD_API_KEY = os.environ.get("ORIGINAL_API_KEY")
OLD_HOST = os.environ.get("ORIGINAL_URL")
NEW_API_KEY = os.environ.get("CLOUD_ONE_API_KEY")
NEW_HOST = os.environ.get("NEW_URL")
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
cert = False

test_ebt_dict = {
    "eventBasedTasks": [
        {
            "name": "Computer Moved",
            "type": "computer-moved-by-system",
            "enabled": True,
            "actions": [{"type": "deactivate"}],
            "conditions": [{"field": "applianceProtectionActivated", "value": "true"}],
            "ID": 5,
        }
    ]
}


class TestLists(unittest.TestCase):
    def test_listeventtask(self):
        self.assertEqual(
            ListEventTask(OLD_HOST, OLD_API_KEY)[1],
            ["5"],
            "Should be Advanced Real-Time Scan Configuration",
        )
        self.assertEqual.__self__.maxDiff = None


if __name__ == "__main__":
    unittest.main()
