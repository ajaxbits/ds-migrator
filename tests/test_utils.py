import os
import unittest

import urllib3
from dsmigrator.migrator_utils import safe_request

OLD_API_KEY = os.environ.get("ORIGINAL_API_KEY")
OLD_HOST = os.environ.get("ORIGINAL_URL")
NEW_API_KEY = os.environ.get("CLOUD_ONE_API_KEY")
NEW_HOST = os.environ.get("NEW_URL")
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
cert = False


class TestSafeHttp(unittest.TestCase):
    def test_basic_connection(self):
        response = safe_request(
            OLD_API_KEY, "GET", url=f"{OLD_HOST}api/policies", payload={}, cert=False
        )
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
