# Author:  Alexan Mardigian
# Version: 0.1

from   api_3dprinttracker import get_datetimes
from   copy      import deepcopy
from   db_config import mysql
from   flask     import abort, jsonify, request

import app
import datetime
import json
import unittest

BASE_URL   = "http://127.0.0.1:5000"
ADD_URL    = BASE_URL + "/file/add"
FILE_URL   = BASE_URL + "/file/wolf_skull.stl"
FILES_URL  = BASE_URL + "/files"
LATEST_URL = BASE_URL + "/file/latestprint"

BLUE_BOAT = "blue_boat.stl"

class TestAPIFuncs(unittest.TestCase):
    def setUp(self):
        self.app = app.app.test_client()
        self.app.testing = True

    def test_get_files(self):
        response = self.app.get(FILES_URL)
        data = json.loads(response.get_data())
        self.assertEqual(response.status_code, 200, "Should return HTTP 200.")

    def test_get_file(self):
        response = self.app.get(FILE_URL)
        data = json.loads(response.get_data())
        self.assertEqual(response.status_code, 200, "Should return HTTP 200.")

    def test_get_latest_print(self):
        response = self.app.get(LATEST_URL)
        data = json.loads(response.get_data())
        self.assertEqual(response.status_code, 200, "Should return HTTP 200.")

    def test_put_add_record(self):
        record = {"filename": BLUE_BOAT, "lastPrintTime": 3650.94738242}
        response = self.app.put(ADD_URL,
                                data = json.dumps(record),
                                content_type='application/json')
        self.assertEqual(response.status_code, 200, "Adding a well formed record should return HTTP 200.")

    def test_put_update_record(self):
        record = {"filename": BLUE_BOAT}
        response = self.app.put(ADD_URL,
                                data = json.dumps(record),
                                content_type='application/json')
        self.assertEqual(response.status_code, 200, "Updating a record should return HTTP 200.")

    def test_put_no_filename(self):
        record = {}
        response = self.app.put(ADD_URL,
                                data = json.dumps(record),
                                content_type='application/json')
        self.assertEqual(response.status_code, 400, "Adding a record with an empty json payload should return HTTP 400.")

    def test_put_error(self):
        record = {"filename": "red_boat.stl"}
        response = self.app.put(ADD_URL,
                                data = json.dumps(record),
                                content_type='application/json')
        self.assertEqual(response.status_code, 400, "Adding a record with no \"lastPrintTime\" should return HTTP 400.")

if __name__ == '__main__':
    unittest.main()
