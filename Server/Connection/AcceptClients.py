from Server.MachineClient.Identification import Identification


# This class is used to accept clients to the server
# s is the socket
# clients is a list of all the clients
# After every accept you must update the local self.clients
# the accept function must be the first to be called
class Accept:
    def __init__(self, s, clients):
        self.s = s
        self.clients = clients

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

        except Exception:
            self.c.send(b"Something Went wrong...")
            pass

    # if the client is machine this will preform the handshake
    def accept_machine(self):
        if not Identification(self.creds.split(","), len(self.clients)).check():
            self.c.send(b"Your UserName is taken please change it.")
            self.c.close()
            return

        self.clients.append([self.c, None])
        self.c.send(b"OK")
        print("Connected " + self.addr[0])

    # if the client is a remote web this will preform the handshake
    def accept_remote_client(self):
        self.creds = self.creds.split(",")
        self.creds.pop(0)

        if Identification(self.creds, len(self.clients)).check_remote_client()[0]:

            self.clients[Identification(self.creds, len(self.clients)).check_remote_client()[1]][1] = self.c
            self.c.send(b"OK")

            self.clients[Identification(self.creds, len(self.clients)).check_remote_client()[1]][0].send(B"Start"
                                                                                                         B"-Remote"
                                                                                                         B"-Control")
            print(self.addr[0] + " Just connected to " + self.creds[0])

        else:
            self.c.send(b"UserName or password is wrong")
            self.c.close()
