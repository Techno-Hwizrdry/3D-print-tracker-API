# Author:  Alexan Mardigian
# Version: 0.1

from   app       import app
from   datetime  import datetime
from   db_config import mysql
from   flask     import abort, jsonify, request
import sys
import traceback

START_DATETIME_INDEX = 4

def update_file_data(conn, cursor, filename):
    cursor.execute(f"SELECT id, print_count FROM 3dprints WHERE filename='{filename}'")
    file_data = cursor.fetchall()[0]
     
    # Increment the print_count.
    id_3dprint = file_data[0]
    updated_print_count = file_data[1] + 1
    cursor.execute(f"UPDATE 3dprints SET print_count='{updated_print_count}' WHERE filename='{filename}'")
    conn.commit()

    add_datetime(conn, cursor, id_3dprint)  # Add a new print datetime for filename.

def add_datetime(conn, cursor, new_id_3dprint):
    sql  = "INSERT INTO print_datetimes(id_3dprint, start_datetime) VALUES(%s, %s)"
    data = (new_id_3dprint, datetime.now())
    cursor.execute(sql, data)
    conn.commit()

def get_datetimes(file_data):
    datetimes = {}

    for row in file_data:
        id = row[0]

        # If a list of datetimes has not been created for id
        # then initialize the list of datetimes with the first datetime.
        # Otherwise, append the new datetime to the list.
        try:
            temp_list = datetimes[id]
            temp_list.append(row[START_DATETIME_INDEX])
            datetimes[id] = temp_list
        except KeyError:
            datetimes[id] = [ row[START_DATETIME_INDEX] ]

    return datetimes

def create_file_data(data, dtimes):
    id = data[0]
    file_data = {
        'id': id,
        'filename': data[1],
        'print_count': data[2],
        'print_time': data[3],
        'datetimes_printed': dtimes
    }

    return file_data

@app.route('/', methods=['GET'])
def home():
    return '''<h1>3D Print Tracker API</h1>'''

@app.route('/files', methods=['GET'])
def get_files():
    _3dprints = []
    conn   = None
    cursor = None

    try:
        conn   = mysql.connect()
        cursor = conn.cursor()

        sql = "SELECT p.*, d.start_datetime FROM 3dprints p INNER JOIN print_datetimes d ON p.id = d.id_3dprint"
        cursor.execute(sql)
        results = cursor.fetchall()
        datetimes = get_datetimes(results)

        for row in results:
            # results will have multiple rows with the same id, filename, print_coint, and print_time,
            # but different start_datetimes.  To avoid duplicate entries into _3dprints, check _3dprints
            # if 'filename' already exists.  If it does not, then append the file data and it's datetimes to _3dprints.
            filename_count = len(list(filter(lambda file_data: file_data['filename'] == row[1], _3dprints)))

            if filename_count == 0:  # 'filename' does not exist in _3dprints.
                id = row[0]
                _3dprint = create_file_data(row, datetimes[id])
                _3dprints.append(_3dprint)
    except Exception as e:
        traceback.print_exc(file=sys.stderr)
    finally:
        if cursor:
            cursor.close()

        if conn:
            conn.close()

    return jsonify({'files': _3dprints})

@app.route('/file/<string:filename>', methods=['GET'])
def get_file(filename):
    file_data = {}
    conn   = None
    cursor = None

    try:
        conn   = mysql.connect()
        cursor = conn.cursor()

        sql = f"SELECT p.*, d.start_datetime FROM 3dprints p INNER JOIN print_datetimes d ON p.id = d.id_3dprint WHERE p.filename='{filename}'"
        cursor.execute(sql)
        response = cursor.fetchall()
        file_data = create_file_data(response[0], get_datetimes(response))

    except IndexError:
        abort(404)  # File not found.
    except Exception as e:
        traceback.print_exc(file=sys.stderr)
    finally:
        if cursor:
            cursor.close()

        if conn:
            conn.close()

    return jsonify({'file': file_data})

@app.route('/file/latestprint', methods=['GET'])
def get_latest_print():
    file_data = {}
    conn   = None
    cursor = None

    try:
        conn   = mysql.connect()
        cursor = conn.cursor()

        sql = "SELECT p.*, d.start_datetime FROM 3dprints p INNER JOIN print_datetimes d ON p.id = d.id_3dprint ORDER BY start_datetime DESC LIMIT 0, 1"
        cursor.execute(sql)
        response  = cursor.fetchall()[0]
        file_data = create_file_data(response, response[START_DATETIME_INDEX])
    except IndexError:
        pass   # There are no records in the 3dprints table. An empty JSON object will be returned. 
    except Exception as e:
        traceback.print_exc(file=sys.stderr)
    finally:
        if cursor:
            cursor.close()

        if conn:
            conn.close()

    return jsonify({'file': file_data})

# To successfully add a new record, the PUT request needs to supply a 'filename' and a 'lastPrintTime'.
# lastPrintTime is in seconds.
# To successfully update an existing record, the PUT request only needs a 'filename'.
@app.route('/file/add', methods=['PUT'])
def put_file():
    # If there is no filename in the json PUT request,
    # or no json at all, then return a 400 (Bad Request) HTTP error code.
    if not request.json or not 'filename' in request.json:
        abort(400)

    SECONDS_IN_HOUR = 3600
    DECIMAL_PLACES  = 2

    filename = request.json['filename']
    response = None
    conn     = None
    cursor   = None

    try:
        conn   = mysql.connect()
        cursor = conn.cursor()

        cursor.execute(f"SELECT filename FROM 3dprints WHERE filename='{filename}'")
        filename_data = cursor.fetchall()

        # Check if the file already exsits in the database.
        # If it does, update the start datetime and increment
        # the print count by 1.  Otherwise, create a new record..
        if len(filename_data) > 0:
            update_file_data(conn, cursor, filename)
            response = jsonify(f"{filename} updated successfully.")
            response.status_code = 200
        elif not 'lastPrintTime' in request.json:    # 'lastPrintTime' is needed to create a new record in 3dprints.
            response = jsonify(f"ERROR: 'lastPrintTime' was not provided in request.json.")
            response.status_code = 400
        else:
            print_hours = round(request.json['lastPrintTime'] / SECONDS_IN_HOUR, DECIMAL_PLACES)
            sql  = "INSERT INTO 3dprints(filename, print_count, print_time) VALUES(%s, %s, %s)"
            data = (filename, 1, print_hours)
            cursor.execute(sql, data)
            new_id_3dprint = cursor.lastrowid
            conn.commit()
            add_datetime(conn, cursor, new_id_3dprint)
            response = jsonify(f"{filename} added successfully.")
            response.status_code = 200

        #response.status_code = 200
    except Exception as e:
        traceback.print_exc(file=sys.stderr)
    finally:
        if cursor:
            cursor.close()

        if conn:
            conn.close()

    return response


if __name__ == "__main__":
    app.run()
