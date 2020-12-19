from flask import Flask, request
import socket
import threading


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
        self.image = "images"

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

        @app.route("/image")
        def get_image():
            return self.image

        @app.route("/login")
        def login():
            username = request.args.get('username')
            password = request.args.get('password')

        @app.route("/command/<command>")
        def get_command(command):
            self.commands.append(command)
            return "OK"

        if not self.is_port_in_use():
            app.run(debug=True, use_reloader=False, port=self.port)
        else:
            raise PortInUseError(self.port)
