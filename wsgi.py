from flask import *
from datetime import datetime
import csv
import json
import MySQLdb
from clients.client_mqtt import ClientMQTT
from clients.client_plain import ClientPlain

# setup
app = Flask(__name__)


def get_devices(count):
    # database interaction setup
    conn = MySQLdb.connect(host="139.144.177.81", user="ADMIN", password="", database="mydatabase")
    cursor = conn.cursor()
    cursor.execute("SELECT * from device ORDER BY name DESC")
    rows_device = cursor.fetchall()

    output = list()

    lines = count
    for row in rows_device:
        # if row is an actual row
        if len(row) > 3:
            if lines > 0:
                data_row = dict()
                data_row['device_id'] = row[0]
                data_row['device_type'] = row[1]
                data_row['longitude'] = row[2]
                data_row['latitude'] = row[3]
                data_row['altitude'] = row[4]
                data_row['packets'] = row[5]
                data_row['avg_rssi'] = row[6]
                output.append(data_row)
            lines -= 1
    # return the string with ' quotes because the other ones need to be excaped with \
    cursor.close()
    return output.__str__()


# gets statuses for a device with that
def get_statuses_for_device_equ(name, number=1):
    conn = MySQLdb.connect(host="139.144.177.81", user="ADMIN", password="", database="mydatabase")
    cursor = conn.cursor()
    cursor.execute("SELECT * from status WHERE device_id = %s ORDER BY time DESC LIMIT %s", (name, number,))
    rows_status = cursor.fetchall()
    output = list()

    for row in rows_status:
        # if row is an actual row
        if len(row) > 3:
            data_row = dict()
            data_row["status_id"] = row[0]
            data_row["device_id"] = row[1]
            data_row["battery_v"] = row[2]
            data_row["battery_stat"] = row[3]
            data_row["temp_inside"] = row[4]
            data_row["temp_outside"] = row[5]
            data_row["pressure"] = row[6]
            data_row["light"] = row[7]
            data_row["humidity"] = row[8]
            data_row["time"] = datetime.strftime(row[9], "%Y-%m-%d %H:%M:%S")
            data_row["consumed_aittime"] = row[10]
            data_row["curr_rssi"] = row[11]
            data_row["gateway"] = row[12]
            output.append(data_row)

    cursor.close()
    return output


# get devices with that name
def get_devices_equ(name):
    conn = MySQLdb.connect(host="139.144.177.81", user="ADMIN", password="", database="mydatabase")
    cursor = conn.cursor()
    cursor.execute("SELECT * from status WHERE device_id = %s ORDER BY time DESC", (name, ))
    rows_device = cursor.fetchall()

    output = list()

    lines = len(rows_device)
    for row in rows_device:
        # if row is an actual row
        if len(row) > 3:
            if lines > 0:
                data_row = dict()
                data_row["status_id"] = row[0]
                data_row["device_id"] = row[1]
                data_row["battery_v"] = row[2]
                data_row["battery_stat"] = row[3]
                data_row["temp_inside"] = row[4]
                data_row["temp_outside"] = row[5]
                data_row["pressure"] = row[6]
                data_row["light"] = row[7]
                data_row["humidity"] = row[8]
                data_row["time"] = datetime.strftime(row[9], "%Y-%m-%d %H:%M:%S")
                data_row["consumed_aittime"] = row[10]
                data_row["curr_rssi"] = row[11]
                data_row["gateway"] = row[12]
                output.append(data_row)
            lines -= 1
    # return the string with ' quotes because the other ones need to be excaped with \
    cursor.close()
    return output


def get_all_devices():
    conn = MySQLdb.connect(host="139.144.177.81", user="ADMIN", password="", database="mydatabase")
    cursor = conn.cursor()
    cursor.execute("SELECT * from device")
    rows_device = cursor.fetchall()

    output = list()

    lines = len(rows_device)
    for row in rows_device:
        # if row is an actual row
        if len(row) > 3:
            if lines > 0:
                data_row = dict()
                data_row['device_id'] = row[0]
                data_row['device_type'] = row[1]
                data_row['longitude'] = row[2]
                data_row['latitude'] = row[3]
                data_row['altitude'] = row[4]
                data_row['packets'] = row[5]
                data_row['avg_rssi'] = row[6]
                output.append(data_row)
            lines -= 1
    # return the string with ' quotes because the other ones need to be excaped with \
    cursor.close()
    return output


def get_statuses(count):
    # database interaction setup
    conn = MySQLdb.connect(host="139.144.177.81", user="ADMIN", password="", database="mydatabase")
    cursor = conn.cursor()
    cursor.execute("SELECT * from status ORDER BY time DESC")
    rows_status = cursor.fetchall()

    output = list()

    lines = count
    for row in rows_status:
        # if row is an actual row
        if len(row) > 3:
            if lines > 0:
                data_row = dict()
                data_row["status_id"] = row[0]
                data_row["device_id"] = row[1]
                data_row["battery_v"] = row[2]
                data_row["battery_stat"] = row[3]
                data_row["temp_inside"] = row[4]
                data_row["temp_outside"] = row[5]
                data_row["pressure"] = row[6]
                data_row["light"] = row[7]
                data_row["humidity"] = row[8]
                data_row["time"] = datetime.strftime(row[9], "%Y-%m-%d %H:%M:%S")
                data_row["consumed_aittime"] = row[10]
                data_row["curr_rssi"] = row[11]
                data_row["gateway"] = row[12]
                output.append(data_row)
            lines -= 1
    # return the string with ' quotes because the other ones need to be excaped with \
    cursor.close()
    return output


