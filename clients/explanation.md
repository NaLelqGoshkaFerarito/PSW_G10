# Clients explanation
The two clients separate the functionality, which technically can be implemented with only one. A clearer description below 

## ClientPlaintext
This client is mainly for data storage and tracking of IDs

### Variables
1. Static variables
- `__logger` - logs the activity within the class
- `__global_id` - count of all clients; also helps with indexing of `MQTTClient`s
*Note: two underscores in front of a variable is python's way of denoting a `private` (although it is pseudo-`private`)*

2. Instance variables
-  `__host` - `"eu1.cloud.thethings.network"` is what we will be running for this project
- `__port` - `1883` is the standard port `8883` can be used as well (for TLS connections)
- `__username` - `"project-software-engineering@ttn"` is what we will be running for this project
- `__password` = `"NNSXS.DTT4HTNBXEQDZ4QYU6SG73Q2OXCERCZ6574RVXI.CQE6IG6FYNJOO2MOFMXZVWZE4GXTCC2YXNQNFDLQL4APZMWU6ZGA"`
- `__id` - ID of the current instance

*Note: for more information on the MQTT-specific variables reference `paho-mqtt` in the python index*

### Functions
For the sake of brevity a description of those is omitted, but they are just getters.

## ClientMQTT
Receives data from an MQTT broker and cleans it up so that out `BrokerInteract` class can implement it. A prettier implementation of the default client. 

### Variables
1. Static variables
- `__logger` - analogous to ClientPlain
- `__client` - the stock client implementation; has to be static because of `__self__`

2. Instance variables
`__plaintext`, `__id`
Self-explanatory, check the source code if interested