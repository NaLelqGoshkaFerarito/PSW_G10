import paho.mqtt.client as mqtt

from loggers.console_logger import ConsoleLogger
from clients import client_plain


# mqtt interactions happen here
class BrokerInteract:
    __logger = ConsoleLogger()

    def __init__(self):
        self.__plain = client_plain.ClientPlain()
        self.__logger.log("Created MQTT broker")
