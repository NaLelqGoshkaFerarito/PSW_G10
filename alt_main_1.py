from clients.client_plain import ClientPlain
from clients.client_mqtt import ClientMQTT

# always the same
cp = ClientPlain()
mqtt = ClientMQTT(cp)
mqtt.connect()
msg = mqtt.subscribe("v3/project-software-engineering@ttn/devices/py-saxion/up")
mqtt.loop_forever()
