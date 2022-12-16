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
            conn = MySQLdb.connect(host="139.144.177.81", user="jesse", password="Kaas@1234", database="mydatabase")
            cursor = conn.cursor()
            cursor.execute(
                "INSERT IGNORE INTO device(name, longitude, latitude,  altitude) VALUES (%s, %s, %s, %s)",
                (data.device_id, data.longitude, data.latitude, data.latitude))
            cursor.execute(
                "INSERT INTO status(temperature, pressure, humidity, light, time) VALUES (%s, %s, %s, %s,%s)",
                (data.temperature, data.pressure, 0, data.light, data.datetime))
        else:
            DBLogger.__console_logger.log(data)
