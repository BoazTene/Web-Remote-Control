import socket
from Server.MachineClient.Identification import Identification
from Server.SQL import DataBase
import threading
import time
from Server.Connection.AcceptClients import Accept
from Server.Connection.ConnectionCheck import ConnectionCheck
from Server.Clients_Data import Clients
from Server.HTTP_Server.Server import run
from multiprocessing import Process


class Main:
    """
    This class is the main Server.

    This class serve both web and tcp + udp connections.
    """
    DATABASE_PATH = r"C:\Users\user\Documents\RemoteControl\Server\pythonsqlite.db"
    WEB_PORT = 5000

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.db = DataBase(self.DATABASE_PATH)
        self.data = ""
        self.clients = Clients()
        self.remote_client = []

    def connection_check(self):
        """
        This function sends every 2 seconds Alive check message to see which clients are still connected.

        :return:
        """

        connection_check = ConnectionCheck(self.s, self.clients)

        if connection_check.check_database_update():
            return

        while True:
            time.sleep(2)
            connection_check.connect_db()
            self.clients = connection_check.start()

    def accept(self):
        """
        This function is the main handler to accept new clients.
        :return:
        """

        while True:
            a = Accept(self.s, self.clients, self.host)
            a.accept()
            self.clients = a.clients

    def start(self):
        """
        This function is the main function which starts three threads:
            1. web - the web thread
            2. accept - the client accept thread
            3. keep alive - the keep alive thread
        :return:
        """

        self.s.bind((self.host, self.port))
        self.s.listen(5)
        web = Process(target=run, args=(self.WEB_PORT,))
        web.start()
        # web = threading.Thread(target=run, args=(self.WEB_PORT,))
        # web.start()

        accept = threading.Thread(target=self.accept)
        accept.start()

        conn_check = threading.Thread(target=self.connection_check)
        conn_check.start()


if __name__ == "__main__":
    server = Main("0.0.0.0", 8080)
    server.start()
