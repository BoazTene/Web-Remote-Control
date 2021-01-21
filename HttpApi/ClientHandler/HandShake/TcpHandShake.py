import socket


class TcpHandShake:
    """
    This class is the Tcp handshake.

    handShake stages:
    1. client connects to the server
    2. in case the client is trying to connect as host he will send: 'username,password'
       but if the client is trying to connect to host he will send: 'r,username,password'

    3. the server sends Ok message or an error message
    """

    def __init__(self, host, port, user_name, password):
        super().__init__()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = host
        self.port = port
        self.user_name = user_name
        self.password = password

        self.success = None

    def connect(self):
        """
        This function is used to perform the first stage of the handshake, connect to the server.
        :return:
        """
        self.socket.connect((self.host, self.port))

    def send_creds(self):
        """
        This function is used to perform the second stage of the handshake,
        send the creds to the server.
        :return:
        """
        self.socket.send(f"r,{self.user_name},{self.password}".encode("utf-8"))

    def ok(self):
        """
        This function is used to perform the last stage of the handshake,
        makine sure the server sends an ok message and not an error one.
        :return:
        """
        while True:
            data = self.socket.recv(1024).decode("utf-8")

            if data.lower() == "ok":
                return [True, self.get_port()]
            elif data.split('!')[0].lower() == 'ok':
                return [True, [data.split('!')[1], data.split('!')[2]]]
            elif data == 'Alive Check':
                continue
            else:
                return [False, None]

    def get_port(self):
        """
        This function is used to perform the first stage of the Udp handshake,
        Get the key and the port of the private server.
        This function will be called only if all the other stages went successfully.
        :return:
        """
        return self.socket.recv(1024).decode("utf-8").split("!")

    def run(self):
        """
        This is the main function that handles the entire handshake.
        :return:
        """
        try:
            self.connect()
            self.send_creds()
            return self.ok()
        except Exception:
            return [False, None]
