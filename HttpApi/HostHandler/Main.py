from HttpApi.HostHandler.Handshake import TCPHandshake, UDPHandshake, NewPort
from HttpApi.HostHandler.Handler import HostHandler
from HttpApi.HostHandler.KeyboardHandler import KeyboardHandler
from HttpApi.HostHandler.MouseHandler import MouseHandler

import threading
import socket
import multiprocessing


class Main(threading.Thread):
    """
    This class is the main handler for the host.
    """

    def __init__(self, host_ip, port, username, password, **kwargs):
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

        self.mouse_session = None
        self.mouse_address = None

        self.handler = False

        self.is_close = False

        if kwargs['tcp'] is not None:
            self.tcp = kwargs['tcp']
        else:
            self.tcp = None

    def tcp_handshake(self):
        """
        This class handles the tcp Handshake
        :return:
        """

        tcp = TCPHandshake.TCPHandshake(self.host_ip, self.port, self.username, self.password)
        result = tcp.run()
        self.tcp_session = tcp.session
        print(result)
        return result

    def udp_handshake(self):
        """
        This function handles the udp handshake
        :return:
        """

        udp = UDPHandshake.UDPHandshake(self.tcp_session, self.host_ip)
        result = udp.run()

        self.udp_session = udp.session
        self.udp_address = udp.address

        return result

    def keep_alive(self, until_data):
        """
        This function wats until the server sends the until data value.
        :param until_data:
        :return:
        """

        while True:
            data = self.tcp_session.recv(1024).decode("utf-8")

            if data == until_data:
                self.tcp_session.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
                return

    def remote_control(self):
        """
        This function handles the remote control stage.
        :return:
        """

        handler = HostHandler(self.udp_session, self.udp_address)
        handler.start()
        # handler.join()

        mouse_handler = MouseHandler(self.mouse_session, self.mouse_address)
        mouse_handler.start()

        keyboard_handler = KeyboardHandler(self.keyboard_session, self.keyboard_address)
        keyboard_handler.start()

        self.keyboard_handler = keyboard_handler

        while handler.is_alive() and keyboard_handler.is_alive():
            pass

        keyboard_handler.close()
        handler.close()

    def new_port(self):
        """
        This function opens new udp hole punching port.
        The function opens the port using the another udp hole punching port.
        :return:
        """

        new_port = NewPort.NewPort(self.udp_session, self.udp_address)
        return new_port.run()

    def close(self):
        """
        Closes all open connections.
        :return:
        """
        assert self.udp_session and self.tcp_session and self.keyboard_session

        self.keyboard_handler.close()
        self.udp_session.close()
        self.tcp_session.close()
        self.keyboard_session.close()

        self.is_close = True

    def run(self):
        """
        The main function
        :return:
        """

        while not self.is_close and ((self.tcp and self.tcp_session) or self.tcp_handshake()):
            print(self.is_close)
            self.tcp = False

            print("da")
            self.keep_alive("Start-Remote-Control")

            if not self.udp_handshake():
                continue

            print("Done")

            self.keyboard_session, self.keyboard_address = self.new_port()
            self.mouse_session, self.mouse_address = self.new_port()
            print(self.mouse_address)

            self.remote_control()
            print("Disconnected")
