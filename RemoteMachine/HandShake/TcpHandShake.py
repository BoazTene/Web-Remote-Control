import socket
import threading


class TcpHandShake:
    def __init__(self, host, port, user_name, password):
        super().__init__()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = host
        self.port = port
        self.user_name = user_name
        self.password = password

        self.success = None

    def connect(self):
        self.socket.connect((self.host, self.port))

    def send_creds(self):
        self.socket.send(f"r,{self.user_name},{self.password}".encode("utf-8"))

    def ok(self):
        while True:
            data = self.socket.recv(1024).decode("utf-8")
            print(data.lower(), "d")
            if data.lower() == "ok":
                return [True, self.get_port()]
            elif data.split('!')[0].lower() == 'ok':
                return [True, [data.split('!')[1], data.split('!')[2]]]
            elif data == 'Alive Check':
                continue
            else:
                return [False, None]

    def get_port(self):
        return self.socket.recv(1024).decode("utf-8").split("!")

    def run(self):
        try:
            self.connect()
            self.send_creds()
            return self.ok()
        except Exception:
            return [False, None]
