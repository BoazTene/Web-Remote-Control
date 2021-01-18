import socket
import threading
import sys
from .Images.ScreenShot import ScreenShot
from .RemoteControl.HandShake import HandShake
from .RemoteControl.RemoteControl import RemoteControl
from .md5 import Md5


class Client:
    def __init__(self, host, port, user_name, password):
        self.remote_addr = None
        self.host = host
        self.port = port
        self.cred = [user_name, password]
        self.s = socket.socket()

    def keep_alive(self, until_data):
        while True:
            data = self.s.recv(1024).decode("utf-8")
            print(data)
            if data == until_data:
                self.s.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
                print(data, until_data)
                return

    def hand_shake(self):
        print("String HandShake")
        hand_shake = HandShake(self.s, self.host)
        print(str(hand_shake.hand_shake) + " dam")
        self.remote_addr = hand_shake.addr
        self.s.close()

        if not hand_shake.hand_shake:
            return False

        self.s = hand_shake.s

        # self.remote_addr = hand_shake.addr

        return True

    def remote_control(self):
        remote_control = RemoteControl(self.s, self.remote_addr)

        print("addr: %s" % str(self.remote_addr))
        remote_control.send_image()
        # exit(0)
        while True:
            remote_control.send_image()

        remote_control.screen_shot.stop()

    def connect(self):
        self.s.connect((self.host, self.port))
        print(self.s.gettimeout())
        # print(Md5(self.cred[0]).encrypt().encode("utf-8") + b"," + Md5(self.cred[1]).encrypt().encode("utf-8"))

        # self.s.send(Md5(self.cred[0]).encrypt().encode("utf-8") + b"," + Md5(self.cred[1]).encrypt().encode("utf-8"))
        self.s.send(self.cred[0].encode("utf-8") + b"," + self.cred[1].encode("utf-8"))

        data = self.s.recv(1024).decode("utf-8")
        print(data)
        if data == "OK":
            while True:
                self.keep_alive("Start-Remote-Control")
                print("Connect to remote client")
                # self.remote_control()
                if not self.hand_shake():
                    print("disconnect")
                    continue

                self.remote_control()


# if __name__ == "__main__":
#     client = Client("localhost", 8080, sys.argv[1], "1234")
#     client.connect()
