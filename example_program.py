import paho.mqtt.client as client
from loggers.console_logger import ConsoleLogger
from loggers.i_logger import ILogger
from clients.client_plain import ClientPlain
from clients.client_mqtt import ClientMQTT
from loggers.file_logger import FileLogger
import time
import json
from loggers.csv_logger import CSVLogger
from clients.data import Data

# bi = BrokerInteract()
# bi.start()
# while True:
#     pass
cp = ClientPlain()
mqtt = ClientMQTT(cp)
mqtt.connect()
msg = mqtt.subscribe("v3/project-software-engineering@ttn/devices/py-wierden/up")
mqtt.loop_forever()

