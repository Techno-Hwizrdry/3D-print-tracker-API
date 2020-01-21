# Author:  Alexan Mardigian
# Version: 0.1

# This python script will handle all the MySQL configurations.

from app import app
from flaskext.mysql import MySQL

import sys

PW_FILE_PATH = './mysqluser_pw.txt'

def get_dbuser_password(file_path):
    dbuser_password = ""

    try:
        with open(file_path) as password_file:
            dbuser_password = password_file.readline().strip()
    except IOError:
        print(f"\nCould not read file: {file_path}", file=sys.stderr)
        print("Check if the file path is valid, and try again.\n", file=sys.stderr)

    return dbuser_password


mysql = MySQL()

app.config['MYSQL_DATABASE_USER'] = '3dprintertracker_user'
app.config['MYSQL_DATABASE_PASSWORD'] = get_dbuser_password(PW_FILE_PATH)
app.config['MYSQL_DATABASE_DB'] = '3dprinttrackerdb'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_PORT'] = 3306
app.config['MYSQL_DATABASE_SOCKET'] = None

mysql.init_app(app)
