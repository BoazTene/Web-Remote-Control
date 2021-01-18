import os
import sys

sys.path.append(os.getcwd().rsplit('\\', 2)[0])

from flask import Flask, request
from flask_cors import CORS, cross_origin
import socket
import threading
from RemoteMachine import HandShake
from Machine_Client.main import Client as Register
from Image.GetImage import GetImage


class PortInUseError(Exception):
    def __init__(self, port):
        self.port = port

    def __str__(self):
        return "The Port {}, in use please choose another port.".format(self.port)


# This class creates an http server
# You can start the server in this way:
# server = Server(1234) # The 1234 represent the port
# all the is stored in self.commands and self.images
class Server:
    def __init__(self, port):
        self.port = port
        self.commands = []
        self.image = "Image"
        self.udp = None
        self.get_image = None
        threading.Thread(target=self.thread).start()

    # checking if the port is in use
    def is_port_in_use(self):
        ADDRESS = "127.0.0.1"
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        if s.connect_ex((ADDRESS, self.port)) == 0:
            return False
        else:
            return True

    def thread(self):
        app = Flask(__name__)
        cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

        @app.route("/image")
        @cross_origin()
        def get_image():
            # print(len(self.get_image.images))
            return self.get_image.images
            # return ""
            # return "Error: Permission denied"

        @app.route("/register")
        @cross_origin()
        def register():
            username = request.args.get('username')
            password = request.args.get('password')
            print(password, username)
            host = Register("localhost", 8080, username, password)
            self.register_thread = threading.Thread(target=host.connect())
            self.register_thread.start()
            return "True"

        @app.route("/login")
        @cross_origin()
        def login():
            username = request.args.get('username')
            password = request.args.get('password')
            tcp_hand_shake = HandShake.TcpHandShake("localhost", 8080, username, password)

            state = tcp_hand_shake.run()

            if not state[0]:
                return str(False)
            else:
                self.udp = HandShake.UdpHandShake(state, "localhost")
                if self.udp.success:
                    self.get_image = GetImage(self.udp.session, (self.udp.host, self.udp.port))
                    self.get_image.start()
                return str(self.udp.success)


        @app.route("/command/<command>")
        def get_command(command):
            self.commands.append(command)
            return "OK"

        if self.is_port_in_use():
            app.run(debug=True, use_reloader=False, port=self.port)
        else:
            raise PortInUseError(self.port)


if __name__ == "__main__":
    server = Server(int(sys.argv[1]))
    while True:
        pass