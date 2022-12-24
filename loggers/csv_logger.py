import csv
from .i_logger import ILogger
from datetime import datetime
from clients.data import PYData
from .console_logger import ConsoleLogger


# implements csv file logging functionality
class CSVLogger(ILogger):
    __file_name = datetime.now().strftime("log_%m_%Y.csv")
    __console_logger = ConsoleLogger()

    def __init__(self):
        __type = "CSV Logger"

    def log(self, data):
        # if data is a message from the MQTT broker save in a csv file
        if type(data) == PYData:
            with open("./loggers/logs_csv/" + self.__file_name, "a") as file:
                writer = csv.writer(file)
                # writes the data for device table then for the data table
                writer.writerow([data.device_id, data.latitude, data.longitude, data.altitude, data.light, data.temperature, data.pressure, data.datetime, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), data.consumed_airtime])
        # else print it for debugging
        else:
            CSVLogger.__console_logger.log(data)
