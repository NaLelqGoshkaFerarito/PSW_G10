from clients.client_plain import ClientPlain
from clients.client_mqtt import ClientMQTT

# Specific for custom sensor
cp = ClientPlain("eu1.cloud.thethings.network", 1883, "py-group9@ttn", "NNSXS.6UBOQVANSOLQ6DXWKLPWSUTPT4LZ7KOXXWA73II.KQKFA72QGPCRUEHVAP26RHEOQZIOE45KXJWDZYCHIAVNZP27YGMA")
mqtt = ClientMQTT(cp)
mqtt.connect()
msg = mqtt.subscribe("v3/py-group9@ttn/devices/py-group9/up")
mqtt.loop_forever()
