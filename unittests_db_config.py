# Author:  Alexan Mardigian
# Version: 0.1

from   db_config import get_dbuser_password
import unittest

class TestDBConfigFuncs(unittest.TestCase):
    def test_get_dbuser_password(self):
        filepath = './mysqluser_pw.txt'
        self.assertEqual(bool(get_dbuser_password(filepath)), not '', "Should not be an empty string.")

    def test_get_dbuser_password_badpath(self):
        filepath = '../badpath.txt'
        self.assertEqual(get_dbuser_password(filepath), '', "Should be an empty string.")


if __name__ == '__main__':
    unittest.main()
