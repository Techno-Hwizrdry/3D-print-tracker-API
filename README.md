# 3D Print Tracker API
A RESTful Python 3 / Flask API for tracking the history and print count of your 3D prints. 

# Prerequisites
This RESTful API requires python3, python3-pip, flask, and flaskext.  Since this document assumes that 3D Print Tracker API
will run on your local machine (for development only), all 3 must be installed on your local machine before the API can be used.

The prerequisites can be installed on a Debian based linux machine, like so:

`sudo apt-get update && sudo apt-get install python3 python3-pip`

Then install the required python libraries by running this command:

`pip3 install -r requirements.txt`

# Quick Start
To being handling API requests, via the Flask development server, run the following command from the 3D-print-tracker-API directory:

`python3 api_3dprinttracker.py`

The base URL for handling API requests should be:

`http://127.0.0.1:5000`

A description of the end points is coming soon.
