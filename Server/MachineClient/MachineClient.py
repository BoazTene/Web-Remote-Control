import socket
from Server.MachineClient.Identification import Identification
from Server.SQL import DataBase
import threading
import time
from Server.Connection.AcceptClients import Accept
from Server.Connection.ConnectionCheck import ConnectionCheck


class MachineClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.db = DataBase(r"C:\Users\user\Documents\RemoteControl\Server\pythonsqlite.db")
        self.data = ""
        self.client = []
        self.remote_client = []

    def connection_check(self):
        while True:
            time.sleep(2)
            self.client = ConnectionCheck(self.s, self.client).start()

    def connection(self):
        while True:
            for c in self.client:
                if c[1] is not  None:
                    print("connection")
                    self.s.settimeout(0.5)
                    try:
                        print(c[0].recv(10000).decode())
                    except socket.timeout:
                        pass
                    # c[1].send()

    def accept(self):
        while True:
            a = Accept(self.s, self.client)
            a.accept()
            self.client = a.clients

    def start(self):
        self.s.bind((self.host, self.port))
        self.s.listen(5)

        accept = threading.Thread(target=self.accept)
        accept.start()

        conn_check = threading.Thread(target=self.connection_check)
        conn_check.start()

        # connection = threading.Thread(target=self.connection)
        # connection.start()


if __name__ == "__main__":
    server = MachineClient("localhost", 8080)
    server.start()
