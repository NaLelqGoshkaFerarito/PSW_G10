# all py sensors are the same
class PYData:
    def __init__(self):
        self.device_id = ""

        # decoded payload
        self.pressure = ""
        self.temperature = ""
        self.light = ""

        # other data
        self.datetime = ""
        self.consumed_airtime = ""
        self.latitude = ""
        self.longitude = ""
        self.altitude = ""
        self.metadata = dict()


# our custom py sensor
class CustomPY:
    def __init__(self):
        self.device_id = ""

        # decoded payload
        self.light = ""
        self.temperature = ""
        self.humidity = ""

        # other data
        self.datetime = ""
        self.consumed_airtime = ""
        self.latitude = ""
        self.longitude = ""
        self.altitude = ""
        self.metadata = dict()


# lht illumination sensor data
class LHTDataLight:
    def __init__(self):
        self.device_id = ""

        # decoded payload
        # battery voltage
        self.b_voltage = ""
        # battery status
        self.b_status = ""
        self.humidity = ""
        self.light = ""
        self.temperature = ""

        # other data
        self.datetime = ""
        self.consumed_airtime = ""
        self.latitude = ""
        self.longitude = ""
        self.metadata = dict()


# lht temperature sensor
class LHTDataTemp:
    def __init__(self):
        self.device_id = ""

        # decoded payload
        # battery voltage
        self.b_voltage = ""
        # battery status
        self.b_status = ""
        self.humidity = ""
        self.temperature_inside = ""
        self.temperature_outside = ""

        # other data
        self.datetime = ""
        self.consumed_airtime = ""
        self.latitude = ""
        self.longitude = ""
        self.metadata = dict()