def get_statuses_for_device_for_time_period(name, time_period="day"):
    conn = MySQLdb.connect(host="139.144.177.81", user="ADMIN", password="", database="mydatabase")
    cursor = conn.cursor()
    cursor.execute("SELECT * from device")
    rows_status = str()

    if time_period == "day":
        cursor.execute("select * from status WHERE DATE_SUB(current_date(), interval 1 day)")
        rows_status = cursor.fetchall()
    elif time_period == "week":
        cursor.execute("select * from status WHERE DATE_SUB(current_date(), interval 1 week)")
        rows_status = cursor.fetchall()
    elif time_period == "month":
        cursor.execute("select * from status WHERE DATE_SUB(current_date(), interval 1 month)")
        rows_status = cursor.fetchall()
    # else get the statuses for the last hour
    # else:
    #     cursor.execute("select * from status where time >= DATE_SUB(localtimestamp(), interval 1 hour)")

        rows_status = cursor.fetchall()
        output = list()

        for row in rows_status:
            # if row is an actual row
            if len(row) > 3:
                data_row = dict()
                data_row["status_id"] = row[0]
                data_row["device_id"] = row[1]
                data_row["battery_v"] = row[2]
                data_row["battery_stat"] = row[3]
                data_row["temp_inside"] = row[4]
                data_row["temp_outside"] = row[5]
                data_row["pressure"] = row[6]
                data_row["light"] = row[7]
                data_row["humidity"] = row[8]
                data_row["time"] = datetime.strftime(row[9], "%Y-%m-%d %H:%M:%S")
                data_row["consumed_aittime"] = row[10]
                data_row["curr_rssi"] = row[11]
                data_row["gateway"] = row[12]
                output.append(data_row)

        cursor.close()
        return output


def get_messages_deprecated(count):
    output = dict()
    # open this month's file
    with open(datetime.now().strftime("loggers/logs_csv/log_%m_%Y.csv")) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        lines = count
        for row in csv_reader:
            # if row is an actual row
            if len(row) > 5:
                if lines > 0:
                    data_row = {'device_id': f'{row[0]}', 'latitude': f'{row[1]}', 'longitude': f'{row[2]}',
                                'altitude': f'{row[3]}', 'light': f'{row[4]}', 'temperature': f'{row[5]}',
                                'pressure': f'{row[6]}', 'datetime': f'{row[7]}', 'receive_time': f'{row[8]}',
                                'consumed_airtime': f'{row[9]}'}
                    # dictionary looks like number: data
                    output[f'{count - lines}'] = f'data_row: {data_row.__str__()}'
                lines -= 1
    # return the string with ' quotes because the other ones need to be excaped with \
    return f'{output.__str__()}'.replace('"', "'")


# get last message
@app.route("/")
def default():
    return "<p>Hi :D</p>"


@app.route("/devices/all/")
def all_devices():
    return json.dumps(get_all_devices())


# get a number of devices
@app.route("/devices/")
def number_of_devices():
    # ask for input in the format "/devices/?number=NUM_OF_DEVICES"
    query = int(request.args.get("number"))
    return json.dumps(get_devices(query))


@app.route("/device/")
def name_of_device():
    # ask for input in the format "/device/?name=DEVICE_NAME"
    query = str(request.args.get("name"))
    return json.dumps((get_devices_equ(query)))


# get a number of messages
@app.route("/statuses/")
def number_of_statuses():
    # ask for input in the format "/statuses/?number=NUM_OF_STATUSES"
    query = int(request.args.get("number"))
    return json.dumps(get_statuses(query))


@app.route("/statuses/device/")
def number_of_statuses_for_device():
    # ask for input in the format "/statuses/device/?name=DEVICE_NAME&number=NUMBER_OF_STATUSES"
    name = str(request.args.get("name"))
    try:
        number = int(request.args.get("number"))
    except:
        number = 1
    return json.dumps(get_statuses_for_device_equ(name, number))


# get statuses based on the time the packet was received
@app.route("/statuses/device_time/")
def statuses_datetime():
    # ask for input in the format "/statuses/device_time/?name=DEVICE_NAME&time_period=TIME_PERIOD_STR"
    name = str(request.args.get("name"))
    try:
        time_period = str(request.args.get("number"))
    except:
        time_period = "day"
    return json.dumps(get_statuses_for_device_for_time_period(name, time_period))


if __name__ == "__main__":
    app.run(port=7777, debug=True)
