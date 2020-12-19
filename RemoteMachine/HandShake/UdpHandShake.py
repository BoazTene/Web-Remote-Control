import socket
from RemoteMachine.HandShake.util import *


class UdpHandShake:
    def __init__(self, creds, host):
        self.session = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        print(creds)
        try:
            self.port = int(creds[1][0])
            self.key = creds[1][1]
        except ValueError:
            self.port = int(creds[1][1])
            self.key = creds[1][2]

        self.host = host
        self.success = False

        self.send_key()

        if self.OK("ok"):
            if self.OK("ok"):
                self.get_client()
                self.session.sendto(b"Ok, Client", self.addr)
                print("The HandShake completed successfully")
                self.success = True
                return
            else:
                print("The HandShake failed because of the remote client.")
                return
        else:
            print("The key isn't correct.")

    def get_client(self):
        data, addr = self.session.recvfrom(1024)
        print(data)
        self.addr = msg_to_addr(data)

    def send_key(self):
        self.session.sendto(self.key.encode("utf-8"), (self.host, self.port))

    def OK(self, recv):
        try:
            data, addr = self.session.recvfrom(1024)
            print(data)
        except Exception:
            return False

        data = data.decode('utf-8')
        print(data)
        if data.lower() == recv:
            return True
        elif data == "Alive Check":
            return self.OK(recv)
        else:
            print("Failed! " + data)
            return False