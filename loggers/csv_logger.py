import csv
from .i_logger import ILogger
from datetime import datetime
from clients.data import Data
from .console_logger import ConsoleLogger


# implements csv file logging functionality
class CSVLogger(ILogger):
    __file_name = datetime.now().strftime("log_%m_%Y.csv")
    __console_logger = ConsoleLogger()

    def __init__(self):
        __type = "CSV Logger"

    def log(self, data):
        # if data is a message from the MQTT broker save in a csv file
        if type(data) == Data:
            with open("./loggers/logs_csv/" + self.__file_name, "a") as file:
                writer = csv.writer(file)
                # writes light, temperature, pressure, time of measurement, three rows on location, time of reading
                writer.writerow([data.light, data.temperature, data.pressure, data.datetime, data.latitude, data.longitude, data.altitude, datetime.now().strftime("%m/%d/%Y, %H:%M:%S")])
        # else print it for debugging
        else:
            CSVLogger.__console_logger.log(data)
