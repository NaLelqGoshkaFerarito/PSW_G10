from flask import *
from datetime import datetime
import csv
import json, time
from clients.client_mqtt import ClientMQTT
from clients.client_plain import ClientPlain

# setup
app = Flask(__name__)


def get_messages(count):
    output = dict()
    # open this month's file
    with open(datetime.now().strftime("loggers/logs_csv/log_%m_%Y.csv")) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        lines = count
        for row in csv_reader:
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
    return json.dumps(get_messages(1))


# get a number of messages
@app.route("/messages/")
def number_of_times():
    # ask for input in the format "/messages/?times=NUM_OF_TIMES"
    query = int(request.args.get("times"))
    return json.dumps(get_messages(query))


if __name__ == "__main__":
    app.run(port=7777, debug=True)
