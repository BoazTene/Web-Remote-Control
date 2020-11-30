from Server.Random.RandomPort import GetPort
from Server.Random.RandomKey import RandomKey
import socket, threading
from Server.RemoteControlConnection.util import *
from Server.RemoteControlConnection.Time import CountTime

# HandShake stages:
# 1. the Server sends the clients a random port and a identity key
# 2. the Server creates a private server on the random port
# 3. each clients need to connect the private server and send the indentity key
# 4. if the key is ok the client get an OK message from the server
# 5. the client send 'r' or 'm'. 'r' -> remote_client, 'm' -> machine_client
# 6. the client gets an Ok message from the server
# 7. if both clients successfully completed the HandShake they will get another OK


# This class is the handShake of the remote control
# the change in self.clients is a list [server, machine_client, remote_client]
class HandShake:
    def __init__(self, machine_client, remote_client, clients, host):
        self.BACKLOG_QUEUE_LENGTH = 2
        self.clients = clients
        self.machine_client = machine_client
        self.remote_client = remote_client
        self.host = host
        self.address = []
        self.TIMEOUT = 5

        self.key = RandomKey().key

        self.index = 0
        self.hand_shake = False

        self.getPort()

        self.create_socket()

        accept = threading.Thread(target=self.accept)
        accept.start()

        time = CountTime()

        while time.get_pass_time() < self.TIMEOUT:
            pass

        if not self.hand_shake:
            self.failed()

    def failed(self):
        try:
            self.clients[self.index][2][1].send(b"NO")
            pass
        except Exception:
            try:
                self.s.sendto(b"NO", self.address[0])
            except Exception:
                pass

        try:
            self.clients[self.index][2][2].send(b"NO")
            pass
        except Exception:
            try:
                self.s.sendto(b"NO", self.address[1])
            except Exception:
                pass


        self.s.close()

    # creating the socket on a random port and sending to the
    def create_socket(self):
        self.s = socket.socket(socket.AF_INET, # Internet
                         socket.SOCK_DGRAM) # UDP

        self.s.bind((self.host, self.port))


        # sending the port to the new server and the key to connect
        self.machine_client.send((str(self.port) + "!").encode("utf-8") + self.key.encode("utf-8"))
        self.remote_client.send((str(self.port) + "!").encode("utf-8") + self.key.encode("utf-8"))

        # self.index = self.clients.index([self.machine_client, self.remote_client])
        # self.clients[self.index].append([self.s, None, None])

    def accept(self):
        while True:
            data, addr = self.s.recvfrom(1024)
            print(data, addr)
            if data.decode('utf-8') == self.key:
                self.address.append(addr)
                self.s.sendto(b"OK", addr)
            else:
                print("key:", self.key)
                print("data:", data)
                self.s.sendto(b"NO", addr)

            if len(self.address) >= 2:
                try:
                    self.s.sendto(b"OK", self.address[0])
                    self.s.sendto(b"OK", self.address[-1])
                except Exception:
                    return

                self.s.sendto(addr_to_msg(self.address[1]), self.address[0])
                self.s.sendto(addr_to_msg(self.address[0]), self.address[1])

                try:
                    self.s.sendto(b"OK", self.address[0])
                    self.s.sendto(b"OK", self.address[-1])
                except Exception:
                    return

                self.address.pop(1)
                self.address.pop(0)

                self.s.close()

                self.hand_shake = True

                return

    def getPort(self):
        self.port = GetPort().port