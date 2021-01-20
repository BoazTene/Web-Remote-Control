import os
import sys

sys.path.append(os.getcwd().rsplit('\\', 2)[0])

from flask import Flask, request
from flask_cors import cross_origin
import socket
import threading
from RemoteMachine import HandShake
from RemoteMachine.ClientHandler.Handler import ClientHandler
from RemoteMachine.HostHandler.Main import Main


class PortInUseError(Exception):
    """
        This exception raised when the Server starts on a used port
    """

    def __init__(self, port):
        self.port = port

    def __str__(self):
        return "The Port {}, in use please choose another port.".format(self.port)


class Server:
    """
    This class creates an http server
    You can start the server in this way:
    server = Server(1234) # The 1234 represent the port
    all the is stored in self.commands and self.images
    """

    HOST_IP = "localhost"
    PORT = 8080

    def __init__(self, port):
        self.port = port
        self.commands = []
        self.image = "Image"
        self.udp = None
        self.handler = None
        threading.Thread(target=self.thread).start()

    def is_port_in_use(self):
        """
        This function return if the port in self.port in use.
        """

        ADDRESS = "127.0.0.1"
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        return s.connect_ex((ADDRESS, self.port)) != 0
    
    def register(self, username, password):
        """
        This function called each time the client wants to be register as a host.
        :param username:
        :param password:
        :return:
        """
        main = Main(self.HOST_IP, self.PORT, username, password)
        main.start()

    def login(self, username, password):
        """
        This function called each time the client wants to connect to host.

        :param username:
        :param password:
        :return:
        """
        tcp_hand_shake = HandShake.TcpHandShake("localhost", 8080, username, password)

        state = tcp_hand_shake.run()

        if not state[0]:
            return str(False)
        else:
            self.udp = HandShake.UdpHandShake(state, "localhost")
            if self.udp.success:
                self.handler = ClientHandler(self.udp.session, (self.udp.host, self.udp.port))
                self.handler.start()
            return str(self.udp.success)

    def thread(self):
        """
        This function is the main thread for the flask http server.
        """
        app = Flask(__name__)

        @app.route("/image")
        @cross_origin()
        def get_image():
            """
            This function is the handler for http request in the /image directory.
            This function will return the last image received from the host.
            :return:
            """
            return self.handler.image

        @app.route("/register")
        @cross_origin()
        def register():
            """
            This function is the handler for http request in the /register directory.
            This function will register the as a host, with the username & password parameters.
            :return:
            """
            username = request.args.get('username')
            password = request.args.get('password')

            self.register(username, password)

            return "True"

        @app.route("/login")
        @cross_origin()
        def login():
            """
            This function is the handler for http request in the /login directory.
            This function tries to connect to the host with the username & password parameters.
            :return:
            """
            username = request.args.get('username')
            password = request.args.get('password')
            return self.login(username, password)

        if self.is_port_in_use():
            app.run(debug=True, use_reloader=False, port=self.port)
        else:
            raise PortInUseError(self.port)


if __name__ == "__main__":
    server = Server(int(sys.argv[1]))
    while True:
        pass
