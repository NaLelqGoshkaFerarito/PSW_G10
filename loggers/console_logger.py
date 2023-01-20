# logs to the console directly; used by other loggers for debugging

from .i_logger import ILogger
from datetime import datetime


class ConsoleLogger(ILogger):
    def __init__(self):
        __type = "Console Logger"

    def log(self, data):
        print("[" + datetime.now().strftime("%m/%d/%Y, %H:%M:%S") + "]: " + data)
