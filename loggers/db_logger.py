from .i_logger import ILogger
from datetime import datetime
from clients.data import Data
from .console_logger import ConsoleLogger
import MySQLdb


# implements csv file logging functionality
class DBLogger(ILogger):
    __console_logger = ConsoleLogger()

    def __init__(self):
        __type = "Database Logger"

    def log(self, data):
        # if data is a message from the MQTT broker save to the database
        if type(data) == Data:
            conn = MySQLdb.connect(host="139.144.177.81", user="ADMIN", password="", database="mydatabase")
            cursor = conn.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS device("
                           "name VARCHAR(255) NOT NULL,"
                           "longitude VARCHAR(255),"
                           "latitude VARCHAR(255),"
                           "altitude VARCHAR(255),"
                           "PRIMARY KEY (name))")

            cursor.execute("CREATE TABLE IF NOT EXISTS status("
                           "status_id INTEGER AUTO_INCREMENT,"
                           "device_id VARCHAR(255) ,"
                           "temperature INTEGER NOT NULL,"
                           "pressure INTEGER NOT NULL,"
                           "humidity INTEGER NOT NULL,"
                           "light INTEGER NOT NULL,"
                           "time DATETIME,"
                           "PRIMARY KEY (status_id),"
                           "FOREIGN KEY (device_id) REFERENCES device(name))")
            cursor.execute(
                "INSERT IGNORE INTO device(name, longitude, latitude,  altitude) VALUES (%s, %s, %s, %s)",
                (data.device_id, data.longitude, data.latitude, data.altitude))
            cursor.execute(
                "INSERT INTO status(device_id, temperature, pressure, humidity, light, time) VALUES (%s, %s, %s, %s, %s,%s)",
                (data.device_id, data.temperature, data.pressure, 0, data.light, data.datetime))
            conn.commit()
            cursor.close()
        else:
            DBLogger.__console_logger.log(data)
