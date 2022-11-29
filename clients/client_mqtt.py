import paho.mqtt.client as mqtt
from clients.client_plain import ClientPlain
from loggers.console_logger import ConsoleLogger
from loggers.csv_logger import CSVLogger
from clients.data import Data
import json


# provides an implementation of the MQTT client
class ClientMQTT:
    __logger = CSVLogger()
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
        if rc != 0:
            ClientMQTT.__logger.log("Connection error, disconnecting...")
            client.disconnect()
            return
        ClientMQTT.__logger.log("Connection status: " + mqtt.connack_string(rc))

    def connect(self):
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
        self.__client.disconnect()

    def _on_message(client, userdata, message):
        ClientMQTT.__logger.log("Received message")
        msg_decoded = ClientMQTT.decode(message.payload)
        ClientMQTT.__logger.log("Decoded message, logging")
        # logs to a csv file
        ClientMQTT.__logger.log(msg_decoded)

    # decoding should be accessible as a static method
    @staticmethod
    def decode(input):
        # input is in the form of a bytes object, turn it into a string
        msg_str = input.decode("utf-8").replace("'", '"')
        ClientMQTT.__logger.log(msg_str)
        # turn that string into a json (basically a dictionary)
        msg_json = json.loads(msg_str)
        # dictionary within a dictionary
        data_json_1 = msg_json["uplink_message"]
        time = msg_json["received_at"]
        # dictionary within a dictionary within a dictionary
        decoded_payload = data_json_1["decoded_payload"]
        rx_metadata = data_json_1["rx_metadata"]
        # rx_metadata is a list of length 1 for some reason
        location = rx_metadata[0]["location"]
        # get the list of gateway IDs (length 1) and extract the ID from there
        gateway_id = rx_metadata[0]["gateway_ids"]["gateway_id"]
        location_latitude = location["latitude"]
        location_longitude = location["longitude"]
        location_altitude = location["altitude"]
        data = Data()
        # store the data in a predefined data object
        data.pressure = decoded_payload["pressure"].__str__()
        data.light = decoded_payload["light"].__str__()
        data.temperature = decoded_payload["temperature"].__str__()
        data.datetime = time.__str__()
        data.longitude = location_longitude.__str__()
        data.latitude = location_latitude.__str__()
        data.altitude = location_altitude.__str__()
        return data

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
