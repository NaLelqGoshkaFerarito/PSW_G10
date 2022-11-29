import paho.mqtt.client as mqtt

from loggers.csv_logger import CSVLogger
from clients.client_plain import ClientPlain
from clients.client_mqtt import ClientMQTT


# mqtt interactions happen here
class BrokerInteract:
    __logger = CSVLogger()

    def __init__(self):
        self.__plain = ClientPlain()
        self.__client = ClientMQTT(self.__plain)
        self.__should_disconnect = False
        self.__logger.log("Created MQTT client")

    def start(self):
        self.__client.loop_start()
        self.__client.connect()
        return_tuple = self.__client.subscribe("v3/project-software-engineering@ttn/devices/py-wierden/up")
        # self.__client.loop_forever()
        self.__client.loop_start()
        # self.__client.disconnect()

    def end(self):
        BrokerInteract.__logger.log("End function called, disconnecting")
        self.__client.disconnect()

