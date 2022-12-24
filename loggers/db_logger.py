from .i_logger import ILogger
from datetime import datetime
from clients.data import PYData
from clients.data import LHTDataLight
from clients.data import LHTDataTemp
from .console_logger import ConsoleLogger
import MySQLdb


# implements csv file logging functionality
class DBLogger(ILogger):
    __console_logger = ConsoleLogger()

    def __init__(self):
        __type = "Database Logger"

    def log(self, data):
        # if data is a message from the MQTT broker save to the database
        if type(data) == PYData or type(data) == LHTDataLight or type(data) == LHTDataTemp:
            conn = MySQLdb.connect(host="139.144.177.81", user="ADMIN", password="", database="mydatabase")
            cursor = conn.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS device("
                           "name VARCHAR(255) NOT NULL,"
                           "type VARCHAR(255) NOT NULL,"
                           "longitude VARCHAR(255),"
                           "latitude VARCHAR(255),"
                           "altitude VARCHAR(255),"
                           "packets INT,"
                           "avg_rssi FLOAT,"
                           "PRIMARY KEY (name))")

            cursor.execute("CREATE TABLE IF NOT EXISTS status("
                           "status_id INTEGER AUTO_INCREMENT,"
                           "device_id VARCHAR(255) ,"
                           "b_status INT,"
                           "b_voltage FLOAT,"
                           "temp_in FLOAT,"
                           "temp_out FLOAT,"
                           "pressure FLOAT,"
                           "light FLOAT,"
                           "humidity FLOAT,"
                           "time DATETIME,"
                           "consumed_airtime FLOAT,"
                           "curr_rssi INT,"
                           "gateway VARCHAR(255),"
                           "PRIMARY KEY (status_id),"
                           "FOREIGN KEY (device_id) REFERENCES device(name))")

            if type(data) == PYData:
                cursor.execute(
                    "INSERT IGNORE INTO device(name, type, longitude, latitude,  altitude) "
                    "VALUES (%s, %s, %s, %s, %s)",
                    (data.device_id, "py", data.longitude, data.latitude, data.altitude))
                cursor.execute(
                    "INSERT INTO status(device_id, temp_in, pressure, light, "
                    "time, consumed_airtime, curr_rssi, gateway) "
                    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                    (data.device_id, data.temperature, data.pressure, data.light,
                     data.datetime, data.consumed_airtime.replace("s", ""), data.metadata["rssi"], data.metadata["gateway_id"]))

            elif type(data) == LHTDataTemp:
                cursor.execute(
                    "INSERT IGNORE INTO device(name, type, longitude, latitude) "
                    "VALUES (%s, %s, %s, %s)",
                    (data.device_id, "lht_temp", data.longitude, data.latitude))
                cursor.execute(
                    "INSERT INTO status(device_id, b_status, b_voltage, temp_in, temp_out, humidity, "
                    "time, consumed_airtime, curr_rssi, gateway) "
                    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                    (data.device_id, data.b_voltage, data.b_status, data.temperature_inside, data.temperature_outside, data.humidity,
                     data.datetime, data.consumed_airtime.replace("s", ""), data.metadata["rssi"], data.metadata["gateway_id"]))

            else:
                cursor.execute(
                    "INSERT IGNORE INTO device(name, type, longitude, latitude) "
                    "VALUES (%s, %s, %s, %s)",
                    (data.device_id, "lht_light", data.longitude, data.latitude))
                cursor.execute(
                    "INSERT INTO status(device_id, b_status, b_voltage, temp_out, light, humidity, "
                    "time, consumed_airtime, curr_rssi, gateway) "
                    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                    (data.device_id, data.b_voltage, data.b_status, data.temperature, data.light, data.humidity,
                     data.datetime, data.consumed_airtime.replace("s", ""), data.metadata["rssi"], data.metadata["gateway_id"]))

            # update No. of packets
            cursor.execute("UPDATE device SET device.packets = ("
                           "SELECT COUNT(status.status_id) FROM status WHERE device.name = status.device_id)")
            # update average rssi
            cursor.execute("UPDATE device SET device.avg_rssi = ("
                           "SELECT AVG(status.curr_rssi) FROM status WHERE device.name = status.device_id)")

            conn.commit()
            cursor.close()
        else:
            DBLogger.__console_logger.log(data)
