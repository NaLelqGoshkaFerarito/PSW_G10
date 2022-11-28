import paho.mqtt.client as client
from loggers.console_logger import ConsoleLogger
from loggers.i_logger import ILogger
from clients.client_plain import ClientPlain
from clients.client_mqtt import ClientMQTT
from loggers.file_logger import FileLogger
import time
import json

fl = FileLogger()
fl.log("Testing")
time.sleep(2)
fl.log("Testing after 2 seconds")
fl2 = FileLogger()
fl2.log("Testing with the second logger")

# cp = ClientPlain()
# mqtt = ClientMQTT(cp)
# mqtt.connect()
# msg = mqtt.subscribe("v3/project-software-engineering@ttn/devices/py-wierden/up")
# mqtt.loop_forever()



