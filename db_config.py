# Author:  Alexan Mardigian
# Version: 0.2

# This python script will handle all the MySQL configurations.
# The configuration parameters are stored in the file, CONFIG_FILE_PATH.

from app import app
from flaskext.mysql import MySQL

import configparser
import sys

CONFIG_FILE_PATH = './db.conf'
DB_SECTION = 'mysql'

config = configparser.ConfigParser()

if not config.read(CONFIG_FILE_PATH):
    raise FileNotFoundError(f"Could not find the database config file: {CONFIG_FILE_PATH}")

for key in dict(config.items(DB_SECTION)).keys():
    app.config[key.upper()] = config.getint('mysql', key) if key.upper() == 'MYSQL_DATABASE_PORT' else config['mysql'][key]

app.config['MYSQL_DATABASE_SOCKET'] = None

mysql = MySQL()
mysql.init_app(app)
