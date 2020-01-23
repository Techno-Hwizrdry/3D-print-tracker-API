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
BLUE_BOAT  = "blue_boat.stl"
ADD_URL    = f"{BASE_URL}/file/add"
FILE_URL   = f"{BASE_URL}/file/{BLUE_BOAT}"
FILES_URL  = f"{BASE_URL}/files"
LATEST_URL = f"{BASE_URL}/file/latestprint"

DEFAULT_DB_HOST = app.app.config['MYSQL_DATABASE_HOST']
INVALID_DB_HOST = "Intentionally bad hostname"

class TestAPIFuncs(unittest.TestCase):
    def _setup_db_host(self, db_host=DEFAULT_DB_HOST):
        app.app.config['MYSQL_DATABASE_HOST'] = db_host
        self.app = app.app.test_client()
        self.app.testing = True

    def test_get_files(self):
        self._setup_db_host()
        response = self.app.get(FILES_URL)
        data = json.loads(response.get_data())
        self.assertEqual(response.status_code, 200, "Should return HTTP 200.")

    def test_get_files_500(self):
        self._setup_db_host(INVALID_DB_HOST)
        response = self.app.get(FILES_URL)
        data = json.loads(response.get_data())
        self.assertEqual(response.status_code, 500, "Should return HTTP 500.")

    def test_get_file(self):
        self._setup_db_host()
        response = self.app.get(FILE_URL)
        data = json.loads(response.get_data())
        self.assertEqual(response.status_code, 200, "Should return HTTP 200.")

    def test_get_file_404(self):
        self._setup_db_host()
        response = self.app.get(FILE_URL + "does_not_exist")
        data = json.loads(response.get_data())
        self.assertEqual(response.status_code, 404, "Should return HTTP 404.")

    def test_get_file_500(self):
        self._setup_db_host(INVALID_DB_HOST)
        response = self.app.get(FILE_URL)
        data = json.loads(response.get_data())
        self.assertEqual(response.status_code, 500, "Should return HTTP 500.")

    def test_get_latest_print(self):
        self._setup_db_host()
        response = self.app.get(LATEST_URL)
        data = json.loads(response.get_data())
        self.assertEqual(response.status_code, 200, "Should return HTTP 200.")

    def test_get_latest_print_500(self):
        self._setup_db_host(INVALID_DB_HOST)
        response = self.app.get(LATEST_URL)
        data = json.loads(response.get_data())
        self.assertEqual(response.status_code, 500, "Should return HTTP 500.")

    def test_put_add_record(self):
        self._setup_db_host()
        record = {"filename": BLUE_BOAT, "lastPrintTime": 3650.94738242}
        response = self.app.put(ADD_URL,
                                data = json.dumps(record),
                                content_type='application/json')
        self.assertEqual(response.status_code, 200, "Adding a well formed record should return HTTP 200.")

    def test_put_update_record(self):
        self._setup_db_host()
        record = {"filename": BLUE_BOAT}
        response = self.app.put(ADD_URL,
                                data = json.dumps(record),
                                content_type='application/json')
        self.assertEqual(response.status_code, 200, "Updating a record should return HTTP 200.")

    def test_put_no_filename(self):
        self._setup_db_host()
        record = {}
        response = self.app.put(ADD_URL,
                                data = json.dumps(record),
                                content_type='application/json')
        self.assertEqual(response.status_code, 400, "Adding a record with an empty json payload should return HTTP 400.")

    def test_put_error(self):
        self._setup_db_host()
        record = {"filename": "red_boat.stl"}
        response = self.app.put(ADD_URL,
                                data = json.dumps(record),
                                content_type='application/json')
        self.assertEqual(response.status_code, 400, "Adding a record with no \"lastPrintTime\" should return HTTP 400.")

    def test_put_add_record_500(self):
        self._setup_db_host(INVALID_DB_HOST)
        record = {"filename": "benchy.stl", "lastPrintTime": 4444.44}
        response = self.app.put(ADD_URL,
                                data = json.dumps(record),
                                content_type='application/json')
        self.assertEqual(response.status_code, 500, "Should return HTTP 500.")

if __name__ == '__main__':
    unittest.main()
