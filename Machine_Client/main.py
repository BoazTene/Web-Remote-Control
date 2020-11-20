import socket
import pyautogui
from io import BytesIO
import base64
import threading
from time import sleep
import sys


class Client:
    def __init__(self, host, port, user_name, password):
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

    def remote_control(self):

        def check_connection():
            while True:
                data = self.s.recv(1024).decode("utf-8")
                if data == "disconnected":
                    print("disconnected")
                    return

        conn_check = threading.Thread(target=check_connection())
        conn_check.start()

        while True:
            if not conn_check.is_alive():
                return
            screen_shot = ScreenShot()
            screen_shot.capture()
            self.s.send(screen_shot.convert_to_base64())

    def connect(self):
        self.s.connect((self.host, self.port))
        print(self.s.gettimeout())
        self.s.send((self.cred[0] + "," + self.cred[1]).encode("utf-8"))

        data = self.s.recv(1024).decode("utf-8")
        print(data)
        if data == "OK":
            while True:
                self.keep_alive("Start-Remote-Control")
                print("Connect to remote client")
                self.remote_control()


class ScreenShot:
    def __init__(self, location=None):
        self.location = location
        self.img = None

    def capture(self):
        if self.location is None:
            self.img = pyautogui.screenshot()
        else:
            self.img = pyautogui.screenshot(region=self.location)

    def convert_to_base64(self):
        buffered = BytesIO()
        self.img.save(buffered, format="JPEG")
        return base64.b64encode(buffered.getvalue())


if __name__ == "__main__":
    client = Client("localhost", 8080, sys.argv[1], "1234")
    client.connect()
