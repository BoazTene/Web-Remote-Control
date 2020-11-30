import socket
from RemoteControl.util import *
import time


# This is the HandShake client
# The Socket object is saved after the HandShake in self.s, the addr save in self.addr
# If the HandShake completed successfully the self.hand_shake value is True else its value is False

class HandShake:
    def __init__(self, s, host):
        self.host = host

        self.port, self.key = HandShake.get_port_and_key(s)

        self.hand_shake = False

        print(self.port, self.key)

        self.connect()

        print("This code is strong as static and benel with ana zack eating lahoh")

        if self.OK():
            print("yes yes")
            if self.OK():
                self.get_client()
                if self.OK():
                    self.hand_shake = True
                    print("The HandShake completed successfully")
                    return
                else:
                    print("Something bad happened..")
                    return
            else:
                print("The HandShake failed because of the remote client.")
                return
        else:
            print("The key isn't correct.")

    # This function gets the identity key from the server and the port of the private server
    @staticmethod
    def get_port_and_key(s):
        while True:
                port = s.recv(1024).decode("utf-8")
                print(port)
                if port != "Alive Check":
                    break
                else:
                    print(port)

        return int(port.split("!")[0]), port.split("!")[1]

    # This function connects to the server
    def connect(self):
        self.s = socket.socket(socket.AF_INET, # Internet
                         socket.SOCK_DGRAM)
        self.s.sendto(self.key.encode("utf-8"), (self.host, self.port))
        print("laflaf")


    def get_client(self):
        data, addr = self.s.recvfrom(1024)
        print(data)
        self.addr = msg_to_addr(data)

    # this function sends that this is a machine client -> m
    def send_type(self):
        self.s.send(b"m")

    # This function checks if Ok arrived
    def OK(self):
        try:
            data, addr = self.s.recvfrom(1024)
        except Exception:
            return False

        data = data.decode('utf-8')
        print(data)
        if data.lower() == 'ok':
            return True
        elif data == "Alive Check":
            return self.OK()
        else:
            print("Failed! " + data)
            return False