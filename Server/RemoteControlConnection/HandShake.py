from Server.Random.RandomPort import GetPort
from Server.Random.RandomKey import RandomKey
import socket, threading

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

        self.key = RandomKey().key

        self.index = 0
        self.hand_shake = False

        self.getPort()

        self.create_socket()


        client1 = threading.Thread(target=self.accept)
        client2 = threading.Thread(target=self.accept)
        client1.start()
        client2.start()

        while not (not self.verification() and (not client1.is_alive() or not client2.is_alive())):
            pass

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

    def verification(self):
        if self.clients[self.index][2][1] is not None and self.clients[self.index][2][1] is not None:
            self.hand_shake = True
            return True
        else:
            self.hand_shake = False
            return False

    def accept(self):
        self.s.settimeout(5)
        try:
            c, addr = self.s.accept()
        except socket.timeout:
            return

        if c.recv(1024).decode("utf-8") == self.key:
            # Key is right
            c.send(b"Ok")
            print("HandShake succeeded with " + addr[0])
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