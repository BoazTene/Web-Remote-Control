from Server.MachineClient.Identification import Identification
from Server.RemoteControlConnection.HandShake import HandShake
import threading
from Server.SQL import DataBase


class Accept:
    """
        This class is used to accept clients to the server
        s is the socket
        clients is a list of all the clients
        After every accept you must update the local self.clients
        the accept function must be the first to be called
    """

    def __init__(self, s, clients, host):
        self.s = s
        self.clients = clients
        self.host = host

        self.c = None
        self.addr = None
        self.creds = None

    def accept(self):
        """
        This is the main function who get the creds from the clients
        This must be the first function to be called
        :return:
        """

        self.s.settimeout(None)
        self.c, self.addr = self.s.accept()

        try:
            self.creds = self.c.recv(1024).decode("utf-8")

            if not self.creds.split(",")[0] == "r":
                self.accept_machine()
            else:
                self.accept_remote_client()

        except Exception:
            self.c.send(b"Something Went wrong...")
            pass

    def accept_machine(self):
        """
        This function accepts hosts.
        :return:
        """

        if not Identification(self.creds.split(","), len(self.clients.data)).check():
            self.c.send(b"Your UserName is taken please change it.")
            self.c.close()
            return
        self.clients.data.append([self.c, None])
        self.c.send(b"OK")
        print("Connected " + self.addr[0])

    def accept_remote_client(self):
        """
        This function accepts clients.
        :return:
        """

        self.creds = self.creds.split(",")

        self.creds.pop(0)

        if Identification(self.creds, len(self.clients.data)).check_remote_client()[0]:

            self.clients.data[Identification(self.creds, len(self.clients.data)).check_remote_client()[1]][1] = self.c
            self.c.send(b"OK")

            self.clients.data[Identification(self.creds, len(self.clients.data)).check_remote_client()[1]][0].send(B"Start"
                                                                                                         B"-Remote"
                                                                                                         B"-Control")
            print(self.addr[0] + " Just connected to " + self.creds[0] + ". Starting handShake")

            threading.Thread(target=self.hand_shake).start()
        else:
            self.c.send(b"UserName or password is wrong")
            self.c.close()

    def hand_shake(self):
        """
        This function handles the tcp handshake.
        """

        clients_copy = self.clients.data.copy()

        self.clients.data.pop(Identification(self.creds, len(self.clients.data)).check_remote_client()[1])

        handshake = HandShake(clients_copy[Identification(self.creds, len(clients_copy)).check_remote_client()[1]][0],
                              self.c, clients_copy, self.host)
        if handshake.hand_shake:
            print(self.addr[0] + " and " + self.creds[0] + " handShake is done successfully ")

            # delete the userName from the database
            db = DataBase(r"C:\Users\user\Documents\RemoteControl\Server\pythonsqlite.db")
            db.exec("DELETE FROM machines WHERE client = '%s'" % len(self.clients.data))
            
            db.c.execute("INSERT INTO Authorized VALUES(?, ?, ?, ?)" , (self.c.getsockname()[0], self.creds[0], self.creds[1], 0,),)
            db.commit()
            db.close()

        else:
            print(self.addr[0] + " and " + self.creds[0] + " handShake failed. ")

            self.handshake_failed(clients_copy)

    def append_diff(self, handshake):
        """
        This function updates the clients.
        """

        [self.clients.data.append(item) for item in handshake.clients if item not in self.clients.data]

    def handshake_failed(self, clients_copy):
        """
        This function will run if the handShake failed

        :param clients_copy:
        :return:
        """

        self.clients.data[Identification(self.creds, len(self.clients.data)).check_remote_client()[1]][0].send(b"disconnected")

