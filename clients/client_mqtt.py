# provides general broker interaction functionality

import paho.mqtt.client as mqtt
from clients.data import PYData
from clients.data import LHTDataTemp
from clients.data import LHTDataLight
from clients.data import CustomPY
import json
from loggers.db_logger import DBLogger
import re


# provides an implementation of the MQTT client
class ClientMQTT:
    __logger = DBLogger()
    # ideally this line would be in the init method but then python doesnt let me assign the callbacks
    __client = mqtt.Client()

    def __init__(self, cp):
        # plaintext and MQTT ID should match
        self.__id = cp.count_of_clients()
        self.__plaintext = cp
        self.__client.username_pw_set(self.__plaintext.username(), self.__plaintext.password())
        # default connection timeout on 10 packets
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

    # this code is going to be executed on every disconnect
    def _on_disconnect(client, userdata, rc):
        ClientMQTT.__logger.log("Disconnecting...")

    def disconnect(self):
        self.__connection_timeout = 1

    def _on_message(client, userdata, message):
        ClientMQTT.__logger.log("Received message")
        msg_decoded = ClientMQTT.decode(message.payload)
        ClientMQTT.__logger.log("Decoded message, logging")
        # logs to a csv file
        ClientMQTT.__logger.log(msg_decoded)

    # decoding should be accessible as a static method
    @staticmethod
    def decode(received_data):
        # input is in the form of a bytes object, turn it into a string
        msg_str = received_data.decode("utf-8").replace("'", '"')
        ClientMQTT.__logger.log(msg_str)
        # turn that string into a json (basically a dictionary)
        msg_json = json.loads(msg_str)

        device_id = msg_json["end_device_ids"]["device_id"]

        # dictionary within a dictionary
        uplink_message = msg_json["uplink_message"]
        time = msg_json["received_at"]
        # most important data in here
        decoded_payload = uplink_message["decoded_payload"]
        # rx_metadata is a list (of length 1)
        rx_metadata = uplink_message["rx_metadata"]
        location = rx_metadata[0]["location"]

        gateway_id = rx_metadata[0]["gateway_ids"]["gateway_id"]
        rssi = rx_metadata[0]["rssi"]
        location_latitude = location["latitude"]
        location_longitude = location["longitude"]
        airtime = uplink_message["consumed_airtime"]
        # time in format 2022-12-16T09:53:30.131080123Z, needs parsing
        temp_time = time.__str__()
        temp_time2 = temp_time.replace("T", " ")
        datetime = temp_time2.split(".")[0]

        # if the sensor name starts with "py-"
        if re.findall("\Apy-", device_id):
            ClientMQTT.__logger.log(f"Currently logging a py sensor")
            location_altitude = location["altitude"]

            # store the data in a predefined data object

            try:
                data = PYData()
                data.pressure = decoded_payload["pressure"].__str__()
                data.light = decoded_payload["light"].__str__()
                data.temperature = decoded_payload["temperature"].__str__()
            except:
                data = CustomPY()
                data.light = decoded_payload["bytes"][1]
                data.humidity = decoded_payload["bytes"][0]
                data.temperature = decoded_payload["bytes"][2]

            data.device_id = device_id.__str__()
            data.datetime = datetime
            data.longitude = location_longitude.__str__()
            data.latitude = location_latitude.__str__()
            data.altitude = location_altitude.__str__()
            data.consumed_airtime = airtime.__str__()
            data.metadata["gateway_id"] = gateway_id.__str__()
            data.metadata["rssi"] = rssi.__str__()
            return data

        # else the sensor is lht
        else:
            # try reading data as temperature
            try:
                ClientMQTT.__logger.log(f"Currently logging an lht sensor (type {decoded_payload['Ext_sensor']}")
                data = LHTDataTemp()
                data.device_id = device_id.__str__()

                data.b_voltage = decoded_payload["BatV"].__str__()
                data.b_status = decoded_payload["Bat_status"].__str__()
                data.humidity = decoded_payload["Hum_SHT"].__str__()
                data.temperature_inside = decoded_payload["TempC_SHT"].__str__()
                data.temperature_outside = decoded_payload["TempC_DS"].__str__()

                data.datetime = datetime
                data.longitude = location_longitude.__str__()
                data.latitude = location_latitude.__str__()
                data.consumed_airtime = airtime.__str__()
                data.metadata["gateway_id"] = gateway_id.__str__()
                data.metadata["rssi"] = rssi.__str__()
                return data
            # if that breaks, read data as light
            except:
                ClientMQTT.__logger.log(f"Currently logging an lht sensor (type {decoded_payload['Work_mode']}")
                data = LHTDataLight()
                data.device_id = device_id.__str__()

                data.b_voltage = decoded_payload["BatV"].__str__()
                data.b_status = decoded_payload["Bat_status"].__str__()
                data.humidity = decoded_payload["Hum_SHT"].__str__()
                data.light = decoded_payload["ILL_lx"].__str__()
                data.temperature = decoded_payload["TempC_SHT"].__str__()

                data.datetime = datetime
                data.longitude = location_longitude.__str__()
                data.latitude = location_latitude.__str__()
                data.consumed_airtime = airtime.__str__()
                data.metadata["gateway_id"] = gateway_id.__str__()
                data.metadata["rssi"] = rssi.__str__()
                return data

    # note: topic can be an array of (topic = string, qos = int) tuples if you want to connect to multiple topics
    # and qos stands for quality of service (defaults to 0)
    def subscribe(self, topic, qos=0):
        ClientMQTT.__logger.log("Subscribing to " + topic + " with QoS: " + qos.__str__())
        # v3/project-software-engineering@ttn/devices/py-wierden/up is what the MQTT explorer gave me so I'll use that
        return self.__client.subscribe(topic, qos)

    def loop_forever(self):
        self.__client.loop_forever()

    __client.on_connect = _on_connect
    __client.on_disconnect = _on_disconnect
    __client.on_message = _on_message
