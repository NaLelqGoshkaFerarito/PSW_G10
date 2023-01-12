# PSW_G10
Repo for Project Software weather application (Group 10)

# Loggers
The loggers are responsible for logging the messages we receive. There are five different loggers, some of which use others for debugging purposes. Every single one has the method `log()`, which allows us to use them interchangeably.

## Console logger
The most widely used logger. It outputs text with a timestamp to the console. The CSV and database logger use it for debugging purposes.

## File logger
Logs text + timestamp to a `.txt` file. It was a prototype for the next logger.

## CSV logger
Logs `PYData` objects to a `.csv` file, otherwise prints status messages to the console. It was used because `.csv` files made testing and prototyping easier. When it was implemented `py` sensors were the only type of sensors supported.

## DB logger
Logs `PYData`, `LHTDataTemp` and `LHTDataLight` objects to a database, otherwise prints status messages to the console. It made the implementation much more streamlined. Before it was implemented, the only way to log to the database was through a scan of the `.csv` file from the last logger. This meant that a lot more code was needed
# Broker interaction
For a quick start read `Example code`

The two clients separate the functionality, which technically can be implemented with only one. A clearer description is present below. There is also a class which enforces a standard for data across the whole application
*Note: logging will not be mentioned for most functions, but if you run the code it will be there*
## Data
The data classes have no methods, only variables. This makes sure everyone on the team uses the same input and output.

### PYData
The member variables are as follows: 
- `device_id` - the name of the device
- `pressure`, `temperature`, `light` - the extracted payload (reference `MQTTClient` -> `Functions`) information 
- `datetime` - the time retrieved from the client 
- `consumed_airtime` - travel time of the packet 
- `latitude`, `longitude`, `altitude` - location of the sensor
- `metadata` - a dictionary containing rssi and gateway information 

### LHTDataTemp
The member variables are as follows: 
- `device_id` - the name of the device
- `b_voltage`, `b_status` - battery info; part of the extracted payload (reference `MQTTClient` -> `Functions`) information 
- `humidity`, `temperature_inside`, `temperature_outside` - part of the extracted payload (reference `MQTTClient` -> `Functions`) information 
- `datetime` - the time retrieved from the client 
- `consumed_airtime` - travel time of the packet 
- `latitude`, `longitude` - location of the sensor
- `metadata` - a dictionary containing rssi and gateway information

### LHTDataLight
The member variables are as follows: 
- `device_id` - the name of the device
- `b_voltage`, `b_status` - battery info; part of the extracted payload (reference `MQTTClient` -> `Functions`) information 
- `humidity`, `light`, `temperature` - part of the extracted payload (reference `MQTTClient` -> `Functions`) information 
- `datetime` - the time retrieved from the client 
- `consumed_airtime` - travel time of the packet 
- `latitude`, `longitude` - location of the sensor
- `metadata` - a dictionary containing rssi and gateway information


### SI-Units
- `pressure` - Pascal [Pa]
- `temperature` - Degrees centigrade [°C]
- `light` - Lux (Technically not an SI-unit) 
- `consumed_airtime` - seconds [s]

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
Receives data from an MQTT broker and cleans it up so that the MQTT functionality can be implemented. A prettier implementation of the default client. 

### Variables
1. Static variables
- `__logger` - analogous to ClientPlain
- `__client` - the stock client implementation; has to be static because of `__self__`

2. Instance variables
- `__plaintext` - a plaintext client, stores the client details
- `__id` - equal to `__plaintext` ID

### Functions
This is the most important part of the directory, because these functions are responsible for interfacing with the broker and decoding the message. You can use all functions, but it is recommended that you only use `Interface functions` 
1. Static functions
- `decode` - (see also `txts`->`example_data.json` and `example_data`) this method has 3 steps i. Type change/cleanup - the input data changes types from `bytes` to `string` to `json`
ii. Data extraction - the data is extracted from the `json` and the type of the sensor is checked.
iii. Data entry - the data is entered into its respective object and returned

2. Instance functions
- `constructor` - initializes instance values and sets the password and username of the client

3. Client handling functions
- `connect` - connect to the `plaintext`'s host and port (set `keepalive` (max time between messages/pings) to 60 seconds) 
- `subscribe` - subscribes to a specified topic with *quality of service* (QoS) beteween 0 and 2 (for our `decoder` to work optimally, a QoS of 0 is advised)

