from HttpApi.ClientHandler.HandShake import TcpHandShake, UdpHandShake, NewPort
from HttpApi.ClientHandler.Handler import ClientHandler
from HttpApi.ClientHandler.KeyboardHandler import KeyboardHandler
from HttpApi.ClientHandler.Handler import ClientHandler
from HttpApi.WebSocket.Server import Server as WebSocketServer
import threading
import socket


class Main:
    """
    This class is the main handler for the client.
    """

    def __init__(self, host_ip, port, username, password):
        super(Main, self).__init__()

        self.host_ip = host_ip
        self.port = port
        self.username = username
        self.password = password

        self.tcp_session = None

        self.udp_session = None
        self.udp_address = None

        self.keyboard_session = None
        self.keyboard_address = None

        self.keyboard_handler = None
        self.image_handler = None

    def tcp_handshake(self):
        """
        This function is the main handler for the tcp handshake.
        :return:
        """

        tcp_hand_shake = TcpHandShake(self.host_ip, self.port, self.username, self.password)

        self.tcp_session = tcp_hand_shake.socket

        return tcp_hand_shake.run()

    def close(self):
        """
        Closes all open connections.
        :return:
        """
        assert self.udp_session and self.tcp_session and self.keyboard_session

        self.udp_session.close()
        self.tcp_session.close()
        self.keyboard_session.close()

    def udp_handshake(self, result):
        """
        This function is the main handler for the udp handshake
        :param result:
        :return:
        """

        udp = UdpHandShake(result, self.host_ip)

        self.udp_session = udp.session
        self.udp_address = udp.addr

        return udp.success

    def remote_control(self):
        websocket_server = threading.Thread(target=WebSocketServer, args=(self,))
        websocket_server.start()

        # possible add here a wait for the client to connect

        self.image_handler = ClientHandler(self.udp_session, self.udp_address)
        self.image_handler.start()

        self.keyboard_handler = KeyboardHandler(self.keyboard_session, self.keyboard_address)
        self.keyboard_handler.start()

    def new_port(self):
        new_port = NewPort(self.udp_session, self.udp_address)
        return new_port.run()

    def run(self):
        """
        The main function
        :return:
        """

        result = self.tcp_handshake()

        if not result[0]:
            return str(False)
        else:
            if self.udp_handshake(result):
                print("port")
                self.keyboard_session, self.keyboard_address = self.new_port()
                print(self.keyboard_session, self.keyboard_address)
                self.remote_control()
                return "True"

        return "False"
