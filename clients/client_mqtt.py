import paho.mqtt.client as mqtt
import paho.mqtt.subscribe as subscribe
from clients.client_plain import ClientPlain
from loggers.console_logger import ConsoleLogger


# provides an implementation of the MQTT client
class ClientMQTT:
    __logger = ConsoleLogger()
    # ideally this line would be in the init method but then python doesnt let me assign the callbacks
    __client = mqtt.Client()

    def __init__(self, cp):
        # plaintext and MQTT ID should match
        self.__id = cp.count_of_clients()
        self.__plaintext = cp
        self.__client.username_pw_set(self.__plaintext.username(), self.__plaintext.password())
        ClientMQTT.__logger.log("MQTT client created from (Plaintext ID: " + self.__id.__str__() + ")")

    # this code is going to be executed every time an attempt to connect is made
    def _on_connect(client, userdata, flags, rc):
        ClientMQTT.__logger.log("Attempting connection...")
        if rc == 5:
            ClientMQTT.__logger.log("Auth error")
            client.disconnect()
            return
        ClientMQTT.__logger.log("Connection status: " + mqtt.connack_string(rc))

    def connect(self):
        # checks the type of the argument
        if type(self.__plaintext) is not ClientPlain:
            self.__logger.log("Argument in ClientMQTT is not a plaintext client, throwing error")
            raise TypeError()
        self.__client.connect(self.__plaintext.host(), self.__plaintext.port(), 60)

    # this code is going to be executed on every disconnect,
    # even if it doesnt go through the ClientMQTT.disconnect function
    def _on_disconnect(client, userdata, rc):
        if rc != 0:
            ClientMQTT.__logger.log("Unexpected disconnection")
            return
        ClientMQTT.__logger.log("Disconnecting...")
        ClientMQTT.__logger.log("Status: " + mqtt.connack_string(rc))

    def disconnect(self):
        self.__logger.log("Disconnecting")
        self.__client.disconnect()

    def _on_message(client, userdata, message):
        ClientMQTT.__logger.log("Received message: " + message.decode("utf-8").payload())

    # note: topic can be an array of (topic = string, qos = int) tuples if you want to connect to multiple topics
    # and qos stands for quality of service (defaults to 0)
    def subscribe(self, topic, qos=0):
        ClientMQTT.__logger.log("Subscribing to " + topic + " with QoS: " + qos.__str__())
        # v3/project-software-engineering@ttn/devices/py-wierden/up is what the MQTT explorer gave me so I'll use that
        return self.__client.subscribe(topic, qos)

    def loop_start(self):
        self.__client.loop_start()

    def loop_stop(self):
        self.__client.loop_stop()

    def loop_forever(self):
        self.__client.loop_forever()

    __client.on_connect = _on_connect
    __client.on_disconnect = _on_disconnect
    __client.on_message = _on_message
