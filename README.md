# 3D Print Tracker API
A RESTful Python 3 / Flask API for tracking the history and print count of your 3D prints. 

# Prerequisites
This RESTful API requires python3 (version 3.6 or later), python3-pip, flask, and flaskext.  Also, this Flask app uses MySQL.
Therefore, you will need a MySQL to store and retrieve data.  The structure for this database (and both of
it's tables) is included in this repo.

Since this document assumes that 3D Print Tracker API will run on your local machine (for development only),
all 3 must be installed on your local machine before the API can be used.

The prerequisites can be installed on a Debian based linux machine, like so:

`sudo apt-get update && sudo apt-get install python3 python3-pip`

Then install the required python libraries by running this command:

`pip3 install -r requirements.txt`

Next, add the empty MySQL database schema to your mysql server:

`mysql -h HOSTNAME -u username -p 3dprinttrackerdb < 3dprinttrackerdb.sql`

Replace HOSTNAME with the host (or IP address) of your your MySQL server.  Also, replace username with a MySQL username that
has permission to create a new database.

# Database connection configuration
Before using this API, you will need to configure a file called db.conf.
This file is read by `db_config.py` to give this application the necessary MySQL database connection parameters.
See `db.conf_example` for an example config file.

# Quick Start
To being handling API requests, via the Flask development server, run the following command from the 3D-print-tracker-API directory:

`python3 api_3dprinttracker.py`

The base URL for handling API requests should be:

`http://127.0.0.1:5000`

A description of the end points is coming soon.
