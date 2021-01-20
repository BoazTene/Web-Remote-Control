import socket


class TCPHandshake:
    """
    This class is the Host's tcp handshake
    
    handShake stages:
    1. client connects to the server
    2. in case the client is trying to connect as host he will send: 'username,password'
       but if the client is trying to connect to host he will send: 'r,username,password'

    3. the server sends Ok message or an error message
    """
    def __init__(self, host_ip, port, user_name, password):
        self.host_ip = host_ip
        self.port = port
        self.user_name = user_name
        self.password = password
        
        self.session = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def send_creds(self):
        """
        This function sends to the server the username and password parameters.
        :return:
        """
        self.session.send(b"%s,%s" % (self.user_name.encode("utf-8"), self.password.encode("utf-8")))

    def check_ok(self):
        """
        This function checks if the server sent an Ok massage
        :return:
        """
        return self.session.recv(1024).decode("utf-8").upper() == "OK"

    def connect(self):
        """
        This function connects to the server.
        :return:
        """
        self.session.connect((self.host_ip, self.port))

    def run(self):
        """
        This function is the main handler for the handshake
        :return:
        """
        self.connect()
        self.send_creds()
        return self.check_ok()
