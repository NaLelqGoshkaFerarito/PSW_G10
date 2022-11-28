from .i_logger import ILogger
from datetime import datetime


# implements console logging functionality
class FileLogger(ILogger):
    __file_name = datetime.now().strftime("log_%m_%d_%Y.txt")

    def __init__(self):
        __type = "File Logger"
        # create or open file for appending, with closes the file automatically
        with open("./loggers/logs/" + self.__file_name, "a") as file:
            file.write("--New log started at [" + datetime.now().strftime("%m/%d/%Y, %H:%M:%S") + "]--\n")

    def log(self, data):
        with open("./loggers/logs/" + self.__file_name, "a") as file:
            file.write("[" + datetime.now().strftime("%m/%d/%Y, %H:%M:%S") + "]: " + data + "\n")