4. Loop functions
`loop_forever`is implemented and is exactly the same as the default implementation (see `paho-mqtt` in PyPi)
   
5. Callback functions
These have the syntax `_on_function` and are called every time `function` is called
- `_on_message` - decodes the message and logs it
- `_on_connect` - connect, unless the connection is bad (in which case disconnect)
- `_on_disconnect` - not much was added (aside from logging)


### Example Code
```python
from clients.client_plain import ClientPlain
from clients.client_mqtt import ClientMQTT

# always the same
cp = ClientPlain()
mqtt = ClientMQTT(cp)
mqtt.connect()
msg = mqtt.subscribe("v3/project-software-engineering@ttn/devices/py-wierden/up")
mqtt.loop_forever()
```
*Note: For more detailed explanations reference the appropriate chapters*

The program creates a default plaintext broker (we only need a default constructor, because the broker used is always the same). This broker gives the necessary data to the MQTT client class, which interfaces with the broker. It then runs indefinitely and logs data in the meantime.

# API
For the time being the server application we are using requires the user to open the site manually at least once and dismiss the message.
The final base url is not decided yet, but it will be in the format `https://1054-145-76-102-198.ngrok.io` and `base-url` will be used instead, for the time being.

## Endpoints 
### Default
Just a smiley

### Get all devices
Gets a JSON containing all the devices from the database in the form of a dictionary.
Can be accessed at `base-url/devices/`.

### Get statuses by device name
Gets a JSON containing all statuses for the device called `NAME` from the database in the form of a dictionary. 
Can be accessed at `base-url/device/?name=NAME`. Deprecated, because it gets *all* statuses, should only be used for testing.

### Get all devices
Gets a JSON containing all devices from the database in the form of a dictionary. 
Can be accessed at `base-url/device/all/`.

### Get a number of statuses
Gets a JSON containing `NUM_OF_STATS` logs from the database in the form of a dictionary.
Can be accessed at `base-url/statuses/?number=NUM_OF_STATS`.

### Get a number of statuses for a device
Gets a JSON containing `NUM_OF_STATS` logs from the database for device `DEVICE_NAME` in the form of a dictionary.
Can be accessed at `base-url/statuses/device/?name=DEVICE_NAME&number=NUM_OF_STATS`. In case `NUM_OF_STATS` is omitted, one status will be returned

### Get all statuses for a device in a given time period
Gets a JSON containing logs from the past `TIME_PERIOD_STR` for device `DEVICE_NAME` in the form of a dictionary.
Can be accessed at `base-url/statuses/device_time/?name=DEVICE_NAME&time_period=TIME_PERIOD_STR`. In case `TIME_PERIOD_STR` is omitted, the statuses for the last day will be returned.
Possible values for `TIME_PERIOD_STR`: 
- `week`
- `month`
- anything else (will return the statuses from the last `day`)

### Get supported data for a sensor type
Gets a JSON with the supported columns `base-url/device/type/?type=DEVICE_TYPE&all=ZERO_OR_ONE` in a list. 
All is an optional argument, which lets you choose if you want all columns (ids, metadata, etc.), `1` is `true`. 
Set it to `0` to only get the data extracted from the payload of the status.

## Database
The database is hosted on a server, and the tables are created by the `db_logger`. 
These tables are called `device` and `status`.

### device
Device has 7 columns
- `name` - a.k.a. `device_id`
- `type` - value is `py`, `lht_temp` or `lht_light` depending on the device type
- `longitude`, `latitude` and `altitude` - positional info (`altidude` is `null` for lht sensors)
- `packets` - total number of packets for this device
- `avg_rssi` - average rssi for this device

### status
Device has 13 columns
- `status_id` - auto incremented primary key 
- `device_id` - foreign key (=`device.name`)
- `b_status` - battery status
- `b_voltage` - battery voltage
- `temp_in` - inside temperature
- `temp_out` - outside temperature
- `pressure`, `light` and `humidity`
- `time` - date and time taken from the packet
- `consumed_airtime` - travel time
- `curr_rssi` - rssi extracted from the packet
- `gateway` - gateway for the packet