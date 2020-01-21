# Author:  Alexan Mardigian
# Version: 0.1

from   app       import app
from   datetime  import datetime
from   db_config import mysql
from   flask     import abort, jsonify, request
import sys
import traceback

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

def get_datetimes(cursor, id_3dprint=0):
    START_DATETIME_INDEX = 2

    sql = "SELECT * FROM print_datetimes"

    if id_3dprint > 0:
        sql += f" WHERE id_3dprint={id_3dprint}"

    cursor.execute(sql)
    rows_dt   = cursor.fetchall()
    datetimes = {}

    for row in rows_dt:
        id = row[1]

        # If a list of datetimes has not been created for id (i)
        # then initialize the list of datetimes with the first datetime.
        # Otherwise, append the new datetime to the list.
        try:
            temp_list = datetimes[id]
            temp_list.append(row[START_DATETIME_INDEX])
            datetimes[id] = temp_list
        except KeyError:
            datetimes[id] = [ row[START_DATETIME_INDEX] ]

    return datetimes

def create_file_data(data, dtime):
    id = data[0]
    file_data = {
        'id': id,
        'filename': data[1],
        'print_count': data[2],
        'print_time': data[3],
        'datetimes_printed': dtime
    }

    return file_data

@app.route('/', methods=['GET'])
def home():
    return '''<h1>3D Print Tracker API</h1>'''

@app.route('/files', methods=['GET'])
def get_files():
    _3dprints = []

    try:
        conn   = mysql.connect()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM 3dprints")
        rows_3dprints = cursor.fetchall()
        datetimes = get_datetimes(cursor)

        for row in rows_3dprints:
            id = row[0]
            _3dprint = create_file_data(row, datetimes[id])
            _3dprints.append(_3dprint)
    except Exception as e:
        traceback.print_exc(file=sys.stderr)
    finally:
        cursor.close() 
        conn.close()
        
    return jsonify({'files': _3dprints})

@app.route('/file/<string:filename>', methods=['GET'])
def get_file(filename):
    file_data = {}

    try:
        conn   = mysql.connect()
        cursor = conn.cursor()

        cursor.execute(f"SELECT * FROM 3dprints WHERE filename='{filename}'")
        response = cursor.fetchall()[0]
        id = response[0]
        file_data = create_file_data(response, get_datetimes(cursor, id))

    except IndexError:
        abort(404)
    except Exception as e:
        traceback.print_exc(file=sys.stderr)
    finally:
        cursor.close()
        conn.close()

    return jsonify({'file': file_data})

@app.route('/file/latestprint', methods=['GET'])
def get_latest_print():
    file_data = {}

    try:
        conn   = mysql.connect()
        cursor = conn.cursor()

        cursor.execute("SELECT id_3dprint FROM print_datetimes ORDER BY start_datetime DESC LIMIT 0, 1")
        dtime = cursor.fetchall()[0]
        id = dtime[0]

        cursor.execute(f"SELECT * FROM 3dprints WHERE id='{id}'")
        response  = cursor.fetchall()[0]
        file_data = create_file_data(response, get_datetimes(cursor, id))
    except IndexError:
        pass   # There are no records in the 3dprints table. An empty JSON object will be returned. 
    except Exception as e:
        traceback.print_exc(file=sys.stderr)
    finally:
        cursor.close()
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
        cursor.close()
        conn.close()

    return response


if __name__ == "__main__":
    app.run()
