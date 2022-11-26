from .i_logger import ILogger
from datetime import datetime


# implements console logging functionality
class ConsoleLogger(ILogger):
    def __init__(self):
        __type = "Console Logger"

    def log(self, data):
        print("[" + datetime.now().strftime("%m/%d/%Y, %H:%M:%S") + "]: " + data)
