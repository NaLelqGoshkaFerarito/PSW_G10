from loggers.db_logger import DBLogger


# this class directly interfaces with the broker
class ClientPlain:
    __logger = DBLogger()
    __global_id = 0

    # default constructor
    def __init__(self):
        ClientPlain.__global_id += 1
        self.__host = "eu1.cloud.thethings.network"
        self.__port = 1883
        self.__username = "project-software-engineering@ttn"
        self.__password = "NNSXS.DTT4HTNBXEQDZ4QYU6SG73Q2OXCERCZ6574RVXI.CQE6IG6FYNJOO2MOFMXZVWZE4GXTCC2YXNQNFDLQL4APZMWU6ZGA"
        self.__id = ClientPlain.__global_id
        self.__logger.log("Default plaintext client created (ID: " + self.__id.__str__() + ")")

    # constructor in case Saxion's details are not used
    # def __init__(self, host, port, username, password):
    #     ClientPlain.__global_id += 1
    #     self.__host = host
    #     self.__port = port
    #     self.__username = username
    #     self.__password = password
    #     self.__id = ClientPlain.__global_id
    #     self.__logger.log("Custom plaintext clients created, connectiong to host: " + self.__host)

    def host(self):
        return self.__host

    def port(self):
        return self.__port

    def username(self):
        return self.__username

    def password(self):
        return self.__password
