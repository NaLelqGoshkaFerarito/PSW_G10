# Clients explanation
For a quick start read `MQTTClient` -> `Functions` -> `6. Interface functions`
The two clients separate the functionality, which technically can be implemented with only one. A clearer description is present below. There is also a class which enforces a standard for data across the whole application
*Note: logging will not be mentioned for most functions, but if you run the code it will be there*
## Data
This class has no methods, only variables. This makes sure everyone on the team uses the same input and output.
The member variables are as follows: 
- `device_id` - the name of the device
- `pressure`, `temperature`, `light` - the extracted payload (reference `MQTTClient` -> `Functions`) information 
- `datetime` - the time retrieved from the client 
- `consimed_airtime` - travel time of the packet 
- `latitude`, `longitude`, `altitude` - location of the sensor

## ClientPlain
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
- `__connection_timeout` - number of packets to receive before timeout (for exact number and recommended settings reference the implementation)

2. Instance variables
- `__plaintext` - a plaintext client, stores the client details
- `__id` - equal to `__plaintext` ID

### Functions
This is the most important part of the directory, because these functions are responsible for interfacing with the broker and decoding the message. You can use all functions, but it is recommended that you only use `Interface functions` 
1. Static functions
- `decode` - (see also `txts`->`example_data.json`) this method has 3 steps i. Type change/cleanup - the input data changes types from `bytes` to `string` to `json`
ii. Data extraction - the data is extracted from the `json`
iii. Data entry - the data is entered into a `Data object` and returned

2. Instance functions
- `constructor` - initializes instance values and sets the password and username of the client

3. Client handling functions
- `connect` - connect to the `plaintext`'s host and port (set `keepalive` (max time between messages/pings) to 60 seconds) 
- `subscribe` - subscribes to a specified topic with *quality of service* (QoS) beteween 0 and 2 (for our `decoder` to work optimally, a QoS of 0 is advised)
- `read` - reads input as the socket is assumed to be an input socket

4. Loop functions
`loop_forever`is implemented and is exactly the same as the default implementation (see `paho-mqtt` in PyPi)
   
5. Callback functions
These have the syntax `_on_function` and are called every time `function` is called
- `_on_message` - decodes the message and logs it (also decrements `__connection_timeout`)
- `_on_connect` - connect, unless the connection is bad (in which case disconnect)
- `_on_disconnect` - not much was added (aside from logging)

6. Interface functions
- `connection_timeout` - set how many packets to read before disconnecting (setter for `connection_timeout`)
- `run` - run the read loop after `__connection_timeout` is set
