from Server.Random.RandomPort import GetPort
from Server.Random.RandomKey import RandomKey
import socket, threading


# This class is the handShake of the remote control
# the change in self.clients is a list [server, machine_client, remote_client]
class HandShake:
    def __init__(self, machine_client, remote_client, clients, host):
        self.BACKLOG_QUEUE_LENGTH = 2
        self.clients = clients
        self.machine_client = machine_client
        self.remote_client = remote_client
        self.host = host
        self.key = RandomKey().key
        self.index = 0

        self.getPort()

        self.create_socket()

        client1 = threading.Thread(target=self.accept)
        client2 = threading.Thread(target=self.accept)
        client1.start()
        client2.start()

    # creating the socket on a random port and sending to the
    def create_socket(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((self.host, self.port))
        self.s.listen(self.BACKLOG_QUEUE_LENGTH)

        # sending the port to the new server and the key to connect
        self.machine_client.send((str(self.port) + "!").encode("utf-8"))
        self.remote_client.send((str(self.port) + "!").encode("utf-8"))

        self.machine_client.send(self.key.encode("utf-8"))
        self.remote_client.send(self.key.encode("utf-8"))

        self.index = self.clients.index([self.machine_client, self.remote_client])
        self.clients[self.index].append([self.s, None, None])

    def accept(self):
        self.s.settimeout(5)
        try:
            c, addr = self.s.accept()
        except socket.timeout:
            return

        if c.recv(1024).decode("utf-8") == self.key:
            # Key is right
            c.send(b"Ok")
            try:
                type = c.recv(1024).decode("utf-8")
            except socket.timeout:
                return

            # r is stand for remote client and m is stand for machine client
            if type == 'r':
                self.clients[self.index][2][1] = c
            elif type == 'm':
                self.clients[self.index][2][2] = c

            # the handShake is successfully done
            c.send(b"OK")
        else:
            # handShake failed
            c.send(b"NO")
            c.close()

    def getPort(self):
        self.port = GetPort().port