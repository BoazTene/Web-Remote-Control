import os
import sys
import time
from datetime import datetime
from itertools import combinations

sys.path.append(os.getcwd().rsplit('\\', 2)[0])

from flask import Flask, request
from flask_cors import cross_origin
import socket
import threading
# from flask_socketio import SocketIO
from HttpApi.ClientHandler.Main import Main as ClientMain
from HttpApi.HostHandler.Main import Main
from HttpApi.ClientHandler.Mouse import Mouse
from datetime import datetime
import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
from multiprocessing import Process


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

    HOST_IP = "192.168.1.38"
    PORT = 8080

    def __init__(self, port):
        self.port = port
        self.commands = []
        self.image = "Image"
        self.udp = None
        self.handler = None
        self.keyboard_handler = None
        self.main_handler = None
        self.mouse_handler = None

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
        # try:
        handler = Main(self.HOST_IP, self.PORT, username, password, tcp=True)
        handler.tcp_handshake()

        handler.start()

        self.main_handler = handler

        return "True"
        # except Exception as e:
        #     print(e)
        #     return "False"

    def login(self, username, password):
        """
        This function called each time the client wants to connect to host.
        :param username:
        :param password:
        :return:
        """
        handler = ClientMain(self.HOST_IP, self.PORT, username, password)
        result = handler.run()
        self.main_handler = handler
        self.handler = handler.image_handler
        self.mouse_handler = handler.mouse_handler
        self.keyboard_handler = handler.keyboard_handler

        return result

    def thread(self):
        """
        This function is the main thread for the flask http server.
        """
        app = Flask(__name__)
        # app.config['SECRET_KEY'] = '1234'
        # socketio = SocketIO(app, cors_allowed_origins="*")

        @app.route("/image")
        @cross_origin()
        def get_image():
            """
            This function is the handler for http request in the /image directory.
            This function will return the last image received from the host.
            :return:
            """
            try:

                return self.handler.image
            except Exception:
                return 'None'

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


            return self.register(username, password)

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

        @app.route("/key", methods=['POST'])
        @cross_origin()
        def keyboard():
            try:
                combination = request.args.get('combination')
                hold = request.args.get('hold')
                print(combination, hold)
                if combination == "true":
                    key = request.args.get('key')
                    self.keyboard_handler.keyboard(key, combination=True)
                elif hold == 'true':
                    key = request.args.get('key')
                else:
                    key = request.args.get('key')
                    print(key)
                    self.keyboard_handler.keyboard(key)

                # print(key)
                # print("Key recv at: %s" % str(datetime.now()))
                # self.keyboard_handler.keyboard(key)
                return "True"
            except Exception as e:
                return "False"

        @app.route("/mouse")
        @cross_origin()
        def mouse():
            x = float(request.args.get('x'))
            y = float(request.args.get('y'))
            click = request.args.get('click')
            scroll = int(request.args.get('scroll'))
            print(x, y, click, scroll)
            self.mouse_handler.mouse(x, y, click, scroll)

            # if click == 'n': # mouse only moves
            #     Mouse(x, y).move_mouse()
            # elif click == 'r': # right click
            #     Mouse(x, y).right_button()
            # elif click == 'l': # left click
            #     Mouse(x, y).left_button()
            # elif click == 'm': # middle click
            #     Mouse(x, y).middle_button()

            return "True"

        @app.route("/close")
        @cross_origin()
        def close():
            """
            Disconnects from all connections.
            :return:
            """
            # sys.exit(0)
            try:
                print("\n\n\n\n\n\n\n\n\n\nexit\n\n\n\n\n\n\n")
                assert self.main_handler
                self.main_handler.close()
                # self.keyboard_handler.close()

                return "True"
            except Exception as e:
                print(e, "196")
                return "False"

        if self.is_port_in_use():
            # app.logger.disabled = True
            app.run(debug=True, use_reloader=False, port=self.port)
        else:
            raise PortInUseError(self.port)


if __name__ == "__main__":
    server = Server(int(sys.argv[1]))
    while True:
        pass
