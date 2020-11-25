from Server.MachineClient.Identification import Identification
from Server.RemoteControlConnection.HandShake import HandShake


# This class is used to accept clients to the server
# s is the socket
# clients is a list of all the clients
# After every accept you must update the local self.clients
# the accept function must be the first to be called
class Accept:
    def __init__(self, s, clients, host):
        self.s = s
        self.clients = clients
        self.host = host

    # This is the main function who get the creds from the clients
    # This must be the first function to be called
    def accept(self):
        self.s.settimeout(None)
        self.c, self.addr = self.s.accept()

        try:
            self.creds = self.c.recv(1024).decode("utf-8")
            print(self.creds)

            if not self.creds.split(",")[0] == "r":
                self.accept_machine()
            else:
                self.accept_remote_client()

        except Exception as e:
            self.c.send(b"Something Went wrong...")
            pass

    # if the client is machine this will preform the handshake
    def accept_machine(self):
        if not Identification(self.creds.split(","), len(self.clients.data)).check():
            self.c.send(b"Your UserName is taken please change it.")
            self.c.close()
            return

        self.clients.data.append([self.c, None])
        self.c.send(b"OK")
        print("Connected " + self.addr[0])

    # if the client is a remote web this will preform the handshake
    def accept_remote_client(self):
        self.creds = self.creds.split(",")
        self.creds.pop(0)

        if Identification(self.creds, len(self.clients.data)).check_remote_client()[0]:

            self.clients.data[Identification(self.creds, len(self.clients.data)).check_remote_client()[1]][1] = self.c
            self.c.send(b"OK")

            self.clients.data[Identification(self.creds, len(self.clients.data)).check_remote_client()[1]][0].send(B"Start"
                                                                                                         B"-Remote"
                                                                                                         B"-Control")
            print(self.addr[0] + " Just connected to " + self.creds[0] + ". Starting handShake")

            clients_copy = self.clients.data.copy() # This line is the bug

            self.clients.data.pop(Identification(self.creds, len(self.clients.data)).check_remote_client()[1])


            handshake = HandShake(clients_copy[Identification(self.creds, len(clients_copy)).check_remote_client()[1]][0], self.c, clients_copy, self.host)
            if handshake.hand_shake:
                print(self.addr[0] + " and " + self.creds[0] + " handShake is done successfully ")
            else:
                print(self.addr[0] + " and " + self.creds[0] + " handShake failed. ")
                
                self.append_diff(handshake)

                self.handshake_failed(clients_copy)
        else:
            self.c.send(b"UserName or password is wrong")
            self.c.close()

    def append_diff(self, handshake):
        [self.clients.data.append(item) for item in handshake.clients if item not in self.clients.data]

    # this function will run if the handShake failed
    def handshake_failed(self, clients_copy):

        self.clients.data[Identification(self.creds, len(self.clients.data)).check_remote_client()[1]][1] = None

        self.clients.data[Identification(self.creds, len(self.clients.data)).check_remote_client()[1]][2][0].close()
        self.clients.data[Identification(self.creds, len(self.clients.data)).check_remote_client()[1]][1].pop(2)

        self.clients.data[Identification(self.creds, len(self.clients.data)).check_remote_client()[1]][0].send(b"disconnected")

