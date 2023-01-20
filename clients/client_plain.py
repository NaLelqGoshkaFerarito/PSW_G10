# provides plaintext information for the other client class, which interacts with the MQTT broker

from loggers.db_logger import DBLogger


class ClientPlain:
    __logger = DBLogger()
    __global_id = 0

    # default constructor
    # uses Saxion TTN as default source
    def __init__(self, host="eu1.cloud.thethings.network", port=1883, username="project-software-engineering@ttn",
                 password="NNSXS.DTT4HTNBXEQDZ4QYU6SG73Q2OXCERCZ6574RVXI.CQE6IG6FYNJOO2MOFMXZVWZE4GXTCC2YXNQNFDLQL4APZMWU6ZGA"):
        ClientPlain.__global_id += 1
        self.__host = host
        self.__port = port
        self.__username = username
        self.__password = password
        self.__id = ClientPlain.__global_id
        self.__logger.log("Custom plaintext clients created, connecting to host: " + self.__host)

    def host(self):
        return self.__host

    def port(self):
        return self.__port

    def username(self):
        return self.__username

    def password(self):
        return self.__password

    @staticmethod
    def count_of_clients():
        return ClientPlain.__global_id
