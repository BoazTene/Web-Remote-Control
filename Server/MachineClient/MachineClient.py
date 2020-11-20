import socket
from Server.MachineClient.Identification import Identification
from Server.SQL import DataBase
from Server.Port.GetPort import GetPort
import threading
import time
from Server.Connection.AcceptClients import Accept

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
            print(self.client)
            time.sleep(2)
            db = DataBase(r"C:\Users\user\Documents\RemoteControl\Server\pythonsqlite.db")
            data = db.get_data()

            delete = []
            remote_client_delete = []

            if len(data) != len(self.client):
                db.exec("DELETE FROM machines")
                db.commit()

                self.client = []
                continue

            for row in data:
                try:
                    self.client[int(row[2])][0].send(b"Alive Check")
                except Exception as e:
                    delete.append(row[0])
                    pass

                try:
                    if self.client[int(row[2])][1] is not None:
                        self.client[int(row[2])][1].send(b"Alive Check")
                except ConnectionResetError:
                    remote_client_delete.append(int(row[2]))
                except IndexError:
                    continue

            for i in remote_client_delete:
                try:
                    self.client[i][1] = None
                    self.client[i][0].send(b"disconnected")
                    print("Delete remote machine")
                except IndexError:
                    print("IndexError")
                    pass

            for user_name in delete:
                index = 0
                for i in db.exec("SELECT * FROM machines WHERE UserName = '%s'" % user_name):
                    index = i[2]
                    try:
                        self.client.pop(int(index))
                        db.delete(user_name)
                        print("Deleted " + user_name)
                    except:
                        pass
            db.commit()
            db.close()

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
